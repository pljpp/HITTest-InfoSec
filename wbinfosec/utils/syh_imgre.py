import os
import timeit
import numpy as np
import base64
import logging
from io import BytesIO
from keras.models import load_model
from keras import backend as K
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from keras.utils import image_utils
from wbinfosec.utils import handlefile

if K.image_data_format() == 'channels_first':
    input_shape = (3, 224, 224)
else:
    input_shape = (224, 224, 3)

# # 定义log
logger = logging.getLogger(__name__)

# print("开始加载模型：")
logger.info("开始加载模型")
starttime = timeit.default_timer()
# 模型路径
mdpt = handlefile.getPath('model_base.h5')
model = load_model(mdpt)
endtime = timeit.default_timer()
# print("模型加载完成，用时为：", endtime - starttime)
logger.info("模型加载完成，用时为：%s", endtime - starttime)

def predictWithImagePath(img_path):
    '''
    根据输入图像path，来分析图像，并作出分类。
    :param img_path:图像路径
    :return: 图像的类别
    '''
    # 加载图像
    img = image_utils.load_img(img_path, target_size = input_shape)
    # 图像预处理
    x = image_utils.img_to_array(img) / 255.0  # 与训练一致
    x = np.expand_dims(x, axis = 0)

    # 对图像进行分类
    preds = model.predict(x)  # Predicted: [[1.0000000e+00 1.4072199e-33 1.0080164e-22 3.4663230e-32]]
    # print('Predicted:', preds)  # 输出预测概率
    predicted_class_indices = np.argmax(preds, axis = 1)
    # print('predicted_class_indices:', predicted_class_indices)  # 输出预测类别的int

    labels = {'neutral': 0, 'political': 1, 'porn': 2, 'terrorism': 3}
    labels = dict((v, k) for k, v in labels.items())
    predicted_class = labels[predicted_class_indices[0]]
    # predictions = [labels[k] for k in predicted_class_indices]
    # print("predicted_class :", predicted_class)
    return predicted_class, preds[0][predicted_class_indices[0]]

def predictWithImageBase64(imageBase64String):
    """
    根据输入图像Base64，来分析图像，并作出分类。
    :param ImageBase64:图像Base64编码
    :return: 图像的类别
    """
    try:
        # 加载图像 base64
        imageBase64String = imageBase64String.split(',')
        if (len(imageBase64String) > 1):
            imageBase64String = imageBase64String[1]
        else:
            imageBase64String = imageBase64String[0]

        imageBinaryData = base64.b64decode(imageBase64String)  # 解码base64
        imageData = BytesIO(imageBinaryData)  # 在内存中读取

        img = image_utils.load_img(imageData, target_size = input_shape)  # 读取图片，并压缩至指定大小
        # 图像预处理
        x = image_utils.img_to_array(img) / 255.0  # 与训练一致
        x = np.expand_dims(x, axis = 0)
    except:
        return "98", "失败，解析 imageBase64String 参数的过程失败。", 0, 0
    # 对图像进行分类
    try:
        preds = model.predict(x)  # Predicted: [[1.0000000e+00 1.4072199e-33 1.0080164e-22 3.4663230e-32]]
    except:
        return "98", "失败，模型运行失败。", 0, 0
    # print('Predicted:', preds)  # 输出预测概率
    logger.info('Predicted:%s', preds)
    predicted_class_indices = np.argmax(preds, axis = 1)
    # print('predicted_class_indices:', predicted_class_indices)  # 输出预测类别的int
    logger.info('predicted_class_indices:%s', predicted_class_indices)

    labels = {'neutral': 0, 'political': 1, 'porn': 2, 'terrorism': 3}
    labels = dict((v, k) for k, v in labels.items())
    predicted_class = labels[predicted_class_indices[0]]
    # predictions = [labels[k] for k in predicted_class_indices]
    # print("predicted_class :", predicted_class)
    logger.info('predicted_class:%s', predicted_class)
    return "00", "成功", predicted_class, preds[0][predicted_class_indices[0]]

def imgreco(img_list):
    '''
    对微博话题中爬取的图片进行图片识别
    :param img_list: 图片列表
    :return: 图片的种类
    '''
    # 正常图片
    neutral = []
    # 政治图片
    political = []
    # 恐怖图片
    terrorism = []
    # 色情图片
    porn = []
    for imnm in img_list:
        impt = handlefile.getPath('wbfile/wbtalk_pic/' + imnm)
        # starttime = timeit.default_timer()
        cate, prob = predictWithImagePath(impt)
        match cate:
            case 'neutral':
                neutral.append(imnm)
            case 'political':
                political.append(imnm)
            case 'terrorism':
                terrorism.append(imnm)
            case 'porn':
                porn.append(imnm)
        # endtime = timeit.default_timer()
    return neutral, political, terrorism, porn

if __name__ == '__main__':
    pcpt = handlefile.getPath('wbfile/wbtalk_pic/')
    img_list = os.listdir(pcpt)[0:20]
    # 正常图片
    neutral = []
    # 政治图片
    political = []
    # 恐怖图片
    terrorism = []
    # 色情图片
    porn = []
    print("开始预测：")
    for imnm in img_list:
        impt = handlefile.getPath('wbfile/wbtalk_pic/' + imnm)
        print(impt)
        starttime = timeit.default_timer()
        cate, prob = predictWithImagePath(impt)
        print('a是: ', cate)
        print('b是: ', prob)
        match cate:
            case 'neutral':
                neutral.append(imnm)
            case 'political':
                political.append(imnm)
            case 'terrorism':
                terrorism.append(imnm)
            case 'porn':
                porn.append(imnm)
            case _:
                print('>>>>>>>>>>>error')
                print('>>>>>>>>>>>error')
                print('>>>>>>>>>>>error')
                print('>>>>>>>>>>>error')
                print('>>>>>>>>>>>error')
        endtime = timeit.default_timer()
        print("单次调用模型预测时间为：", endtime - starttime)
        print('----------------------------------')
    print(neutral)
    print(political)
    print(terrorism)
    print(porn)
