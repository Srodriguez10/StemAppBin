from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.utils import timezone
from django.http import HttpResponseForbidden
from django.forms import modelformset_factory
from django.db.models import Sum, Count
from .forms import *

def index(request):
    username_pk = request.user.pk
    if username_pk is None:
        return redirect('login')
    else:
        student_check = StudentProfile.objects.filter(username=request.user)
        parent_check = ParentProfile.objects.filter(username=request.user)
        if len(student_check)>0:
            student = StudentProfile.objects.get(username=request.user)
            detention = Detention.objects.filter(demerit__student=student).values('detention_date', 'parent_approval').annotate(Count('detention_date'))
            demerit_count = Demerit.objects.filter(student=student).aggregate(Sum('demerit_quantity'))
            demerit = Demerit.objects.filter(student=student)
            parent = None
        elif len(parent_check)>0:
            parent = ParentProfile.objects.get(username=request.user)
            detention = Detention.objects.filter(demerit__student=parent.student_username).values('detention_date', 'parent_approval').annotate(Count('detention_date'))
            demerit_count = Demerit.objects.filter(student=parent.student_username).aggregate(Sum('demerit_quantity'))
            demerit = Demerit.objects.filter(student=parent.student_username)
            student = None
    context = {'student':student, 'det': detention, 'dem_total': demerit_count, 'demerit': demerit, 'parent': parent}
    return render(request, 'detention/index.html', context)

def studentregister(request):
    if request.method == "POST":
        form_register = StudentRegistrationForm(request.POST)
        if form_register.is_valid():
            register = form_register.save(commit=False)
            password = register.password
            user_username = register.username
            email = register.email
            user = User.objects.create_user(user_username, email, password)
            register.save()
            user.save()
            user = authenticate(username=user_username, password=password)
            login(request, user)
            return redirect('index')
    else:
        error = None
        form_register = StudentRegistrationForm()
    context = {'form_register':form_register,}
    return render(request, 'registration/student_registration_form.html', context)

def parentregister(request):
    if request.method == "POST":
        form_register = ParentRegistrationForm(request.POST)
        if form_register.is_valid():
            register = form_register.save(commit=False)
            password = register.password
            user_username = register.username
            email = register.email
            user = User.objects.create_user(user_username, email, password)
            register.save()
            user.save()
            user = authenticate(username=user_username, password=password)
            login(request, user)
            return redirect('index')
    else:
        error = None
        form_register = ParentRegistrationForm()
    context = {'form_register':form_register,}
    return render(request, 'registration/parent_registration_form.html', context)

def profile(request):
    username_pk = request.user.pk
    if username_pk is None:
        return redirect('login')
    else:
        try:
            parent = ParentProfile.objects.get(username=request.user)
            if request.method == "POST":
                form_unamepass = ChangeParentProfileForm(request.POST or None, instance= request.user)
                if form_unamepass.is_valid():
                    up = form_unamepass.save(commit=False)
                    newpassword = up.password
                    newusername = up.username
                    newemail = up.email
                    u = User.objects.get(username=request.user)
                    u.set_password(newpassword)
                    u.username = newusername
                    u.email = newemail
                    up.save()
                    u.save()
                    user = authenticate(username=newusername, password=newpassword)
                    login(request, user)
                    return redirect('profile')
            else:
                form_unamepass = ChangeParentProfileForm(instance=request.user)
            context = {'parent': parent, 'form_unamepass':form_unamepass}
        except:
            student = StudentProfile.objects.get(username=request.user)
            if request.method == "POST":
                form_unamepass = ChangeStudentProfileForm(request.POST or None, instance= request.user)
                if form_unamepass.is_valid():
                    up = form_unamepass.save(commit=False)
                    newpassword = up.password
                    newusername = up.username
                    newemail = up.email
                    u = User.objects.get(username=request.user)
                    u.set_password(newpassword)
                    u.username = newusername
                    u.email = newemail
                    up.save()
                    u.save()
                    user = authenticate(username=newusername, password=newpassword)
                    login(request, user)
                    return redirect('profile')
            else:
                form_unamepass = ChangeStudentProfileForm(instance=request.user)
            context = {'student': student, 'form_unamepass':form_unamepass}

    return render(request, 'detention/profile.html', context)

def demerit(request):
    username_pk = request.user.pk
    if username_pk is None:
        return redirect('login')
    else:
        student_check = StudentProfile.objects.filter(username=request.user)
        parent_check = ParentProfile.objects.filter(username=request.user)
        if len(student_check)>0:
            student = StudentProfile.objects.get(username=request.user)
            print(student)
            print(request.user)
            demerit_count = Demerit.objects.filter(student=student).aggregate(Sum('demerit_quantity'))
            demerit = Demerit.objects.filter(student=student)
            print(demerit)
            parent = None
        elif len(parent_check)>0:
            parent = ParentProfile.objects.get(username=request.user)
            demerit_count = Demerit.objects.filter(student=parent.student_username).aggregate(Sum('demerit_quantity'))
            demerit = Demerit.objects.filter(student=parent.student_username)
            student = None
    context = {'dem_total': demerit_count, 'demerit': demerit, 'student':student, 'parent':parent}
    return render(request, 'detention/demerit.html', context)

def detention(request):
    username_pk = request.user.pk
    if username_pk is None:
        return redirect('login')
    else:
        student_check = StudentProfile.objects.filter(username=request.user)
        parent_check = ParentProfile.objects.filter(username=request.user)
        if len(student_check)>0:
            student = StudentProfile.objects.get(username=request.user)
            detention = Detention.objects.filter(demerit__student=student).values('detention_date', 'parent_approval', 'parent_approval_date', 'id', 'start_time').annotate(Count('detention_date'))
            parent = None
        elif len(parent_check)>0:
            parent = ParentProfile.objects.get(username=request.user)
            detention = Detention.objects.filter(demerit__student=parent.student_username).values('detention_date', 'parent_approval', 'parent_approval_date', 'id','start_time').annotate(Count('detention_date'))
            student = None
    context = {'student':student, 'det': detention, 'parent': parent}
    return render(request, 'detention/detention.html', context)

def detention_view(request, id):
    username_pk = request.user.pk
    if username_pk is None:
        return redirect('login')
    else:
        student_check = StudentProfile.objects.filter(username=request.user)
        parent_check = ParentProfile.objects.filter(username=request.user)
        if len(student_check)>0:
            student = StudentProfile.objects.get(username=request.user)
            detention = Detention.objects.get(id=id)
            parent = None
        elif len(parent_check)>0:
            parent = ParentProfile.objects.get(username=request.user)
            detention = Detention.objects.get(id=id)
            student = None
    context = {'student':student, 'det': detention, 'parent': parent}
    return render(request, 'detention/detention_view.html', context)

def detention_approve(request, id):
    username_pk = request.user.pk
    if username_pk is None:
        return redirect('login')
    else:
        parent_check = ParentProfile.objects.filter(username=request.user)
        if len(parent_check)>0:
            instance = Detention.objects.get(pk=id)
            instance.parent_approval = True
            instance.parent_approval_date = timezone.now()
            instance.save()
            return redirect('detentions')
        else:
            return redirect('forbidden')