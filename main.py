#!/usr/bin/python3
from container.container import *
import sys
import argparse
import json
args = None
config = {}
def init_argparse():
    global args
    parser = argparse.ArgumentParser()
    parser.add_argument("-c","--config",help="set your_photo_border config",required=True)
    parser.add_argument("-f","--file",help="load photo",required=True)
    parser.add_argument("-o","--output",help="save photo",required=True)
    args = parser.parse_args()
def load_config(path) -> dict:
    with open(path,"r") as f:
        return json.loads(f.read())
def test(photo_path,output_path):
    PhotoBorder(photo_path,config).generate().save(output_path)

def main():
    global config
    init_argparse()
    config = load_config(args.config)
    print(args)
    test(args.file,args.output)
if __name__ == "__main__":
    main()