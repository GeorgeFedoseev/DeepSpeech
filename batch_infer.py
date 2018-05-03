# -*- coding:utf-8 -*-

import DeepSpeech

import sys

if __name__ == '__main__':
    DeepSpeech.initialize_globals()
    DeepSpeech.do_single_file_inference(sys.argv[1])