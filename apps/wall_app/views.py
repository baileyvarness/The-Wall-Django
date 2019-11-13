import bcrypt
from django.contrib import messages
from django.shortcuts import redirect, render

from .models import *

def index(request):
    return render(request, "index.html")

def register(request):
    print('request.POST: ', request.POST)
    errors = User.objects.validator(request.POST)
    print('errors :', errors)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        hashed_password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt())
        new_user = User.objects.create(first_name=request.POST['first_name'],
                                       last_name=request.POST['last_name'],
                                       email=request.POST['email'],
                                       password=hashed_password)
        if new_user:
            request.session['uid'] = new_user.id
        else:
            print('there was a problem creating the user')
            return redirect('/')
    return redirect('/wall')

def login(request):
    user_list = User.objects.filter(email=request.POST['email'])
    if len(user_list) > 0:
        hashed_password = user_list[0].password
        if bcrypt.checkpw(request.POST['password'].encode(), hashed_password.encode()):
            request.session['uid'] = user_list[0].id
            return redirect('/wall')
    messages.error(request, 'invalid email and/or password')
    return redirect('/')

def wall(request):
    if 'uid' not in request.session:
        print('we do not have a user id in session')
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['uid']),
        'all_messages': Message.objects.all()
    }
    return render(request, 'wall.html', context)

def message(request, user_id):
    user = User.objects.get(id=user_id)
    Message.objects.create(message=request.POST['message'], user=user)
    return redirect('/wall')

def comment(request, user_id, message_id):
    user = User.objects.get(id=user_id)
    message = Message.objects.get(id=message_id)
    Comment.objects.create(comment=request.POST['comment'], user=user, message=message)
    return redirect('/wall')

def logout(request):
    request.session.clear()
    messages.error(request, "You have successfully logged out.")
    return redirect('/')