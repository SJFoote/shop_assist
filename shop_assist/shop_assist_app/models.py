from django.db import models
import json, bcrypt, re
import requests
from bs4 import BeautifulSoup
from lxml import etree
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

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
        return bookList

    def getDescription(request):
        soup = BeautifulSoup(page.text, 'lxml')
        bookList = []
        for heading in soup.select('a[href*="catalogue"]'):
            bookDescription = heading.get('description')#bookDescription = heading.get('p')?
            print(soup.description)
        return bookList

    def getPrice(request):
        #1
        soup = BeautifulSoup(page.text, 'lxml')
        bookList = []
        for heading in soup.select('a[href*="catalogue"]'):
            bookPrice = heading.get('price')#bookPrice = heading.get('int') bookPrice = heading.get('integer')?
            print(soup.price)
        return bookList
        #2
        soup = BeautifulSoup(page.text, 'lxml')
        bookList = []
        for price in soup.find_all('price'):
            print(price.string)
            print(str(price.text))
        return bookList
        #3
        for price in soup.find_all('price'):
            print(soup.get('price'))
        return bookList


class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()


class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First Name must be at least 2 characters'

        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last Name must be at least 2 characters'

        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Invalid Email Address'

        email_check = self.filter(email=postData['email'])
        if email_check:
            errors['email'] = "Already in use"
        if len(postData['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters'
        return errors

    def authenticate(self, email, password):
        users = self.filter(email=email)
        if not users:
            return False
        user = users[0]
        return bcrypt.checkpw(password.encode(), user.password.encode())

    def register(self, postData):
        pw = bcrypt.hashpw(
            postData['password'].encode(), bcrypt.gensalt()).decode()
        return self.create(
            first_name=postData['first_name'],
            last_name=postData['last_name'],
            email=postData['email'],
            password=pw,
        )
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=55)
    last_name = models.CharField(max_length=55)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    objects = UserManager()
