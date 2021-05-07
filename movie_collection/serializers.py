from django.db import transaction
from rest_framework import serializers
from rest_framework.response import Response
from movie_collection.models import MovieCollection, CollectionMovieMapping



class MovieCollectionSerializer(serializers.Serializer):
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=True, allow_blank=True, allow_null=True)
    movies = serializers.ListField(required=True)


    @transaction.atomic()
    def create(self, validated_data):

            # getting context of the user
            user = self.context.get('user')
            # creating new movie collection
           
           
            collection = MovieCollection.objects.create(user=user, title=validated_data['title'],
                                                            description=validated_data['description'])

            #creating movies collection array
            collection_movies=[]
            for movie in validated_data['movies']:
                collection_movies.append(
                    CollectionMovieMapping(collection=collection, movie_uuid=movie['uuid'], title=movie['title'], description=movie['description'], genres=movie['genres']) 
                )

            # collection created in DB
            CollectionMovieMapping.objects.bulk_create(collection_movies)

            return collection


    @transaction.atomic()
    def update(self, instance, validated_data):
            if len(validated_data['movies']) > 0:
                # updating movie list if the payload is not empty
                CollectionMovieMapping.objects.filter(collection=instance).delete()
                 #creating movies collection array
            collection_movies=[]
            for movie in validated_data['movies']:
                collection_movies.append(
                    CollectionMovieMapping(collection=instance, movie_uuid=movie['uuid'], title=movie['title'], description=movie['description'], genres=movie['genres']) 
                )

                CollectionMovieMapping.objects.bulk_create(collection_movies)
            # popping validated_data[movies]
            validated_data.pop('movies')
            # PUT for movie collection
            MovieCollection.objects.filter(pk=instance.pk).update(**validated_data)

            return instance


    def to_representation(self, instance):
            def get_movies():
                # get method for movie collection
                return [movie for movie in instance.collection_movies.values('title', 'description', 'genres', 'movie_uuid')]

            return {
                'title': instance.title,
                'uuid': instance.uuid,
                'description': instance.description,
                'movies': get_movies()
            }



