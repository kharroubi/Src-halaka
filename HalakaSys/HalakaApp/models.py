from django.db import models
from datetime import timedelta, datetime
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
import os
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.
import django
from django.contrib.auth.models import AbstractUser




class Courses(models.Model):
    class Meta:
        verbose_name = "الحلقة"
        verbose_name_plural = ' الحلقات '

    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=255, verbose_name="اسم الحلقة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f' {self.course_name}  '
class Centers(models.Model):
    class Meta:
        verbose_name = "مركز الحلقة"
        verbose_name_plural = ' مراكز الحلقات '

    id = models.AutoField(primary_key=True)
    center_name = models.CharField(max_length=255, verbose_name="اسم المركز")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = models.Manager()

    def __str__(self):
        return f' {self.center_name}  '
class Contact(models.Model):
    name = models.CharField(max_length=150, verbose_name="الاسم ")
    email = models.CharField(max_length=150, verbose_name=" الأيمايل")
    feedback = models.TextField(verbose_name="الموضوع")
    def __str__(self):
        return self.name


class Staffs(models.Model):
    class Meta:
        verbose_name = "أستاذ"
        verbose_name_plural = ' الأساتذة '

    GENDER = [
        ('1', 'طلاب'),
        ('2', ' طالبات'),
    ]

    registration_number = models.AutoField(primary_key=True)
    ikama_number = models.CharField(max_length=200, unique=True, verbose_name=" رقم الهوية / الأقامة")
    surname = models.CharField(max_length=200, verbose_name="اللقب")
    firstname = models.CharField(max_length=200, verbose_name="الاسم ")
    other_name = models.CharField(max_length=200, blank=True, verbose_name="اسم الأب")
    center_id = models.ForeignKey(Centers, on_delete=models.DO_NOTHING, verbose_name="نوع الحلقة ")
    sex = models.CharField(max_length=10, choices=GENDER, default='1', verbose_name="شطر الطلاب / الطالبات")
    author = models.ForeignKey(User, null=True, blank=True, on_delete=models.DO_NOTHING,verbose_name=" المستخدم الخاص بالأستاذ ")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f' {self.firstname} {self.other_name} {self.surname}  '



class Students(models.Model):
    class Meta:
        verbose_name = "الطالب"
        verbose_name_plural = ' الطلاب '

    STATUS = [
        ('active', 'نشط'),
        ('inactive', 'غير نشط')
    ]

    GENDER = [
        ('1', 'طلاب'),
        ('2', ' طالبات'),
    ]
   # teacher = 'teacher'
  #  student = 'student'

  #  user_types = [
   #     (teacher, 'teacher'),
   #     (student, 'student'),

   # ]
    registration_number = models.AutoField(primary_key=True)
    current_status = models.CharField(max_length=10, choices=STATUS, default='active')
    ikama_number = models.CharField(max_length=20, unique=True, verbose_name=" رقم الهوية / الأقامة")
    firstname = models.CharField(max_length=20, verbose_name="الاسم ")
    surname = models.CharField(max_length=20, verbose_name="اللقب")
    other_name = models.CharField(max_length=20, blank=True, verbose_name="اسم الأب")
    sex = models.CharField(max_length=10, choices=GENDER, default='1', verbose_name="شطر الطلاب / الطالبات")
    date_of_birth = models.PositiveIntegerField(null=True, blank=True, verbose_name=" العمر ")
    date_of_admission = models.DateField(default=timezone.now, verbose_name=" تاريخ الإنظمام")
    profile_pic = models.ImageField(null=True, blank=True, upload_to='profile_pic', verbose_name="الصورة")
    mobile_number = models.CharField(max_length=13, blank=True,verbose_name="جوال الطالب")
    parent_mobile_number = models.CharField(max_length=13, blank=True,verbose_name="جوال الأب")
    address = models.CharField(max_length=100,blank=True, verbose_name="العنوان ")
    #others = models.TextField(max_length=10,blank=True, verbose_name=" معلومات اخرى")
    course_id = models.ForeignKey(Courses, null=True, blank=True, on_delete=models.DO_NOTHING,verbose_name="نوع الحلقة ")
    center_id = models.ForeignKey(Centers, null=True, blank=True, on_delete=models.DO_NOTHING, verbose_name=" المركز ")
    staff_id = models.ForeignKey(Staffs, null=True, blank=True, on_delete=models.DO_NOTHING,verbose_name=" شيخ الحلقة ")
    author = models.OneToOneField(User,null=True, blank=True,on_delete=models.CASCADE,verbose_name=" المستخدم الخاص بالطالب ")
    #user_type = models.CharField(max_length=10, choices=user_types, default=student, blank=True, null=True)

    def __str__(self):
        return f' {self.firstname} {self.other_name} {self.surname}  '

class Degree(models.Model):
    class Meta:
        verbose_name = "التقييم"
        verbose_name_plural = ' التقييمات '
        ordering = ['-attendance_date']
    STATUS = [('جيد', 'جيد'), ('جيد جدا', 'جيد جدا'),('ممتاز', 'ممتاز'),('غير حافظ', 'غير حافظ'),('غائب', 'غائب'),]
    STATUS2 = [('جيد', 'جيد'), ('جيد جدا', 'جيد جدا'),('ممتاز', 'ممتاز'),('غير حافظ', 'غير حافظ'),('غائب', 'غائب'),]
    id = models.AutoField(primary_key=True, verbose_name="التاريخ  ")
    stud_id = models.ForeignKey(Students, on_delete=models.DO_NOTHING, verbose_name=" الطالب ")
    status = models.CharField(max_length=10, choices=STATUS, null=True, blank=True, verbose_name="درجة الحفظ ")
    status2 = models.CharField(max_length=10, null=True, blank=True, choices=STATUS2, verbose_name="درجة المراجعة ")
    #attendance_date_id = models.ForeignKey(Attendance,on_delete=models.CASCADE,default=datetime.now(),verbose_name=" التاريخ ")
    attendance_date = models.DateField(auto_now=True,verbose_name="التاريخ ")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f'  {self.stud_id}  '

