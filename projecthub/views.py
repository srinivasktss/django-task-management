from operator import mul
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.contrib.auth import authenticate, login

from projecthub.tasks import add, xsum, xsum
from .models import Project
from .serializers import ProjectSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

# Create your views here.
@api_view(['GET'])
def project_list(request):
    project_list = Project.objects.all()
    response = {
        'projects': project_list
    }
    return Response(response, status=status.HTTP_200_OK)

@api_view(['POST'])
def create_project(request):
    data = request.data
    projectSerializer = ProjectSerializer(data=data)
    try:
        projectSerializer.is_valid(raise_exception=True)
        projectSerializer.save()
        return Response({'data': projectSerializer.data}, status=status.HTTP_201_CREATED)
    except ValidationError as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def keycloak_login(request):
    token = request.headers.get('Authorization', '').split('Bearer ')[-1]
    user = authenticate(request, token=token)
    if user:
        login(request, user)
        return JsonResponse({'message': 'Login successful'})
    return JsonResponse({'error': 'Invalid token'}, status=401)

@api_view(['POST'])
def user_login(request):
    # Retrieve credentials from POST data
    data = request.data
    if not data or 'username' not in data or 'password' not in data:
        return Response("Missing credentials.", status=status.HTTP_400_BAD_REQUEST)
    
    username = data.get('username')
    password = data.get('password')
    
    # Use Django's authentication backend (which might be extended by Keycloak)
    user = authenticate(request, username=username, password=password)
    
    if user is not None:
        # Valid credentials: log the user in
        login(request, user)
        return Response("Login successful.", status=status.HTTP_200_OK)
    else:
        # Invalid credentials: return an error response
        return Response("Invalid credentials.", status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['GET'])
@permission_classes([AllowAny])
def add_task(request):
    data = request.query_params
    task_type = data.get('task_type')
    try:
        a:int = int(data.get('a', 0))
        b:int = int(data.get('b', 0))
    except ValueError:
        return Response("Invalid input. Please provide integers for 'a' and 'b'.", status=status.HTTP_400_BAD_REQUEST)

    if task_type == 'add':
        result = add.delay(a, b)
    elif task_type == 'mul':
        result = mul.delay(a, b)
    elif task_type == 'xsum':
        result = xsum.delay([a, b])
    else:
        return Response("Invalid task type.", status=status.HTTP_400_BAD_REQUEST)

    return Response({"task_id": result.id}, status=status.HTTP_202_ACCEPTED)