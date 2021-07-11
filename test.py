# import pyrebase
#
# firebaseConfig = {
#     'apiKey': "AIzaSyBQwup5w7OoBcSrn8_ggVivckCJ2TSN3AQ",
#     'authDomain': "fundpak-531e2.firebaseapp.com",
#     'projectId': "fundpak-531e2",
#     'storageBucket': "fundpak-531e2.appspot.com",
#     'messagingSenderId': "588369785043",
#     'appId': "1:588369785043:web:b0a25f4da16f657302e426",
#     'measurementId': "G-1NZH718QKV",
#     'databaseURL': 'https://fundpak-531e2.firebaseio.com'
# }
#
#
# firebase = pyrebase.initialize_app(firebaseConfig)
#
# authf = firebase.auth()
# authf.sign_in_with_email_and_password()

#
# db = firebase.database()
# db.child("users").child("23P4V4uBbWamCeLw3kUUtcrW47y1").child("email").get()


import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./fundpak-531e2-firebase-adminsdk-x9xtf-fa810f22e3.json")
firebase_admin.initialize_app(cred)

db = firestore.client()
db.collection("users").document(user['localId'])