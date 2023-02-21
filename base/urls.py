from django.urls import path
from . import views          # imports the views which is in the same folder as this URLS.PY (in this case folder/APP base)
                            # base/views.py is where we defined the business logic of home and room


# We need a list urlpatterns so that we can specify all the url paths the user can go to 

urlpatterns = [
    # (route: str, view: (...) -> _ResponseType, name: str = ...)
    
    path('login/', views.loginPage, name="login"),                          
    path('logout/', views.logoutUser, name="logout"),   
    path('signup/', views.signupUser, name="signup"),                          


    path('', views.home, name="home"),                          # name is so that we can refer to the view by its name later(dynamic)
    # path('room/', views.room, name="room"),                   # tell which fn we are gonna trigger when we open our room page('room/')
    path('room/<str:room_id>/', views.room, name="room"),
    path('profile/<str:user_id>/', views.userProfile, name="user-profile"),

    path('create-room/', views.createRoom, name="create-room"),
    path('update-room/<str:pk>/', views.updateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.deleteRoom, name="delete-room"),

    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),   # we can refer to this by delete-message in html

]                

# room/< x >  < x > is a dynamic url         e.g. 'room/1/' 
# THERE IS A REASON WHY WE ADDED A URL name here (e.g. name="room") so that 
# even if the url changes to 'room_name/<str:room_id>/'  we can still refer to the url as "room" IN THE HTML pages


# EVEN AFTER CONFIGURING THIS , WE HAVE TWO URLS BUT THE DJANGO DOES NOT KNOW ABOUT THESE , 
# go to the main urls file and import a functionn called include 