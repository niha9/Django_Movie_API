import uuid as uuid
from django.db import models
from user.models import User

class MovieCollection(models.Model):
    uuid               = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    title              = models.CharField(max_length=100, default='')
    description        = models.TextField(default='')
    user               = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_collections')
    modified_on        = models.DateTimeField(auto_now=True, null=True)
    created_on         = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __str__(self):
        return self.uuid.__str__()

class CollectionMovieMapping(models.Model):
    collection        = models.ForeignKey(MovieCollection, on_delete=models.CASCADE, related_name='collection_movies',db_index=True)
    title             = models.CharField(max_length=100)
    description       = models.CharField(max_length=100)
    genres            = models.CharField(max_length=100)
    movie_uuid        = models.CharField(max_length=100)




