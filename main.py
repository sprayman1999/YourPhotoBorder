#!/usr/bin/python3
from container.container import *
import sys
import argparse
import json
import os
from multiprocessing import Process
from analyzers.jpeg_analyzer import JpegAnalyzer
import re
args = None
config = {}

def init_argparse():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config",help="set your_photo_border config",required=True)
    parser.add_argument("-f","--file",help="load photo",required=False)
    parser.add_argument("-sf","--source-file",help="source photo with exif",required=False)
    parser.add_argument("-o","--output",help="save photo",required=True)
    args = parser.parse_args()
    
def load_config(path) -> dict:
    with open(path,"r") as f:
        return json.loads(f.read())
    
def test(input_path,output_path,source_path):
    for rule in config['rules']:
        camera_company = JpegAnalyzer(input_path).get_camera_company()
        if camera_company.find(rule['camera_company']) != -1:
            PhotoBorder(input_path,config,source_exif_path=source_path).generate().save(output_path)


def worker(input_path,output_path,rule,source_path=None):
    if JpegAnalyzer(input_path).get_image_orientation()[0] == 'Horizontal':
        border_config = rule['camera_horizontal_config']
    else:
        border_config = rule['camera_rotated_config']
    with open(border_config,"r") as f:
        PhotoBorder(f"{input_path}",json.loads(f.read()),source_exif_path=source_path) \
            .generate() \
            .save(output_path)
    
def folder_func(input_dir:str,output_dir:str,source_dir=None):
    white_list = ['.jpeg','.jpg']
    file_list = list(filter(lambda item: '.' + item.lower().split(".").pop() in white_list,os.listdir(input_dir)))
    for file in file_list:
        input_path = f"{input_dir}/{file}"
        output_path = f"{output_dir}/{file}"
        source_path = f"{source_dir}/{file}"
        for rule in config['rules']:
            camera_company = JpegAnalyzer(input_path).get_camera_company()
            if camera_company.find(rule['camera_company']) != -1:
                worker(input_path=input_path,output_path=output_path,rule=rule,source_path=source_path)
                break


def main():
    global config
    init_argparse()
    config = load_config(args.config)
    print(args)
    
    if os.path.isdir(args.file):
        if os.path.isdir(args.output) == False:
            print(f"[!] \"-o\" must be a folder.")
            exit(-1)
        folder_func(args.file,args.output,args.source_file)
    else:
        test(args.file,args.output)
    
if __name__ == "__main__":
    main()