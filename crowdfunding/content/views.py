from django.http import Http404
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .models import Project, Pledge
from .serializers import ContentSerializer, PledgeSerializer, ContentDetailSerializer
from .permissions import IsOwnerOrReadOnly


# Create your views here.

class ProjectList(APIView):
    
    def get(self, request):
        projects = Project.objects.all()
        serializer = ContentSerializer(projects, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = ContentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(owner=request.user)
        return Response(
            serializer.data,
            status=status.HTTP_400_BAD_REQUEST
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
        # project = self.get_object(pk)
        # serializer = ContentSerializer(project)
        # return Response(serializer.data)
    def get(self, request, pk):
        project = self.get_object(pk)
        serializer = ContentDetailSerializer(project)
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

class PledgeList(APIView):

    def get (self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many = True)
        return Response(serializer.data)
    
    def post(self,request):
        serializer = PledgeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_201_CREATED
            )
        
        return Response(
            serializer.errors,
            status = status.HTTP_400_BAD_REQUEST
        )