import sys
if __name__ != "__main__":
    sys.path.append("../")

from analyzers.jpeg_analyzer import *
from analyzers.png_analyzer import *
from utils.utils import *
from PIL import Image, ImageDraw, ImageFont
import imghdr

class PhotoBorder(object):
    def __init__(self,path:str ,config:dict,source_exif_path: str = ""):
        if source_exif_path == "":
            self.source_exif_path = path
        else:
            self.source_exif_path = source_exif_path
            
        
        self.path = path
        if path.lower().endswith(".jpg") or path.endswith(".jpeg"):
            self.analyzer = JpegAnalyzer(path)
        self.config = config
        
        
        # 二次修正数据
        self.fix_config()
        
    def fix_config(self):
        if self.config['camera_args_direction'] == 'left' or self.config['camera_args_direction'] == 'right':
            if isinstance(self.config['extra_length'],int) is False:
                # 将20% 处理成 0.2
                # 再将 0.2 * 宽度 赋值给 extra_length 
                self.config['extra_length'] = int(self.analyzer.get_width() * percent2float(self.config['extra_length']))
        if self.config['camera_args_direction'] == 'up' or self.config['camera_args_direction'] == 'down':
            if isinstance(self.config['extra_length'],int) is False:
                # 同上
                self.config['extra_length'] = int(self.analyzer.get_height() * percent2float(self.config['extra_length']))
                
        replace_dict = {
            "${CAMERA_MODEL}": self.analyzer.get_camera_model(),
            # 把图片的时间文本转化为时间戳，再二次转化为任意时间格式
            "${PHOTO_ORIGINAL_DATETIME}": timestamp2str(
                str2timestamp(
                    self.analyzer.get_original_datetime(),
                    time_format=self.config['original_time_format']
                ),
                time_format=self.config['target_time_format']
            ),
            "${CAMERA_ISO}": self.analyzer.get_camera_iso(),
            "${APERTURE}": self.analyzer.get_camera_aperture(),
            "${EXPOSURE_TIME}": self.analyzer.get_camera_exposure_time(),
            "${FOCAL_LENGTH}": str(self.analyzer.get_camera_focal_length()),
            "${CAMERA_LENS_MODEL}": self.analyzer.get_camera_lens_model()
        }
        for label_item in self.config['labels']:
            if isinstance(label_item['font_size'],str):
                label_item['font_size'] = int(self.analyzer.get_height() * percent2float(label_item['font_size']))
            for replace_key in replace_dict:
                label_item['content'] = label_item['content'].replace(replace_key,replace_dict[replace_key])
                    
        
        
    def get_canvas_width(self) -> int:
        if self.config['camera_args_direction'] == 'left' or self.config['camera_args_direction'] == 'right':
            return self.analyzer.get_width() + self.border_size * 2 + self.config['extra_length']
        else:
            return self.analyzer.get_width() + self.border_size * 2

    def get_canvas_height(self) -> int:
        if self.config['camera_args_direction'] == 'up' or self.config['camera_args_direction'] == 'down':
            return self.analyzer.get_height() + self.border_size * 2 + self.config['extra_length']
        else:
            return self.analyzer.get_height() + self.border_size * 2 

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
        
    # 获取用户自定义区域坐标
    def get_custom_box(self) -> tuple:
        '''
        tuple element: left top width height
        '''
        if self.config['camera_args_direction'] == 'left':
            return (0,0,self.config['extra_length'] + self.config['border_size'],self.analyzer.get_height())
        if self.config['camera_args_direction'] == 'right':
            return (self.analyzer.get_width(),0,self.config['extra_length'] + self.config['border_size'],self.analyzer.get_height())
        if self.config['camera_args_direction'] == 'up':
            return (0,0,self.analyzer.get_width(),self.config['extra_length'] + self.config['border_size'])
        if self.config['camera_args_direction'] == 'down':
            return (0,self.analyzer.get_height(),self.analyzer.get_width(),self.config['extra_length'] + self.config['border_size'])
        
    def draw_photos_to_canvas(self,canvas: Image):
        offset_left,offset_top,_,_ = self.get_custom_box()
        offset_left += self.config['border_size']
        offset_top += self.config['border_size']
        for photo_item in self.config['photos']:
            photo_path = photo_item['path']
            photo_image = Image.open(photo_path)
            rate = photo_image.width / photo_image.height
            
            photo_image = photo_image.resize(
                (
                    # 必须要缩放，否则会贴在边缘，不好看
                    int(rate * self.config['extra_length'] * percent2float(photo_item['scale'])),
                    int(self.config['extra_length'] * percent2float(photo_item['scale']))
                ),
                resample=Image.ANTIALIAS
            )
            canvas.paste(
                photo_image,
                (
                    # 如果不偏移的话，照片可能会贴在边缘，所以需要做一个整体便宜，缩放的计算是 offset + (宽 * （ 1 - 缩放比率 ) / 2
                    offset_left + 
                        int(self.analyzer.get_width() * percent2float(photo_item['position_offset'][0])) + 
                        int(rate * self.config['extra_length'] * (1 - percent2float(photo_item['scale'])) / 2),
                    offset_top + 
                        int(self.analyzer.get_height() * percent2float(photo_item['position_offset'][1])) + 
                        int(self.config['extra_length'] * (1 - percent2float(photo_item['scale']))/2)
                )
            )
            photo_image.close()
            
    def draw_labels_to_canvas(self,canvas: Image):
        offset_left,offset_top,_,_ = self.get_custom_box()
        offset_left += self.config['border_size']
        offset_top += self.config['border_size']
        draw = ImageDraw.Draw(canvas)
        for label_item in self.config['labels']:

            font = ImageFont.truetype(font=label_item['font_path'],size=label_item['font_size'])
            draw.text(
                (
                    offset_left + int(self.analyzer.get_width() * percent2float(label_item['position_offset'][0])),
                    offset_top + int(self.analyzer.get_height() * percent2float(label_item['position_offset'][1]))
                ),
                label_item['content'],
                font=font,
                fill=(label_item['font_color'][0], label_item['font_color'][1], label_item['font_color'][2])
            )
        
        
    def generate(self):
        #MODES = ["1", "CMYK", "F", "HSV", "I", "L", "LAB", "P", "RGB", "RGBA", "RGBX", "YCbCr"]
        self.border_size = self.config['border_size']
        self.canvas_width = self.get_canvas_width()
        self.canvas_height = self.get_canvas_height()
        self.canvas_color = self.get_canvas_background()
        
        # 创建画布
        canvas = Image.new("RGB",(self.canvas_width,self.canvas_height),self.canvas_color)
        
        # 打开原始照片
        image = Image.open(self.path)
        
        # 把原始照片粘贴到画布上
        ## 是否需要旋转
        orientation = self.analyzer.get_image_orientation()
        if orientation[0] == 'Rotated' and orientation[2] == 'CCW':
            image = image.rotate(angle=float(orientation[1]),expand=True)
        if orientation[0] == 'Rotated' and orientation[2] == 'CW':
            image = image.rotate(angle=float(360.0 - orientation[1]),expand=True)
        
        canvas.paste(image,self.get_photo_position())
        
        image.close()
        
        # 粘贴图片组
        self.draw_photos_to_canvas(canvas)
        
        # 绘制文字
        self.draw_labels_to_canvas(canvas)
        
        # 保存结果
        self.canvas = canvas
        
        return self
    
    def save(self,path):
        self.canvas.save(path,format="JPEG",quality=self.config['output_quality'])
        
def test():
    pass
def main():
    test()
if __name__ == "__main__":
    main()