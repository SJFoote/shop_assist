from django.db import models
import json
import requests
from bs4 import BeautifulSoup
from lxml import etree

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

    def getPrice(request):
        #1
        soup = BeautifulSoup(page.text, 'lxml')
        bookList = []
        for heading in soup.select('a[href*="catalogue"]'):
            bookPrice = heading.get('price')
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
    #price = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()
