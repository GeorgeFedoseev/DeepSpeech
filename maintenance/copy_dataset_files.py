# coding=utf-8
import os
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import csv

import shutil

from tqdm import tqdm




def copy_dataset_files(in_csv_path, out_dir_path):
    print "copying files from %s to %s" % (in_csv_path, out_dir_path)

    if not os.path.exists(out_dir_path):
        os.makedirs(out_dir_path)



    with open(in_csv_path, 'r') as in_f:
        csv_reader = csv.reader(in_f)
        all_rows = list(csv_reader)[1:] # skip header

        pbar = tqdm(total=len(all_rows))

        copy_count = 0

        for r in all_rows:
            from_path = r[0]
            to_path = os.path.join(out_dir_path, os.path.basename(from_path))
            if not os.path.exists(to_path) or os.path.getsize(from_path) != os.path.getsize(to_path):
                shutil.copyfile(from_path, to_path)
                copy_count += 1

            pbar.update(1)

        pbar.close()

        print "copy count: %i" % (copy_count) 




    



if __name__ == "__main__":
    if len(sys.argv) < 3:
        print('USAGE: python copy_dataset_files.py <in_csv_path> <out_dir_path>')
    else:
        copy_dataset_files(sys.argv[1], sys.argv[2])






