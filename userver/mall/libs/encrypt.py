import base64
import pickle

def set_encrypt(image):

    # pickle把json转为bytes
    image1 = pickle.dumps(image)

    # 用base64对bytes数据加密
    image2 = base64.b64encode(image1)

    return image2
