from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint
import json
from Model import Model
# import Model
from sqlalchemy import and_, or_
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


# 蓝图名 蓝图路径
loginRoute = Blueprint('loginRoute', __name__)
CORS(loginRoute, resources=r'/*')	# 注册CORS, "/*" 允许访问所有api

def AdminLogin(admin_id, admin_pwd):
    admin = Model.Admin.query.filter(Model.Admin.admin_id == admin_id).first()
    if not admin:
        return "UserNotExist"
    admin = Model.Admin.query.filter(and_(Model.Admin.admin_pwd == admin_pwd,Model.Admin.admin_id == admin_id)).first()
    if not admin:
        return "PasswordWrong"
    else:
        return "Login"

@loginRoute.route('/adminLogin/',methods=['POST']) 
def adminLogin():
    # 接口本身
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    check = AdminLogin(data['userID'],data['password'])
    return check

# @loginRoute.route('/login/',methods=['POST']) 
# def adminLogin():
#     # 接口本身
#     data = request.form
#     name = data.get('username')
#     pwd = data.get('password')
#     adName  = admin = Model.Admin.query.filter(Model.Admin.name == name).first()
#     admin = Model.Admin.query.filter(and_(Model.Admin.admin_pwd == admin_pwd,Model.Admin.name == name)).first()
    



# @loginRoute.route('/studentLogin/',methods=['POST'])  
# def stuLogin():
#     # 接口本身
#     data = request.form
#     check = StudentLogin(data.get('username'),data.get('password'))
#     return check

@loginRoute.route('/login/',methods=['POST'])
def Login():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    uid = data['id']
    pwd = data['password']
    
    teacher = Model.Teacher.query.filter(Model.Teacher.t_id == uid).first()
    if teacher:
        if teacher.check_password(pwd):
            s = Serializer('WEBSITE_SECRET_KEY', 60*100)
            token = s.dumps({'id': uid,'role':2,'isactive':teacher.is_active}).decode('utf-8')
            return jsonify({'status':"TSuccess",'token':token,'is_active':teacher.is_active})
        else:
            return jsonify({'status':"PasswordWrong",'token': None,'is_active':None})
    student = Model.Student.query.filter(Model.Student.s_id == uid).first()
    if student:
        if student.check_password(pwd):
            s = Serializer('WEBSITE_SECRET_KEY', 60*100)
            token = s.dumps({'id': uid,'role':1,'isactive':student.is_active}).decode('utf-8')
            return jsonify({'status':"SSuccess",'token':token,'is_active':student.is_active})
        else:
            return jsonify({'status':"PasswordWrong",'token': None,'is_active':None})
    return jsonify({'status':"UserNotExist",'token': None,'is_active':None})
