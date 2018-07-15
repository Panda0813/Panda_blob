from django.db.models import F
from django.utils.deprecation import MiddlewareMixin
from mainapp.models import Blob

#中间件的方法增加浏览量
class ClickBlob(MiddlewareMixin):
    def process_request(self,req):
        path = req.path
        if path.find('/user/show') == 0:  #表示这个url是请求url的第一个位置
            #判断成功，就给浏览量加1
            blob_id = path.split('/')[-1]
            Blob.objects.filter(id=blob_id).update(cnt=F('cnt')+1)