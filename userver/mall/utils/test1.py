# a='你好'
# a_b=a.encode('utf-8')
# print(a_b)
# print(type(a_b))
# for i in a_b:
#     print(i)
# for i in a_b:
#     print(bin(i))
#

# key = '1234567890!@#$%^'
# print(type(key))


import os
file = '/home/u2/Downloads/gold.jpeg'

#########start 获取文件路径、文件名、后缀名############

def jwkj_get_filePath_fileName_fileExt(filename):

  (filepath,tempfilename) = os.path.split(filename)

  (shotname,extension) = os.path.splitext(tempfilename)

  return filepath,shotname,extension

#########end 获取文件路径、文件名、后缀名############

a = jwkj_get_filePath_fileName_fileExt(file)

print(a)

# ('/home/u2/Downloads', 'gold', '.jpeg')