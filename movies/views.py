from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template import loader
from movies.forms import UserRegisteration, UserLoginn
from django.db.models import Q
from movies.models import *
import pandas as pd
import numpy as np
import random

myuser = ""  # to use variable myuser from def login and put it in def profile >>(Answer #2) https://stackoverflow.com/questions/16043797/python-passing-variables-between-functions
user = ""  # will use it to check if user is_authenticated to get rating stars in def details

def login_view(request):
    form = UserLoginn(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        global user  # will use it to check if user is_authenticated to get rating stars in def details
        user = authenticate(username=username, password=password)
        login(request, user)
        print(request.user.is_authenticated())  # print True in run for debugging

        global myuser
        myuser = AuthUser.objects.values().get(username=username)
        muserid = myuser['userid']
        print ("KKKKKKKKKKKKKKK >> " + str(muserid) + " ... " + str(myuser))

    context = {'form': form, 'error_message': ">> Sorry, that login was invalid. Please try again."}
    return render(request, "movies/index.html", context)


def register_view(request):
    form = UserRegisteration(request.POST or None)
    if form.is_valid():
        print("True")  # debugging
        user = form.save(commit=False)
        password = form.cleaned_data.get('password')
        user.set_password(password)
        user.save()
        return redirect('movies:myindex')
    return render(request, "movies/index.html", {'form': form})


def userLogout(request):
    logout(request)
    return redirect('movies:myindex')


def userRecommend(request):
    login_view(request)
    register_view(request)

    # Search
    mySearch = None

    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))
        # end of search

    # Users Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
    # end of users search

    # User Recommendations
    global myuser  # variable from login def
    myyuser = myuser
    muserid = myyuser['userid']
    moviesRec = recommended(muserid)


    movie1 = moviesRec[0]
    movieRec1 = Movies.objects.values().get(title=movie1)
    movie2 = moviesRec[1]
    movieRec2 = Movies.objects.values().get(title=movie2)
    movie3 = moviesRec[2]
    movieRec3 = Movies.objects.values().get(title=movie3)
    movie4 = moviesRec[3]
    movieRec4 = Movies.objects.values().get(title=movie4)
    movie5 = moviesRec[4]
    movieRec5 = Movies.objects.values().get(title=movie5)
    movie6 = moviesRec[5]
    movieRec6 = Movies.objects.values().get(title=movie6)
    movie7 = moviesRec[6]
    movieRec7 = Movies.objects.values().get(title=movie7)
    movie8 = moviesRec[7]
    movieRec8 = Movies.objects.values().get(title=movie8)
    movie9 = moviesRec[8]
    movieRec9 = Movies.objects.values().get(title=movie9)
    movie10 = moviesRec[9]
    movieRec10 = Movies.objects.values().get(title=movie10)
    movie11 = moviesRec[10]
    movieRec11 = Movies.objects.values().get(title=movie11)
    movie12 = moviesRec[11]
    movieRec12 = Movies.objects.values().get(title=movie12)


    # User Recommendations

    all_movies = Movies.objects.values()  # get list of movies
    template = loader.get_template('movies/list.html')
    context = {'all_movies': all_movies, 'mySearch': mySearch, 'mySearch2': mySearch2, 'movieRec1': movieRec1,
               'movieRec2': movieRec2, 'movieRec3': movieRec3, 'movieRec4': movieRec4, 'movieRec5': movieRec5,
               'movieRec6': movieRec6, 'movieRec7': movieRec7, 'movieRec8': movieRec8, 'movieRec9': movieRec9,
               'movieRec10': movieRec10, 'movieRec11': movieRec11, 'movieRec12': movieRec12}
    return HttpResponse(template.render(context, request))

def userBased(request):
    login_view(request)
    register_view(request)

    # Search
    mySearch = None

    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))
        # end of search

    # Users Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
        # end of users search

    #Userbased
    global myuser
    muserid = myuser['userid']

    alloutput = run(muserid)
    moviesIds = alloutput.index

    moviesObj = []
    expectedRate = []

    for i in moviesIds:
        movie = Movies.objects.values().get(movieid=i)
        moviesObj.append(movie)
        expectedRate.append(round(alloutput[i], 2))

    count = 0
    for i in moviesObj:  # loop through every movie and add it's rate as new dic element "expRate":"value"
        i.update({"expRate": expectedRate[count]})
        count = count + 1


    all_movies = Movies.objects.values()  # get list of movies
    template = loader.get_template('movies/userBasedmovies.html')
    context = {'all_movies': all_movies, 'mySearch': mySearch, 'mySearch2': mySearch2, 'moviesObj': moviesObj}
    return HttpResponse(template.render(context, request))

def profile(request):
    # Movies rated by logging user
    global myuser  # variable from login def
    print ("<<<<<<<<<<<<<<<<<<<<<<<<<<" + str(myuser))

    myyuser = myuser
    muserid = myyuser['userid']
    print ("KKKKKKK >> " + str(muserid) + " ... " + str(myyuser))

    rates = []
    for i in (Ratings.objects.filter(userid=muserid)):
        rates.append(i)  # List of rates objects that belongs to logged user
    idsList = []

    for i in rates:
        movieeid = i.movieid
        idsList.append(movieeid)  # list of movies id that rated by the same user

    myMovies = []
    for i in idsList:
        movie = Movies.objects.values().get(movieid=i)  # every movie object that rated by him
        myMovies.append(movie)
        # print movie['title']

    mrates = []  # list of rates
    for i in rates:
        mrates.append(i.rating)

    s = []  # list of Movies
    for i in myMovies:
        s.append(i)

    count = 0
    for i in s: #loop through every movie and add it's rate as new dic element "rate":"value"
        i.update({"rate": mrates[count]})
        count = count + 1

    print s  # debug

    # Movies rated by logging user

    login_view(request)
    register_view(request)

    # Search
    mySearch = None

    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))
        # end of search


    # Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
    # end of search

    all_movies = Movies.objects.values()
    template = loader.get_template('movies/profile.html')
    context = {'all_movies': all_movies, 's': s, 'mySearch': mySearch, 'mySearch2': mySearch2}
    return HttpResponse(template.render(context, request))

def details(request, pk):
    login_view(request)
    register_view(request)
    # Search
    mySearch = None

    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))
    # end of search
    # Users Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
    # end of users search

    # bottom movies in detail page
    randomMovie1 = random.randint(1, 5)
    randMovie1 = Movies.objects.values().get(movieid=randomMovie1)
    randomMovie2 = random.randint(6, 10)
    randMovie2 = Movies.objects.values().get(movieid=randomMovie2)
    randomMovie3 = random.randint(11, 15)
    randMovie3 = Movies.objects.values().get(movieid=randomMovie3)
    randomMovie4 = random.randint(16, 20)
    randMovie4 = Movies.objects.values().get(movieid=randomMovie4)
    randomMovie5 = random.randint(21, 25)
    randMovie5 = Movies.objects.values().get(movieid=randomMovie5)
    randomMovie6 = random.randint(26, 30)
    randMovie6 = Movies.objects.values().get(movieid=randomMovie6)
    randomMovie7 = random.randint(31, 35)
    randMovie7 = Movies.objects.values().get(movieid=randomMovie7)
    randomMovie8 = random.randint(36, 40)
    randMovie8 = Movies.objects.values().get(movieid=randomMovie8)
    randomMovie9 = random.randint(41, 45)
    randMovie9 = Movies.objects.values().get(movieid=randomMovie9)
    # bottom movies in detail page


    ##################################################################  pplWhoLiked Movies
    r_cols = ['user_id', 'movie_id', 'rating']
    ratings = pd.read_csv('E:\Project\Desktop\Book.csv', sep=',', names=r_cols, usecols=range(3))

    movieRatings = ratings.pivot_table(index=['user_id'], columns=['movie_id'], values='rating')
    starWarsRatings = movieRatings[int(pk)]
    similarMovies = movieRatings.corrwith(starWarsRatings)
    similarMovies = similarMovies.dropna()
    df = pd.DataFrame(similarMovies)
    similarMovies.sort_values(ascending=False)

    movieStats = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
    popularMovies = movieStats['rating']['size'] >= 100
    movieStats[popularMovies].sort_values([('rating', 'mean')], ascending=False)[:15]
    df = movieStats[popularMovies].join(pd.DataFrame(similarMovies, columns=['similarity']))
    df = df.sort_values(['similarity'], ascending=False)[:15]

    a1Movieid = df.index[1]
    sim1 = df['similarity'][a1Movieid]
    views1 = int(df['rating', 'size'][a1Movieid])

    a2Movieid = df.index[2]
    sim2 = df['similarity'][a2Movieid]
    views2 = int(df['rating', 'size'][a2Movieid])

    a3Movieid = df.index[3]
    sim3 = df['similarity'][a3Movieid]
    views3 = int(df['rating', 'size'][a3Movieid])

    a4Movieid = df.index[4]
    sim4 = df['similarity'][a4Movieid]
    views4 = int(df['rating', 'size'][a4Movieid])

    a5Movieid = df.index[5]
    sim5 = df['similarity'][a5Movieid]
    views5 = int(df['rating', 'size'][a5Movieid])

    a6Movieid = df.index[6]
    sim6 = df['similarity'][a6Movieid]
    views6 = int(df['rating', 'size'][a6Movieid])

    a7Movieid = df.index[7]
    sim7 = df['similarity'][a7Movieid]
    views7 = int(df['rating', 'size'][a7Movieid])

    a8Movieid = df.index[8]
    sim8 = df['similarity'][a8Movieid]
    views8 = int(df['rating', 'size'][a8Movieid])


    movie1 = Movies.objects.values().get(movieid=a1Movieid)
    movie2 = Movies.objects.values().get(movieid=a2Movieid)
    movie3 = Movies.objects.values().get(movieid=a3Movieid)
    movie4 = Movies.objects.values().get(movieid=a4Movieid)
    movie5 = Movies.objects.values().get(movieid=a5Movieid)
    movie6 = Movies.objects.values().get(movieid=a6Movieid)
    movie7 = Movies.objects.values().get(movieid=a7Movieid)
    movie8 = Movies.objects.values().get(movieid=a8Movieid)

    ################################################################## pplWhoLiked Movies

    one_movie = Movies.objects.values().get(movieid=pk)

    one_movieId = df.index[0]
    one_movie_sim = df['similarity'][one_movieId] #Similarity of main movie
    one_movie_views = int(df['rating', 'size'][one_movieId]) #no. of rates of main movie


    ############################################################## Rating

    global user #for authentication
    if request.user.is_authenticated:
        if request.POST.get("rating") != None:

            myRate = request.POST.get("rating")
            movieid = int(pk)

            global myuser  # variable from login def
            myyuser = myuser
            muserid = myyuser['userid']
            write_db(muserid, movieid, myRate)

            print (">> >> >> >  " + str(muserid) + "," + str(movieid) + "," + str(myRate))

    ############################################################## Rating

    context = {'one_movie': one_movie, 'one_movie_views': one_movie_views, 'one_movie_sim': one_movie_sim, 'randMovie1': randMovie1, 'randMovie2': randMovie2, 'randMovie3': randMovie3,
               'randMovie4': randMovie4, 'randMovie5': randMovie5, 'randMovie6': randMovie6, 'randMovie7': randMovie7,
               'randMovie8': randMovie8, 'randMovie9': randMovie9,
               'all_movies': all_movies, 'not_found': ">> Sorry, We can't find your request!", 'mySearch': mySearch
        , 'movie1': movie1, 'movie2': movie2, 'movie3': movie3, 'movie4': movie4, 'movie5': movie5, 'movie6': movie6,
               'movie7': movie7, 'movie8': movie8, 'mySearch2': mySearch2,
               'sim1': sim1, 'sim2': sim2, 'sim3': sim3, 'sim4': sim4, 'sim5': sim5, 'sim6': sim6, 'sim7': sim7, 'sim8': sim8,
               'views1': views1, 'views2': views2, 'views3': views3, 'views4': views4, 'views5': views5, 'views6': views6, 'views7': views7, 'views8': views8}
    template = "movies/single.html"
    return render(request, template, context)

def write_db(user_id, movie_id, rate):
    newRate = Ratings.objects.create(userid=user_id, movieid=movie_id, rating=rate)
    newRate.save()

# userN = "" #to use variable userN from def index and put it in def profile >>(Answer #2) https://stackoverflow.com/questions/16043797/python-passing-variables-between-functions

def myindex(request):
    login_view(request)
    register_view(request)

    # Search
    mySearch = None
    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))


    # Users Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
    # end of users search


    # Banner Movies
    bannerMov1 = Movies.objects.values().get(movieid=30)
    bannerMov2 = Movies.objects.values().get(movieid=31)
    bannerMov3 = Movies.objects.values().get(movieid=32)
    bannerMov4 = Movies.objects.values().get(movieid=33)
    bannerMov5 = Movies.objects.values().get(movieid=34)
    bannerMov6 = Movies.objects.values().get(movieid=150)
    # End Banner Movies

    # second part
    randomMovie1 = random.randint(1, 4)
    randMovie1 = Movies.objects.values().get(movieid=randomMovie1)
    randomMovie2 = random.randint(5, 10)
    randMovie2 = Movies.objects.values().get(movieid=randomMovie2)
    randomMovie3 = random.randint(11, 15)
    randMovie3 = Movies.objects.values().get(movieid=randomMovie3)
    randomMovie4 = random.randint(16, 20)
    randMovie4 = Movies.objects.values().get(movieid=randomMovie4)
    randomMovie5 = random.randint(21, 24)
    randMovie5 = Movies.objects.values().get(movieid=randomMovie5)
    randomMovie6 = random.randint(25, 30)
    randMovie6 = Movies.objects.values().get(movieid=randomMovie6)
    randomMovie7 = random.randint(31, 34)
    randMovie7 = Movies.objects.values().get(movieid=randomMovie7)
    randomMovie8 = random.randint(35, 40)
    randMovie8 = Movies.objects.values().get(movieid=randomMovie8)
    randomMovie9 = random.randint(41, 45)
    randMovie9 = Movies.objects.values().get(movieid=randomMovie9)
    # End second part

    ############################################################## Popular movies
    r_cols = ['user_id', 'movie_id', 'rating']
    ratings = pd.read_csv('E:\Project\Desktop\Book.csv', sep=',', names=r_cols, usecols=range(3))
    movieRatings = ratings.pivot_table(index=['user_id'], columns=['movie_id'], values='rating')
    movieStats = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
    popularMovies = movieStats['rating']['size'] >= 100
    movieStats = movieStats[popularMovies].sort_values([('rating', 'size')], ascending=False)[:15]
    movieidsList = movieStats.index #List of popular movies


    a1Movieid = movieidsList[0]
    a2Movieid = movieidsList[1]
    a3Movieid = movieidsList[2]
    a4Movieid = movieidsList[3]
    a5Movieid = movieidsList[4]
    a6Movieid = movieidsList[5]
    a7Movieid = movieidsList[6]
    a8Movieid = movieidsList[7]
    a9Movieid = movieidsList[8]
    a10Movieid = movieidsList[9]
    a11Movieid = movieidsList[10]
    a12Movieid = movieidsList[11]
    a13Movieid = movieidsList[12]
    a14Movieid = movieidsList[13]


    movie1 = Movies.objects.values().get(movieid=a1Movieid)
    movie2 = Movies.objects.values().get(movieid=a2Movieid)
    movie3 = Movies.objects.values().get(movieid=a3Movieid)
    movie4 = Movies.objects.values().get(movieid=a4Movieid)
    movie5 = Movies.objects.values().get(movieid=a5Movieid)
    movie6 = Movies.objects.values().get(movieid=a6Movieid)
    movie7 = Movies.objects.values().get(movieid=a7Movieid)
    movie8 = Movies.objects.values().get(movieid=a8Movieid)
    movie9 = Movies.objects.values().get(movieid=a9Movieid)
    movie10 = Movies.objects.values().get(movieid=a10Movieid)
    movie11 = Movies.objects.values().get(movieid=a11Movieid)
    movie12 = Movies.objects.values().get(movieid=a12Movieid)
    movie13 = Movies.objects.values().get(movieid=a13Movieid)
    movie14 = Movies.objects.values().get(movieid=a14Movieid)

    ############################################################## Popular movies

    ############################################################## Top Rated

    r_cols = ['user_id', 'movie_id', 'rating']
    ratings = pd.read_csv('E:\Project\Desktop\Book.csv', sep=',', names=r_cols, usecols=range(3))
    movieRatings = ratings.pivot_table(index=['user_id'], columns=['movie_id'], values='rating')
    movieStats = ratings.groupby('movie_id').agg({'rating': [np.size, np.mean]})
    popularMovies = movieStats['rating']['size'] >= 100
    movieStats = movieStats[popularMovies].sort_values([('rating', 'mean')], ascending=False)[:15]
    movieidsList = movieStats.index


    topr1 = movieidsList[0]
    topr2 = movieidsList[1]
    topr3 = movieidsList[2]
    topr4 = movieidsList[3]
    topr5 = movieidsList[4]
    topr6 = movieidsList[5]
    topr7 = movieidsList[6]
    topr8 = movieidsList[7]
    topr9 = movieidsList[8]
    topr10 = movieidsList[9]
    topr11 = movieidsList[10]
    topr12 = movieidsList[11]

    topmovie1 = Movies.objects.values().get(movieid=topr1)
    topmovie2 = Movies.objects.values().get(movieid=topr2)
    topmovie3 = Movies.objects.values().get(movieid=topr3)
    topmovie4 = Movies.objects.values().get(movieid=topr4)
    topmovie5 = Movies.objects.values().get(movieid=topr5)
    topmovie6 = Movies.objects.values().get(movieid=topr6)
    topmovie7 = Movies.objects.values().get(movieid=topr7)
    topmovie8 = Movies.objects.values().get(movieid=topr8)
    topmovie9 = Movies.objects.values().get(movieid=topr9)
    topmovie10 = Movies.objects.values().get(movieid=topr10)
    topmovie11 = Movies.objects.values().get(movieid=topr11)
    topmovie12 = Movies.objects.values().get(movieid=topr12)



    ############################################################## Top Rated

    context = {'randMovie1': randMovie1, 'randMovie2': randMovie2, 'randMovie3': randMovie3, 'randMovie4': randMovie4,
               'randMovie5': randMovie5, 'randMovie6': randMovie6, 'randMovie7': randMovie7, 'randMovie8': randMovie8,
               'randMovie9': randMovie9,
               'bannerMov1': bannerMov1, 'bannerMov2': bannerMov2, 'bannerMov3': bannerMov3, 'bannerMov4': bannerMov4,
               'bannerMov5': bannerMov5, 'bannerMov6': bannerMov6,
               'all_movies': all_movies, 'not_found': ">> Sorry, We can't find your request!", 'mySearch': mySearch, 'mySearch2': mySearch2,
               'movie1': movie1, 'movie2': movie2, 'movie3': movie3, 'movie4': movie4, 'movie5': movie5,
               'movie6': movie6, 'movie7': movie7, 'movie8': movie8, 'movie9': movie9, 'movie10': movie10,
               'movie11': movie11, 'movie12': movie12, 'movie13': movie13, 'movie14': movie14,
               'topmovie1': topmovie1, 'topmovie2': topmovie2, 'topmovie3': topmovie3, 'topmovie4': topmovie4, 'topmovie5': topmovie5,
               'topmovie6': topmovie6, 'topmovie7': topmovie7, 'topmovie8': topmovie8, 'topmovie9': topmovie9, 'topmovie10': topmovie10,
               'topmovie11': topmovie11, 'topmovie12': topmovie12}
    template = loader.get_template('movies/index.html')
    return HttpResponse(template.render(context, request))

def similarUsers(request):
    login_view(request)
    register_view(request)

    # Search
    mySearch = None

    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))
        # end of search

    # Users Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
        # end of users search

    #Userbased
    global myuser
    muserid = myuser['userid']
    simUsersMethod = similarUsersAlgo(muserid)
    simUsers = simUsersMethod.index
    listUsersObjs = []
    for i in simUsers:
        mUser = AuthUser.objects.values().get(userid=i)
        listUsersObjs.append(mUser)

    listSim = []
    for i in simUsers:
        listSim.append(round(simUsersMethod[i], 3))

    count = 0
    for i in listUsersObjs:  # loop through every movie and add it's rate as new dic element "rate":"value"
        i.update({"similarity": listSim[count]})
        count = count + 1

    all_movies = Movies.objects.values()  # get list of movies
    template = loader.get_template('movies/simUsers.html')
    context = {'all_movies': all_movies, 'mySearch': mySearch, 'mySearch2': mySearch2, 'listUsersObjs': listUsersObjs}
    return HttpResponse(template.render(context, request))

def usersearch(request, pkuser):

    # Movies rated by search user
    rates = []
    for i in (Ratings.objects.filter(userid=pkuser)):
        rates.append(i)  # List of rates objects that belongs to logged user
    idsList = []

    for i in rates:
        movieeid = i.movieid
        idsList.append(movieeid)  # list of movies id that rated by the same user

    myMovies = []
    for i in idsList:
        movie = Movies.objects.values().get(movieid=i)  # every movie object that rated by him
        myMovies.append(movie)
        # print movie['title']

    mrates = []  # list of rates
    for i in rates:
        mrates.append(i.rating)

    s = []  # list of Movies
    for i in myMovies:
        s.append(i)

    count = 0
    for i in s:  # loop through every movie and add it's rate as new dic element "rate":"value"
        i.update({"rate": mrates[count]})
        count = count + 1

    print s  # debug

    # Movies rated by search user

    login_view(request)
    register_view(request)

    #Movies Search
    mySearch = None

    all_movies = Movies.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch = all_movies.filter(
            Q(title__icontains=query) | Q(genres__icontains=query))
        # end of Movies search

    #Users Search
    mySearch2 = None

    all_users = AuthUser.objects.values()

    query = request.GET.get("Search")  # getString from url
    if query:
        mySearch2 = all_users.filter(Q(username__icontains=query))
        # end of users search


    all_movies = Movies.objects.values()

    searchUser = all_users.get(userid=pkuser)

    ##################################################Follow

    global user, myuser  # for authentication
    muserid = myuser['userid']
    if request.user.is_authenticated:
        if request.GET.get("follow"):
            follow = Followuser.objects.create(userid=muserid, userfollowid=pkuser, isfollow=True)
            follow.save()
            print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>" + str(muserid) + "," + str(pkuser))

    template = loader.get_template('movies/usersearch.html')
    context = {'all_movies': all_movies, 's': s, 'mySearch': mySearch, 'mySearch2': mySearch2, 'searchUser': searchUser}
    return HttpResponse(template.render(context, request))

def recommended(userid): # Algorithm
    r_cols = ['user_id', 'movie_id', 'rating']
    ratings = pd.read_csv('E:\Project\Desktop\Book.csv', sep=',', names=r_cols, usecols=range(3))
    m_cols = ['movie_id', 'title']
    movies = pd.read_csv('E:\Project\Desktop\movies_.csv', sep=';', names=m_cols, usecols=range(2))
    ratings = pd.merge(movies, ratings)
    userRatings = ratings.pivot_table(index=['user_id'], columns=['title'], values='rating')
    corrMatrix = userRatings.corr(method='pearson', min_periods=100)
    myRatings = userRatings.loc[userid].dropna()
    simCandidates = pd.Series()
    for i in range(0, len(myRatings.index)):
        # print "Adding sims for " + str(myRatings.index[i]) + "..."
        # Retrieve similar movies to this one that I rated
        sims = corrMatrix[myRatings.index[i]].dropna()
        # Now scale its similarity by how well I rated this movie
        sims = sims.map(lambda x: x * myRatings[i])
        # Add the score to the list of similarity candidates
        simCandidates = simCandidates.append(sims)
    # Glance at our results so far:
    print "sorting..."
    simCandidates.sort_values(inplace=True, ascending=False)
    simCandidates = simCandidates.groupby(simCandidates.index).sum()
    simCandidates.sort_values(inplace=True, ascending=False)
    # filteredSims = simCandidates.drop(myRatings.index)
    for i in simCandidates:
        if i in myRatings:
            simCandidates.drop(i)
    return simCandidates.index

#Userbased
def load():
 r_cols = ['user_id', 'movie_id', 'rating']
 ratings = pd.read_csv('E:\Project\Desktop\Book.csv', sep=',', names=r_cols, usecols=range(3))
 return ratings
def correlation(ratings):

 userRatings = ratings.pivot_table(index=['movie_id'],columns=['user_id'],values='rating')
 #correlation between every pair of users and on mutual movies
 #condition: 10 movies in common at least
 corrMatrix = userRatings.corr(method='pearson', min_periods=10)
 return userRatings,corrMatrix
#fetch user1 and drop every other user with NA similarity
def user_based(user,userRatings,corrMatrix):
  sims = corrMatrix[user].dropna()
  sims.sort_values(inplace = True, ascending = False)
  Top_matches = sims[1:16]
  Recommendations = pd.Series()
  for i in Top_matches.index:
    for j in userRatings[i].dropna().index:
       if j not in userRatings[user].dropna().index:
        Recommendations.set_value(j,userRatings[i][j]*Top_matches[i])
  Recommendations.sort_values(inplace = True, ascending = False)
  return Recommendations
def run(user):
 ratings = load()
 userRatings,corrMatrix = correlation(ratings)
 rec = user_based(user,userRatings,corrMatrix)
 return rec

def similarUsersAlgo (userid):# Algorithm

    r_cols = ['user_id', 'movie_id', 'rating']
    ratings = pd.read_csv('E:\Project\Desktop\Book.csv', sep=',', names=r_cols, usecols=range(3))

    m_cols = ['movie_id', 'title']
    movies = pd.read_csv('E:\Project\Desktop\movies_.csv', sep=';', names=m_cols, usecols=range(2))

    ratings = pd.merge(movies, ratings)
    # index title,    columns user_id (swap)
    userRatings = ratings.pivot_table(index=['title'], columns=['user_id'], values='rating')
    # correlation between every pair of users and on mutual movies
    # condition: 10 movies in common at least
    corrMatrix = userRatings.corr(method='pearson', min_periods=10)
    # fetch user1 and drop every other user with NA similarity
    sims = corrMatrix[userid].dropna()

    sims.sort_values(inplace=True, ascending=False)
    return sims[1:15]