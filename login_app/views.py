from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *

# Create your views here.
def index(request):
    return render (request, 'login.html')

def register(request):
    # if request.method =='GET':
    #     return redirect('/')
    errors = User.objects.validations(request.POST)
    if errors:
        for error in errors.values():
            messages.errors(request, error)
        return redirect ('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session[user_id] = new_user.id
        messages.success(request, 'You have successfully registered.')
        return redirect('/success/{{new_user.id}}')

def login(request):
    # if it is a GET request redirect 
    if request.method == 'GET':
        return redirect('/')
    # if the user email and password in login validation is false, this grabs the login validations method
    if not User.objects.login_validation(request.POST['email'], request.POST['password']):
    # send errors, and redirect
        messages.errors(request, 'Invalid Email or Password')
        return redirect('/')
    # else put current user in a variable bu grabbing email
    user = User.objects.get(email = request.POST['email'])
    # set a variable to grab users id, and redirect
    request.session['user_id'] = user.id
    messages.errors(request, 'You have Successfully logged in.')
    return redirect('/success/{{user.id}}')


def success(request, user_id):
    if user_id not in request.session:
        return redirect('/')
    user = User.objects.get(id=user_id)
    context = {
        'user' : user
    }
    return render(request, 'success.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')