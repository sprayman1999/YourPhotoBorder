#!/usr/bin/python3
from container.container import *
import sys
import argparse
import json
import os
from multiprocessing import Pool
from analyzers.jpeg_analyzer import JpegAnalyzer
import re
from concurrent.futures import ThreadPoolExecutor
args = None
config = {}

def init_argparse():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config",help="set your_photo_border config",required=True)
    parser.add_argument("-f","--file",help="load photo",required=False)
    parser.add_argument("-sf","--source-file",help="source photo with exif",required=False)
    parser.add_argument("-o","--output",help="save photo",required=True)
    parser.add_argument("-dim","--default-image-maker",help="default image maker",required=False)
    parser.add_argument("-ec","--enforce-config",help="enforce to set photo's config",required=False)
    args = parser.parse_args()
    
def load_config(path) -> dict:
    with open(path,"r") as f:
        return json.loads(f.read())
    
def photo_border_single_worker(input_path,output_path,source_path):
    local_source_path = input_path if source_path == input_path or source_path == None or source_path == "" else source_path
    analyzer = JpegAnalyzer(local_source_path)
    camera_company = analyzer.get_camera_company()
    if camera_company == None:
        camera_company = args.default_image_maker
    border_config = None
    target_rule = None
    for rule in config['rules']:
        if camera_company.lower().find(rule['camera_company'].lower()) != -1:
            target_rule = rule
            break
    
    if target_rule == None:
        print(f"[X] failed to generate photo because of null \"Image Maker\".\n\tPhotoPath: {input_path}\tOutputPath: {output_path}\tExifSourcePath: {local_source_path}")
        return

    if analyzer.get_image_orientation()[0] == 'Horizontal' and analyzer.get_width() > analyzer.get_height():
        border_config = target_rule['camera_horizontal_config']
    else:
        border_config = target_rule['camera_rotated_config']
    print(f"[*] Target Rule: {target_rule['camera_company']}\n\tPhotoPath: {input_path}\n\tOutputPath: {output_path}\n\tExifSourcePath: {local_source_path}\n\tConfig: {border_config}\n")
    with open(border_config,"r") as f:
        PhotoBorder(f"{input_path}",json.loads(f.read()),source_exif_path=local_source_path) \
            .generate() \
            .save(output_path)


def photo_border_worker(args):
    input_path, output_path, source_path = args
    photo_border_single_worker(input_path=input_path,output_path=output_path,source_path=source_path)

    
def folder_func(input_dir:str,output_dir:str,source_dir=None):
    global config
    white_list = ['.jpeg','.jpg']
    file_list = list(filter(lambda item: '.' + item.lower().split(".").pop() in white_list,os.listdir(input_dir)))

    with ThreadPoolExecutor(max_workers=4) as executor:
        task_list = []
        for file in file_list:
            print(f"find photo -> {file}")
            input_path = f"{input_dir}{os.sep}{file}"
            output_path = f"{output_dir}{os.sep}{file}"
            if source_dir != None:
                source_path = f"{source_dir}{os.sep}{file}"
            else:
                source_path = None
            print(f"create work -> {(input_path,output_path,source_path)}")
            task = executor.submit(photo_border_worker,(input_path,output_path,source_path))
            task_list.append(task)
            #pool.apply_async(func=photo_border_worker, args=(input_path,output_path,source_path))
            #photo_border_worker(input_path,output_path,source_path)
        for task in task_list:
            task.done()

    print("[*] All task is finished!")

def main():
    global config
    init_argparse()
    config = load_config(args.config)
    print(args)
    
    if os.path.isdir(args.file):
        if os.path.isdir(args.output) == False:
            print(f"[!] \"-o\" must be a folder.")
            exit(-1)
        if args.source_file != None and os.path.isdir(args.source_file) == False:
            print(f"[!] \"-sf\" must be a folder.")
            exit(-1)
        folder_func(args.file,args.output,args.source_file)
    else:
        photo_border_single_worker(args.file,args.output,args.source_file)
    
if __name__ == "__main__":
    main()
