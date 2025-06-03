from django.db.models import Sum
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.contrib import messages

from .models import Attendance,Notice,StudentExtra,TeacherExtra
from .forms import AttendanceForm,StudentExtraForm,StudentUserForm,TeacherExtraForm,TeacherUserForm,AdminSigupForm,AskDateForm,ContactusForm,NoticeForm
from django import forms
from django.contrib.auth.decorators import login_required,user_passes_test




def index(request):
    classes=['Bsc.Physics','Bsc.Chemistry','Bsc.Botany','Bsc.Zoology','Bsc.Mathmatics','Bsc.Electronics']
    return render(request,'index.html',{'courses':classes})


def admin_signup_view(request):
    form=AdminSigupForm()
    if request.method=='POST':
        form=AdminSigupForm(request.POST)
        if form.is_valid():
            user=form.save()
            user.set_password(user.password)
            user.save()


            my_admin_group = Group.objects.get_or_create(name='ADMIN')
            my_admin_group[0].user_set.add(user)

            return HttpResponseRedirect('admin-login')
    return render(request,'admin-signup.html',{'form':form})

def teacher_signup_view(request):
    form1=TeacherUserForm()
    form2=TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=TeacherUserForm(request.POST)
        form2=TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return HttpResponseRedirect('teacher-login')
    return render(request,'teacher-signup.html',context=mydict)

def student_signup_view(request):
    form1=StudentUserForm()
    form2=StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=StudentUserForm(request.POST)
        form2=StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.user=user
            user2=f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)

        return HttpResponseRedirect('student-login')
    return render(request,'student-signup.html',context=mydict)


def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def admin_view(request):
    if request.user.is_authenticated:
        if is_admin(request.user):
            return redirect('app:admin_dash')
    return HttpResponseRedirect('admin-login')


def teacher_view(request):
    if request.user.is_authenticated:
        if is_teacher(request.user):
            account_approval=TeacherExtra.objects.all().filter(user_id=request.user.id,status=True)
            if account_approval:
                return redirect('app:teacher-dash')



    return HttpResponseRedirect('teacher-login')


def student_view(request):
    if request.user.is_authenticated:
        if is_student(request.user):
            account_approval = StudentExtra.objects.all().filter(user_id=request.user.id, status=True)
            if account_approval:
                return redirect('app:student-dash')
            else:
                # messages.error(request, 'Your request not confirmed')
                return redirect('app:admin-login')

    return HttpResponseRedirect('student-login')


def login_view(request):
    if is_admin(request.user):
        return redirect('app:admin-view')
    elif is_teacher(request.user):
        return redirect('app:teacher-view')

    elif is_student(request.user):
        return redirect('app:student-view')







@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    teachercount=TeacherExtra.objects.all().filter(status=True).count()
    pendingteachercount=TeacherExtra.objects.all().filter(status=False).count()

    studentcount=StudentExtra.objects.all().filter(status=True).count()
    pendingstudentcount=StudentExtra.objects.all().filter(status=False).count()

    teachersalary=TeacherExtra.objects.filter(status=True).aggregate(Sum('salary'))
    pendingteachersalary=TeacherExtra.objects.filter(status=False).aggregate(Sum('salary'))

    studentfee=StudentExtra.objects.filter(status=True).aggregate(Sum('fee',default=0))
    pendingstudentfee=StudentExtra.objects.filter(status=False).aggregate(Sum('fee'))

    notice=Notice.objects.all()

    #aggregate function return dictionary so fetch data from dictionay
    mydict={
        'teachercount':teachercount,
        'pendingteachercount':pendingteachercount,

        'studentcount':studentcount,
        'pendingstudentcount':pendingstudentcount,

        'teachersalary':teachersalary['salary__sum'],
        'pendingteachersalary':pendingteachersalary['salary__sum'],

        'studentfee':studentfee['fee__sum'],
        'pendingstudentfee':pendingstudentfee['fee__sum'],

        'notice':notice

    }

    return render(request,'admin-dashboard.html',context=mydict)

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_teacher_view(request):
    return render(request,'admin-teacher.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_teacher_view(request):
    form1=TeacherUserForm()
    form2=TeacherExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=TeacherUserForm(request.POST)
        form2=TeacherExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)

        return redirect('app:admin-teacher')
    return render(request,'admin-add-teacher.html',context=mydict)



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_teacher_view(request):
    teachers=TeacherExtra.objects.all().filter(status=True)
    return render(request,'admin-view-teacher.html',{'teachers':teachers})


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_approve_teacher_view(request):
    teachers=TeacherExtra.objects.all().filter(status=False)
    return render(request,'admin-approve-teacher.html',{'teachers':teachers})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def approve_teacher_view(request,pk):
    teacher=TeacherExtra.objects.get(id=pk)
    teacher.status=True
    teacher.save()
    return redirect('app:admin-teacher-view')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_teacher_view(request,pk):
    teacher=TeacherExtra.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('app:admin-teacher-approve')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_update_teacher_view(request,pk):
    teacher=TeacherExtra.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)

    form1=TeacherUserForm(instance=user)
    form2=TeacherExtraForm(instance=teacher)
    mydict={'form1':form1,'form2':form2}

    if request.method=='POST':
        form1=TeacherUserForm(request.POST,instance=user)
        form2=TeacherExtraForm(request.POST,instance=teacher)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('app:admin-teacher-view')
    return render(request,'admin-update-teacher.html',context=mydict)



@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def delete_teacher_from_school_view(request,pk):
    teacher=TeacherExtra.objects.get(id=pk)
    user=User.objects.get(id=teacher.user_id)
    user.delete()
    teacher.delete()
    return redirect('admin-teacher-view')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_teacher_salary_view(request):
    teachers=TeacherExtra.objects.all().filter(status=True)
    return render(request,'admin-view-teacher-salary.html',{'teachers':teachers})




@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_student_view(request):
    return render(request,'admin-student.html')

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_student_view(request):
    students=StudentExtra.objects.all().filter(status=True)
    return render(request,'admin-student-view.html',{'students':students})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_add_student_view(request):
    form1=StudentUserForm()
    form2=StudentExtraForm()
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=StudentUserForm(request.POST)
        form2=StudentExtraForm(request.POST)
        if form1.is_valid() and form2.is_valid():
            print("form is valid")
            user=form1.save()
            user.set_password(user.password)
            user.save()

            f2=form2.save(commit=False)
            f2.user=user
            f2.status=True
            f2.save()

            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        else:
            print("form is invalid")
        return HttpResponseRedirect('admin-student')
    return render(request,'admin-student-add.html',context=mydict)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_approve_student_view(request):
    students=StudentExtra.objects.all().filter(status=False)
    return render(request,'admin-student-approve.html',{'students':students})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def approve_student(request,pk):
    students=StudentExtra.objects.get(id=pk)
    students.status=True
    students.save()
    return redirect(reverse('app:admin-student-approve'))

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def cancel_student_view(request,pk):
    student=StudentExtra.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('app:admin-student-approve')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def update_student_view(request,pk):
    student=StudentExtra.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    form1=StudentUserForm(instance=user)
    form2=StudentExtraForm(instance=student)
    mydict={'form1':form1,'form2':form2}
    if request.method=='POST':
        form1=StudentUserForm(request.POST,instance=user)
        form2=StudentExtraForm(request.POST,instance=student)
        print(form1)
        if form1.is_valid() and form2.is_valid():
            user=form1.save()
            user.set_password(user.password)
            user.save()
            f2=form2.save(commit=False)
            f2.status=True
            f2.save()
            return redirect('app:admin-student-view')
    return render(request,'admin-student-update.html',context=mydict)


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def delete_student_from_school_view(request,pk):
    student=StudentExtra.objects.get(id=pk)
    user=User.objects.get(id=student.user_id)
    user.delete()
    student.delete()
    return redirect('app:admin-student-view')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_student_fee_view(request):
    students=StudentExtra.objects.all().filter(status=True)
    return render(request,'admin-student-fee.html',{'students':students})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_notice_view(request):
    form=NoticeForm()
    if request.method=='POST':
        form=NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('app:admin_dash')
    return render(request,'admin-notice.html',{'form':form})

@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_attendance_view(request):
    return render(request,'admin-attendance.html')


@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_take_attendance_view(request,cl):
    students=StudentExtra.objects.all().filter(cl=cl,status=True)
    print(students)
    aform=AttendanceForm()
    if request.method=='POST':
        form=AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('app:admin-attendance')
        else:
            print('form invalid')
    return render(request,'admin-take-attendance.html',{'students':students,'aform':aform})



@login_required(login_url='admin-login')
@user_passes_test(is_admin)
def admin_view_attendance_view(request,cl):
    form=AskDateForm()
    if request.method=='POST':
        form=AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendance_data=Attendance.objects.all().filter(date=date,cl=cl)
            student_data=StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendance_data,student_data)
            return render(request,'admin-attendance-view.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'admin-attendance-ask-date.html',{'cl':cl,'form':form})




























@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_dashboard_view(request):
    teacherdata=TeacherExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=Notice.objects.all()
    mydict={
        'salary':teacherdata[0].salary,
        'mobile':teacherdata[0].mobile,
        'date':teacherdata[0].joindate,
        'notice':notice
    }
    return render(request,'teacher-dashboard.html',context=mydict)

@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_view_student_view(request):
    students=StudentExtra.objects.all().filter(status=True)
    return render(request,'teacher-student-view.html',{'students':students})


@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_student_fee_view(request):
    students=StudentExtra.objects.all()
    return render(request,'teacher-student-fee.html',{'students':students})





@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_attendance_view(request):
    return render(request,'teacher-attendance.html')


@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_take_attendance_view(request,cl):
    students=StudentExtra.objects.all().filter(cl=cl,status=True)
    aform=AttendanceForm()
    if request.method=='POST':
        form=AttendanceForm(request.POST)
        if form.is_valid():
            Attendances=request.POST.getlist('present_status')
            date=form.cleaned_data['date']
            for i in range(len(Attendances)):
                AttendanceModel=Attendance()
                AttendanceModel.cl=cl
                AttendanceModel.date=date
                AttendanceModel.present_status=Attendances[i]
                AttendanceModel.roll=students[i].roll
                AttendanceModel.save()
            return redirect('app:teacher-attendance')
        else:
            print('form invalid')
    return render(request,'teacher-take-attendance.html',{'students':students,'aform':aform})



@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_view_attendance_view(request,cl):
    form=AskDateForm()
    if request.method=='POST':
        form=AskDateForm(request.POST)
        if form.is_valid():
            date=form.cleaned_data['date']
            attendancedata=Attendance.objects.all().filter(date=date,cl=cl)
            studentdata=StudentExtra.objects.all().filter(cl=cl)
            mylist=zip(attendancedata,studentdata)
            return render(request,'teacher-attendance-view.html',{'cl':cl,'mylist':mylist,'date':date})
        else:
            print('form invalid')
    return render(request,'teacher-attendance-ask-date.html',{'cl':cl,'form':form})



@login_required(login_url='teacher-login')
@user_passes_test(is_teacher)
def teacher_notice_view(request):
    form=NoticeForm()
    if request.method=='POST':
        form=NoticeForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            form.by=request.user.first_name
            form.save()
            return redirect('app:teacher-dash')
        else:
            print('form invalid')
    return render(request,'teacher-notice.html',{'form':form})









@login_required(login_url='student-login')
@user_passes_test(is_student)
def student_dashboard_view(request):
    studentdata=StudentExtra.objects.all().filter(status=True,user_id=request.user.id)
    notice=Notice.objects.all()
    mydict={
        'roll':studentdata[0].roll,
        'mobile':studentdata[0].mobile,
        'fee':studentdata[0].fee,
        'notice':notice,
        'class':studentdata[0].cl
    }
    return render(request,'student-dashboard.html',context=mydict)

@login_required(login_url='student-login')
@user_passes_test(is_student)
def student_attendance_view(request):
    studentdata=StudentExtra.objects.all().filter(user_id=request.user.id,status=True)
    attendancedata=Attendance.objects.all().filter(cl=studentdata[0].cl,roll=studentdata[0].roll)
    mylist=zip(attendancedata,studentdata)
    return render(request,'student-attendance-view.html',{'mylist':mylist})
