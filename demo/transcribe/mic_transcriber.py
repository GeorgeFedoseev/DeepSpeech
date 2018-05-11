import os
import sys
current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir, os.pardir)
sys.path.insert(0, project_root_path)

import mic_listener
import infer

import time

from util import audio_filter_utils as audio_utils



import wave


from threading import Thread



data_path = os.path.join(project_root_path, "data")
tmp_dir_path = os.path.join(project_root_path, "tmp")


if __name__ == "__main__":
    start_time = time.time()
    infer.init(language_tool_language="")
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

    mic_listener.init(_recording_dir=tmp_dir_path, _callback_func=mic_listener_callback)
    mic_listener.listen()