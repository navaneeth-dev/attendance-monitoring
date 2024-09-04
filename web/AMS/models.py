from django.db import models
from cryptography.fernet import Fernet
from django.conf import settings


cipher_suite = Fernet(settings.ENCRYPTION_KEY)

class Student(models.Model):
    registerNo = models.CharField(max_length=10, unique=True)
    studName = models.CharField(max_length=100)
    encrypted_password = models.CharField(max_length=256) 

    def set_password(self, raw_password):
        encrypted_password = cipher_suite.encrypt(raw_password.encode())
        self.encrypted_password = encrypted_password.decode('utf-8')

    def get_password(self):
        decrypted_password = cipher_suite.decrypt(self.encrypted_password.encode()).decode('utf-8')
        return decrypted_password

    def __str__(self):
        return self.studName

class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    date = models.DateField()
    percentage = models.FloatField()

    def __str__(self):
        return f'{self.student.studName} - {self.date} - {self.percentage}%'
