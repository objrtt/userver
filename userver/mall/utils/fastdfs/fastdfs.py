#coding:utf8

#1.您的自定义存储系统必须是以下子类 django.core.files.storage.Storage
from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from django.utils.deconstruct import deconstructible
from django.conf import settings

#4.您的存储类必须是可解构的，
# 以便在迁移中的字段上使用时可以对其进行序列化。只
# 要您的字段具有可自行序列化的参数，就 可以使用
# django.utils.deconstruct.deconstructible类装饰器

@deconstructible
class MyStorage(Storage):

    #2.Django必须能够在没有任何参数的情况下实例化您的存储系统。
    # 这意味着任何设置都应该来自django.conf.settings
    #?

    def __init__(self, path=None,ip=None):
        if not path:
            path = settings.FDFS_CLIENT_CONF
            self.path = path

        if not ip:
            ip = settings.FDFS_URL
            self.ip = ip


    #3.您的存储类必须实现_open()和_save() 方法以及
    # 适用于您的存储类的任何其他方法

    #  打开文件 因为我们获取图片的时候 是采用的 http的方式
    #http://192.168.229.133:8888/group1/M00/00/02/wKjlhVvFtGeAL05sAAAyZgOTZN0413.jpg
    # 所以此方法我们不用实现
    def _open(self, name, mode='rb'):
        pass


    # save 保存
    # 实现保存方法， 将图片通过Fdfs 保存 Storage中
    def _save(self, name, content, max_length=None):

        #1.创建client
        # client = Fdfs_client('utils/fastdfs/client.conf')
        # client = Fdfs_client(settings.FDFS_CLIENT_CONF)
        client = Fdfs_client(self.path)

        #2.获取图片

        # save 参数中：
        # name: 表示图片的名字 不是路径
        # content: 内容 二进制内容
        data = content.read()

        #3.上传
        # buffer 上传二进制
        result = client.upload_by_buffer(data)

        """
        result :
            {'Remote file_id': 'group1/M00/00/02/wKjlhVvFtGeAL05sAAAyZgOTZN0413.jpg',
            'Uploaded size': '12.00KB',
            'Status': 'Upload successed.',
            'Storage IP': '192.168.229.133',
            'Local file name': '/home/python/Desktop/images/1.jpg',
            'Group name': 'group1'}

        """
        #4.判断上传的状态，并获取 file_id
        if result.get('Status') == 'Upload successed.':
            file_id = result.get('Remote file_id')
        else:
            raise Exception('上传失败')


        # 5.需要把 file_id 返回就可以
        return file_id


    # 还有2个方法
    # 是否存在 exists
    # 不会出现图片覆盖的情况，直接返回false
    def exists(self, name):
        return False


    def url(self, name):

        # name 默认就是我们在save中返回的 file_id
        #group1/M00/00/02/wKjlhVvFtGeAL05sAAAyZgOTZN0413.jpg
        #我们实际在访问图片的时候  是通过 http://ip:port/ + file_id

        # return 'http://192.168.229.133:8888/' + name



        # from mall import settings

        # return settings.FDFS_URL + name

        return self.ip + name


