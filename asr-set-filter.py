import sys
import pandas

import csv

from infer import infer

from util import text as text_utils


def filter_asr(csv_path, output_csv):

    CER_CALC_NUM = 15

    try:
        if csv_path.split(".")[-1] != "csv":
            raise
    except:
        print("Wrong input path: %s" % (csv_path))



    total_passed_num = 0
    approved_num = 0

    with open(output_csv, 'wb') as csv_f:
        csv_writer = csv.writer(csv_f)

        # write header of new csv
        csv_writer.writerow(["wav_filename", "wav_filesize", "transcript"])

        df = pandas.read_csv(csv_path, encoding='utf-8', na_filter=False)
        for index, row in df.iterrows():
            total_passed_num+=1


            original = row[2].strip()

            decoded = infer(row[0])
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
                csv_writer.writerow(row)
            else:
                print "SKIP"

            print "%.1f approved" % (float(approved_num)/float(total_passed_num)*100)


    pass

if __name__ == "__main__":
    #filter_asr("~/Desktop/test-file.csv")

    if len(sys.argv) <= 2:
        print("Usage: python asr-set-filter <dataset_csv_path> <output_csv_path>")
        sys.exit(1)

    filter_asr(sys.argv[1], sys.argv[2])
