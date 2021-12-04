# I have created this view file
from django.http import HttpResponse
from django.shortcuts import render
import pyrebase
from django.contrib import auth

config = {
    'apiKey': "AIzaSyAGeLBOkIuVxZCtdCClTOKdrjnzg7yAG-w",
    'authDomain': "krishworks-7d6d8.firebaseapp.com",
    'databaseURL': "https://krishworks-7d6d8-default-rtdb.firebaseio.com",
    'projectId': "krishworks-7d6d8",
    'storageBucket': "krishworks-7d6d8.appspot.com",
    'messagingSenderId': "828238082663",
    'appId': "1:828238082663:web:c72ab112bc4cc2e39fdac2"
}

firebase = pyrebase.initialize_app(config)
authe = firebase.auth()
database = firebase.database()
storage = firebase.storage()

def index(request):
    return HttpResponse('Hello')

def about(request):
    return HttpResponse('About page')

def home(request):
    day = database.child('Data').child('Day').get().val()
    id = database.child('Data').child('Id').get().val()
    projectname = database.child('Data').child('Projectname').get().val()

    data = {
        'day' : day,
        'id' : id,
        'projectname' : projectname
    }

    return render(request, "Home.html", data)

def signIn(request):
    return render(request, "signIn.html")

def postSignIn(request):
    email = request.POST.get('email')
    password = request.POST.get('password')

    # Log the user in
    try:
        user = authe.sign_in_with_email_and_password(email, password)
    except:
        error = "Invalid email or password."
        return render(request, "signIn.html", { 'message': error})

    uid = user['localId']

    name = database.child('users').child(uid).child('details').child('name').get().val()
    address = database.child('users').child(uid).child('profile').child('address').get().val()
    dob = database.child('users').child(uid).child('profile').child('dob').get().val()
    url = database.child('users').child(uid).child('profile').child('url').get().val()

    return render(request, 'dashboard.html', {'name': name, 'address': address, 'dob': dob, 'url': url})

def signUp(request):
    return render(request, "signUp.html")

def postSignUp(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('password')

    try:
        user = authe.create_user_with_email_and_password(email, password)
    except:
        message = 'Unable to create account'
        return render(request, "signUp.html", {'message': message})

    uid = user['localId']
    idToken = user['idToken']
    data = {'name': name}

    database.child('users').child(uid).child('details').set(data, idToken)

    return render(request, "signIn.html")

def dashboard(request):
    if authe == '':
        return render(request, "dashboard.html")
    else:
        message = "Please login first!"
        return render(request, "signIn.html", {'message': message})

def postDashboard(request):
    address = request.POST.get('address')
    dob = request.POST.get('dob')
    imageUrl = request.POST.get('url')

    try:
        uid = authe.current_user['localId']
        idToken = authe.current_user['idToken']

        data = {
            'address' : address,
            'dob' : dob,
            'url' : imageUrl
        }

        database.child('users').child(uid).child('profile').set(data, idToken)

        name = database.child('users').child(uid).child('details').child('name').get().val()
        address = database.child('users').child(uid).child('profile').child('address').get().val()
        dob = database.child('users').child(uid).child('profile').child('dob').get().val()
        url = database.child('users').child(uid).child('profile').child('url').get().val()
        message = 'Profile updated successfully'

        return render(request, "dashboard.html", { 'name':name, 'address':address, 'dob':dob, 'url':url, 'message': message })
    except KeyError:
        message = "Oops! User already logged out"
        return render(request, 'signIn.html', {'message':message})

def logOut(request):
    try:
        # del request.session['uid']
        del authe.current_user['idToken']
    except KeyError:
        pass

    return  render(request, "signIn.html")

def forgot(request):
    return render(request, "forgotPassword.html")

def postForgot(request):
    email = request.POST.get('email')
    authe.send_password_reset_email(email)

    success = "Email sent successfully, please check email!"

    return render(request, 'signIn.html', { 'success': success})