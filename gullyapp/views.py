from django.shortcuts import render,redirect
from django.http import request,HttpResponseRedirect
from .models import createTeam
from . models import Carousel
from . models import Category
from . models import Userprofile
from .models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import user_passes_test

def home(request):
    return render(request,'home.html')

def index(request):
    return render(request, 'navigation.html')

def main(request):
    data = Carousel.objects.all()
    context={'data':data}
    return render(request, 'index.html',context)

def adminLogin(request):
    msg = None
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        try:
            if user.is_staff:
                login(request, user)
                msg = "User login successfully"
                return redirect('admindashboard')
            else:
                msg = "Invalid Credentials"
        except:
            msg = "Invalid Credentials"
    dic = {'msg': msg}
    return render(request, 'admin_login.html', dic)

def adminHome(request):
    return render(request, 'admin_base.html')

def is_admin(user):
    return user.is_authenticated and user.is_staff

@user_passes_test(is_admin, login_url='admin_login')
def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def add_category(request):
    if request.method == "POST":
        name=request.POST.get('name')
        Category.objects.create(name=name)
        messages.info(request,"Category Added successfully")
        return redirect ('view-category')
    return render(request,'add_category.html')

def view_category(request):
    category=Category.objects.all()
    context={'category':category}
    return render(request,'view_category.html',context)

def edit_category(request, pid):
    category = Category.objects.get(id = pid)
    if request.method == "POST":
        name = request.POST['name']
        category.name = name
        category.save()
        msg = "Category Updated"
        return redirect('view-category')
    return render(request, 'edit_category.html', locals())
    
    

def delete_category(request,pid):
    category=Category.objects.get(id=pid)
    category.delete()
    return redirect('view-category')



from django.contrib.auth.decorators import login_required
@login_required(login_url='userlogin')
def create_team(request):
    category = Category.objects.all()

    if request.method == "POST":
        name = request.POST['name']
        cat_id = request.POST['category']
        contact = request.POST['contact']
        noofplayers = request.POST['noofplayers']
        image = request.FILES['image']
        location = request.POST['location']

        try:
            
            cat_obj = Category.objects.get(id=cat_id)

           
            team_instance = createTeam(
                name=name,
                contact=contact,
                category=cat_obj,
                noofplayers=noofplayers,
                image=image,
                location=location,
                teamcaptain=request.user  
            )

            team_instance.save()
            
            messages.success(request, "Team Created")
            return redirect('home')  

        except Category.DoesNotExist:
            messages.error(request, f"Category with ID '{cat_id}' does not exist.")

    return render(request, 'createteam.html', locals())

@login_required(login_url='userlogin')
def view_team(request,pid):
    if pid == 0:
        team = createTeam.objects.all()
    else:
        category = Category.objects.get(id=pid)
        team = createTeam.objects.filter(category=category)
    allcategory = Category.objects.all()
    return render(request, "jointeamview.html", locals())
        
    
   



from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Userprofile

def registration(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        password = request.POST['password']
        address = request.POST['address']
        mobile = request.POST['mobile']
        image = request.FILES['image']

        
        if User.objects.filter(username=email).exists():
            messages.error(request, "A user with this email already exists.")
        else:
            
            user = User.objects.create_user(username=email, first_name=fname, last_name=lname, email=email, password=password)
            Userprofile.objects.create(user=user, mobile=mobile, address=address, image=image)
            messages.success(request, "Registration successful")

    return render(request, 'registration.html', locals())



def userlogin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.success(request, "User login successfully")
            return redirect('home')
        else:
            messages.success(request,"Invalid Credentials")
    return render(request, 'userlogin.html', locals())

def profile(request):
    data = Userprofile.objects.get(user=request.user)
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        address = request.POST['address']
        mobile = request.POST['mobile']
        try:
            image = request.FILES['image']
            data.image = image
            data.save()
        except MultiValueDictKeyError:
            pass
        user = User.objects.filter(id=request.user.id).update(first_name=fname, last_name=lname)
        Userprofile .objects.filter(id=data.id).update(mobile=mobile, address=address)
        messages.success(request, "Profile updated")
        return redirect('profile')
    return render(request, 'profile.html', locals())

from django.shortcuts import render

def profile_view(request):
    user_avatar_url = request.user.profile.avatar.url 
    return render(request, 'profile.html', {'user_avatar_url': user_avatar_url})

def logoutuser(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('home')
def adminlogout(request):
    logout(request)
    messages.success(request,"Logout Successfully")
    return redirect('home')

def change_password(request):
    if request.method == 'POST':
        o = request.POST.get('old')
        n = request.POST.get('new')
        c = request.POST.get('confirm')
        user=authenticate(username=request.user.username,password=o)
        if user:
            if n==c:
                user.set_password(n)
                user.save()
                messages.success(request,"password Changed")
                return redirect('home')
            else:
                messages.warning(request, "Password not matching")
                return redirect('change_password')
        else:
            messages.error(request, "Invalid Password")
            return redirect('change_password')
    return render(request, 'change_password.html')


def team_detail(request, pid):
    team = createTeam.objects.get(id=pid)
    latest_product = createTeam.objects.filter().exclude(id=pid).order_by('-id')[:10]
    return render(request, "team_detail.html", locals())

import math
from django.db.models import F
from .models import createTeam

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distance = R * c
    return distance



from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.db.models import F
from .models import createTeam,ShownTeamsHistory,MatchRequest
from .utils import get_current_team, find_nearby_teams
@login_required(login_url='userlogin')
def search_opponents(request):
    current_team = get_current_team(request)

    if current_team:
        max_distance_km = 50  

        if request.method == 'POST':
            # Handle the case when the user clicks on "Challenge Opponent"
            opponent_username = request.POST.get('opponent_username')

            # Retrieve the opponent team
            opponent_team = get_object_or_404(createTeam, teamcaptain__username=opponent_username)

            # Create a match request
            match_request = MatchRequest.objects.create(team=current_team, opponent=opponent_team)

            # Send a notification to the opponent team captain
           # opponent_captain = opponent_team.teamcaptain
            #message = f"Match request received from {current_team.name}"
            #Notification.objects.create(user=opponent_captain, message=message)

            

        
        current_team.shown_teams.clear()

        
        nearby_teams = find_nearby_teams(current_team, max_distance_km)

        
        for team in nearby_teams:
            ShownTeamsHistory.objects.create(team=current_team, shown_team=team)

        return render(request, 'opponents_search_results.html', {'nearby_teams': nearby_teams})

    else:
        
        return render(request, 'no_team.html')



from .models import MatchRequest, Notification

def request_for_match(request, opponent_id):
    current_team = get_current_team(request)
    opponent_team = createTeam.objects.get(id=opponent_id)

    
    match_request = MatchRequest.objects.create(team=current_team, opponent=opponent_team)

    # Send a notification to the opponent team captain
    opponent_captain = opponent_team.teamcaptain
    message = f"Match request received from {current_team.name}"
    Notification.objects.create(user=opponent_captain, message=message)

   
    return redirect('success_page')
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.http import JsonResponse







from django.http import HttpResponse, JsonResponse


def create_notification(request, user_id, message):
    user = get_object_or_404(User, id=user_id)
    Notification.objects.create(user=user, message=message)
    return HttpResponse("Notification created successfully!")
from django.shortcuts import render
from .models import Notification

def notification_panel(request):
    notifications = Notification.objects.filter(user=request.user, is_read=False)
    return render(request, 'notification_panel.html', {'notifications': notifications})

from django.utils.datastructures import MultiValueDictKeyError
from .models import Userprofile, createTeam, Notification

from django.urls import reverse
from django.utils.safestring import mark_safe

# views.py
import uuid


def challenge_opponent(request, team_captain_username):
    try:
        sender_team = get_object_or_404(createTeam, teamcaptain__username=request.user.username)
    except createTeam.DoesNotExist:
        messages.error(request, "Your team does not exist.")
        return redirect('some_redirect_view')  # Replace with the actual redirect view

    recipient_team = get_object_or_404(createTeam, teamcaptain__username=team_captain_username)

    # Ensure that we access the 'name' attribute to retrieve its value
    sender_team_name = sender_team.name  # Replace 'name' with the correct attribute for the team name

    # Generate the URL for the team details page
    team_details_url = reverse('team_detail', args=[sender_team.id])  # Replace 'team_detail' with your actual URL name

    # Create a notification for the team captain of the opponent team
    message = mark_safe(
        f"{sender_team_name} wants to play a match with you."
    )
    Notification.objects.create(
        user=recipient_team.teamcaptain,
        message=message,
    )

    # Redirect or render as needed
    messages.success(request, 'Challenge sent successfully!')
    return redirect('search_opponents')  # Replace with the actual redirect view
'''def challenge_opponent(request, team_captain_username):
    try:
        sender_team = get_object_or_404(createTeam, teamcaptain__username=request.user.username)
    except createTeam.DoesNotExist:
        messages.error(request, "Your team does not exist.")
        return redirect('some_redirect_view')

    recipient_team = get_object_or_404(createTeam, teamcaptain__username=team_captain_username)

    sender_team_name = sender_team.name
    team_details_url = reverse('team_detail', args=[sender_team.id])

    # Generate a unique challenge ID using uuid4
    challenge_id = str(uuid.uuid4())

    message = f"{sender_team_name} wants to play a match with you.  "
    Notification.objects.create(
        user=recipient_team.teamcaptain,
        message=message,
        challenge_id=challenge_id
    )

    messages.success(request, 'Challenge sent successfully!')
    return redirect('search_opponents')'''












#notification functions start-------


def accept_challenge(request, challenge_id):
    challenge = get_object_or_404(createTeam, id=challenge_id)
    # Additional logic for accepting the challenge (e.g., update status)
    messages.success(request, 'Challenge accepted successfully!')
    return redirect('search_opponents')

def send_notification_to_opponent(opponent_username, message):
    
    pass

def reject_challenge(request, challenge_id):
    challenge = get_object_or_404(createTeam, id=challenge_id)
    # Additional logic for rejecting the challenge (e.g., update status)
    messages.info(request, 'Challenge rejected.')
    return redirect('search_opponents')

def update_team_location(request, team_id):
    if request.method == 'POST':
        location_data = request.POST.get('location')  
        print('Received Location:', location_data)
        
        team = createTeam.objects.get(id=team_id)
        team.location = location_data
        team.save()

        return JsonResponse({'status': 'Team location updated successfully'})

    return JsonResponse({'status': 'Invalid request'}, status=400)

import re

    
def fetch_nearby_teams(request):
    if request.method == 'POST':
        
        location_data = request.POST.get('location')

        
        current_lat, current_lon = map(float, re.findall(r'-?\d+\.\d+', location_data))

        
        max_distance_km = 50
        nearby_teams = createTeam.objects.all()  
        nearby_teams = [
            {
                'name': team.name,
                'distance': haversine(current_lat, current_lon, *map(float, re.findall(r'-?\d+\.\d+', team.location))),
            }
            for team in nearby_teams
        ]
        nearby_teams = [team for team in nearby_teams if team['distance'] <= max_distance_km]

        
        nearby_teams = sorted(nearby_teams, key=lambda x: x['distance'])

        return JsonResponse(nearby_teams, safe=False)

    return JsonResponse({'error': 'Invalid request'}, status=400)
from django.db.models import Q
from .models import ChatMessage
def chat_view(request, opponent_username):
    opponent = User.objects.get(username=opponent_username)
    messages = ChatMessage.objects.filter(
        (Q(sender=request.user) & Q(recipient=opponent)) |
        (Q(sender=opponent) & Q(recipient=request.user))
    ).order_by('timestamp')

    return render(request, 'chat_template.html', {'opponent': opponent, 'messages': messages})



















        









        
