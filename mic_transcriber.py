import mic_listener
import infer

import time

from util import audio_filter_utils as audio_utils

import os

import wave


from threading import Thread


if __name__ == "__main__":
    start_time = time.time()
    infer.init(n_hidden=2048,
        checkpoint_dir="/Users/gosha/Desktop/yt-vad-1k-2048/yt-vad-1k-2048-checkpoints",
        alphabet_config_path="data/alphabet.txt",
        language_tool_language="")
    print("DeepSpeech init took %.2f sec" % (time.time() - start_time))

    

    start_time = time.time()
    session = infer.init_session()
    print("session init took %.2f sec" % (time.time() - start_time))




    def mic_listener_callback(rec_path):
        #print "got path %s" % rec_path

        def transcriber_worker(rec_path):
            
            wav_obj = wave.open(rec_path)
            if not audio_utils.has_speech(wav_obj):
                #print "no speech"
                return
                
            print "got speech"
            

            tmp_dir_path = os.path.join(os.getcwd(), "tmp")
            # filter
            # normalize volume
            audio_wav_volume_normalized_path = rec_path+"_normalized.wav"        
            #print("Normalizing volume... %s" % (audio_wav_path))
            audio_utils.loud_norm(rec_path, audio_wav_volume_normalized_path)

            # correct volume
            audio_wav_volume_corrected_path = rec_path+"_volume_corrected.wav"        
            #print("Correcting volume...")
            audio_utils.correct_volume(audio_wav_volume_normalized_path, audio_wav_volume_corrected_path)

            # apply bandpass filter
            audio_wav_filtered_path = rec_path+"_filtered.wav"   
            #print("Applying bandpass filter...")
            audio_utils.apply_bandpass_filter(audio_wav_volume_corrected_path, audio_wav_filtered_path)


            start_time = time.time()
            print "t: " + infer.infer(audio_wav_filtered_path, session)
            print "infer took: %.2f sec" % (time.time()-start_time)

        thr = Thread(target=transcriber_worker, args=[rec_path])
        thr.daemon = True
        thr.start()

    mic_listener.init(_recording_dir="tmp", _callback_func=mic_listener_callback)
    mic_listener.listen()