import sys
if __name__ != "__main__":
    sys.path.append("../")

from analyzers.jpeg_analyzer import *
from analyzers.png_analyzer import *

from PIL import Image, ImageDraw, ImageCms

class PhotoBorder(object):
    def __init__(self,path:str ,config:dict):
        self.path = path
        self.analyzer = JpegAnalyzer(path)
        self.config = config
        self.output_profile = ImageCms.createProfile("sRGB")
        
    def get_canvas_width(self) -> int:
        if self.config['camera_args_direction'] == 'left' or self.config['camera_args_direction'] == 'right':
            return self.analyzer.get_width() + self.border_size * 2 + self.config['extra_length']
        else:
            return self.analyzer.get_width() + self.border_size * 2

    def get_canvas_height(self) -> int:
        if self.config['camera_args_direction'] == 'up' or self.config['camera_args_direction'] == 'down':
            return self.analyzer.get_height() + self.border_size * 2 + self.config['extra_length']
        else:
            return self.analyzer.get_width() + self.border_size * 2 

    def get_canvas_background(self) -> tuple:
        return (self.config['background'][0], self.config['background'][1], self.config['background'][2])

    def get_photo_position(self)->tuple:
        if self.config['camera_args_direction'] == 'left':
            return (self.config['extra_length'] + self.border_size,self.border_size)
        if self.config['camera_args_direction'] == 'right':
            return (self.border_size,self.border_size)
        if self.config['camera_args_direction'] == 'up':
            return (self.border_size,self.config['extra_length'] + self.border_size)
        if self.config['camera_args_direction'] == 'down':
            return (self.border_size,self.border_size)
    def generate(self):
        #MODES = ["1", "CMYK", "F", "HSV", "I", "L", "LAB", "P", "RGB", "RGBA", "RGBX", "YCbCr"]
        self.border_size = self.config['border_size']
        self.canvas_width = self.get_canvas_width()
        self.canvas_height = self.get_canvas_height()
        self.canvas_color = self.get_canvas_background()
        
        self.canvas = Image.new("RGB",(self.canvas_width,self.canvas_height),self.canvas_color)
        image = Image.open(self.path)
        
        self.canvas.paste(image,self.get_photo_position())
        image.close()
        return self
    
    def save(self,path):
        self.canvas.save("./output/output.jpg",format="JPEG")
        
def test():
    pass
def main():
    test()
if __name__ == "__main__":
    main()
'''
from PIL import Image, ImageDraw

# 创建画布
canvas_width = 800
canvas_height = 600
canvas_color = (255, 255, 255)  # 白色
canvas = Image.new("RGB", (canvas_width, canvas_height), canvas_color)

# 打开JPEG图像
image = Image.open("your_image.jpg")

# 缩放图像以适应画布
image = image.resize((canvas_width, canvas_height))

# 在画布上绘制图像
canvas.paste(image, (0, 0))

# 显示画布
canvas.show()
'''