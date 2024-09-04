from django.contrib import admin
from django.core.management import call_command
from django.shortcuts import redirect
from .models import Student, Attendance

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('registerNo', 'studName')
    search_fields = ('registerNo', 'studName')

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'date', 'percentage')
    list_filter = ('date', 'student')
    search_fields = ('student__studName', 'date')
