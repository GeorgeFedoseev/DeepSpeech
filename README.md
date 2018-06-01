# DeepSpeech for Russian language

Project DeepSpeech is an open source Speech-To-Text engine implemented by Mozilla, 
based on [Baidu's Deep Speech research paper](https://arxiv.org/abs/1412.5567)
using [TensorFlow](https://www.tensorflow.org/).

This particular repository is focused on creating big vocabulary ASR system for Russian language.

Big datasets for training are being crawled
using [developed method](https://github.com/GeorgeFedoseev/YouTube-Captions-Based-Speech-Dataset-Parser) 
from YouTube videos with captions.

Developed speech recognition system for Russian language achieves 21% WER on custom
dataset crawled from [voxforge.com](http://www.repository.voxforge1.org/downloads/Russian/Trunk/Audio/Main/16kHz_16bit/).


Created ASR system was applied to speech search task in big collection of video files.  


Here is a demo:  


![search-demo-5](search-demo-5.gif)
