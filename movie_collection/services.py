from rest_framework.response import Response
from django.db.models import Count

from movie_collection.models import MovieCollection, CollectionMovieMapping
from movie_collection.serializers import MovieCollectionSerializer
from movie_collection.utils import fetch_movie_list


class MovieService:
    def ThirdPartyAPIList(self, page_no):
        response = fetch_movie_list(page_no)
        return response

    def createList(self, request):
        #Creates new movie collection """
    
        serializer = MovieCollectionSerializer(data=request.data, context={'user': request.user})

        #checks if the serializer is valid
        if serializer.is_valid():
            serializer.save()
            return Response({
                'collection_uuid': serializer.data['uuid']
            })
        # returning validation errors
        return Response({
            'error': serializer.errors
        })

    def Fetchlist(self, request):
        # fetching movie collection list for the user
        queryset = MovieCollection.objects.prefetch_related('collection_movies').filter(user=request.user)
        serializer = MovieCollectionSerializer(queryset, many=True)
        genres = CollectionMovieMapping.objects.values('genres').annotate(c=Count('genres')).order_by('-c')
        genres = genres[:3]
        print(genres)
        for value in genres:
            print(value.pop('c'))
        return Response({
            'is_success': True,
            'favourite_genres': genres,
            'data': {
                'collections': serializer.data
            }
        })

    def retrieve(self, instance):

        # retrieving movie collection details
        serializer = MovieCollectionSerializer(instance)
        return Response({
            'collections': serializer.data
        })

    def update(self, request, instance):

        # updating movie collection data
        serializer = MovieCollectionSerializer(instance=instance, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'collection_uuid': serializer.data['uuid']
            })
        return Response({
            'error': serializer.errors
        })

    def delete(self, instance):
        instance.delete()
        return Response({
            'message': 'movie collection deleted successfully.'
        })
