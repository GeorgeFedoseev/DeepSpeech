# -*- coding:utf-8 -*-

import DeepSpeech
import tensorflow as tf

import sys
import re

import time

import os

from util import text as text_utils


initialized = False

def init(n_hidden, checkpoint_dir, alphabet_config_path="data/alphabet.txt", use_lm=False, language_tool_language='ru-RU'):
    global initialized

    if initialized:
        return

    sys.argv.append("--alphabet_config_path")
    sys.argv.append(alphabet_config_path)
    sys.argv.append("--n_hidden")
    sys.argv.append(str(n_hidden))
    sys.argv.append("--checkpoint_dir")
    sys.argv.append(checkpoint_dir)
    sys.argv.append("--infer_use_lm="+("1" if use_lm else "0"))
    sys.argv.append("--lt_lang="+language_tool_language)    


    DeepSpeech.initialize_globals()

    initialized = True

def init_session():
    print('Use Language Model: %s' % str(DeepSpeech.FLAGS.infer_use_lm))

    session = tf.Session(config=DeepSpeech.session_config)

    inputs, outputs = DeepSpeech.create_inference_graph(batch_size=1, use_new_decoder=DeepSpeech.FLAGS.infer_use_lm)
    # Create a saver using variables from the above newly created graph
    saver = tf.train.Saver(tf.global_variables())
    # Restore variables from training checkpoint
    # TODO: This restores the most recent checkpoint, but if we use validation to counterract
    #       over-fitting, we may want to restore an earlier checkpoint.
    checkpoint = tf.train.get_checkpoint_state(DeepSpeech.FLAGS.checkpoint_dir)
    if not checkpoint:
        print('Checkpoint directory ({}) does not contain a valid checkpoint state.'.format(DeepSpeech.FLAGS.checkpoint_dir))
        sys.exit(1)

    checkpoint_path = checkpoint.model_checkpoint_path
    saver.restore(session, checkpoint_path)

    return session, inputs, outputs


def infer(wav_path, session_tuple):
    session, inputs, outputs = session_tuple    

    start_time = time.time()
    mfcc = DeepSpeech.audiofile_to_input_vector(wav_path, DeepSpeech.n_input, DeepSpeech.n_context)
    

    start_time = time.time()
    output = session.run(outputs['outputs'], feed_dict={
        inputs['input']: [mfcc],
        inputs['input_lengths']: [len(mfcc)],
    })
    #print "INFER took %.2f" % (time.time() - start_time)

    text = DeepSpeech.ndarray_to_text(output[0][0], DeepSpeech.alphabet)

    return text

if __name__ == "__main__":

    start_time = time.time()
    init(n_hidden=2048,checkpoint_dir="/Users/gosha/Desktop/yt-vad-1k-2048/yt-vad-1k-2048-checkpoints", alphabet_config_path="data/alphabet.txt")
    print("DeepSpeech init took %.2f sec" % (time.time() - start_time))

    

    start_time = time.time()
    session = init_session()
    print("session init took %.2f sec" % (time.time() - start_time))

    test_file_path = os.path.join(os.getcwd(), "data/infer_test_3.wav")

    for i in range(0, 10):
        start_time = time.time()
        print infer(test_file_path, session)
        print("infer took %.2f sec" % (time.time() - start_time))













