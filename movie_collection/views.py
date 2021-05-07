from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from user.permissions import IsOwnerOrAdmin
from .models import MovieCollection
from .services import MovieService

service = MovieService()


class ThirdPartyAPiMovieList(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication
    #get
    def get(self, request):
        #gives movie data from third party API 
        page_no = request.query_params.get('page')
        return service.ThirdPartyAPIList(page_no)
       
        

class MovieCollectionListCreateView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_class = JSONWebTokenAuthentication

    #Post
    def post(self, request):  
        return service.createList(request=request)

    #Get
    def get(self, request):
       
        return service.Fetchlist(request=request)


class MovieCollectionOperationsView(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrAdmin)
    authentication_class = JSONWebTokenAuthentication

    def get_queryset(self):
        return MovieCollection.objects.prefetch_related('collection_movies').get(pk=self.kwargs['uuid'])


    def get(self, request, *args, **kwargs):
        """method for get request for  movie collection"""
        try:
            self.check_object_permissions(self.request, self.get_queryset())
            return service.retrieve(instance=self.get_queryset())
        except MovieCollection.DoesNotExist:
            return Response({
                'error': 'Invalid UUID'
            })

    #update
    def put(self, request, *args, **kwargs):

        try:
            self.check_object_permissions(self.request, self.get_queryset())
            return service.update(request=request, instance=self.get_queryset())

        except MovieCollection.DoesNotExist:
            return Response({
                'error': 'This UUID movie does not exist'
            })

    #Delete
    def delete(self, request, *args, **kwargs):

        try:
            self.check_object_permissions(self.request, self.get_queryset())
            return service.delete(instance=self.get_queryset())
        except MovieCollection.DoesNotExist:
            return Response({
                'error': 'This UUID movie does not exist'
            })



