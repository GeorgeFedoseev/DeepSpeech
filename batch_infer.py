# -*- coding:utf-8 -*-

import DeepSpeech

import sys

import time

if __name__ == '__main__':
    DeepSpeech.initialize_globals()

    for i in range(0, 20):
        print("Inference %i" % (i))
        start_time = time.time()
        DeepSpeech.do_single_file_inference(sys.argv[1])
        print("Inference %i took %.2f seconds" % (i, time.time() - start_time))