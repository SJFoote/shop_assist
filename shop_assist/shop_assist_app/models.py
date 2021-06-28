from django.db import models
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree
import re
import bcrypt
from datetime import datetime, timedelta
from django.utils import timezone


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        check = User.objects.filter(email=postData['email'])
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if not EMAIL_REGEX.match(postData['email']):
            errors['regex'] = ("Invalid email address!")
            
        email_check= self.filter(email= postData['email'])
        if email_check:
            errors['email'] = "Email already in use"  
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData['password'] != postData['confirm']:
            errors['password'] = 'Passwords do not match'
        return errors
    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False

        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())
    

    def register(self, postData):
        pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name = postData['first_name'],
            last_name = postData['last_name'],
            email = postData['email'],
            password = pw
        )

URL = 'https://books.toscrape.com/?'
page = requests.get(URL)

# Create your models here.
class BookManager(models.Manager):
    def getTitles(request):
        soup = BeautifulSoup(page.text, 'lxml')
        bookList = []
        for heading in soup.select('a[href*="catalogue"]'):
            bookTitle = heading.get('title')
            if bookTitle != None:
                bookList.append(bookTitle)
        print(len(bookList))
        return bookList

class Book(models.Model): 
    title = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()