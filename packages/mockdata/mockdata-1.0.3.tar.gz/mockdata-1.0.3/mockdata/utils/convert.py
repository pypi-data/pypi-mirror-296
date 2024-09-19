import base64
import io
from PIL import Image


def base64_to_image(image_base, image_path):
    '''
    将base64编码转换为图片
    :param image_base: base64编码
    :param image_path: 图片路径
    :return:
    '''

    bytes = base64.b64decode(image_base)  # 将base64解码为bytes
    image = io.BytesIO(bytes)
    image = Image.open(image)
    image.save(image_path)
