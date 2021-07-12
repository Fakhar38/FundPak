from django.shortcuts import render
import pyrebase
import firebase_admin
from firebase_admin import credentials, firestore
from django.http import HttpResponseRedirect
from django.urls import reverse
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


# firebase-admin setup
cred = credentials.Certificate("./fundpak-531e2-firebase-adminsdk-x9xtf-fa810f22e3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

# Create your views here.


def get_all_products():
    prods = db.collection("products").document("eVa2BlDFUQHAjY9zS7gC").collection("product").get()
    prods_list = []
    if prods:
        prods_list = [x.to_dict() for x in prods]
        prods_list = sorted(prods_list, key=lambda x: x['frt'], reverse=True)
    return prods_list


def index(request):
    try:
        user_id = request.session['uid']
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
    else:
        is_logged = False

    # Getting products
    all_prods = get_all_products()
    if len(all_prods) > 6:
        all_prods = all_prods[:6]

    context = {
        'is_logged': is_logged,
        "all_prods": all_prods
    }
    return render(request, 'index.html', context)


def product_detail(request, prod_id):
    try:
        user_id = request.session['uid']
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
    else:
        is_logged = False

    all_prods = get_all_products()
    this_prod = ''
    for prod in all_prods:
        if prod['id'] == prod_id:
            this_prod = prod
            all_prods.pop(all_prods.index(prod))
    if len(all_prods) > 4:
        extra_prods_to_show = all_prods[:4]
    else:
        extra_prods_to_show = all_prods
    # print(f"This prod: {this_prod}")

    context = {
        'is_logged': is_logged,
        "this_prod": this_prod,
        "extra_prods": extra_prods_to_show
    }
    return render(request, 'product-details.html', context)


def product_categories(request):
    return render(request, 'product-categories.html')


def featured(request):
    return render(request, 'featured.html')


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
            err_email = ''
            err_password = ''
            if "EMAIL_NOT_FOUND" in err_desc:
                err_email = "Email not found."
            elif "INVALID_PASSWORD" in err_desc:
                err_password = "Invalid password."
            if err_email:
                return render(request, 'login.html', {'err_email': err_email})
            elif err_password:
                return render(request, 'login.html', {'err_password': err_password})
            else:
                return render(request, "login.html", {'err_message': "Unknown error occurred. Try again"})
        else:
            session_id = user['localId']
            print(f"Session id: {session_id}")
            request.session['uid'] = session_id
            return HttpResponseRedirect(reverse("core:index"))

    else:
        try:
            request.session['uid']
        except KeyError:
            return render(request, 'login.html')
        else:
            return HttpResponseRedirect(reverse("core:index"))


def signup_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        first_name = request.POST.get("firstname")
        last_name = request.POST.get("lastname")
        print(f"Email: {email}")
        print(f"pas: {password}")
        print(f"First name: {first_name}")
        print(f"last name: {last_name}")

        try:
            user = auth_firebase.create_user_with_email_and_password(email, password)
        except Exception as e:
            print(e)
            err_desc = str(e)
            err_email = ''
            err_password = ''
            if "EMAIL_EXISTS" in err_desc:
                err_email = "Email already exists"
                return render(request, 'signup.html', {'err_email': err_email})
            elif "WEAK_PASSWORD" in err_desc:
                err_pass = "Weak Password"
                return render(request, 'signup.html', {'err_pass': err_pass})
            else:
                err_message = "An Error Occurred. Please try again later."
                return render(request, "signup.html", {'err_message': err_message})
        else:
            user_id = user['localId']
            data = {
                'email': email,
                'userId': user_id,
                "username": f"{first_name} {last_name}",
                "image_url": ''
            }
            try:
                db.collection('users').document(user_id).set(data)
            except Exception as e:
                print(e)

            request.session['uid'] = user_id
            return HttpResponseRedirect(reverse("core:index"))

    else:
        return render(request, 'signup.html')


def logout(request):
    del request.session['uid']
    return HttpResponseRedirect(reverse("core:index"))


def about_us(request):
    return render(request, 'about-us.html')


def start_campaign_not_logged(request):
    return render(request, "start-a-campaign1.html")


def start_campaign_logged(request):
    return render(request, "start-a-campaign2.html")