from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import ( HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT )
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .serializers import MedicineSerializer
from medicalstore.models import Medicine


# http://127.0.0.1:8000/storeapi/register
@csrf_exempt
@api_view(['POST'])
@permission_classes((AllowAny,))
def Register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    password1 = request.data.get('password1')

    if password != password1:
        return Response({'error': 'Confirmation Password is Wrong'}, status=HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username= username, email=email, password=password)
    user.save() 

    return Response({'Success': 'User Creation Successfully'}, status=HTTP_201_CREATED)


# http://127.0.0.1:8000/storeapi/login
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},status=HTTP_400_BAD_REQUEST)
   
    user = authenticate (username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},status=HTTP_404_NOT_FOUND)
    
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token':token.key},status=HTTP_200_OK)


# http://127.0.0.1:8000/storeapi/logout
@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def Logout(request):
    if request.user.is_authenticated:
        Token.objects.filter(user=request.user).delete()
    return Response('You have successfully logged out.',status=HTTP_200_OK)


# http://127.0.0.1:8000/storeapi/medicine
@csrf_exempt
@api_view(['GET', 'POST'])
def Medicine_List(request):
    if request.method == "GET":
        medicines = Medicine.objects.all()
        serializer = MedicineSerializer(medicines, many=True)
        return Response(serializer.data,status=HTTP_200_OK)
    
    elif request.method == "POST":
        serializer = MedicineSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTP_201_CREATED)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)


# http://127.0.0.1:8000/storeapi/medicines/3
@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def Medicine_Detail(request,id):
    try:
        medicine = Medicine.objects.get(id=id)

    except Medicine.DoesNotExist:
        return Response({'error': 'Post not found'},status=HTTP_404_NOT_FOUND)


    if request.method == "GET":
        serializer = MedicineSerializer(medicine)
        return Response(serializer.data,status=HTTP_200_OK)
    
    elif request.method == "PUT":
        serializer = MedicineSerializer(medicine, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=HTTP_200_OK)
        return Response(serializer.errors,status=HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        medicine.delete()
        return Response('Deleted Successfully',status=HTTP_204_NO_CONTENT)