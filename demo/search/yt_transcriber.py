import os
import sys
reload(sys)

sys.setdefaultencoding("utf-8")

current_dir_path = os.path.dirname(os.path.realpath(__file__))
project_root_path = os.path.join(current_dir_path, os.pardir, os.pardir)
sys.path.insert(0, project_root_path)

import subprocess
import wave
import shutil

import const
from utils.yt_utils import download_yt_audio
from utils.slicing_utils import slice_audio_by_silence
from utils import audio_utils


from models import Transcription
from utils import db_util

from timeit import default_timer as timer

import file_transcriber

import indexer

import csv
import time


# YT_VIDEOS_TO_INDEX = [
#     "EC9t2-Lkgl4",
#     "AhZa26nDZfA",
#     "NTqB5ged4Rw",
#     "SAQFzYnRTts",
#     "LR_n8at2ORg",
#     "LrHIBkjOl2Y",
#     "0XRUbnKznOI",
#     "uuULi6X6yqU",
#     "RedxkKdFfkY",
#     "6KiAr8w6o7E"
# ]


class TimedOutExc(Exception):
  pass

def deadline(timeout, *args):
  def decorate(f):
    def handler(signum, frame):
      raise TimedOutExc()

    def new_f(*args):

      signal.signal(signal.SIGALRM, handler)
      signal.alarm(timeout)
      return f(*args)
      signa.alarm(0)

    new_f.__name__ = f.__name__
    return new_f
  return decorate



def check_dependencies():
    try:
        subprocess.check_output(['soxi'], stderr=subprocess.STDOUT)        
        subprocess.check_output(['ffmpeg', '--help'], stderr=subprocess.STDOUT)
        #subprocess.check_output(['deepspeech', '-h'], stderr=subprocess.STDOUT)
    except Exception as ex:
        print 'ERROR: some of dependencies are not installed: ffmpeg or sox: '+str(ex)
        return False

    return True



def process_video(yt_video_id, video_title):
    print("process video %s" % (yt_video_id))    

    video_data_path = os.path.join(const.VIDEO_DATA_DIR, yt_video_id)

    video_done_flag_path = os.path.join(video_data_path, "DONE")

    if os.path.exists(video_done_flag_path):
        print 'already processed'
        return

    # download video
    try:
        @deadline(900) # 15 mins deadline
        original_audio_path = download_yt_audio(yt_video_id)
    except Exception as ex:
        print 'Error downloading: %s\nRetrying in 5 sec...' % (str(ex))
        time.sleep(5)
        process_video(yt_video_id, video_title)

    # convert audio and apply filters
    wav_audio_path = os.path.join(video_data_path, "audio.wav")
    if not os.path.exists(wav_audio_path):
        audio_utils.convert_to_wav(original_audio_path, wav_audio_path)

    wav_vol_corr_path = os.path.join(video_data_path, "audio_vol_corr.wav")
    print("correct_volume")
    if not os.path.exists(wav_vol_corr_path):  
       audio_utils.correct_volume(wav_audio_path, wav_vol_corr_path, db=-12)

    wav_filtered_path = os.path.join(video_data_path, "audio_filtered.wav")
    if not os.path.exists(wav_filtered_path):    
        print("apply_bandpass_filter")
        audio_utils.apply_bandpass_filter(wav_vol_corr_path, wav_filtered_path, low=2500)

    wave_o = wave.open(wav_filtered_path, "r")

    print("slice audio")
    pieces, avg_len_sec = slice_audio_by_silence(wave_o)
    print("total pieces: %i, avg_len_sec: %f" % (len(pieces), avg_len_sec))

    
    pieces_folder_path = os.path.join(video_data_path, "pieces/")
    if not os.path.exists(pieces_folder_path):
        os.makedirs(pieces_folder_path)

    


    print("start transcribing...")
    for i, piece in enumerate(pieces):

        piece_procesing_path = os.path.join(pieces_folder_path, "piece_%i_%.2f_processing.wav" % (i, piece["start"]))
        piece_done_path = os.path.join(pieces_folder_path, "piece_%i_%.2f_done.wav" % (i, piece["start"]))

        if not (os.path.exists(piece_procesing_path) or os.path.exists(piece_done_path)):
            audio_utils.save_wave_samples_to_file(piece["samples"], n_channels=1, byte_width=2, sample_rate=16000, file_path=piece_procesing_path)        

        if not os.path.exists(piece_done_path):
            # run inference
            start_t = timer()
            print("Transcribing piece %s" % piece_procesing_path)
            transcript = file_transcriber.transcribe_file(piece_procesing_path).decode("utf-8").strip()            
            print("transcription took %.f seconds" % (timer()-start_t))

            print(transcript)            

            video_title = video_title.decode("utf-8").strip()
            t = Transcription(media_type="youtube", media_name=video_title, media_id=yt_video_id, time_start=piece["start"], time_end=piece["end"], transcription=transcript)
            db_util.add_item(t)            

            os.rename(piece_procesing_path, piece_done_path)

    with open(video_done_flag_path, 'w'):
        pass

    print 'DONE'
        

if __name__ == "__main__":

    if len(sys.argv) > 1:

        if check_dependencies():
            db_util.init_db()

            with open(sys.argv[1], 'r') as csv_f:
                yt_video_rows = list(csv.reader(csv_f))

            for r in yt_video_rows:
                process_video(r[0], r[1])

            print 'rebuilding search index...'
            indexer.index_all()
    else:
        print 'Usage: yt_transcriber.py <path_to_csv>'
















