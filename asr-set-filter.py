import sys
import pandas


from infer import infer

from util import text as text_utils


def filter_asr(csv_path):

    CER_CALC_NUM = 5

    try:
        if csv_path.split(".")[-1] != "csv":
            raise
    except:
        print("Wrong input path: %s" % (csv_path))

    df = pandas.read_csv(csv_path, encoding='utf-8', na_filter=False)
    for index, row in df.iterrows():
        original = row[2]

        decoded = infer(row[0])
        decoded = decoded.strip()

        print "-------------------"
        print original
        print decoded

        original_start = list(original)[:CER_CALC_NUM]
        decoded_start = list(decoded)[:CER_CALC_NUM]
        start_cer = text_utils.levenshtein(list(original_start), list(decoded_start))/float(len(original_start))

        original_end = list(original)[-CER_CALC_NUM:]
        decoded_end = list(decoded)[-CER_CALC_NUM:]
        end_cer = text_utils.levenshtein(list(original_end), list(decoded_end))/float(len(original_end))

        print "start: %s vs %s" % ("".join(original_start), "".join(decoded_start))
        
        print "end: %s vs %s" % ("".join(original_end), "".join(decoded_end))
        
        print "start_cer: %.3f, end_cer: %.3f" % (start_cer, end_cer)


    pass

if __name__ == "__main__":
    #filter_asr("~/Desktop/test-file.csv")

    if len(sys.argv) <= 1:
        print("Usage: python asr-set-filter <dataset_csv_path>")
        sys.exit(1)

    filter_asr(sys.argv[1])
