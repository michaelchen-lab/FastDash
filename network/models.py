from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True
    )
    followers = models.ManyToManyField(User, blank=True, related_name="followers")
    following = models.ManyToManyField(User, blank=True, related_name="following")
    
    def __str__(self):
        return self.user.username
    
    def serialize(self, current_user_pk):
        if self.user.pk == current_user_pk:
            ## If this profile belongs to current user
            is_user = True
            is_following = False # Does not matter
        elif current_user_pk in [followers.pk for followers in self.followers.all()]:
            ## If current user follows this profile
            is_user = False
            is_following = True
        else:
            print([self.followers.all()])
            print(current_user_pk)
            is_user = False
            is_following = False
            
        return {
            "user": self.user.username,
            "num_of_followers": self.followers.all().count(),
            "num_of_following": self.following.all().count(),
            "is_user": is_user,
            "is_following": is_following
        }

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")
    
    def __str__(self):
        return str(self.pk)
    
    def get_number_of_likes(self):
        return self.likes.count()
    
    def serialize(self, current_user_pk):
        ## Check if current user has liked the post
        users_who_liked = [user.pk for user in self.likes.all()]
        user_liked = False
        if current_user_pk in users_who_liked:
            user_liked = True
        
        ## Check if the current user created this post
        is_user = False
        if self.user.pk == current_user_pk:
            is_user = True
        
        return {
            "user_id": self.user.pk,
            "post_id": self.pk,
            "user": self.user.username,
            "body": self.body,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),
            "likes": self.get_number_of_likes(),
            "liked_by_user": user_liked,
            "is_user": is_user
        }
