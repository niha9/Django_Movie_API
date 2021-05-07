from django.db import transaction
from rest_framework import serializers

from movie_collection.models import MovieCollection, CollectionMovieMapping


class MovieCollectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = MovieCollection()
        fields = ['title','description','movies']
        depth = 1
        extra_kwargs = {'title': {'required': True}, 'description': {'required': True}, 'movies': {'required': True}} 

   
    @transaction.atomic()
    def create(self, validated_data):
       
        # getting context of the user
        user = self.context.get('user')
        # creating new movie collection
        collection_movies = validated_data.pop('movies')
       
        collection = MovieCollection.objects.create(**validated_data)
       

       
        #storing all the movies in collection_movies array 
        if len(collection_movies) > 0:
            MoviesArray = []
            for movie in collection_movies:
                MoviesArray.append(CollectionMovieMapping(collection = collection, movie_uuid = movies['uuid'], 
                                title = movies['title'], description = movies['description'], genres = movies['genres']))

       
        # saving data in DB
        CollectionMovieMapping.objects.bulk_create(MoviesArray)

        return collection


    @transaction.atomic()
    def update(self, instance, validated_data):
        if len(validated_data['movies']) > 0:
            # updating movie list if the payload is not empty
            CollectionMovieMapping.objects.filter(collection=instance).delete()
            #collection_movies = validated_data.pop('movies')
            #MovieCollection.participants.set(participants)
            collection_movies = validated_data.pop('movies')



            MoviesArray = []
            for movie in validated_data['movies']:
                MoviesArray.append(CollectionMovieMapping(collection = collection, movie_uuid = movie['uuid'], 
                                title = movie['title'], description = movie['description'], genres = movie['genres']))

            CollectionMovieMapping.objects.bulk_create(MoviesArray)

        # popping validated_data[movies]
        validated_data.pop('movies')
        # PUT for movie collection
        MovieCollection.objects.filter(pk=instance.pk).update(**validated_data)

        return instance


    """ 
    def to_representation(self, instance):
        def get_movies():
            # get method for movie collection
            return [movie for movie in instance.collection_movies.values('title', 'description', 'genres', 'movie_uuid')]
            #for movie in instance.collection_movies.values('title', 'description', 'genres', 'movie_uuid'):

        return {
            'title': instance.title,
            'uuid': instance.uuid,
            'description': instance.description,
            'movies': get_movies()
        }"""
