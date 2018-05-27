import os
import sys
sys.path.insert(0,os.getcwd()) 

import const

import pafy

from timeout import timeout




@timeout(900)  # 15 mins deadline
def download_yt_audio(yt_video_id):

    curr_dir_path = const.curr_dir_path
    video_data_path = os.path.join(curr_dir_path, const.VIDEO_DATA_DIR + yt_video_id + "/")

    if not os.path.exists(video_data_path):
        os.makedirs(video_data_path)


    video = pafy.new(yt_video_id)
    # download audio
    audio_lowest_size = sorted(
        video.audiostreams, key=lambda x: x.get_filesize())[0]
    #print 'audio lowest download size: ' + str(audio_lowest_size.get_filesize())
    if audio_lowest_size.get_filesize() > 500000000:
        raise Exception("audio_file_is_too_big")

    audio_path = os.path.join(
        video_data_path, "audio." + audio_lowest_size.extension)

    if not os.path.exists(audio_path):
        print 'downloading audio ' + audio_path
        audio_lowest_size.download(filepath=audio_path, quiet=True)

    if not os.path.exists(audio_path):
        raise Exception("audio_download_failed")

    return audio_path