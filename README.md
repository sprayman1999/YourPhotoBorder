# YourPhotoBorder
## 使用教程
### 环境配置
首先需要安装[python3](https://www.python.org/downloads/)
```
$ git clone https://github.com/sprayman1999/YourPhotoBorder
$ cd YourPhotoBorder
$ python3 -m pip install --requirement requirements.txt
```
### 运行命令如下
```
$ python3 ./main.py -c ./configs/default.json -f ./test/test_photo.jpg -o ./output/output.jpg
```

## Config
### 转译
### Default Config
```
{
    "border_size": 0,
    "background": [255,255,255],
    "extra_length": "20%",
    "camera_args_direction": "down",
    "original_time_format": "%Y:%m:%d %H:%M:%S",
    "target_time_format": "%Y-%m-%d %H:%M:%S",
    "labels": [
        {
            "label_name": "camera model label",
            "font_path": "./fonts/AlibabaPuHuiTi-3-75-SemiBold/AlibabaPuHuiTi-3-75-SemiBold.ttf",
            "font_size": "4.5%",
            "content": "${CAMERA_MODEL}",
            "position_offset": ["3%","5%"],
            "font_color": [0,0,0]
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
    "photos": [
        {
            "path": "./assets/camera_logos/NIKON/logo.png",
            "position_offset": ["55%","0%"],
            "scale": "65%"
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

## BUG
 - sRGB JPEG导出后和原图相比，暗部会偏白