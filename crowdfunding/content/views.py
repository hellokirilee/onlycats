from django.http import Http404
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions, exceptions
from .models import Category, Project, Pledge
from .serializers import (
    ContentSerializer, PledgeSerializer, ContentDetailSerializer,
    SupporterContentDetailSerializer, ImageSerializer
)
from .permissions import IsOwnerOrReadOnly


# Create your views here.

class ProjectList(APIView):
    
    def get(self, request):
        projects = Project.objects.all()
        
        # Filtering
        user = request.query_params.get('user')
        if user is not None:
            projects = projects.filter(owner__user__username=user)

        category = request.query_params.get('category')
        if category is not None:
            projects = projects.filter(category__category__iexact=category)
        
        
        serializer = ContentSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user.profile)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ProjectDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    def get_object(self,pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404
        
    def get(self, request, pk):
        project = self.get_object(pk)
        is_supporter = project.pledges.filter(supporter=request.user).exists()
        serializer_class = SupporterContentDetailSerializer if is_supporter else ContentDetailSerializer
        serializer = serializer_class(project)
        return Response(serializer.data)

    def put(self, request, pk):
        project = self.get_object(pk)
        data = request.data
        serializer = ContentDetailSerializer(
            instance=project,
            data=data,
            partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, pk):
        project = self.get_object(pk)
        if not request.user.is_staff:
            raise exceptions.PermissionDenied()
        
        project.delete()
        return Response(status=status.HTTP_200_OK)

        

class PledgeList(APIView):

    def get (self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(supporter=request.user)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )

class OwnerImageLibrary(APIView):

    def get_object(self,pk):
        try:
            return Project.objects.get(pk=pk)
        except Project.DoesNotExist:
            raise Http404

    def post(self, request, pk):
        project = self.get_object(pk)
        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(project=project)
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )