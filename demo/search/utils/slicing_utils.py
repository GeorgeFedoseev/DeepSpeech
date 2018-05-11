import re
import wave
import webrtcvad

def is_bad_piece(audio_duration, transcript):   

    MAX_SECS = 20
    MIN_SECS = 3    
    
    MIN_SEC_PER_SYMBOL = 0.04375

    # remove audios that are shorter than 0.5s and longer than 20s.
    # remove audios that are too short for transcript.
    if audio_duration > MIN_SECS and audio_duration < MAX_SECS and transcript!="" and audio_duration/len(transcript) > MIN_SEC_PER_SYMBOL:
        return True
    return False

def is_bad_subs(subs_text):
    bad = False

    if subs_text.strip() == "":
        bad = True

    if len(re.findall(r'[0-9]+', subs_text)) > 0:
        bad = True
    if len(re.findall(r'[A-Za-z]+', subs_text)) > 0:
        bad = True

    return bad


def slice_audio_by_silence(wave_obj, min_audio_length=5, max_audio_length=20, vad_silence_volume_param=1):
    SPEECH_FRAME_SEC = 0.01

    vad = webrtcvad.Vad(vad_silence_volume_param)

    samples_per_second = wave_obj.getframerate()    
    samples_per_frame = int(SPEECH_FRAME_SEC*samples_per_second)
    total_samples = wave_obj.getnframes()    
    
    wave_obj.setpos(0)

    out_pieces = []

    current_piece_start_sec = 0    
    current_piece_length_sec = 0

    current_piece_samples = ""

    total_length = 0

    searching_for_piece = False
    searching_for_piece_start_begin_sec = -1

    
    while wave_obj.tell() < total_samples:       
        
        wav_samples = wave_obj.readframes(samples_per_frame)
        current_frame_length_sec = float(samples_per_frame)/samples_per_second       

        
        try:
            is_speech = vad.is_speech(wav_samples, samples_per_second)
        except Exception as ex:
            #print("VAD Exception: %s" % str(ex))
            continue

        if searching_for_piece:
            current_piece_start_sec += current_frame_length_sec
            if is_speech:
                #print("WARNING: skipped %f seconds searching for speech start" % (current_piece_start_sec - searching_for_piece_start_begin_sec))
                searching_for_piece = False
            else:
                continue



        current_piece_length_sec += current_frame_length_sec
        current_piece_samples += wav_samples

        if (current_piece_length_sec > min_audio_length):
            if not is_speech:
                # push current piece to out
                out_pieces.append({
                    "start": current_piece_start_sec,
                    "end": current_piece_start_sec+current_piece_length_sec,
                    "samples": current_piece_samples
                    })
                total_length += current_piece_length_sec
                # and reset current piece
                current_piece_samples = ""
                current_piece_start_sec += current_piece_length_sec
                current_piece_length_sec = 0
            else:
                if current_piece_length_sec > max_audio_length:
                    #print("WARNING: cannot find end of piece, skip fragment and start searching for silence...")                    
                    searching_for_piece_start_begin_sec = current_piece_start_sec
                    current_piece_samples = ""
                    current_piece_start_sec += current_piece_length_sec
                    current_piece_length_sec = 0
                    searching_for_piece = True

                    # push current piece to out
                    # out_pieces.append({
                    #     "start": current_piece_start_sec,
                    #     "end": current_piece_start_sec+current_piece_length_sec,
                    #     "samples": current_piece_samples
                    #     })
                    # total_length += current_piece_length_sec
                    # and reset current piece
                    # current_piece_samples = ""
                    # current_piece_start_sec += current_piece_length_sec
                    # current_piece_length_sec = 0



    return out_pieces, total_length/len(out_pieces)