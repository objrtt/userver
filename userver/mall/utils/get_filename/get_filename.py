
import os

#########start 获取文件路径、文件名、后缀名############

def Path_Name_fileExt(filename):

  (filepath,tempfilename) = os.path.split(filename)

  (shotname,extension) = os.path.splitext(tempfilename)

  return filepath,shotname,extension

#########end 获取文件路径、文件名、后缀名############


# ('/home/u2/Downloads', 'gold', '.jpeg')