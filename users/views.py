from django.shortcuts import redirect,render
from rest_framework.views import APIView
from .serializers import UserSerializer
from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed
import jwt,datetime
from django.http import JsonResponse
from rest_framework import status
from django.contrib.auth.hashers import make_password
from users.models import User
from rest_framework.parsers import MultiPartParser
from django.urls import reverse
from django.contrib.auth import authenticate, login


# class RegisterUser(APIView):
#     parser_classes = [MultiPartParser]

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
        
#         # Redirect to the login page
#         return redirect(reverse('login'))

from rest_framework.exceptions import APIException

class RegisterUser(APIView):
    parser_classes = [MultiPartParser]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except APIException as e:
            # If validation fails, return detailed error message
            return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

        # Save the user if validation passes
        serializer.save()

        # Return success message
        return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)


class LoginUser(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        
        # Finding user by using email
        user = authenticate(request, email=email, password=password)
        
        if user is None:
            raise AuthenticationFailed('User not found')
        
        # Creating token using JWT
        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=180),
            'iat': datetime.datetime.utcnow()
        }
        
        token = jwt.encode(payload, 'secrete', algorithm='HS256')

        # Returning token via JSON response
        response = JsonResponse({'jwt': token})
        response.set_cookie('jwt', token, httponly=True)

        return response

    def get(self, request):
        # Handle GET requests for login page
        # Return the HTML template for the login page
        return render(request, 'user/login.html')

class LogoutUser(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Successfully logged out'
        }
        return redirect('/')
    

class UserView(APIView):
    def get_user_from_token(self, request):
        token = request.COOKIES.get('jwt')
        
        if not token:
            raise AuthenticationFailed('unauthenticated')
        
        try:
            payload = jwt.decode(token, 'secrete', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('unauthenticated')
        
        user = User.objects.filter(id=payload['id']).first()
        
        if not user:
            raise AuthenticationFailed('user not found')
        
        return user

    # this will return login user
    def get(self, request):
        user = self.get_user_from_token(request)
        serializer = UserSerializer(user)
        return Response(serializer.data)



    def delete(self, request):
        user = self.get_user_from_token(request)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
   
    
    def put(self, request):
        user = self.get_user_from_token(request)
        password = request.data.get('password')

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Hash the password if it is provided in the request
        if password:
            mutable_data['password'] = make_password(password)

        serializer = UserSerializer(user, data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)  # Print the error details for troubleshooting
            
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def userdashboard(request):
    return render(request=request,template_name="user/user_dashboard.html")


