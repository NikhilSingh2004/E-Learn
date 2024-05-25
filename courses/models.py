from django.db import models

'''
    Need to Create Two Tables

    Contain detail about an course 

    1) Course 
        - ID (Default)
        - Course Name : Ex Python   
        - Course Description : Ex For Beginners
        - Course Start Date : Ex 10 Feb 2024
        - No. of Topics : Integer field
        - Course Image : An Background Image for the Course
        More...
        
    Topics are small unit containg content about a specific topic Ex : Python Input...
    Every Topic will have an Foreign Key Course, which tells that the topic is part of XYZ Course!

    2) Topics
        - Course : Foreign Key (Course)
        - ID (Default)
        - Topic Name : Ex Python Input...
        - Topic Content : Ex In Order to Take input in Python we need to use the input() function...
        - Topic Slug : Ex Python-Input-Function...
        More...
'''


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    # instructor = models.CharField(max_length=100)
    # duration = models.IntegerField()
    
    def __str__(self):
        return self.name

class Topic(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    slug = models.SlugField(unique=True)
    # difficulty_level = models.CharField(max_length=20)
    # resources = models.URLField()
    
    def __str__(self):
        return self.name
