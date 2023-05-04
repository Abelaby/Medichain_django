from django.shortcuts import render, redirect
from .forms import SignUpForm, LoginForm
from django.contrib.auth import authenticate, login


def SendRequest(request):
    return render(request, 'parties/sendrequest.html')

def ApproveRequest(request):
    return render(request, 'parties/approverequest.html')


def register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('/parties/login/')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'core/signup.html', {'form': form, 'msg': msg})


def login_view(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.Data_Subject:
                login(request, user)
                return redirect('/chain/request-list')
            elif user is not None and user.Requesting_party:
                login(request, user)
                return redirect('/chain/request-form')
            else:
                msg= 'invalid credentials'
        else:
            msg = 'error validating form'
    return render(request, 'core/login.html', {'form': form, 'msg': msg})



def dataSubject(request):
    return render(request,'parties/DsDashboard.html')


def requestingParty(request):
    return render(request,'parties/Rqpdashboard.html')

