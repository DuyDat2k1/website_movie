from rest_framework import serializers
from .models import *
from .models import CustomUser
from rest_framework.serializers import ModelSerializer, EmailField, CharField
from rest_framework.validators import UniqueValidator


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'password', 'is_active', 'is_admin']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email','password']
class YearSerializer(serializers.ModelSerializer):
    class Meta:
        model = YearMovie
        fields = "__all__"
class SubtitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subtitle
        fields = "__all__"
class MovieTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieType
        fields = "__all__"
class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreMovie
        fields = "__all__"
class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CountryMovie
        fields = "__all__"
class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields = "__all__"
class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = "__all__"
class EpisodeMovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ['title_episode', 'video_file']
class MovieSerializer(serializers.ModelSerializer):
    Year = YearSerializer()
    genres = GenreSerializer(many=True)
    type = MovieTypeSerializer()
    country = CountrySerializer()
    subtitle = SubtitleSerializer()
    actor = ActorSerializer(many = True )
    director = DirectorSerializer()
    class Meta:
        model = Movie
        fields = '__all__'
class MovieHistoryserilizer(serializers.ModelSerializer):
    episode_title = serializers.IntegerField(source='episode.title_episode', read_only=True)
    movie_title = serializers.CharField(source='episode.movie.title_Vietnamese', read_only=True)
    video_url = serializers.FileField(source = 'episode.video_file',read_only = True)
    type_movie = serializers.CharField(source ='episode.movie.type.name',read_only = True)
    class Meta:
        model=MovieHistory
        fields = "__all__"
class MovieReviewserilizer(serializers.ModelSerializer):
    class Meta:
        model = MovieReview  # Định nghĩa model mà Serializer sẽ sử dụng
        fields = '__all__'   # Hoặc chỉ rõ các trường mà bạn muốn bao gồm trong serialization
class CommentSerillizer(serializers.ModelSerializer):
    movie_title = serializers.CharField(source='movie.title_Vietnamese', read_only=True)
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = MovieComment
        fields = ['movie', 'user', 'movie_title', 'username', 'comment', 'created_at']