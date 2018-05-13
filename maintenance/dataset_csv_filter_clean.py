# -*- coding: utf-8 -*-
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import csv

SAMPLE_RATE = 16000
BYTE_WIDTH = 2


def filter_clean(in_csv_path, out_csv_path, exclude_not_found=False):
    print "exclude_not_found: %s" % (str(exclude_not_found))

    with open(in_csv_path, 'r') as in_f:
        csv_reader = csv.reader(in_f)
        all_rows = list(csv_reader)[1:] # skip header
        
        print "total rows: %i" % (len(all_rows))


        # clean
        clean_rows = []
        for i, r in enumerate(all_rows):
            try:
                if int(r[3].strip()) == 1:
                    clean_rows.append([r[0], r[1], r[2]]) # append without last filter info column
            except Exception as ex:
                print "bad row %i %s" % (i+2, str(ex))

        print "clean rows: %i" % (len(clean_rows))
        if len(all_rows) > 0:
            print "clean rows percentage: %.1f%%" % (float(len(clean_rows))/len(all_rows)*100)


        found_clean_rows = []
        # calculate clean speech seconds
        clean_speech_seconds = 0
        found_files_count = 0
        for r in clean_rows:
            if os.path.exists(r[0]):
                found_files_count += 1

                wav_filesize = os.path.getsize(r[0])
                audio_length = float(wav_filesize)/SAMPLE_RATE/BYTE_WIDTH
                clean_speech_seconds += audio_length       
                found_clean_rows.append(r)     



        clean_speech_hours = clean_speech_seconds/3600

        print "not found files: %i" % (len(clean_rows) - found_files_count)
        print "found files percentage: %f%%" % (float(found_files_count)/len(clean_rows)*100)
        print "total clean speech hours: %.2f" % (clean_speech_hours)

        if exclude_not_found:
            clean_rows = found_clean_rows

        with open(out_csv_path, 'w') as out_f:
            csv_writer = csv.writer(out_f)
            csv_writer.writerow(["wav_filename", "wav_filesize", "transcript"])
            csv_writer.writerows(clean_rows)

        print "exported clean csv to %s" % (out_csv_path)


    pass



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('USAGE: python dataset_csv_filter_clean.py <in_csv_path> <out_csv_path> [--exclude-not-found]')
    else:

        exclude_not_found = False

        try:
            _ = sys.argv.index("--exclude-not-found")
            exclude_not_found = True
        except:
            pass

        filter_clean(sys.argv[1], sys.argv[2], exclude_not_found)






