# -*- coding:utf-8 -*-

import DeepSpeech
import tensorflow as tf

import sys
import re

import time

from util import text as text_utils



global session, inputs, outputs
session = None
inputs = None
outputs = None

def init_session():
    global session, inputs, outputs

    if session:
        return

    DeepSpeech.initialize_globals()

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


if __name__ == '__main__':

    global session, inputs, outputs

    init_session()

    print('Use Language Model: %s' % str(DeepSpeech.FLAGS.infer_use_lm))
        
    #print("Inference %i" % (i))
    start_time = time.time()

    input_file_path = sys.argv[1]

    mfcc = DeepSpeech.audiofile_to_input_vector(input_file_path, DeepSpeech.n_input, DeepSpeech.n_context)
    output = session.run(outputs['outputs'], feed_dict={
        inputs['input']: [mfcc],
        inputs['input_lengths']: [len(mfcc)],
    })

    text = DeepSpeech.ndarray_to_text(output[0][0], DeepSpeech.alphabet)

    # if DeepSpeech.languageTool != None:
    #     text = DeepSpeech.languageTool.correct(text)
    #     text = text.replace("ё", "е")
    #     text = re.sub(u'[^a-zа-я- ]+', '', text)
    print(text)
    print("Inference took %.2f seconds" % (time.time() - start_time))