# !/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time : 2024/4/16 15:40
# @Author : DZL
# @File : Student.py
# @Software: PyCharm

class Student(object):
    def __init__(self,name,college,ethnic,age,grade,gender,userId):
        self.name = name
        self.college = college
        self.age = age
        self.ethnic = ethnic
        self.grade = grade
        self.gender = gender
        self.userId = userId

    def __str__(self):
        return f"Name: {self.name}\nCollege: {self.college}\nAge: {self.age}\nEthnicity: {self.ethnic}\nGrade: {self.grade}\nGender: {self.gender}"