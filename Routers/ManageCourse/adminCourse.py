from flask import Flask, request, jsonify
from flask_cors import CORS  # 解决跨域的问题
from flask import Blueprint,current_app,make_response
import json
from Model.Model import CourseType
from Model.Model import Course
from Model.Model import Teacher

from sqlalchemy import and_, or_
import time
import dbManage
import os

adminCourseRoute = Blueprint('adminCourseRoute', __name__)
CORS(adminCourseRoute, resources=r'/*')	

@adminCourseRoute.route('/course/addType/',methods=['POST'])  
def addCourseType():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    name = data['name']
    prefix = data['prefix']
    ctype = CourseType.query.filter(CourseType.prefix == prefix).first()
    if ctype:
        return "prefixExist"
    ctype = CourseType.query.filter(CourseType.ct_name == name).first()
    if ctype:
        return "nameExist"
    ctype = CourseType(prefix=prefix, ct_name=name)
    dbManage.db.session.add(ctype)
    dbManage.db.session.commit()
    return "success"

@adminCourseRoute.route('/course/getType/',methods=['GET'])  
def getCourseType():
    typeS = dbManage.db.session.query(CourseType).all()
    content = []
    for type in typeS:
        temp = {'name':type.ct_name,'prefix':type.prefix}
        content.append(temp)
    return jsonify(content)

@adminCourseRoute.route('/course/addDuty/',methods=['POST'])  
def addDuty():
    data = request.get_data()
    data = json.loads(data.decode("utf-8"))
    semester = data['semester']
    year = data['year']
    prefix = data['prefix']
    t_id = data['t_id']
    c_id = prefix + year + semester
    course = Course.query.filter(Course.c_id == c_id).first()
    if course:
        return "CourseExist"
    course = Course(c_id=c_id,prefix=prefix,course_semester=semester,course_year=year,duty_teacher=t_id)
    dbManage.db.session.add(course)
    dbManage.db.session.commit()
    return "success"

@adminCourseRoute.route('/course/getDuty/',methods=['GET'])  
def getDuty():
    courses = dbManage.db.session.query(Course).all()
    content = []
    for course in courses:
        teacher = Teacher.query.filter(Teacher.t_id == course.duty_teacher).first()
        coursetype = CourseType.query.filter(CourseType.prefix == course.prefix).first()
        temp = {'name':coursetype.ct_name,'prefix':course.prefix,'semester':course.course_semester,"year":course.course_year,"t_id":course.duty_teacher,"t_name":teacher.name,"c_id":course.c_id}
        content.append(temp)
    return jsonify(content)