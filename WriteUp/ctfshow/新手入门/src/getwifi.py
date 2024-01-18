# !/usr/bin/env python
# -*-coding:utf-8 -*-

"""
# File       : app.py
# Time       ：2022/11/07 09:16
# Author     ：g4_simon
# version    ：python 3.9.7
# Description：抽老婆，哇偶~
"""

from flask import *
import os
import random
#初始化全局变量
app = Flask(__name__)
app.config['SECRET_KEY'] = 'tanji_is_A_boy_Yooooooooooooooooooooo!'

@app.route('/', methods=['GET'])
def index():  
    return render_template('index.html')


@app.route('/getwifi', methods=['GET'])
def getwifi():
    session['isadmin']=True
    session['current_wifi']='app.py'
    return 'flag'



@app.route('/download', methods=['GET'])
def source(): 
    filename=request.args.get('file')
    if 'flag' in filename:
        return jsonify({"msg":"你想干什么？"})
    else:
        return send_file('static/img/'+filename,as_attachment=True)


@app.route('/secret_path_U_never_know',methods=['GET'])
def getflag():
    if session['isadmin']:
        return jsonify({"msg":flag})
    else:
        return jsonify({"msg":"你怎么知道这个路径的？不过还好我有身份验证"})



if __name__ == '__main__':
    app.run(host='127.0.0.1',port=80,debug=True)
