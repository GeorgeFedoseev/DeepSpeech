import sys
import pandas


from infer import infer

from util import text as text_utils


def filter_asr(csv_path):

    CER_CALC_NUM = 15

    try:
        if csv_path.split(".")[-1] != "csv":
            raise
    except:
        print("Wrong input path: %s" % (csv_path))

    df = pandas.read_csv(csv_path, encoding='utf-8', na_filter=False)
    for index, row in df.iterrows():
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


    pass

if __name__ == "__main__":
    #filter_asr("~/Desktop/test-file.csv")

    if len(sys.argv) <= 1:
        print("Usage: python asr-set-filter <dataset_csv_path>")
        sys.exit(1)

    filter_asr(sys.argv[1])
