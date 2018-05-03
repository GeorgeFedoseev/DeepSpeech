import sys
import time

from infer import infer

if __name__ == '__main__':
    text = input_file_path = sys.argv[1]

    start_time = time.time()
    text = infer(input_file_path)
    print(text)
    print(" ".join(text.split()))

    print("Inference took %.2f seconds" % (time.time() - start_time))