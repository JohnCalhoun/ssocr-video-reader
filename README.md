# Seven Segment Digit Video Reader
This project is a demo of how to read seven segment digits from a LCD screen in a video into a csv file!

## How it works
there are four steps in the processing pipeline. Four each frame in the video

1. Find and isolate the region containing the LCD screen ie. Text detection. Currently this uses the openCV EAST implementation. This takes up the majority of the runtime. see lib/get_roi.py and lib/extract for details. 
2. Convert the region of interest to a black and white image with white background and the LCD text has black. Basically; some simple thresholding. sett lib/process.py for details
3. Use [ssocr](https://www.unix-ag.uni-kl.de/~auerswal/ssocr/) to convert that black and white image to text ie. Text recognition. Next, take the output of ssocr and extract the numbers from it. The typical output of ssocr is messy and looks like “._00.0.” (or something like that) so I use a regex (\d+\.\d\d) to parse out the digits we are looking forsee lib/ocr.py for details

Next you need to clean up the output data. see post_processing.ipynb for some an example. the exact needs needed to clean the data will depend on your application. 

## Installation
- following instructions in https://github.com/auerswal/ssocr to build and install ssocr. the binary for ssocr will need to be on your $PATH
- create a data directory
```shell
mkdir data
```
- install dependencies
```shell
pip3 install -r requirements.txt
```

## Usage
the main script is ssocr-video.py and is usage is:
```
usage: ssocr-video.py [-h] [--log LOG] video output

Parses the seven segment display data from a video

positional arguments:
    video       the location of the video
    output      location to write output csv

optional arguments:
    -h, --help  show this help message and exit
    --log LOG   logging level

USAGE: ssocr-video ./data/video.mp4 ./data/output.csv
```
