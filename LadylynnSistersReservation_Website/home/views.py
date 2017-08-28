from django.shortcuts import render,redirect
from home.forms import UserForm,UserProfileInfoForm,ReservationForm
from home.models import User,UserProfileInfo

from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect,HttpResponse
from django.views.decorators.http import require_http_methods
from home.forms import Reservation, CateringPackages
# Create your views here.

def index(request):
    user_form = UserForm()
    profile_form = UserProfileInfoForm()

    return render(request,"home/body.html",
                          context={'user_form':user_form,
                                   'profile_form':profile_form})

@require_http_methods(["POST"])
def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the body.html file page.
    return render(request,'home/body.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

@require_http_methods(["POST"])
def user_login(request):
    
    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)

        if user:
            if user.is_active:
                login(request,user)
                u = User.objects.get(username=username)
                request.session['user_id'] = u.id
                return HttpResponseRedirect(reverse('home:user_home',args=[u.id]))
            else:
                return HttpResponse("ACCOUNT NOT ACTIVE")
        else:
            print("Someone tried to login and failed")
            print("Username: {} and password {}".format(username,password))
            return HttpResponse("Invalid Login details supplied")
    
    else:
        return HttpResponseRedirect(reverse('index'))

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))

@login_required
def user_home(request,pk):
    userinfo = User.objects.get(id=pk)
    userprofileinfo = UserProfileInfo.objects.get(user_id=pk)
    return render(request,"home/user_home.html",{'user':userinfo,'userprofilepic':userprofileinfo})

@login_required
def loadmake_reservation(request,pk):
    userinfo = User.objects.get(id=pk)
    userprofileinfo = UserProfileInfo.objects.get(user_id=pk)
    reservationform = ReservationForm(initial={'reserver':userinfo.username})
    reservationform.is_bound
    return render(request,"home/make_reservation.html",{'user':userinfo,'userprofilepic':userprofileinfo,'reservationform':reservationform})

@login_required
def reserve(request, pk):
    userinfo = User.objects.get(id=pk)
    userprofileinfo = UserProfileInfo.objects.get(user_id=pk)

    if request.method == "POST":
        # this method is temporary, to be updated
        
        reservationform = ReservationForm(request.POST)
        # check whether it's valid:
        if reservationform.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            reserver = reservationform.cleaned_data['reserver']
            package = reservationform.cleaned_data['package']
            eventtype = reservationform.cleaned_data['eventtype']
            eventdate = reservationform.cleaned_data['eventdate']

            reservation = Reservation.objects.get_or_create(reserver=reserver,package=package,
                                                     eventtype=eventtype,eventdate=eventdate)
            reservation.save()
            return HttpResponseRedirect(reverse('home:user_home',args=[userinfo.id]))

    # if a GET (or any other method) we'll create a blank form
    else:
        reservationform = ReservationForm()

    return render(request, 'home/make_reservation.html', {'user':userinfo,'userprofilepic':userprofileinfo,'reservationform': reservationform})

@login_required
def special(request):
    return HttpResponse("You are logged in, Nice!")

def rtest(request):
    return render(request,"home/index.html",context=None)

