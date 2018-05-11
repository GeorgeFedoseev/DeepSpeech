import infer
import time
from util import audio_filter_utils as audio_utils
import os
import wave

current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir)
data_path = os.path.join(project_root_path, "data")

initialized = False
def init():
    global session, initialized

    if initialized:
        return



    start_time = time.time()
    infer.init(language_tool_language="")
    print("DeepSpeech init took %.2f sec" % (time.time() - start_time))

    

    start_time = time.time()
    session = infer.init_session()
    print("session init took %.2f sec" % (time.time() - start_time))

    initialized = True


def transcribe_file(rec_path):
            
    wav_obj = wave.open(rec_path)
    #if not audio_utils.has_speech(wav_obj):
        #print "no speech"
    #    return ""

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
    
    return infer.infer(audio_wav_filtered_path, session)
    

      