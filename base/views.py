from django.shortcuts import render, redirect
from django.contrib import messages                 # import flash messages

from django.http import HttpResponse
from .models import Room, Topic , Message                      # .models because same file path (IMPORTING THE MODEL WE WANT TO QUERY)


from .forms import RoomForm                                    # GO TO FORMS.PY to know about the form we will be using in the "CREATEROOM" view


from django.db.models import Q

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# USING SIMPLE DECORATORS FOR "restricting a user from specfic pages"
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserCreationForm


# Create your views here.

# rooms = [
#     {'id' : 1, 'name' : 'Lets learn python !'},
#     {'id' : 2, 'name' : 'Design with me !'},
#     {'id' : 3, 'name' : 'Front end developer !'},      # we want to render these data out inside of the html file
# ]


# # TO CREATE Views WE ARE GONNA USE FUNCTION BASED VIEWS HERE       (Views = Business logic)

def loginPage(request):
    page = 'login'

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == "POST":
        username = request.POST.get("username").lower()               # THESE TWO VALUES WILL BE SENT FROM THE FRONTEND
        password = request.POST.get("password")

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)               # to check if all the credentials entered by the VALID user matches with the DB OR NOT

        if user is not None:                                 # if user returns a USER object that matches the credentials then
            login(request, user)                             # add in the session to the DB inside of our browser 
            return redirect('home')                          # and the USER IS LOGGGED IN

        else:
            messages.error(request, 'Wrong username or password')

    context = {'page' : page}
    return render(request, 'base/login_signup.html', context)




def logoutUser(request):
    logout(request)                     # invoke the LOGOUT() method and this is gonna delete that token therefore, deleting the session
    
    return redirect('home')             # no need to render any template just redirect back to home page


def signupUser(request):
    page = 'signup'
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)                 # form is all the username, passwords and stuffs (rquest.POST)
        if form.is_valid():
            user = form.save(commit=False)                # saving the form and freezing it in time so as to be able to access the USER OBJECT
            user.username = user.username.lower()           # cleaning the data (username)
            user.save()
            login(request, user)                                # log in the user when he registers
            return redirect('home')
        
        else:                                                   # there can be many exceptions e.g username already exists in the DB and stuffs
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_signup.html', {'form':form, 'page':page} )


def home(request):                              # the request object is gonna be the http object , tells us what kinda request method is sent, what kinda data is being passed in, whats the user sending to the backend
    # return HttpResponse('Home page')
    rooms = Room.objects.all()                                                             # QuerySet = Modelname.objects.all()
    
    # q = request.GET.get('q')                                                                # RECALL " http://127.0.0.1:8000/?q=Python "
    # rooms = Room.objects.filter(topic__name = q)                                                             # filteredQuerySet = Modelname.objects.filter()
    
    q = request.GET.get("q")  if request.GET.get("q") != None else ''                       # PROBLEM - THE home page " http://127.0.0.1:8000"
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains = q) |
        Q(description__icontains=q)
        )                                 # Do a case insensitive search for all records that contains atleast {q} in the topic.name column:

    topics = Topic.objects.all()                                                      # for now, we want to list out everything , LATER WE WOULD WANT TO FILTER THESE DOWN BY TOP ONES/ MAX ROOMS
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))                                 # THIS IS FOR THE RECENT ACTIVITY FEED, CAN BE MODIFIED TO ONLY SEE FOLLOWING'S RECENT ACTIVITIES

    context_dict = {'rooms' : rooms, 'topics' : topics, 
                    'room_count': room_count, 'room_messages':room_messages}

    return render(request, 'base/home.html', context_dict)                           #  render(request: HttpRequest, template_name: str, {'refer_name in html' : variable} )



def room(request, room_id):
    # room_ = None
    # for room in rooms:
    #     if room['id'] == int(room_id):            MANY TO ONE RELATIONSHIP of the attribute message with the class {{"ROOM"}} u.e MANY different messages possible in ONE class
    #         room_ = room

    room_ = Room.objects.get(id = room_id)                                  # Room = object -> (room_) = the room instance whose 'id'(inbuilt attribute) mathces the parameter passed (room_id)
    room_messages = room_.message_set.all().order_by('-created')                # set of messages related to THIS room / message_all = model_all    #######     "_set" method is for MANY TO ONE RELATIONSHIP     ##### ROOM is related to messages as ONE-MANY relationship
    
    participants = room_.participants.all()                               # get all the participants / no set method for many to many relationships

    if request.method == 'POST':                                   # IFyour method is POST i.e u r adding a comment/ message in the room
        message = Message.objects.create(
            user = request.user,
            room = room_,
            body = request.POST.get('body')                         # Whatever "name" you gave to the input field in 'ROOM.HTML'  
        )
        # in the request.POST method , before we redirect this we r gonna add the person who commented to the participants of the room

        room_.participants.add(request.user)                # request.user = the user who sent the request for POST
        return redirect('room', room_id=room_.id)


    context = {'room' : room_, 'room_messages':room_messages, 'participants':participants}
    return render(request, 'base/room.html', context)   # passing the room_ as 'room' in room.html file so we can refer to it by 'room'  



def userProfile(request, user_id):
    user = User.objects.get(id = user_id) 
    rooms = user.room_set.all()                     # GET ALL THE CHILDREN OF A SPECIFIC OBJECT (to get all the rooms the user has created)
    room_messages = user.message_set.all()          # to get all the room_messages the user has created
    topics = Topic.objects.all()                     # rendering all the topics because we need all of them in the user page as

    context = {'user':user, 'rooms':rooms, 'topics':topics, 'room_messages': room_messages}    # Be CONSISTENT with your NAMING because we may need to pass from different view functions but may have them in a common template    
     
    return render(request, 'base/profile.html', context)              



# CAN ONLY CREATE A ROOM IF YOU ARE LOGGED IN
@login_required(login_url='login')          # send back an unauthenticated user to the login page if he/she clicks on createRoom    
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        # print(request.POST)                       # prints out the Queryset which we send in the backend
        topic_name = request.POST.get('topic')        # gets the topic chosen from the FRONT END since "request.POST" (check roomform.html)
        topic, created = Topic.objects.get_or_create(name=topic_name)   # 5:05:00 Let's say 'Python' , since it is already present CREATED = False but TOPICwould be 'python'

        Room.objects.create(
            host = request.user,        # when we submit the FORM we create that topic and then we redirect the user to home
            topic = topic, 
            name = request.POST.get('name'),             
            description = request.POST.get('description'),
        )
        return redirect('home')

        #######################   OLD CODE   ####################### 
        # # form = RoomForm(request.POST)
        # if form.is_valid():                     # if the data you entered is valid in the sense it matches the type and all
        #     # form.save()                          # then save that value in the DB
        #     room = form.save(commit=False)          # MODIFICATION at 4:01:00 => need an instance of the room to know the USER LOGGED IN => the UPDATE ROOM CREATOR/HOST dynamically 
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')             # Because I have the name 'home' in the url I can access it by the name instead of the url
    
    context = {'form': form, 'topics': topics}
    return render(request, 'base/room_form.html', context)





@login_required(login_url='login')          # send back an unauthenticated user to the login page if 
def updateRoom(request, pk):        # gonna look like create room function
    room = Room.objects.get(id=pk)                      # When we click edit a room, we wanna  know what room were gonna edit
    topics = Topic.objects.all()
    form = RoomForm(instance=room)                       # a PRE FILLED FORM we have (the one we want to edit)

    if request.user != room.host:                       # look up the "MODELS.PY", 'HOST' is the foreign key linking ROOM to USER
        return HttpResponse('You are not authorised to edit this room!! ')


    if(request.method == 'POST'):                                   # passing all that data using request.POST but we need to specify WHICH ROOM to update
        topic_name = request.POST.get('topic')        # gets the topic chosen from the FRONT END since "request.POST" (check roomform.html)
        topic, created = Topic.objects.get_or_create(name=topic_name) 
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')            # From the front end FORM
        room.save()

        # form = RoomForm(request.POST, instance=room)                #  these data which will be filled during edit will replace whatever that room value is
        # if form.is_valid():                      
        #     form.save()                          
        
        return redirect('home')  

    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'base/room_form.html', context)



@login_required(login_url='login')          # send back an unauthenticated user to the login page if 
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)

    if request.user != room.host:                       # if the deleter is not the one who is the room HOST
        return HttpResponse('You are not authorised to edit this room!! ')

    if request.method == "POST":
        room.delete()
        return redirect('home') 
       
    return render(request, 'base/delete.html', {'obj': room})




@login_required(login_url='login')          # send back an unauthenticated user to the login page if 
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:                       # if the deleter is not the one who is the room HOST
        return HttpResponse('You are not authorised to edit this message!! ')

    if request.method == "POST":
        message.delete()
        return redirect('home') 
       
    return render(request, 'base/delete.html', {'obj': message})
