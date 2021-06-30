# -*- coding: utf-8 -*-
# flake8: noqa

from qiniu import Auth

#需要填写你的 Access Key 和 Secret Key
access_key = 'iRHUkzwWgJSVhYyRfKqiecxA9d0gTIA6QB0Ojn1N'
secret_key = '_sBSIOnhTPErhRNTMQCisMGX8t_OOeKmXF2mk8dv'

#构建鉴权对象
q = Auth(access_key, secret_key)

#要上传的空间
bucket_name = 'ssh-ai-album'

#生成上传 Token，可以指定过期时间等

# 上传策略示例
# https://developer.qiniu.com/kodo/manual/1206/put-policy
# policy = {
#  # 'callbackUrl':'https://requestb.in/1c7q2d31',
#  # 'callbackBody':'filename=$(fname)&filesize=$(fsize)'
#  # 'persistentOps':'imageView2/1/w/200/h/200'
#  }

def upload_token(name, policy):
 # 上传后保存的文件名
 # key = 'test.png'

 #3600为token过期时间，秒为单位。3600等于一小时
 token = q.upload_token(bucket_name, name, 3600, policy)
 print(token)
 return token

def download_token(name, policy=None):
 # 有两种方式构造base_url的形式
 if policy is None:
  policy = {}
 base_url = 'http://%s/%s' % (bucket_name, name)
 # 可以设置token过期时间
 private_url = q.private_download_url(base_url, expires=3600)
 print(private_url)
 return private_url

# def modify_token(name, policy):
#  # 上传后保存的文件名
#  # key = 'test.png'
#  base_url = 'http://%s/%s' % (bucket_name, name)
#  #3600为token过期时间，秒为单位。3600等于一小时
#  token = q.upload_token(bucket_name, name, 3600, policy)
#  print(token)
#  return token

