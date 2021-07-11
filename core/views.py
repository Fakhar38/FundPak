from django.shortcuts import render
import pyrebase
from django.contrib import auth as django_auth

# Firebase configuration
firebaseConfig = {
    'apiKey': "AIzaSyBQwup5w7OoBcSrn8_ggVivckCJ2TSN3AQ",
    'authDomain': "fundpak-531e2.firebaseapp.com",
    'projectId': "fundpak-531e2",
    'storageBucket': "fundpak-531e2.appspot.com",
    'messagingSenderId': "588369785043",
    'appId': "1:588369785043:web:b0a25f4da16f657302e426",
    'measurementId': "G-1NZH718QKV",
    'databaseURL': 'https://fundpak-531e2.firebaseio.com'
}
firebase = pyrebase.initialize_app(firebaseConfig)
auth_firebase = firebase.auth()

# Create your views here.


def index(request):
    return render(request, 'index.html')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(f"Email: {email}")
        print(f"Password: {password}")

        try:
            user = auth_firebase.sign_in_with_email_and_password(email, password)
        except Exception as e:
            print(e)
            err_desc = str(e)
            err_message = ''
            if "EMAIL_NOT_FOUND" in err_desc:
                err_message = "Email not found."
            elif "INVALID_PASSWORD" in err_desc:
                err_message = "Invalid password."

            return render(request, 'login.html', {'err_message': err_message})
        else:
            session_id = user['localId']
            request.session['uid'] = session_id
            return render(request, 'index.html')

    else:
        return render(request, 'login.html')


def signup_view(request):
    return render(request, 'signup.html')