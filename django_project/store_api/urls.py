from django.urls import path
from . import views

urlpatterns = [
    path('register',views.Register, name='register'),
    path('login',views.Login, name='login'),
    path('logout',views.Logout, name='logout'),
    path('medicine',views.Medicine_List, name='medicinelist'),
    path('medicines/<int:id>',views.Medicine_Detail, name='medicineDetail'),
    


    
]
