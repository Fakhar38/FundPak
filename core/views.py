from django.shortcuts import render
import pyrebase
import stripe
import json
import firebase_admin
from django.views.decorators.csrf import csrf_exempt
from firebase_admin import credentials, firestore
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.conf import settings
import datetime
import uuid
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

# Stripe
api_secret_key = "sk_test_51JCJpuLcv3FoFFSqZaOpoUDYQ3bEyD8h5aoGqsYIe3VPM9ed6K8znA9K8vupk1cVUNK54wkXmSAeT5iOhPQCNrlM00CJql5rpg"
webhook_secret_key = "whsec_fBLJSgX735C9MVVVUTlaYcsKpiRVVxIY"
stripe.api_key = api_secret_key

# Create your views here.


def get_all_products():
    prods = db.collection("products").document("eVa2BlDFUQHAjY9zS7gC").collection("product").get()
    prods_list = []
    if prods:
        prods = [x.to_dict() for x in prods]
        for prod in prods:
            if prod['isActive'] == "True":
                prods_list.append(prod)
        prods_list = sorted(prods_list, key=lambda x: x['frt'], reverse=True)
    return prods_list


def get_prods_by_cat(cat):
    all_prods = get_all_products()
    this_prods = []
    for each in all_prods:
        if cat.upper() in each['category'].upper():
            this_prods.append(each)
    return this_prods


def get_prods_by_word(word):
    all_prods = get_all_products()
    this_prods = []
    for each in all_prods:
        if word.upper() in each['title'].upper():
            this_prods.append(each)
    return this_prods


def get_my_campaigns(prods_list, user_id):
    my_campaigns = []
    for prod in prods_list:
        if prod['userId'] == user_id:
            my_campaigns.append(prod)
    return my_campaigns


def get_my_contributions(user_id):
    my_contribs = []
    all_contribs = db.collection("orders").get()
    all_contribs = [x.to_dict() for x in all_contribs]
    for contrib in all_contribs:
        if contrib['userId'] == user_id:
            my_contribs.append(contrib)

    all_prods = get_all_products()
    my_contribs_with_details = []
    for my_contrib in my_contribs:
        prod_id = my_contrib['productId']
        for prod in all_prods:
            if prod['id'] == prod_id:
                prod['orderId'] = my_contrib['orderId']
                prod['time'] = my_contrib['time']
                my_contribs_with_details.append(prod)
                break

    return my_contribs_with_details


def index(request):
    try:
        user_id = request.session['uid']
        print(f"User id: {user_id}")
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
        user = db.collection("users").document(user_id).get().to_dict()
        user_image = user['image_url']
    else:
        is_logged = False
        user_image = None

    # Getting products
    all_prods = get_all_products()
    if len(all_prods) > 6:
        all_prods = all_prods[:6]

    context = {
        'is_logged': is_logged,
        "all_prods": all_prods,
        'user_image': user_image

    }
    return render(request, 'index.html', context)


def product_detail(request, prod_id):
    try:
        user_id = request.session['uid']
        print(f"User id: {user_id}")
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
        user = db.collection("users").document(user_id).get().to_dict()
        user_image = user['image_url']
    else:
        is_logged = False
        user_image = None

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

    print(f"This prod in detail func: {this_prod}")
    context = {
        'is_logged': is_logged,
        "this_prod": this_prod,
        'user_image': user_image,
        "extra_prods": extra_prods_to_show
    }
    return render(request, 'product-details.html', context)


def product_categories(request):
    try:
        user_id = request.session['uid']
        print(f"User id: {user_id}")
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
        user = db.collection("users").document(user_id).get().to_dict()
        user_image = user['image_url']
    else:
        is_logged = False
        user_image = None

    all_prods = get_all_products()
    context = {
        'all_prods': all_prods,
        'is_logged': is_logged,
        "user_image": user_image,
    }

    return render(request, 'product-categories.html', context)


def prod_cat_search(request, category):
    try:
        user_id = request.session['uid']
        print(f"User id: {user_id}")
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
        user = db.collection("users").document(user_id).get().to_dict()
        user_image = user['image_url']
    else:
        is_logged = False
        user_image = None

    cats = category.split("&")
    all_prods_summed = []
    for cat in cats:
        all_prods = get_prods_by_cat(cat)
        for prod in all_prods:
            all_prods_summed.append(prod)

    context = {
        'all_prods': all_prods_summed,
        'is_logged': is_logged,
        "user_image": user_image,
    }

    return render(request, 'product-categories.html', context)


def prod_phrase_search(request):
    try:
        user_id = request.session['uid']
        print(f"User id: {user_id}")
    except KeyError:
        user_id = None
    if user_id:
        is_logged = True
        user = db.collection("users").document(user_id).get().to_dict()
        user_image = user['image_url']
    else:
        is_logged = False
        user_image = None

    phrase = request.POST.get("phrase")
    words = phrase.split(" ")
    all_prods_summed = []
    once_added = []
    for word in words:
        all_prods = get_prods_by_word(word)
        for prod in all_prods:
            if prod['title'] not in once_added:
                once_added.append(prod['title'])
                all_prods_summed.append(prod)


    context = {
        'all_prods': all_prods_summed,
        'is_logged': is_logged,
        "user_image": user_image,
    }

    return render(request, 'product-categories.html', context)


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
                "image_url": 'https://firebasestorage.googleapis.com/v0/b/fundpak-531e2.appspot.com/o/user_image%2F23P4V4uBbWamCeLw3kUUtcrW47y1.jpg?alt=media&token=0adf4076-8906-414a-a74a-d0f80dc7b6be',
            }
            try:
                db.collection('users').document(user_id).set(data)
            except Exception as e:
                print(e)

            request.session['uid'] = user_id
            return HttpResponseRedirect(reverse("core:index"))

    else:
        return render(request, 'signup.html')


def create_checkout_session(request):
    try:
        request.session['uid']
    except KeyError:
        return HttpResponseRedirect(reverse("core:login"))
    else:
        if request.method == "POST":
            this_prod_id = request.POST.get("prod_id")
            all_prods = get_all_products()
            price_usd = 0
            this_prod_title = ''
            this_prod_img = ''
            raised_amount_to_be = ''
            total_backers_to_be = ''
            for prod in all_prods:
                if prod['id'] == this_prod_id:
                    price = prod['price']
                    price_usd = int(price / 156)
                    print(f"USD price: {price_usd}")
                    price_usd = str(price_usd)+"00"

                    this_prod_title = prod['title']
                    this_prod_img = prod['image']

                    last_raised_amount = int(prod['moneyRaised'])
                    raised_amount_to_be = int(price) + last_raised_amount

                    last_total_backers = int(prod['totalBackers'])
                    total_backers_to_be = last_total_backers + 1
                    break

            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                line_items=[
                    {
                        'price_data': {
                            'currency': 'usd',
                            'unit_amount': price_usd,
                            'product_data': {
                                'name': this_prod_title,
                                'images': [this_prod_img, ],
                            },
                        },
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=request.build_absolute_uri(reverse("core:payment_success")),
                cancel_url=request.build_absolute_uri(reverse("core:payment_cancel")),
            )
            print(f"redirect url: {checkout_session.url}")
            payment_intent_id = checkout_session.payment_intent
            print(f"Payment id: {payment_intent_id}")
            data = {
                    'user_id': request.session['uid'],
                    "prod_id": this_prod_id,
                    "amount": price,
                    "amountTobe": raised_amount_to_be,
                    'totalBackersTobe': total_backers_to_be,
                }
            db.collection("pending_payments").document(payment_intent_id).set(data)

            return HttpResponseRedirect(checkout_session.url, status=303)


def logout(request):
    del request.session['uid']
    return HttpResponseRedirect(reverse("core:index"))


def payment_success(request):
    return render(request, 'payment-success.html')


def payment_cancel(request):
    return render(request, 'payment-cancel.html')


@csrf_exempt
def hook_listener(request):
    payload = request.body
    payload = json.loads(payload)

    try:
        payment_id = payload['data']['object']['id']
    except KeyError:
        print(f"ID not found")
    else:
        payment_details = db.collection("pending_payments").document(payment_id).get().to_dict()
        user_id = payment_details['user_id']
        prod_id = payment_details['prod_id']
        amount_to_be = payment_details['amountTobe']
        total_backers_to_be = payment_details['totalBackersTobe']
        data = {
            'orderId': payment_id,
            "productId": prod_id,
            "userId": user_id,
            'time': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
        }

        # Adding order
        db.collection('orders').document(payment_id).set(data)
        db.collection("products").document("eVa2BlDFUQHAjY9zS7gC").collection("product").document(prod_id).update(
            {'moneyRaised': amount_to_be,
             'totalBackers': total_backers_to_be,
             }
        )
        print(f"Orders and Products updated after webhook")

        # deleting pending payment
        batch = db.batch()
        payment_ref = db.collection("pending_payments").document(payment_id).get()
        batch.delete(payment_ref.reference)
        batch.commit()

        return HttpResponse(status=200)

    # print(f"Payload: {payload}")
    # received_sig = request.META["HTTP_STRIPE_SIGNATURE"]
    # event = None
    #
    # try:
    #     event = stripe.Webhook.construct_event(
    #         payload, received_sig, webhook_secret_key
    #     )
    # except ValueError:
    #     print("Error while decoding event!")
    #     return HttpResponse(status=400)
    # except stripe.error.SignatureVerificationError:
    #     print("Invalid signature!")
    #     return HttpResponse(status=400)
    #
    # print(
    #     "Received event: id={id}, type={type}".format(
    #         id=event.id, type=event.type
    #     )
    # )
    # return HttpResponse(status=200)


def campaign_1(request, prod_id):
    try:
        request.session['uid']
    except KeyError:
        return HttpResponseRedirect(reverse("core:login"))
    else:
        if request.method == "POST":
            title = request.POST.get("title")
            tagline = request.POST.get("tagline")
            image = request.POST.get("img_url")
            location = request.POST.get("location")
            category = request.POST.get("category")
            price = int(request.POST.get("price"))
            description = request.POST.get("description")
            frt = 0
            total_backers = 0
            money_raised = 0

            data = {
                "category": category,
                "description": description,
                "frt": frt,
                "image": image,
                "location": location,
                "moneyRaised": money_raised,
                "price": price,
                "tagline": tagline,
                'title': title,
                "totalBackers": total_backers,
            }

            db.collection("products").document("eVa2BlDFUQHAjY9zS7gC").collection("product").document(prod_id).update(data)

            return HttpResponseRedirect(reverse('core:campaign_2', kwargs={'prod_id': prod_id}))

        else:
            return render(request, 'campaign-form-1.html', {'prod_id': prod_id})


def campaign_2(request, prod_id):
    try:
        request.session['uid']
    except KeyError:
        return HttpResponseRedirect(reverse("core:login"))
    else:
        if request.method == "POST":
            goal_amount = request.POST.get("goalAmount")
            iban = request.POST.get("iban")

            data = {
                'goalAmount': goal_amount,
                "IBAN": iban,
                'isActive': "True",
            }

            db.collection("products").document("eVa2BlDFUQHAjY9zS7gC").collection("product").document(prod_id).update(data)
            return HttpResponseRedirect(reverse("core:product_detail", kwargs={'prod_id': prod_id}))

        else:
            return render(request, 'campaign-form-2.html', {'prod_id': prod_id})


def about_us(request):
    return render(request, 'about-us.html')


def start_campaign_not_logged(request):
    try:
        request.session['uid']
    except KeyError:
        return render(request, "start-a-campaign1.html")
    else:
        return HttpResponseRedirect(reverse("core:start_camp_logged"))


def start_campaign_logged(request):
    try:
        request.session['uid']
    except KeyError:
        return HttpResponseRedirect(reverse("core:login"))
    else:
        if request.method == "POST":
            print(f"In Post")
            account_type = request.POST.get("question1")
            location = request.POST.get("location")

            prod_id = str(uuid.uuid4())
            print(f"Prod id: {prod_id}")
            user_id = request.session['uid']
            print(f"User id: {user_id}")

            data = {
                'account_type': account_type,
                "location": location,
                "id": prod_id,
                "userId": user_id,
                'frt': 0,
                'isActive': "False"
            }

            db.collection("products").document("eVa2BlDFUQHAjY9zS7gC").collection("product").document(prod_id).set(data)
            return HttpResponseRedirect(reverse("core:campaign_1", kwargs={'prod_id': prod_id}))
        else:
            return render(request, "start-a-campaign2.html")


def profile(request):
    try:
        user_id = request.session['uid']
    except KeyError:
        return HttpResponseRedirect(reverse("core:login"))
    else:
        user = db.collection('users').document(user_id).get().to_dict()

        all_prods = get_all_products()
        my_campaigns = get_my_campaigns(all_prods, user_id)
        my_contributions = get_my_contributions(user_id)
        profile_update_url = request.build_absolute_uri(reverse('core:update_profile_pic'))

        context = {
            'user': user,
            'campaigns': my_campaigns,
            "contributions": my_contributions,
            "campaign_count": len(my_campaigns),
            "contrib_count": len(my_contributions),
            'update_url': profile_update_url,
        }
        return render(request, 'profile.html', context)


@csrf_exempt
def update_profile_pic(request):
    print(f"update post: {request.POST}")
    img_url = request.POST.get("img_url")
    user_id = request.session['uid']

    db.collection("users").document(user_id).update({'image_url': img_url})
    return HttpResponse(200)
