import sys
import pandas

import csv

import infer

from util import text as text_utils

from multiprocessing.pool import ThreadPool
import threading

from tqdm import tqdm

import tensorflow as tf


csv_writer_lock = threading.Lock()


def filter_asr(csv_path, output_csv):
    # init deepspeech
    infer.init() 

    CER_CALC_NUM = 15
    NUM_THREADS = 4

    try:
        if csv_path.split(".")[-1] != "csv":
            raise
    except:
        print("Wrong input path: %s" % (csv_path))


    global total_passed_num
    global approved_num

    total_passed_num = 0
    approved_num = 0

    sessions_per_thread = {}

    with open(output_csv, 'a+') as csv_f:
        csv_writer = csv.writer(csv_f)        

        # load csv initial rows
        df = pandas.read_csv(csv_path, encoding='utf-8', na_filter=False)
        
        
        # exclude already processed
        already_processed_rows = list(csv.reader(csv_f))[1:] # skip header
        already_processed_files = [row[0] for row in already_processed_rows]
        rows_to_process = [list(row) for row in df.iterrows() if len(row) > 2 and row[0] not in already_processed_files]

        total_rows_to_process = len(rows_to_process)

        p_bar = tqdm(total=len(df))
        p_bar.update(len(already_processed_rows))

        if len(already_processed_rows) == 0:
            csv_writer.writerow(["wav_filename", "wav_filesize", "transcript"])

        session_tuple = infer.init_session()    

        def process_sample(row):
            #thread_name = threading.current_thread().getName()

            #print "processing in thread %s" % (thread_name)

            # if not (thread_name in sessions_per_thread):
            #     # create new session for this thread
            #     #print "created sessiion object for thread %s" % (thread_name)

            #     #scope = tf.get_variable_scope()
            #     #scope.reuse = tf.AUTO_REUSE

            #     #with tf.variable_scope(main_thread_scope, reuse=tf.AUTO_REUSE):
            #     session_tuple = infer.init_session() 
            #     sessions_per_thread[thread_name] = session_tuple
                
            #else:
                #print "using saved session for thread %s" % (thread_name)

            #session_tuple = sessions_per_thread[thread_name]


            #print "process item %i in %s" % (index, str())

            global total_passed_num
            global approved_num

            total_passed_num+=1
            

            original = row[2].strip()

            decoded = infer.infer(row[0], session_tuple)


            decoded = decoded.strip()

            print "-------------------"
            print original
            print decoded


            original_words = original.split()
            decoded_words = decoded.split()

            start_take_num = max(CER_CALC_NUM, len(original_words[0]))
            end_take_num = max(CER_CALC_NUM, len(original_words[-1]))        

            original_start = list(original)[:start_take_num]
            decoded_start = list(decoded)[:start_take_num]
            start_cer = text_utils.levenshtein(list(original_start), list(decoded_start))/float(len(original_start))

            original_end = list(original)[-end_take_num:]
            decoded_end = list(decoded)[-end_take_num:]
            end_cer = text_utils.levenshtein(list(original_end), list(decoded_end))/float(len(original_end))

            print "start: %s vs %s" % ("".join(original_start), "".join(decoded_start))

            print "end: %s vs %s" % ("".join(original_end), "".join(decoded_end))
            
            print "start_cer: %.3f, end_cer: %.3f" % (start_cer, end_cer)

            if start_cer < 0.5 and end_cer < 0.5:
                approved_num+=1
                row.append(1)                
            else:
                print "SKIP"
                row.append(0)

            with csv_writer_lock:
                csv_writer.writerow(row)                

            print "%.1f%% approved (%.2f%% processed of %i)" % (float(approved_num)/float(total_passed_num)*100,
                 float(total_passed_num)/float(total_rows)*100, total_rows_to_process)

            p_bar.update(1)       

        pool = ThreadPool(NUM_THREADS)
        pool.map(process_sample, rows_to_process)

        p_bar.close()


    pass

if __name__ == "__main__":
    #filter_asr("~/Desktop/test-file.csv")

    if len(sys.argv) <= 2:
        print("Usage: python asr-set-filter <dataset_csv_path> <output_csv_path>")
        sys.exit(1)

    filter_asr(sys.argv[1], sys.argv[2])
