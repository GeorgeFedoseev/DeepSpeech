import sys
import csv
import time


csv_writer_lock = threading.Lock()

all_rows = []
clean_output_csv_path = None

total_passed_num = 0
approved_num = 0

def init_with_csv_paths(_csv_paths, _clean_output_path):
    global all_rows
    global clean_output_csv_path

    clean_output_csv_path = _clean_output_path

    for path in _csv_paths:
        with open(path, 'r') as f:
            all_rows += list(csv.reader(f))[1:]

def onDecoded(label, decoding):
    found_row = next([row for row in all_rows if row[2].strip() == label.strip()])
    if found_row:
        with open(clean_output_csv_path, "a+") as f:
            csv_writer = csv.writer(f)

            file_rows = list(csv.reader(f))

            if len(file_rows) == 0:
                # add header
                csv_writer.writerow(["wav_filename", "wav_filesize", "transcript"])

            already_exist_rows = file_rows[1:]

            if not any((row[0] == found_row[0] for row in already_exist_rows)):
                if is_good_cutting(label, decoding):
                    # add 
                    with csv_writer_lock:
                        csv_writer.writerow(found_row)
                        f.flush()
    else:
        print "ERROR: not found %s label in csvs" % (label)
    

def is_good_cutting(label, decoding):
    CER_CALC_NUM = 15

    global total_passed_num
    global approved_num

    total_passed_num+=1    

    original = label.strip()
    decoded = decodeding.strip()

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
        return True              
    else:
        print "SKIP"
        return False

    print "%.1f%% approved " % (float(approved_num)/float(total_passed_num)*100)


if __name__ == "__main__":
   pass
