import os
import sys
current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir)
sys.path.insert(0, project_root_path)

import const

import subprocess



# /DeepSpeech/data/lm/kenlm/build/bin/lmplz --text /DeepSpeech/data/lm/vocabulary.txt --arpa /DeepSpeech/data/lm/words.arpa --o 3 --prune 0 2 2 -S 50%
# /DeepSpeech/data/lm/kenlm/build/bin/build_binary -T -s /DeepSpeech/data/lm/words.arpa /DeepSpeech/data/lm/lm.binary
# /DeepSpeech/native_client/generate_trie /DeepSpeech/data/alphabet.txt /DeepSpeech/data/lm/lm.binary /DeepSpeech/data/lm/vocabulary.txt /DeepSpeech/data/lm/trie

def create_lm(vocabulary_path, o=5, prune=2):

    lmplz_path = os.path.join(const.DEEP_SPEECH_PROJECT_ROOT_PATH, "native_client/kenlm/build/bin/lmplz")
    build_binary_path = os.path.join(const.DEEP_SPEECH_PROJECT_ROOT_PATH, "native_client/kenlm/build/bin/build_binary")
    generate_trie_path = os.path.join(const.DEEP_SPEECH_PROJECT_ROOT_PATH, "native_client/generate_trie")

    prune_str = "0 "
    for i in range(0, o-1):
        prune_str += str(prune)+" "


    command = ("%s --text %s --arpa %s --o %i --prune %s -S 50%%" % (lmplz_path, vocabulary_path, const.DEEP_SPEECH_ARPA_PATH, o, prune_str)) \
    + (" && %s -T -s %s %s" % (build_binary_path, const.DEEP_SPEECH_ARPA_PATH, const.DEEP_SPEECH_LM_PATH)) \
    + (" && %s %s %s %s %s" % (generate_trie_path, const.DEEP_SPEECH_ALPHABET_PATH, const.DEEP_SPEECH_LM_PATH, vocabulary_path, const.DEEP_SPEECH_TRIE_PATH))

    print command

    p = subprocess.Popen([
        command
    ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

    out, err = p.communicate()

    if p.returncode != 0:
        raise Exception("Failed to create language model: %s" % str(err))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        o = 5
        prune = 2

        if len(sys.argv) > 2:
            o = int(sys.argv[2])

        if len(sys.argv) > 3:
            prune = int(sys.argv[3])

        create_lm(sys.argv[1], o, prune)
    else:
        print "Usage: create_language_model.py <path-to-vocabulary-text-fie> [<o - max word seq len>] [<prune - min number of word occurences>]"