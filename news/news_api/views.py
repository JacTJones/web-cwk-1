from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import Test, Story
from .serializers import TestSerializer, StorySerializer
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import api_view
from datetime import datetime


def translateDate(date):
    try:
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        translated_date = date_obj.strftime("%Y-%m-%d")
        return translated_date
    except ValueError:
        return "Invalid date format"


def dbdateToUk(data):
    try:
        date_obj = datetime.strptime(data, "%Y-%m-%dT%H:%M:%S.%fZ")
        translated_date = date_obj.strftime("%d/%m/%Y")
        return translated_date
    except ValueError:
        return "Invalid date format"


@api_view(("POST",))
def loginApiView(request):
    if request.content_type != "application/x-www-form-urlencoded":
        return Response(
            "Invalid content type. Only application/x-www-form-urlencoded is accepted.",
            status=415,
        )
    if "username" not in request.data or "password" not in request.data:
        return Response(
            "Please provide a value for 'username' and 'password' in the request body.",
            status=400,
        )
    username = request.data.get("username")
    password = request.data.get("password")

    # check if username and password is correct
    user = authenticate(username=username, password=password)

    if user is not None:
        request.session["user"] = user.id
        return Response(
            "Successfully logged in, welcome to the news site!",
            status=200,
        )
    else:
        return Response(
            "Login failed, please make sure username and password are correct.",
            status=401,
        )


# User Register - Not needed for the coursework, just makes creating users easier
@api_view(("POST",))
def registerApiView(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = None
    try:
        user = User.objects.create_user(username=username, password=password)
        return Response("User created successfully", status=201)
    except:
        return Response("Error creating user", status=400)


# User Logout
@api_view(("POST",))
def logoutApiView(request):
    if "user" in request.session:
        del request.session["user"]
        return Response("Logged out", status=200)
    else:
        return Response("You are not logged in, so cannot log out.", status=400)


# Stories
@api_view(
    (
        "GET",
        "POST",
    )
)
def storyApiView(request):
    if request.method == "POST":
        if "user" in request.session:
            if (
                "headline" not in request.data
                or "category" not in request.data
                or "region" not in request.data
                or "details" not in request.data
            ):
                return Response(
                    "Please provide a value for 'headline', 'category', 'region' and 'details' in the request body.",
                    status=503,
                )
            userId = request.session["user"]
            user = User.objects.get(pk=userId)
            data = {
                "headline": request.data.get("headline"),
                "category": request.data.get("category"),
                "region": request.data.get("region"),
                "details": request.data.get("details"),
                "author": user.username,
            }
            serializer = StorySerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(status=201)
            else:
                return Response(serializer.errors, status=503)
        else:
            return Response(
                "User not logged in, you must be logged in to create a story.",
                status=503,
            )
    elif request.method == "GET":
        if (
            request.query_params.get("story_cat") is None
            or request.query_params.get("story_region") is None
            or request.query_params.get("story_date") is None
        ):
            return Response(
                "Please provide a value for 'story_cat', 'story_region' and 'story_date' in the request body.",
                status=400,
            )
        category = request.query_params.get("story_cat")
        region = request.query_params.get("story_region")
        dateUkVersion = request.query_params.get("story_date")
        if dateUkVersion == "*":
            date = "*"
        else:
            date = translateDate(dateUkVersion)

        if category == "*":
            categoryFiltered = Story.objects.all()
        else:
            categoryFiltered = Story.objects.filter(category=category)
        if region == "*":
            regionFiltered = categoryFiltered.all()
        else:
            regionFiltered = categoryFiltered.filter(region=region)
        if date == "*":
            dateFiltered = regionFiltered.all()
        else:
            dateFiltered = regionFiltered.filter(story_date__gte=date)
        serializer = StorySerializer(dateFiltered, many=True)
        print(serializer.data)
        if len(serializer.data) == 0:
            return Response("No stories found for these values.", status=404)
        else:
            resultArray = []
            for item in serializer.data:
                itemObject = {
                    "key": item["id"],
                    "headline": item["headline"],
                    "story_cat": item["category"],
                    "story_region": item["region"],
                    "author": item["author"],
                    "story_date": dbdateToUk(item["story_date"]),
                    "story_details": item["details"],
                }
                resultArray.append(itemObject)
            results = {"stories": resultArray}
            return Response(results, status=200)
    else:
        return Response("Method not allowed", status=405)


# Delete story
@api_view(("DELETE",))
def deleteStoryApiView(request, key):
    if "user" in request.session:
        try:
            story = Story.objects.get(pk=key)
            story.delete()
            return Response("Story deleted successfully.", status=200)
        except Story.DoesNotExist:
            return Response("Story with this id not found", status=503)
    else:
        return Response("Must be logged in to delete a story.", status=503)
