from django.contrib import admin
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.site_header = 'منصـة الجمعية الخيرية لتحفيظ القرآن الكريم بالخرمة (اقرأ)'
admin.site.site_title = "الحـلقات القرآنية بالـخـرمــة"
admin.site.index_title = "إدارة منصة الجمعية بالـخـرمــة"

class ProfileInline(admin.StackedInline):
    model = Students
    can_delete = False
    verbose_name_plural = 'الطلاب'

# Define a new User admin
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)

# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)












class StudentsAdmin(admin.ModelAdmin):
    model = Students
    list_display = ('ikama_number','__str__','sex','center_id',  'course_id', 'staff_id',)
    list_filter = ['center_id', 'sex', 'course_id', 'staff_id']
    list_per_page = 30
admin.site.register(Students, StudentsAdmin)

admin.site.register(Staffs)
#admin.site.register(Profile)

admin.site.register(Contact)
class CoursesAdmin(admin.ModelAdmin):
    model = Courses
admin.site.register(Courses, CoursesAdmin)
class CentersAdmin(admin.ModelAdmin):
    model = Centers
admin.site.register(Centers, CentersAdmin)
class DegreeAdmin(admin.ModelAdmin):
    model = Degree
    model = Students
    list_display = ('attendance_date','__str__', 'stud_id', 'status', 'status2',)
    list_filter = ['attendance_date',]
    list_per_page = 30
admin.site.register(Degree, DegreeAdmin)