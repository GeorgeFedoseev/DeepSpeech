import sys
import pandas


from infer import infer


def filter_asr(csv_path):

    try:
        if csv_path.split(".")[-1] != "csv":
            raise
    except:
        print("Wrong input path: %s" % (csv_path))

    df = pandas.read_csv(csv_path, encoding='utf-8', na_filter=False)
    for index, row in df.iterrows():
        print infer(row[0])

    pass

if __name__ == "__main__":
    #filter_asr("~/Desktop/test-file.csv")

    if len(sys.argv) <= 1:
        print("Usage: python asr-set-filter <dataset_csv_path>")
        sys.exit(1)

    filter_asr(sys.argv[1])
