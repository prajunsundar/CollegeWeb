
from django.db import models
from django.contrib.auth.models import User





Department=[('Bsc.Physics','Bsc.Physics'),('Bsc.Chemistry','Bsc.Chemistry'),('Bsc.Botany','Bsc.Botany'),
('Bsc.Zoology','Bsc.Zoology'),('Bsc.Mathmatics','Bsc.Mathmatics'),('Bsc.Electronics','Bsc.Electronics')]
class TeacherExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    salary = models.PositiveIntegerField(null=False)
    joindate=models.DateField(auto_now_add=True)
    mobile = models.CharField(max_length=40)
    department=models.CharField(max_length=30,choices=Department)
    status=models.BooleanField(default=False)
    def __str__(self):
        return self.user.first_name
    @property
    def get_id(self):
        return self.user.id
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name




classes=[('Bsc.Physics','Bsc.Physics'),('Bsc.Chemistry','Bsc.Chemistry'),('Bsc.Botany','Bsc.Botany'),
('Bsc.Zoology','Bsc.Zoology'),('Bsc.Mathmatics','Bsc.Mathmatics'),('Bsc.Electronics','Bsc.Electronics')]
class StudentExtra(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    roll = models.CharField(max_length=10)
    mobile = models.CharField(max_length=40,null=True)
    fee=models.PositiveIntegerField(null=True)
    cl= models.CharField(max_length=30,choices=classes,)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name



class Attendance(models.Model):
    roll=models.CharField(max_length=10,null=True)
    date=models.DateField()
    cl=models.CharField(max_length=30)
    present_status = models.CharField(max_length=10)



class Notice(models.Model):
    date=models.DateField(auto_now=True)
    by=models.CharField(max_length=20,null=True,default='college')
    message=models.CharField(max_length=500)

