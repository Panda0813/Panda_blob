import uuid

import os

from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
import json

#restful用的包
# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from mainapp.serializer import UserSerializer

#普通的后台用的包
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
# from django.contrib.auth.hashers import make_password  #密码加密
from io import BytesIO

from Panda_v2 import settings
from mainapp.models import User, Blob, Replay
from PIL import Image,ImageDraw,ImageFont
import random

# django-restful的装饰器用法

# @api_view(['GET','POST','PUT','DELETE'])
# def User_list(request):
#     if request.method == "GET":
#         users = User.objects.all()
#         serializer = UserSerializer(users,many=True)
#         return Response(serializer.data)
#
#     elif request.method == "POST":
#         print(request.data)
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():  #序列化数据之前，先要用is_valid验证
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# 查看所有用户与添加用户
# class UserListView(APIView):
#     def get(self,request,format=None):
#         users = User.objects.all()
#         users_serializer = UserSerializer(users,many=True)  #查询多个用户加入many
#         return Response(users_serializer.data)
#
#     def post(self,request,format=None):
#         #将请求数据进行序列化
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():  #验证数据有效性，对比model定义
#             serializer.save()  #保存数据
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         # 验证失败，返回错误信息
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# 查看指定用户，修改用户，删除用户
# class UserView(APIView):
#     # 查询用户
#     def get(self,request,id):
#         user = User.objects.get(id=id)
#         user_serializer = UserSerializer(user)
#         return Response(user_serializer.data)
#
#     def put(self,request,id):
#         user = User.objects.get(id=id)
#         serializer = UserSerializer(user,request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

#用户注册

def home(request):
    user = User.objects.filter(name=request.session.get('uname'))
    if user:
        return render(request,'home.html',{
            'user':user.first(),
            'users':User.objects.all()
        })
    else:
        return render(request,'home.html',{
            'users': User.objects.all()
        })

class RegisterView(View):
    def get(self,request):
        return render(request,'regist.html',{'opt':1})
    def post(self,request):
        user = User()
        user.name = request.POST.get('username')
        user.phone = request.POST.get('phone')
        user.passwd = request.POST.get('passwd')
        user.image = request.POST.get('head_path')
        user.save()
        return redirect('/user/login')

#上传图片
def upload(req):
    upFile = req.FILES.get('photo')
    saveName = str(uuid.uuid4())+'.jpg'
    wholePath = os.path.join(settings.MEDIA_ROOT+'/head',saveName)
    print(wholePath)
    with open(wholePath,'wb') as f:
        for part in upFile.chunks():
            f.write(part)
            f.flush()
    return JsonResponse({'path':saveName})

#判断用户名是否存在
def uName(request,name):
    user = User.objects.filter(name=name)
    if user:
        return JsonResponse({'status':'fail','msg':'此用户名已被注册'})
    return JsonResponse({'status':'ok'})

#验证码
def verifycode(request,code):
    sessioncode = request.session.get('vcode')
    if sessioncode.lower() == code.lower():
        return JsonResponse({'status':'ok'})
    return JsonResponse({'status':'fail','msg':'验证码错误'})

#验证码
def vCode(request):
    #创建画布
    img = Image.new(mode='RGB',size=(120,30),color=(100,220,180))
    draw = ImageDraw.Draw(img,mode='RGB')
    chars = ''
    while len(chars) < 4:
        flag = random.randrange(3)
        num = chr(random.randint(48,57) if flag == 0 else random.randint(65,90) if flag == 1 else random.randint(97,122))
        if len(chars) == 0 or chars.find(num) == -1:
            chars += num

    request.session['vcode'] = chars  #存入session,用于js验证
    font = ImageFont.truetype(font='static/fonts/hktt.ttf',size=24)
    for char in chars:
        xy = (15+chars.find(char)*20,random.randrange(2,8))
        draw.text(xy=xy,text=char,fill=(75,75,255),font=font)
    for i in range(35):
        # 随机生成坐标和颜色，然后画上干扰点
        xy = (random.randrange(120), random.randrange(30))
        color = (random.randrange(255), random.randrange(255), random.randrange(255))
        draw.point(xy=xy, fill=color)
    buffer = BytesIO()
    img.save(buffer,'png')
    del draw
    del img

    return HttpResponse(buffer.getvalue(),content_type='image/png')

# 用户登录
class LoginView(View):
    def get(self,request):
        return render(request,'regist.html')

    def post(self,request):
        name = request.POST.get('name')
        passwd = request.POST.get('passwd')
        qs = User.objects.filter(name=name,passwd=passwd)
        if qs:
            user = qs.first()
            request.session['uname'] = user.name
            return redirect('/user')
        else:
            return render(request,'regist.html',{
                'dl_msg':'用户名或密码有误，请重新输入',
                'name':name
            })

#退出登录
def logout(request):
    del request.session['uname']
    return redirect('/user')

#编写博客
def addBlob(request):
    uname = request.session.get('uname')
    if uname:
        return render(request,'blob_edit.html')
    else:
        return redirect('/user/login')


#查看博客
class BlobView(View):
    #查看博客
    def get(self,request):
        uname = request.session.get('uname')
        user = User.objects.filter(name=uname).first()

        if request.GET.get('a') == '1':  #我的文章
            return render(request,'blob_list.html',{
                'blobs':user.blob_set.all(),
                'user':user,
                'bianji':1
            })

        # #修改文章
        elif request.GET.get('id'):
            return render(request,'blob_edit.html',{
                'blob':Blob.objects.filter(id=request.GET.get('id')).first()
            })


        #查看某个博主的文章
        elif request.GET.get('user_id'):
            return render(request,'blob_list.html',{
                'blobs':User.objects.get(id=request.GET.get('user_id')).blob_set.all(),
                'user':user,
                'zuozhe': 2
            })

        #所有博客
        else:
            return render(request,'blob_list.html',{
                'blobs':Blob.objects.all(),
                'user':user
            })

    #创建和修改博客
    def post(self,request):
        uname = request.session.get('uname')
        user = User.objects.filter(name=uname).first()

        id = request.POST.get('blob_id')
        title = request.POST.get('title')
        btype = request.POST.get('btype')
        summary = request.POST.get('summary')
        content = request.POST.get('content')

        #没有id,说明是创建文章
        if not id:
            Blob.objects.create(user_id=user.id,title=title,btype=btype,summary=summary,content=content)
        else:
            #更新文章
            blob = Blob.objects.filter(id=id)
            blob.update(title=title,btype=btype,summary=summary,content=content)
        return JsonResponse({'status':'ok','msg':'发布成功!'})


    def delete(self,request):
        id = request.GET.get('delete_id')
        if id:
            Blob.objects.filter(id=id).delete()
            return JsonResponse({'status':'ok','msg':'删除成功!'})
        else:
            return JsonResponse({'status':'fail'})

#通过装饰器的方法增加浏览量
def clickblob(fn):
    def wrapper(*args,**kwargs):
        b_id = args[0].path.split('/')[-1]
        Blob.objects.filter(id=b_id).update(cnt=F('cnt')+1)
        return fn(*args,**kwargs)
    return wrapper

#显示博客详细信息
@clickblob
def show(request,blob_id):
    #登录的用户
    login_user = User.objects.filter(name=request.session.get('uname')).first()
    blob = Blob.objects.get(id=blob_id)
    return render(request,'show.html',{
        'user':login_user,
        'blob':blob,
    })


#用户评论
def replay(request):
    #查看是否登录，未登录不能评论
    qs = User.objects.filter(name=request.session.get('uname'))
    if not qs:
        return JsonResponse({'status':'fail','msg':'对不起，登录后方可评论!'})

    loginUser = qs.first()

    blob_id = request.POST.get('blob_id')
    content = request.POST.get('content')
    #保存评论
    Replay.objects.create(user_id=loginUser.id,blob_id=blob_id,content=content)

    return JsonResponse({'status':'ok','msg':'评论成功!'})


#所有用户评论
def allreply(request,blob_id,num=1):
    num = int(num)
    blob = Blob.objects.filter(id=blob_id).last()
    #按回复时间降序排列
    replays = blob.replay_set.all().order_by('-reply_time')

    #创建分页器
    paginator = Paginator(replays,3)
    #整个页码范围range(1,x)
    r = paginator.page_range
    page = paginator.page(num)  #当前要看的页面

    #自定义用户点击时的页码变动范围
    #总共显示5个页码
    if r[-1] < 6:  #判断页码是否不足5个
        r = r
    else:
        if num >= r[-1] - 4:
            if num == r[-1]-4:
                r = range(num-1,num+4)  #往前走
            else:
                r = range(r[-1]-4,r[-1]+1)  #往后走
        else:
            if num == 1:
                r = range(1,6)
            else:
                r = range(num-1,num+4)

    return render(request,'replay.html',{
        'page':page,
        'range':r,
        'blob_id':blob.id
    })
