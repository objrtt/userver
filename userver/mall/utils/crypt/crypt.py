from Crypto.Cipher import AES
from Crypto import Random
import binascii


class Crypt(object):

    global key, iv

    key = '1234567890!@#$%^'  # 秘钥，必须是16、24或32字节长度
    #iv = Random.new().read(16)  # 随机向量，必须是16字节长度
    iv = bytes('1234567890!@#$%^','utf-8')

    def encrypt(self, file):

        if type(file) != "<class 'bytes'>":

            cipher1 = AES.new(key, AES.MODE_CFB, iv)  # 密文生成器,MODE_CFB为加密模式
            encrypt_msg = iv + cipher1.encrypt(str(file))  # 附加上iv值是为了在解密时找到在加密时用到的随机iv

            en = binascii.b2a_hex(encrypt_msg)    # 将二进制密文转换为16制显示

            return en

    def decrypt(self, file):

        cipher2 = AES.new(key, AES.MODE_CFB, iv)  # 解密时必须重新创建新的密文生成器

        encrypt_msg = iv + cipher2.encrypt(file)  # 附加上iv值是为了在解密时找到在加密时用到的随机iv
        # bytes(file, encoding='utf8'))

        decrypt_msg = cipher2.decrypt(encrypt_msg[16:])  # 后十六位是真正的密文

        de = decrypt_msg

        return de


if __name__ == '__main__':

    s = Crypt()
    a = s.encrypt(55)
    a = str(a).split("'")[1].split("'")[0]
    print(a)
    print(s.decrypt(a))
    print(type(a))