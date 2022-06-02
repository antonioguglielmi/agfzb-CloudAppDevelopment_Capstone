from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from .models import CarModel
from .restapis import get_dealers_from_cf, get_dealers_by_state, get_dealer_reviews_from_cf, post_request, get_dealer_by_id
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == "GET":
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            return redirect('djangoapp:index')
    else:
        return redirect('djangoapp:index')

# Create a `logout_request` view to handle sign out request
def logout_request(request):

    # Logout user in the request
    logout(request)

    return redirect('djangoapp:index')


# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}

    if request.method == 'GET':

        return render(request, 'djangoapp/registration.html', context)
    
    elif request.method == 'POST':
        
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']

        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            pass

        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # <HINT> Login the user and 
            # redirect to course list page
            return redirect("djangoapp:index")
        else:
            return render(request, 'djangoapp/registration.html', context)



# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    context = {}
    if request.method == "GET":
        url = "https://d4b89807.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers_from_cf(url)
        context['dealership_list'] = dealerships
        return render(request, 'djangoapp/index.html', context)


def get_dealerships_state(request, urlst):
    context = {}
    if request.method == "GET":
        url = "https://d4b89807.us-south.apigw.appdomain.cloud/api/dealership/"
        dealerships = get_dealers_by_state(url, urlst.upper())
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        return HttpResponse(dealer_names)
        #return render(request, 'djangoapp/index.html', context)


# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    if request.method == "GET":
        # get dealer information
        dealer_url = "https://d4b89807.us-south.apigw.appdomain.cloud/api/dealership/"
        dealer = get_dealer_by_id(dealer_url, dealer_id)
        context['dealer'] = dealer
        # get dealer reviews
        reviews_url = "https://d4b89807.us-south.apigw.appdomain.cloud/api/review/"
        reviews = get_dealer_reviews_from_cf(reviews_url, dealer_id)
        context['reviews_list'] = reviews 
        
        return render(request, 'djangoapp/dealer_details.html', context)


# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):

    if request.user.is_authenticated:

        if request.method == 'GET':

            context= {}

            cars = CarModel.objects.filter(dealer_id=dealer_id)
            context['cars'] = cars

            # get dealer information
            dealer_url = "https://d4b89807.us-south.apigw.appdomain.cloud/api/dealership/"
            dealer = get_dealer_by_id(dealer_url, dealer_id)
            context['dealer'] = dealer
            
            return render(request, 'djangoapp/add_review.html', context)

        elif request.method == 'POST':


            # deal with the purchasecheck field
            purchase = request.POST.get('purchasecheck')
            if purchase is None:
                purchase = False
            else:
                if purchase == 'on':
                    purchase = True
                else:
                    purchase = False

            review = {
                'time':         datetime.utcnow().isoformat(),
                'dealership':   dealer_id,
                'review':       request.POST['content'],
                'name':         ' '.join([request.user.first_name, request.user.last_name]),
                'purchase':     purchase
            }

            if review['purchase']:
                car = CarModel.objects.get(id=int(request.POST['car']))
                review.update({
                    'car_make':         car.car_make.name,
                    'car_model':        car.name,
                    'car_year':         car.year.year,
                    'purchase_date':    request.POST['purchasedate']
                })

            json_payload = {
                'review':   review,            
            }

            response = post_request('https://d4b89807.us-south.apigw.appdomain.cloud/api/review/', 
                                    json_payload, dealerId=dealer_id)

    return redirect("djangoapp:dealer_details", dealer_id=dealer_id)


