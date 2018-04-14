#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import codecs
import sys
import tarfile
import pandas
import re
import unicodedata
import threading
from multiprocessing.pool import ThreadPool

from six.moves import urllib
from glob import glob
from os import makedirs, path
from bs4 import BeautifulSoup
from tensorflow.python.platform import gfile
from tensorflow.contrib.learn.python.learn.datasets import base

import subprocess
import os

from tqdm import tqdm

reload(sys)
sys.setdefaultencoding('utf8')

"""The number of jobs to run in parallel"""
NUM_PARALLEL = 8

"""Lambda function returns the filename of a path"""
filename_of = lambda x: path.split(x)[1]

class AtomicCounter(object):
    """A class that atomically increments a counter"""
    def __init__(self, start_count=0):
        """Initialize the counter
        :param start_count: the number to start counting at
        """
        self.__lock = threading.Lock()
        self.__count = start_count

    def increment(self, amount=1):
        """Increments the counter by the given amount
        :param amount: the amount to increment by (default 1)
        :return:       the incremented value of the counter
        """
        self.__lock.acquire()
        self.__count += amount
        v = self.value()
        self.__lock.release()
        return v

    def value(self):
        """Returns the current value of the counter (not atomic)"""
        return self.__count

def _parallel_downloader(voxforge_url, archive_dir, total, counter):
    """Generate a function to download a file based on given parameters
    This works by currying the above given arguments into a closure
    in the form of the following function.

    :param voxforge_url: the base voxforge URL
    :param archive_dir:  the location to store the downloaded file
    :param total:        the total number of files to download
    :param counter:      an atomic counter to keep track of # of downloaded files
    :return:             a function that actually downloads a file given these params
    """
    def download(d):
        """Binds voxforge_url, archive_dir, total, and counter into this scope
        Downloads the given file
        :param d: a tuple consisting of (index, file) where index is the index
                  of the file to download and file is the name of the file to download
        """
        (i, file) = d
        download_url = voxforge_url + '/' + file
        c = counter.increment()
        print('Downloading file {} ({}/{})...'.format(i+1, c, total))

        retry_cnt = 0
        while True:
            filename = filename_of(download_url)
            fullpath = path.join(archive_dir, filename)            
            base.maybe_download(filename, archive_dir, download_url)
            if path.getsize(fullpath) > 1000:
                print('done downloading '+download_url)
                break
            retry_cnt+=1
            print ('File failed to download - retrying...('+str(retry_cnt)+')')           
            
        
    return download

def _parallel_extracter(data_dir, number_of_test, number_of_dev, total, counter):
    """Generate a function to extract a tar file based on given parameters
    This works by currying the above given arguments into a closure
    in the form of the following function.

    :param data_dir:       the target directory to extract into
    :param number_of_test: the number of files to keep as the test set
    :param number_of_dev:  the number of files to keep as the dev set
    :param total:          the total number of files to extract
    :param counter:        an atomic counter to keep track of # of extracted files
    :return:               a function that actually extracts a tar file given these params
    """
    def extract(d):
        """Binds data_dir, number_of_test, number_of_dev, total, and counter into this scope
        Extracts the given file
        :param d: a tuple consisting of (index, file) where index is the index
                  of the file to extract and file is the name of the file to extract
        """
        (i, archive) = d
        if i < number_of_test:
            dataset_dir = path.join(data_dir, "test")
        elif i<number_of_test+number_of_dev:
            dataset_dir = path.join(data_dir, "dev")
        else:
            dataset_dir = path.join(data_dir, "train")


        try:
            if not gfile.Exists(path.join(dataset_dir, '.'.join(filename_of(archive).split(".")[:-1]))):
                c = counter.increment()
                print('Extracting file {} ({}/{})...'.format(i+1, c, total))
                tar = tarfile.open(archive, "r:*")
                tar.extractall(dataset_dir)
                tar.close()
        except Exception as e:
            print ("failed to extract "+archive+' '+str(e))
        
    return extract


def get_audio_length(input_file):    
    result = subprocess.Popen('ffprobe -i '+input_file+' -show_entries format=duration -v quiet -of csv="p=0"', stdout=subprocess.PIPE,stderr=subprocess.STDOUT, shell=True)
    output = result.communicate()

    return float(output[0])

def apply_bandpass_filter(in_path, out_path):
    # ffmpeg -i input.wav -acodec pcm_s16le -ac 1 -ar 16000 -af lowpass=3000,highpass=200 output.wav
    p = subprocess.Popen(["ffmpeg", "-y",
        "-acodec", "pcm_s16le",
         "-i", in_path,    
         "-acodec", "pcm_s16le",
         "-ac", "1",
         "-af", "lowpass=3000,highpass=200",
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

def _download_and_preprocess_data(data_dir):
    # Conditionally download data to data_dir
    if not path.isdir(data_dir):
        makedirs(data_dir)

    archive_dir = data_dir+"/archive"
    if not path.isdir(archive_dir):
        makedirs(archive_dir)

    print("Downloading Voxforge data set into {} if not already present...".format(archive_dir))

    #voxforge_url = 'http://www.repository.voxforge1.org/downloads/SpeechCorpus/Trunk/Audio/Main/16kHz_16bit'
    voxforge_url = 'http://www.repository.voxforge1.org/downloads/Russian/Trunk/Audio/Main/16kHz_16bit/'
    html_page = urllib.request.urlopen(voxforge_url)
    soup = BeautifulSoup(html_page, 'html.parser')

    # list all links
    refs = [l['href'] for l in soup.find_all('a') if ".tgz" in l['href']]

    # download files in parallel
    print('{} files to download'.format(len(refs)))
    downloader = _parallel_downloader(voxforge_url, archive_dir, len(refs), AtomicCounter())
    p = ThreadPool(NUM_PARALLEL)
    p.map(downloader, enumerate(refs))

    # Conditionally extract data to dataset_dir
    if not path.isdir(path.join(data_dir,"test")):
        makedirs(path.join(data_dir,"test"))
    if not path.isdir(path.join(data_dir,"dev")):
        makedirs(path.join(data_dir,"dev"))
    if not path.isdir(path.join(data_dir,"train")):
        makedirs(path.join(data_dir,"train"))

    tarfiles = glob(path.join(archive_dir, "*.tgz"))
    number_of_files = len(tarfiles)
    number_of_test = number_of_files//100
    number_of_dev = number_of_files//100

    # extract tars in parallel
    print("Extracting Voxforge data set into {} if not already present...".format(data_dir))
    extracter = _parallel_extracter(data_dir, number_of_test, number_of_dev, len(tarfiles), AtomicCounter())
    p.map(extracter, enumerate(tarfiles))

    # Generate data set
    print("Generating Voxforge data set into {}".format(data_dir))
    test_files, test_duration = _generate_dataset(data_dir, "test")
    dev_files, dev_duration = _generate_dataset(data_dir, "dev")
    train_files, train_duration = _generate_dataset(data_dir, "train")

    total_audio_duration = test_duration + dev_duration + train_duration

    print('Total audio duration: %s hours' % (format(total_audio_duration/3600, '.2f')))

    # Write sets to disk as CSV files
    train_files.to_csv(path.join(data_dir, "voxforge-train.csv"), index=False)
    dev_files.to_csv(path.join(data_dir, "voxforge-dev.csv"), index=False)
    test_files.to_csv(path.join(data_dir, "voxforge-test.csv"), index=False)

def _generate_dataset(data_dir, data_set):
    extracted_dir = path.join(data_dir, data_set)
    files = []

    dataset_audio_duration_sec = 0


    prompt_files = glob(path.join(extracted_dir+"/*/etc/", "PROMPTS"))

    pbar = tqdm(total=len(prompt_files))

    for promts_file in prompt_files:
        pbar.update(1)

        if path.isdir(path.join(promts_file[:-11],"wav")):
            with codecs.open(promts_file, 'r', 'utf-8') as f:
                for line in f:
                    #print ('line: '+line)
                    id = line.split(u' ')[0].split(u'/')[-1]
                    sentence = u' '.join(line.split(u' ')[1:])
                    sentence = re.sub(u"[^а-я]"," ",sentence.strip().lower())
                    transcript = ""
                    for token in sentence.split(" "):
                        word = token.strip()
                        if word!="" and word!=" ":
                            transcript += word + " "

                    
                    #transcript = unicodedata.normalize("NFKD", transcript.strip())
                    #print ('transcript: '+transcript)

                    wav_file = path.join(promts_file[:-11],"wav/" + id + ".wav")

                    
                    if gfile.Exists(wav_file):

                        # apply filters
                        filtered_path = path.join(promts_file[:-11],"wav/" + id + "_f.wav")
                        if not os.path.exists(filtered_path):
                            from_path = wav_file
                            if not os.path.exists(filtered_path):      
                                tmp_path = "%s.tmp.wav" % filtered_path
                                correct_volume(from_path, tmp_path)
                                apply_bandpass_filter(tmp_path, filtered_path)
                                # remove tmp
                                os.remove(tmp_path)

                        wav_file = filtered_path                       


                    
                        wav_filesize = path.getsize(wav_file)
                        audio_duration = wav_filesize/32000
                        

                        # remove audios that are shorter than 0.5s and longer than 20s.
                        # remove audios that are too short for transcript.
                        if audio_duration > 0.5 and audio_duration < 10 and transcript!="" and \
                            wav_filesize/len(transcript)>1400:

                            dataset_audio_duration_sec += audio_duration
                            files.append((path.abspath(wav_file), wav_filesize, transcript))

    return pandas.DataFrame(data=files, columns=["wav_filename", "wav_filesize", "transcript"]), dataset_audio_duration_sec

if __name__=="__main__":
    _download_and_preprocess_data(sys.argv[1])




