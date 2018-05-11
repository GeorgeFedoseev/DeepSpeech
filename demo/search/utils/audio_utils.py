# -*- coding: utf-8 -*-

import subprocess
import wave

import numpy as np
import webrtcvad



def apply_bandpass_filter(in_path, out_path, low=3000, high=200):
    # ffmpeg -i input.wav -acodec pcm_s16le -ac 1 -ar 16000 -af lowpass=3000,highpass=200 output.wav
    p = subprocess.Popen(["ffmpeg", "-y",
        #"-acodec", "pcm_s16le",
         "-i", in_path,    
         "-acodec", "pcm_s16le",
         "-ac", "1",
         "-af", "lowpass=%i,highpass=%i" % (low, high),
         "-ar", "16000",         
         out_path
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    if p.returncode != 0:
        raise Exception("Failed to apply bandpass filter: %s" % str(err))

def correct_volume(in_path, out_path, db=-10):
    # sox input.wav output.wav gain -n -10
    p = subprocess.Popen(["sox",
         in_path,             
         out_path,
         "gain",
         "-n", str(db)
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    if p.returncode != 0:
        raise Exception("Failed to correct volume: %s" % str(err))


def cut_wave(wave_obj, outfilename, start_ms, end_ms):
    width = wave_obj.getsampwidth()
    rate = wave_obj.getframerate()
    fpms = rate / 1000 # frames per ms
    length = (end_ms - start_ms) * fpms
    start_index = start_ms * fpms

    out = wave.open(outfilename, "w")
    out.setparams((wave_obj.getnchannels(), width, rate, length, wave_obj.getcomptype(), wave_obj.getcompname()))
    
    wave_obj.rewind()
    anchor = wave_obj.tell()
    wave_obj.setpos(anchor + start_index)
    out.writeframes(wave_obj.readframes(length))

def save_wave_samples_to_file(wave_samples, n_channels, byte_width, sample_rate, file_path):
    out = wave.open(file_path, "w")
    length = len(wave_samples)
    out.setparams((n_channels, byte_width, sample_rate, length, 'NONE', 'not compressed'))    
    out.writeframes(wave_samples)
    out.close()

def convert_to_wav(in_audio_path, out_audio_path):
    print 'converting %s to wav' % in_audio_path
    p = subprocess.Popen(["ffmpeg", "-y",
         "-i", in_audio_path,         
         "-ac", "1",
         "-ab", "16",
         "-ar", "16000",         
         out_audio_path
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    try:
        p.kill()
    except:
        pass

    if p.returncode != 0:
        print("failed_ffmpeg_conversion "+str(err))
        return False
    return True

def cut_audio_piece_to_wav(in_audio_path, out_audio_path, start_sec, end_sec):
    p = subprocess.Popen(["ffmpeg", "-y",
         "-i", in_audio_path,
         "-ss", str(start_sec),
         "-to", str(end_sec),
         "-ac", "1",
         "-ab", "16",
         "-ar", "16000",         
         out_audio_path
         ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    out, err = p.communicate()

    try:
        p.kill()
    except:
        pass

    if p.returncode != 0:
        print("failed_ffmpeg_conversion "+str(err))
        return False
    return True





# WAVE CUT CORRECTION
SPEECH_FRAME_SEC = 0.01
CHECK_FRAMES_NUM = 6

def get_speech_int_array(wave, start, end):
    vad = webrtcvad.Vad(3)

    samples_per_second = wave.getframerate()


    samples_per_frame = int(SPEECH_FRAME_SEC*samples_per_second)
    
    
    wave.setpos(start*samples_per_second)

    wave_view_int = []
    while wave.tell() < end*samples_per_second:
        #wave_view_str += "1" if vad.is_speech(wave.readframes(samples_to_get), sample_rate) else "0"
        try:
            wav_samples = wave.readframes(samples_per_frame)
            wave_view_int.append(1 if vad.is_speech(wav_samples, samples_per_second) else 0)                   
        except:
            return []

    return wave_view_int 

def has_speech(wave, start, end):
    speech_array = get_speech_int_array(wave, start, end)
    return np.sum(speech_array) > 0

def starts_with_speech(wave, start, end):
    speech_array = get_speech_int_array(wave, start, end)
    #print 'start2: '+(''.join([str(x) for x in speech_array]))
    return np.sum(speech_array[:CHECK_FRAMES_NUM]) > 0

def ends_with_speech(wave, start, end): 
    speech_array = get_speech_int_array(wave, start, end)
    #print 'end2: '+(''.join([str(x) for x in speech_array]))
    return np.sum(speech_array[-CHECK_FRAMES_NUM:]) > 0

def starts_or_ends_during_speech(wave, start, end):
    speech_array = get_speech_int_array(wave, start, end)

    return np.sum(speech_array[-CHECK_FRAMES_NUM:]) > 0 or np.sum(speech_array[:CHECK_FRAMES_NUM]) > 0


MAX_ALLOWED_CORRECTION_FW_SEC = 0.5
MAX_ALLOWED_CORRECTION_BW_SEC = 0.2
CORRECTION_WINDOW_SEC = SPEECH_FRAME_SEC*5
def try_correct_cut(wave, start, end):

    #print 'try correct cut'

    corrected_start = start   

    need_start_correction = starts_with_speech(wave, start, end)


    if need_start_correction:               
        # try go forward
        while need_start_correction and corrected_start <= start + MAX_ALLOWED_CORRECTION_FW_SEC:            
            corrected_start += CORRECTION_WINDOW_SEC
            need_start_correction = starts_with_speech(wave, corrected_start, end)

        # DISABLE backwards correction for start cause many bad samples with extra word on start
        # if need_start_correction:
        #     # try go backwards
        #     corrected_start = start
        #     while need_start_correction and corrected_start >= start - MAX_ALLOWED_CORRECTION_SEC:            
        #         corrected_start -= CORRECTION_WINDOW_SEC
        #         need_start_correction = starts_with_speech(wave, corrected_start, end)

    if need_start_correction:
        #print 'FAILED to correct start'
        return None



    need_end_correction = ends_with_speech(wave, start, end)
    corrected_end = end

    if need_end_correction:
        # try go forward
        while need_end_correction and corrected_end <= end + MAX_ALLOWED_CORRECTION_FW_SEC:            
            corrected_end += CORRECTION_WINDOW_SEC
            need_end_correction = ends_with_speech(wave, corrected_start, corrected_end)

        if need_end_correction:
            # try go backwards
            corrected_end = end
            while need_end_correction and corrected_end >= end - MAX_ALLOWED_CORRECTION_BW_SEC:            
                corrected_end -= CORRECTION_WINDOW_SEC
                need_end_correction = ends_with_speech(wave, corrected_start, corrected_end)

    if need_end_correction:
        #print 'FAILED to corrected_end'
        return None

    if corrected_start > corrected_end:
        return None

    print 'SUCCESS corrected cut: %f-%f -> %f-%f' % (start, end, corrected_start, corrected_end)

    return (corrected_start, corrected_end)


def print_speech_int_array(speech_int_array):
    print ''.join([str(x) for x in speech_int_array])


def print_speech_frames(wave, start, end):

    wave_view_int = get_speech_int_array(wave, start, end)

    print_speech_int_array(wave_view_int)


    start_view = wave_view_int[:3]
    end_view = wave_view_int[-3:]

    #print  'start: '+(''.join([str(x) for x in start_view]))
    #print  'end: '+(''.join([str(x) for x in end_view]))

    is_speech_on_start = np.sum(start_view)  > 0
    is_speech_on_end = np.sum(end_view)  > 0

    

    #print 'is_speech_on_start: '+str(is_speech_on_start) 
    #print 'is_speech_on_end: '+str(is_speech_on_end)

    return is_speech_on_start or is_speech_on_end


