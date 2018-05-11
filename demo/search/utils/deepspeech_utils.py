import os
import subprocess

import sys
sys.path.insert(0,os.getcwd()) 

import audio_utils

import const


GRAPH_PATH = os.path.join(const.DEEP_SPEECH_MODEL_PATH, "output_graph.pb")
ALPHABET_PATH = os.path.join(const.DEEP_SPEECH_MODEL_PATH, "alphabet.txt")

LM_PATH = os.path.join(const.DEEP_SPEECH_MODEL_PATH, "lm.binary")
TRIE_PATH = os.path.join(const.DEEP_SPEECH_MODEL_PATH, "trie")

def run_deepspeech_for_wav(wav_file_path, use_lm = True):    

    if use_lm:
        p = subprocess.Popen(["deepspeech",        
             GRAPH_PATH,
             ALPHABET_PATH,
             LM_PATH,
             TRIE_PATH,
             wav_file_path,         
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        p = subprocess.Popen(["deepspeech",        
             GRAPH_PATH,
             ALPHABET_PATH,             
             wav_file_path,         
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    if p.returncode != 0:
        raise Exception("Failed to apply bandpass filter: %s" % str(err))

    return out

if __name__ == "__main__":
    # test
    test_wav_path = os.path.join(curr_dir_path, "data/test_piece.wav")
    test_piece_volc_path = test_wav_path+".volc.wav"
    test_piece_filtered_path = test_wav_path+".f.wav"
    test_piece_volc_f_path = test_wav_path+".volc.f.wav"


    # test different volumes
    # result: optimal is -12db
    # for db in range(-20, 20, 2):
    #     audio_utils.correct_volume(test_wav_path, test_piece_volc_path, db=db)
    #     print "vol correct %i db" % db
    #     print run_deepspeech_for_wav(test_piece_volc_path, use_lm=False)

    

    # test different filters
    # result: 2300-3500 optimum
    # for lowpass in range(1300, 5000, 100):

    #     audio_utils.apply_bandpass_filter(test_piece_volc_path, test_piece_filtered_path, low=lowpass)
    #     print "lowpass %i" % lowpass
    #     print run_deepspeech_for_wav(test_piece_filtered_path, use_lm=False)     



    # Test order
    # result volume first better
    # first volume correct, then filter
    # audio_utils.correct_volume(test_wav_path, test_piece_volc_path, db=-12)
    # audio_utils.apply_bandpass_filter(test_piece_volc_path, test_piece_filtered_path, low=2500)
    # print "first volume correct, then filter"
    # print run_deepspeech_for_wav(test_piece_filtered_path, use_lm=False)

    # # first filter, then volume correct
    # audio_utils.apply_bandpass_filter(test_wav_path, test_piece_filtered_path, low=2500)
    # audio_utils.correct_volume(test_piece_filtered_path, test_piece_volc_path, db=-12)
    # print "first filter, then volume correct"
    # print run_deepspeech_for_wav(test_piece_volc_path, use_lm=False)

    audio_utils.correct_volume(test_wav_path, test_piece_volc_path, db=-12)
    audio_utils.apply_bandpass_filter(test_piece_volc_path, test_piece_filtered_path, low=2500)
    
    print "lm"
    print run_deepspeech_for_wav(test_piece_filtered_path, use_lm=True)
















