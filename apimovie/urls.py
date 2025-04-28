from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/search/', SearchAPIView.as_view(), name='search-api'),
    path("api/home",MovieInfo.as_view(),name="movie-home"),
    path("api/category/<str:name>/",MovieCategory.as_view(),name="category"),
    path('api/movie/<str:name>/', DetailsMovie.as_view(), name='movie-detail-by-name'),
    path('api/<str:type>/<str:name>/<str:episode>/', MovieEpisodeDetail.as_view()),
    path("api/signup",SignupView.as_view(),name="signup"),
    path("api/login",LoginView.as_view(),name="login"),
    path("api/history/<str:username>/",MovieHistoryAPIView.as_view(),name="add_history"),
    path('api/rating/<str:moviename>/', MovieRatingAPIView.as_view(), name='movie_rating_api'),
    path('api/ratting/<str:moviename>/', MovieReview1.as_view(), name='movie_review_ratting'),
    path("api/comment/",CommentAPI.as_view(),name="api_comment"),
]
