from datetime import datetime,timedelta

def instructions():
    print('''
          
          
    run (pip install djangorestframework-simplejwt) if you havent

''')

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

access_tkn_life = None
refresh_tkn_life = None



SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME":timedelta(minutes= access_tkn_life or 120),
    "REFRESH_TOKEN_LIFETIME":timedelta(days = refresh_tkn_life or 2)
}

def setTokenLifetime(access_token_life:int,refresh_token_life:int):
    access_tkn_life = access_token_life
    refresh_tkn_life = refresh_token_life
    print ("""
    
    
           Done
           
           
           """)

from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from django.urls import path

def setTokenUrls():
    urls = [
        path("api/gettoken/",TokenObtainPairView.as_view(),name='token_obtain_pair'),
        path("api/tokenrefresh/",TokenRefreshView.as_view(),name='token_refresh')
    ]
    return urls