from random import random
import re
import time
import random
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
import requests
from bs4 import BeautifulSoup
from api.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'premium', 'coins', 'avtar',
                  'shared_fact_counts', 'streak', 'last_seen', 'premium_start_date', 'premium_end_date']


class UserAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'avtar', 'is_staff', 'is_superuser', 'email', 'premium', 'coins',
                  'shared_fact_counts', 'streak', 'last_seen', 'premium_start_date', 'premium_end_date']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            password=make_password(validated_data['password']))
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class SimpleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fact
        fields = "__all__"


class FactSerializer(serializers.ModelSerializer):
    category = SimpleCategorySerializer()

    class Meta:
        model = Fact
        fields = ['id', 'fact', 'timestamp', 'likes_count', 'bookmarks_count',
                  'imgURL', 'imgURL2', 'ref', 'desc', 'category', 'isAd']
    likes_count = serializers.IntegerField(read_only=True)
    bookmarks_count = serializers.IntegerField(read_only=True)


class FactAddSerializer(serializers.ModelSerializer):

    class Meta:
        model = Fact
        fields = ['id', 'fact', 'timestamp', 'category', 'isAd']

    def create(self, validated_data):
        fact = self.validated_data.get('fact')
        category = self.validated_data.get('category')
        isAd = self.validated_data.get('isAd')
        if isAd:
            return Fact.objects.create(**validated_data)
        imgURL, imgURL2, refLink, desc = getFactData(fact)
        if not imgURL:
            cat: Category = Category.objects.filter(name=category).get()
            imgURL = cat.imgURL
        return Fact.objects.create(imgURL=imgURL, imgURL2=imgURL2, ref=refLink, desc=desc, **validated_data)


class BookMarkSerializer(serializers.ModelSerializer):
    fact = FactSerializer()

    class Meta:
        model = BookMark
        fields = "__all__"
    likes_count = serializers.IntegerField(read_only=True)
    bookmarks_count = serializers.IntegerField(read_only=True)


class BookMarkAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookMark
        fields = "__all__"


class LikeSerializer(serializers.ModelSerializer):
    fact = FactSerializer()

    class Meta:
        model = Like
        fields = "__all__"


class LikeAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = "__all__"


class RewardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reward
        fields = "__all__"


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = "__all__"


class UserTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserTasks
        fields = "__all__"


class DailyFactSerializer(serializers.ModelSerializer):
    fact = FactSerializer()

    class Meta:
        model = DailyFact
        fields = ['id', 'date', 'fact']


class DailyFactAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyFact
        fields = "__all__"


class CategoryRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryRequest
        fields = "__all__"


class ReportFactSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReportFact
        fields = "__all__"


class UserInterestSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserInterest
        fields = "__all__"


def getFactData(fact: str):
    print('Gathering reference link and description')
    rawData = requests.get('https://www.google.com/search?q='+fact)
    soup = BeautifulSoup(rawData.text, 'lxml')
    refLink = getRefLink(soup)
    desc = getDes(soup)
    time.sleep(random.randint(4, 8))
    imgURL1, imgURL2 = getImageURL(fact)
    return (imgURL1, imgURL2, refLink, desc)


def getImageURL(fact):
    print('Generating Images')
    rawData = requests.get('https://www.google.com/search?q='+fact+" images")
    soup = BeautifulSoup(rawData.text, 'lxml')
    elements = soup.select('.BVG0Nb')
    url1 = None
    url2 = None
    for i in elements:
        link = i["href"]
        image_url_pattern = '(=http.+.\.jpg|=http.+.\.png|=http.+.\.jpeg|=http.+.\.gif)'
        img_url = re.findall(image_url_pattern, link)
        # print(img_url)
        if img_url:
            if not url1:
                url = img_url[0][1:]
                if is_url_image(url):
                    url1 = url
            else:
                url = img_url[0][1:]
                if is_url_image(url):
                    url2 = url
        if url1 and url2:
            break
    return (url1, url2)


def getRefLink(soup):
    elements = soup.find_all('a', href=True)
    urlLink = None
    for i in elements:
        link = i['href']
        if link.startswith("/url"):
            extracted_url_pattern = '(?:^.+ ?q=)(.+$)'
            url = re.findall(extracted_url_pattern, link)

            urlLink = re.match("(.*?)&", url[0])
            if urlLink:
                urlLink = urlLink.group()[:-1]
        # Ref linked can be checked to block restricted sites
        if urlLink:
            return urlLink


def getDes(soup):
    elements = soup.select('.BNeawe')
    desc = None
    for i in elements:
        desc = i.text
        if desc:
            return desc


def is_url_image(image_url: str):
    print('Verifying Image')
    image_formats = ("image/png", "image/jpeg", "image/jpg", "image/gif")
#    if image_url.count('facebook.com')>0:
#        print('Blocking Images From Restricted Sites')
#        return False
    try:
        r = requests.head(image_url, timeout=10)
    except:
        return False
    if r.headers.get("content-type") in image_formats:
        return True
    return False
