from django.db import models
import re
import bcrypt 


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class userManager(models.Manager):
    def validations(self, postData):
        errors = {}

        # First Name - required; at least 2 characters; letters only
        if len(postData['first_name']) < 2:
            errors['first_name']='First name is required to be at least 2 characters, and letters only'
        # Last Name - required; at least 2 characters; letters only
        if len(postData['last_name']) < 2:
            errors['last_name']='Last name is required to be at least 2 characters, and letters only'
        
        # Email - required; valid format
        if not EMAIL_REGEX.match(postData['email']) and len(postData['email']) < 0:
            errors['email']= 'Your email format is invalid.'

        # check to see if user email is not already in use
        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email']='Email is already in use'

        # Password - required; at least 8 characters; matches password confirmation
        if len(postData['password']) < 8:
            errors['password'] = 'A password is required'

        if postData['password'] != postData['confirm_pw']:
            errors['password']= 'Your password does not match with the confirmed password.'
        return errors

    def login_validation(self, email, password):
        # filter out email being used, to see if it exist in the db
        users = self.filter(email=email)
        # if user email is not in DB return false
        if not users:
            return False
        # current user will be the first in the list, since there is only one email allowed per user, no double use of emails
        user = users[0]
        # return with a password check of the password in db, and current users password
        return bcrypt.checkpw(password.encode(), user.password.encode) 

    def register(self, postData):
        pw= bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt().decode())
        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email= postData['email'],
            password = pw
        )

# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length = 100)
    password = models.CharField(max_length = 60)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = userManager()