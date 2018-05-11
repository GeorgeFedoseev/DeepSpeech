import csv
import os
import sys
import time
import datetime

import threading
from Queue import *


import sys
sys.path.insert(0,os.getcwd()) 

import const



# CSV MEM ABSTRACTION with syncing with filesystem every n seconds
# {filename: {rows: [], queue: } }
CSV_FILES_DICT = {}
CSV_FILES_DICT_rlock = threading.RLock()
CSV_UPDATE_WORKER_THREAD = None


# CSV UPDATING QUEUE

# init from files
def init_csv_from_file(csv_path):    

    # lazy init
    maybe_start_csv_queue_worker_thread()

    with CSV_FILES_DICT_rlock:

        if csv_path in CSV_FILES_DICT:
            return # already inited

        #print("init csv %s" % csv_path)

        # create csv file if not exists
        if not os.path.exists(csv_path):
            open(csv_path, 'a').close()



        f = open(csv_path, "r+")
        csv_reader = csv.reader(f)

        #print("init_csv_from_file - 1")
        rows = list(csv_reader)
        rows = [r for r in rows if len(r) > 0 and r[0].strip() != ""]
        #print("init_csv_from_file - 2")

        
        CSV_FILES_DICT[csv_path] = {
            "rows": rows,
            "queue": Queue(),
            "lock": threading.RLock()
        }

        f.close()



def update_from_file(csv_path):
    #print "start update from file %s" % csv_path
    # in case if first time
    init_csv_from_file(csv_path)

    f = open(csv_path, "r+")
    csv_reader = csv.reader(f)

    #print("update_from_file - 1")
    rows = list(csv_reader)
    rows = [r for r in rows if len(r) > 0 and r[0].strip() != ""]
    #print("update_from_file - 2")
    with CSV_FILES_DICT[csv_path]["lock"]:
        CSV_FILES_DICT[csv_path]["rows"] = rows

    #print "end update from file %s" % csv_path


def sync_csv_to_file(csv_path):
    if not (csv_path in CSV_FILES_DICT):
        return # cant write - dont have data

    #print('sync_csv_to_file - start')

    lines = []
    for row in CSV_FILES_DICT[csv_path]["rows"]:
        rows_str = [str(x) for x in row]
        lines.append(','.join(rows_str))

    #print lines


    #print 'write to %s' % csv_path
    f = open(csv_path, "w")
    f.write('\n'.join(lines)+'\n')
    f.close()
    
    #print('sync_csv_to_file - end')

# writer worker
def csv_queue_worker():
    while 1:

       # print 1
       # update_from_file(const.VID_TO_PROCESS_CSV_FILE)
        #print 2

        #print("perform queue operations - wait for lock")
        with CSV_FILES_DICT_rlock:    

            #print("perform queue operations")
            for csv_path, item in CSV_FILES_DICT.iteritems():

                

                performed_count = 0

                q = item["queue"]              


                # perform all operaions in queue
                while 1:
                    
                    if q.empty():
                        break


                    f, args = q.get()
                    CSV_FILES_DICT[csv_path]["rows"] = f(*([CSV_FILES_DICT[csv_path]["rows"]]+args))
                    performed_count += 1
                    q.task_done()   


                # sync changes to file
                if performed_count > 0:
                    sync_csv_to_file(csv_path)

                

            # finished queue
            # check if main thread is still alive
            is_main_thread_active = lambda : any((i.name == "MainThread") and i.is_alive() for i in threading.enumerate())
            #print("is_main_thread_active: %s" % str(is_main_thread_active()))

            if not is_main_thread_active():
                #print ("main thread is not alive - exit")
                sys.exit()


        #print ("performed %i queue operations" % performed_count)



        time.sleep(0.1) 
        

def maybe_start_csv_queue_worker_thread():
    global CSV_UPDATE_WORKER_THREAD

    if CSV_UPDATE_WORKER_THREAD == None:
        #print '[csv_utils] start_csv_queue_worker_thread'
        CSV_UPDATE_WORKER_THREAD = threading.Thread(target=csv_queue_worker)
        CSV_UPDATE_WORKER_THREAD.daemon = False
        CSV_UPDATE_WORKER_THREAD.start()

    return CSV_UPDATE_WORKER_THREAD

# CSV OPERATIONS


# read operations
def read_all(csv_path):
    #print("read_all")

    # lazy init
    init_csv_from_file(csv_path)

    #print("read_all2 %s" % csv_path)

    # wait untill all queued operations will finish
    with CSV_FILES_DICT[csv_path]["lock"]:
        #print("read_all3 - wait for queue ops: %i" % CSV_FILES_DICT[csv_path]["queue"].qsize())
        CSV_FILES_DICT[csv_path]["queue"].join()
        #print("read_all4")
        # now read latest data
        return CSV_FILES_DICT[csv_path]["rows"]


def get_column_csv(csv_path, column_index):
    data = read_all(csv_path)

    column = []

    for row in data:
        if len(row) > column_index:
            column.append(row[column_index])
    return column

def get_row_in_csv(csv_path, row_first_cell_val):
    data = read_all(csv_path)

    for row in data:        
        if len(row) > 0 and str(row[0]).strip() == str(row_first_cell_val).strip():
            return row
    return None

def is_item_in_csv(csv_path, item):
    return get_row_in_csv(csv_path, item) != None

# modify operations
def clear_csv(csv_path):
    # lazy init
    init_csv_from_file(csv_path)

    def _clear_op(lst):
        return []

    with CSV_FILES_DICT[csv_path]["lock"]:
        CSV_FILES_DICT[csv_path]["queue"].put((_clear_op, []))

def append_rows_to_csv(csv_path, rows):  
    # lazy init
    init_csv_from_file(csv_path)

    def _append_op(lst, rows):
        return lst + rows
    
    with CSV_FILES_DICT[csv_path]["lock"]:        
        CSV_FILES_DICT[csv_path]["queue"].put((_append_op, [rows]))    

def prepend_rows_to_csv(csv_path, rows):  
    # lazy init
    init_csv_from_file(csv_path)

    def _append_op(lst, rows):
        return rows+lst

    with CSV_FILES_DICT[csv_path]["lock"]:
        CSV_FILES_DICT[csv_path]["queue"].put((_append_op, [rows]))

def write_rows_to_csv(csv_path, rows):
    #print("write_rows_to_csv: %s %i" % (csv_path, len(rows)))

    # lazy init
    init_csv_from_file(csv_path)

    def _write_op(lst, rows):
        return rows

    #print("write_rows_to_csv - wait lock")
    with CSV_FILES_DICT[csv_path]["lock"]:
        #print("write_rows_to_csv - got lock")
        CSV_FILES_DICT[csv_path]["queue"].put((_write_op, [rows]))           

def append_column_to_csv(csv_path, column):    
    rows = []
    for val in column:
        rows.append([val])
    append_rows_to_csv(csv_path, rows)

def prepend_column_to_csv(csv_path, column):
    rows = []
    for val in column:
        rows.append([val])
    prepend_rows_to_csv(csv_path, rows)

def write_column_to_csv(csv_path, column):
    #print("write_column_to_csv")
    rows = []
    for val in column:
        rows.append([val])
    write_rows_to_csv(csv_path, rows)


def add_row_to_csv(csv_path, row):
    append_rows_to_csv(csv_path, [row])


def pop_first_row_in_csv(csv_path):    
    first_row = None    

    data = read_all(csv_path)

    if len(data) == 0:
        return None

    #print("pop_first_row_in_csv - get: %i" % len(data))

    first_row = data.pop(0)
    remove_row_by_first_val(csv_path, first_row[0])

    return first_row    

def remove_row_by_first_val(csv_path, val):

    # lazy init
    init_csv_from_file(csv_path)

    def _remove_row_op(lst, val):        
        new_data = []
        for row in lst:
            if not (len(row) > 0 and row[0] == val):
                new_data.append(row)

        return new_data

    with CSV_FILES_DICT[csv_path]["lock"]:        
        CSV_FILES_DICT[csv_path]["queue"].put((_remove_row_op, [val]))     
    
    