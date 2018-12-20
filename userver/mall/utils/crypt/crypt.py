from Crypto.Cipher import AES
from Crypto import Random
import binascii



global key, iv

key = '1234567890!@#$%^'  # 秘钥，必须是16、24或32字节长度
#iv = Random.new().read(16)  # 随机向量，必须是16字节长度
iv = bytes('1234567890!@#$%^', 'utf-8')

def encrypt(file):

    cipher1 = AES.new(key, AES.MODE_CFB, iv)  # 密文生成器,MODE_CFB为加密模式


    encrypt_msg = cipher1.encrypt(str(file))

    return encrypt_msg

def decrypt(file):

    cipher2 = AES.new(key, AES.MODE_CFB, iv)  # 解密时必须重新创建新的密文生成器

    decrypt_msg = cipher2.decrypt(file)

    de = str(decrypt_msg).split("'")[1].split("'")[0]

    return de


if __name__ == '__main__':

    a='eeqw56454wqewqe121@@#'
    a = encrypt(a)
    # a = str(a).split("'")[1].split("'")[0]
    print(a)

    print(type(a))

    b = decrypt(a)
    # b = str(b).split("'")[1].split("'")[0]
    print(b)
    print(type(b))