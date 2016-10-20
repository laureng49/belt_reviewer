from __future__ import unicode_literals
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from django.db import models
import bcrypt
# Create your models here.
class UserManager(models.Manager):
    def login(self, post):
        user_list = User.objects.filter(email=post['email'])
        if user_list:
            user = user_list[0]
            #check their credentials
            if bcrypt.hashpw(post['password'].encode(), user.password.encode()) == user.password:
                #then login is valid
                return user
        #else:
        return None

    def register(self, post):
        encrypted_password = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt())
        User.objects.create(name=post['name'], alias=post['alias'], email=post['email'], password=encrypted_password)

    def validate_user_info(self, post):
        errors = []

        if len(post['name']) < 3:
            errors.append('Name must contain at least 3 characters!')
        # if not post['firstname'].isalpha():
        #     errors.append('All First Name characters must be alphabetic!.')
        if len(post['alias']) == 0:
            errors.append('Alias cannot be blank!')

        if len(post['password']) < 8:
            errors.append('Your password must contain at least 8 characters!')
        if post['password'] != post['confpass']:
            errors.append('Your confirmation password must match your password!')

    	if not EMAIL_REGEX.match(post['email']):
            errors.append('Please enter a valid email address!')
        if len(User.objects.filter(email=post['email'])) > 0:
            errors.append("That Email address is unavailable!")

        return errors

class AuthorManager(models.Manager):
    pass
class BookManager(models.Manager):
    pass
class ReviewManager(models.Manager):
    pass

class User(models.Model):
    name = models.CharField(max_length=100)
    alias = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()

class Author(models.Model):
    name = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = AuthorManager()

class Book(models.Model):
    author = models.ForeignKey(Author)
    title = models.CharField(max_length=250)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()

class Review(models.Model):
    user = models.ForeignKey(User)
    book = models.ForeignKey(Book)
    review = models.CharField(max_length=1000)
    rating = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = ReviewManager()
