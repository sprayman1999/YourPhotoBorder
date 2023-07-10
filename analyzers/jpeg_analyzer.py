import piexif
import exifread
class JpegAnalyzer(object):
    def __init__(self,path):
        self.path = path
    def get_exif(self):
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        
        '''
        for i in tags:
            
            if tags[i].encode().find("NIKON"):
                print(f"{i}: {tags[i]}")
        '''
    
    def get_camera_model(self) -> str:
        '''
        获取相机型号
        '''
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str(tags['Image Model'])
    
    def get_camera_iso(self) -> str:
        '''
        获取照片的ISO
        '''
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str(tags['EXIF ISOSpeedRatings'])
    
    def get_camera_aperture(self) -> str:
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        aperture = str(tags['EXIF FNumber'])
        if aperture.isdigit():
            return aperture
        else:
            aperture_array = aperture.split("/")
            return str(int(aperture_array[0]) / int(aperture_array[1]))
    
    def get_camera_exposure_time(self) -> str:
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str(tags['EXIF ExposureTime'])
    
    def get_camera_lens_model(self) -> str:
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str(tags['EXIF LensModel'])
    
    def get_width(self) -> int:
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return int(str(tags['EXIF ExifImageWidth']))
    
    def get_height(self) -> int:
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return int(str(tags['EXIF ExifImageLength']))
    
    def get_original_datetime(self):
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return str(tags['EXIF DateTimeOriginal'])
    
    def get_camera_focal_length(self) -> str:
        with open(self.path, 'rb') as f:
            tags = exifread.process_file(f)
        return int(str(tags['EXIF FocalLength']))
        
        
def test():
    #test_jpeg_path = '../test/DSC00524.JPG'
    test_jpeg_path = "../test/test_photo.jpg"
    analyzer = JpegAnalyzer(test_jpeg_path)
    print(f"Camera Model: {analyzer.get_camera_model()}")
    print(f"Lens Camera Model: {analyzer.get_camera_lens_model()}")
    print(f"ISO: {analyzer.get_camera_iso()}")
    print(f"Exposure Time: {analyzer.get_camera_exposure_time()}")
    print(f"Aperture: {analyzer.get_camera_aperture()}")
    print(f"Width: {analyzer.get_width()}")
    print(f"Height: {analyzer.get_height()}")
    print(f"Time: {analyzer.get_original_datetime()}")
def main():
    test()
if __name__ == '__main__':
    main()
'''
import exifread

# 打开JPEG文件
with open("your_image.jpg", 'rb') as f:
    # 读取EXIF数据
    tags = exifread.process_file(f)

# 获取相机参数
if 'Image Model' in tags:
    camera_model = tags['Image Model']
else:
    camera_model = 'Unknown'

if 'EXIF ExposureTime' in tags:
    exposure_time = tags['EXIF ExposureTime']
else:
    exposure_time = 'Unknown'

if 'EXIF FNumber' in tags:
    aperture = tags['EXIF FNumber']
else:
    aperture = 'Unknown'

if 'EXIF ISOSpeedRatings' in tags:
    iso = tags['EXIF ISOSpeedRatings']
else:
    iso = 'Unknown'

# 打印相机参数
print("Camera Model:", camera_model)
print("Exposure Time:", exposure_time)
print("Aperture:", aperture)
print("ISO:", iso)
'''