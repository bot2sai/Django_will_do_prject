from time import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm                                                   
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from will_do.models import WillDo
from .forms import WillDoForm
from .models import WillDo
from django.utils import timezone
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'will_do/home.html')

def signupuser(request):
    if request.method == 'GET':
        return render(request,'will_do/signupuser.html', {'form':UserCreationForm()})
    else: 
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('currentwilldo')
            except IntegrityError:
                return render(request,'will_do/signupuser.html', {'form':UserCreationForm(), 'error':'Please choose another user name'})
        else:
            return render(request,'will_do/signupuser.html', {'form':UserCreationForm(), 'error':'Passord didnt match'})

def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

def loginuser(request):
    if request.method == 'GET':
        return render(request,'will_do/loginuser.html', {'form':AuthenticationForm()})
    else: 
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'will_do/loginuser.html', {'form':AuthenticationForm(), 'error':'Username and password wrong'})
        else:
            login(request, user)
            return redirect('currentwilldo')

@login_required
def createwilldo(request):
    if request.method == 'GET':
        return render(request,'will_do/createwilldo.html', {'form':WillDoForm()})        
    else:
        try:
            form = WillDoForm(request.POST)
            newwilldo = form.save(commit=False)
            newwilldo.user = request.user
            newwilldo.save()
            return redirect('currentwilldo')
        except ValueError:
            return render(request,'will_do/createwilldo.html', {'form':WillDoForm(), 'error':'error Bad data'})

@login_required
def currentwilldo(request):
    willdos = WillDo.objects.filter(user = request.user, datecompleted__isnull=True)
    return render(request,'will_do/currentwilldo.html', {'willdos':willdos})

@login_required
def viewwilldo(request, willdo_pk):
    willdo = get_object_or_404(WillDo, pk=willdo_pk, user= request.user)
    if request.method == 'GET':
        form = WillDoForm(instance=willdo)
        return render(request,'will_do/viewwilldo.html', {'willdo':willdo, 'form':form})
    else:
        try:
            form = WillDoForm(request.POST, instance=willdo)
            form.save()
            return redirect('currentwilldo')
        except ValueError:
            return render(request,'will_do/createwilldo.html', {'form':WillDoForm(), 'error':'error Bad info'})

@login_required
def completewilldo(request, willdo_pk):
    willdo = get_object_or_404(WillDo, pk=willdo_pk, user= request.user)
    if request.method == 'POST':
        willdo.datecompleted = timezone.now()
        willdo.save()
        return redirect('currentwilldo')

@login_required
def deletewilldo(request, willdo_pk):
    willdo = get_object_or_404(WillDo, pk=willdo_pk, user= request.user)
    if request.method == 'POST':
        willdo.delete()
        return redirect('currentwilldo')

@login_required
def completed(request):
    willdos = WillDo.objects.filter(user = request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request,'will_do/completed.html', {'willdos':willdos})