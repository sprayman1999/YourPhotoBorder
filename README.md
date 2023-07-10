# YourPhotoBorder
## 使用教程
### 环境配置
首先需要安装[python3](https://www.python.org/downloads/)
```
$ git clone https://github.com/sprayman1999/YourPhotoBorder
$ cd YourPhotoBorder
$ python3 -m pip install --requirement requirements.txt
```



### 命令如下
```
$ python3 ./main.py -c ./configs/default.json -f ./test/test_photo.jpg -o ./output/output.jpg
```
### 样图如下
![样图](https://github.com/sprayman1999/YourPhotoBorder/blob/main/output/output.jpg)


### 命令参数
```
-c : 指定配置文件
-f : 指定输入图片
-o : 指定输出位置
```

## Config
### 转译
### Default Config
```
{
    "border_size": 0, # 边框粗细
    "background": [255,255,255], # 背景颜色
    "extra_length": "20%", # 将原有照片的长或宽进行拓展，也可以设置成整数
    "camera_args_direction": "down", # 相机参数显示在图片下方
    "original_time_format": "%Y:%m:%d %H:%M:%S", # 照片被拍时的时间格式
    "target_time_format": "%Y-%m-%d %H:%M:%S", # 指定时间格式
    "labels": [ # 可以添加自定义文字
        {
            "label_name": "camera model label", # label名称，无用途，只用于区分
            "font_path": "./fonts/AlibabaPuHuiTi-3-75-SemiBold/AlibabaPuHuiTi-3-75-SemiBold.ttf", # 字体路径
            "font_size": "4.5%", # 字体大小 = 图片高度 * 百分比
            "content": "${CAMERA_MODEL}", # 文字内容
            "position_offset": ["3%","5%"], # 文字的相对坐标，也可以设置成整数
            "font_color": [0,0,0] # 字体颜色
        },
        {
            "label_name": "photo original datetime",
            "font_path": "./fonts/AlibabaPuHuiTi-3-45-Light/AlibabaPuHuiTi-3-45-Light.ttf",
            "font_size": "2.5%",
            "content": "${PHOTO_ORIGINAL_DATETIME}",
            "position_offset": ["3%","10%"],
            "font_color": [0,0,0]
        },
        {
            "label_name": "camera iso",
            "font_path": "./fonts/AlibabaPuHuiTi-3-55-Regular/AlibabaPuHuiTi-3-55-Regular.ttf",
            "font_size": "3.8%",
            "content": "${FOCAL_LENGTH}m f/${APERTURE} ${EXPOSURE_TIME} ISO${CAMERA_ISO}",
            "position_offset": ["68%","3.75%"],
            "font_color": [0,0,0]
        },
        {
            "label_name": "camera lens model",
            "font_path": "./fonts/AlibabaPuHuiTi-3-45-Light/AlibabaPuHuiTi-3-45-Light.ttf",
            "font_size": "3.5%",
            "content": "${CAMERA_LENS_MODEL}",
            "position_offset": ["68%","10%"],
            "font_color": [0,0,0]
        }
    ],
    # 可以添加自定义图片
    "photos": [
        {
            "path": "./assets/camera_logos/NIKON/logo.png", # 图片路径
            "position_offset": ["55%","0%"], # 图片偏移
            "scale": "65%" # 图片缩放
        }
    ]
}
```

## TODO
 - 完善config格式
 - 完善各类相机厂家的logo数据
 - 相机厂家logo可被裁切成各种形状，比如圆形
 - 支持PNG导入；支持PNG、BMP导出
 - 支持GUI拖动组件，并最后导出配置文件
 - 图片渲染可能存在乱序，需要设定level来限制渲染顺序
 - 背景可设置成图片

## BUG
 - sRGB JPEG导出后和原图相比，暗部会偏白