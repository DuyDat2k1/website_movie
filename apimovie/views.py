from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import re
from django.core.paginator import Paginator
from django.db.models import Max,F
from rest_framework import status
from .models import *
from .serializers import *
from django.shortcuts import render
from rest_framework import generics
from django.http import Http404
from urllib.parse import unquote
from django.db.models import Max, Subquery, OuterRef
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .backend import CustomUserBackend
from .models import *
class SignupView(APIView):
    def post(self, request):
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            print(user)
            Customuser= CustomUser.objects.get(username=user.username)
            token = TokenObtainPairSerializer.get_token(user)
            # Tạo Refresh Token
            print(len(str(token)))
            # Tạo Access Token
            created = Customtoken.objects.create(user=user,token=str(token))
               
            print(token)

            return Response({
                'token': str(token),
                'access': str(token),
                'username': user.username
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class LoginView(APIView):
    def post(self, request):
        data = request.data
        user = CustomUserBackend().authenticate(request, email=request.data.get('email'), password=request.data.get('password'))
        print(user)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'token':{'refresh': str(refresh),
                'access': str(refresh.access_token),
            },
            
                'username':user.username,
            
            }, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class SearchAPIView(APIView):
    def get(self, request):
        query = request.query_params.get('q', None)
        print(query)
        if query:
            movies = Movie.objects.filter(title_Vietnamese__icontains=query)
            print(movies)
            serializer = MovieSerializer(movies, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
           return Response({"error": "No query parameter provided"}, status=status.HTTP_400_BAD_REQUEST)
from datetime import datetime,timezone        
from datetime import datetime,timedelta
import json
class MovieInfo(APIView):
    def get(self, request):
        Genre = GenreMovie.objects.all()
        countries = CountryMovie.objects.all()
        years = YearMovie.objects.all()
        types = MovieType.objects.all()
        subs = Subtitle.objects.all()
        Hot_movies = Movie.objects.order_by('view_count')[:10]
        Genre_serializer = GenreSerializer(Genre,many=True)
        types_serializer = MovieTypeSerializer(types,many=True)
        country_serializer = CountrySerializer(countries, many=True)
        year_serializer = YearSerializer(years, many=True)
        subtitle_serializer = SubtitleSerializer(subs,many=True)
        Hot_movies_seralizer = MovieSerializer(Hot_movies,many=True)
        rank_series = Movie.objects.filter(type__name="Phim bộ").order_by("-view_count")
        rank_series_seralizer = MovieSerializer(rank_series,many=True)
        rank_single = Movie.objects.filter(type__name = "Phim lẻ").order_by("-view_count")
        rank_single_seralizer = MovieSerializer(rank_single,many=True)
        
        series_movies = Movie.objects.filter(type__name="Phim bộ").order_by("view_count")

# Khởi tạo một danh sách để lưu trữ thông tin về các bộ phim bộ
        series_movies_data = []

# Lặp qua từng bộ phim bộ
        for movie in series_movies:
    # Lấy thông tin về tập mới nhất của bộ phim bộ
            latest_episode = movie.episodes.order_by('-title_episode').first()  # Lấy tập mới nhất dựa trên số tập
            if latest_episode:
        # Nếu có tập mới nhất, sử dụng serializer để chuyển đổi thông tin của bộ phim bộ và tập mới nhất thành dạng JSON
                serializer = MovieSerializer(movie)
                movie_data = serializer.data
                series_movies_data.append({
                'title_Vietnamese': movie_data['title_Vietnamese'],
                'title': latest_episode.title_episode,
                'video_file': latest_episode.video_file.url,
                'video_at': latest_episode.video_at,
                'type':movie_data['type'],
                'subtitle': movie_data['subtitle'],
                'Year': movie_data['Year'],
                'count_episode': movie_data['count_episode'],
                'image': movie_data['image']
             })
        #Phim lẻ mới nhất
        latest_updates = Episode.objects.filter(movie__type__name="Phim lẻ").values('movie').annotate(latest_update=Max('video_at'))
        movies_with_latest_update = Movie.objects.filter(id__in=[update['movie'] for update in latest_updates]).annotate(latest_update=F('episodes__video_at')).order_by('-latest_update')
        serializer = MovieSerializer(movies_with_latest_update, many=True)
        movies_single_data = serializer.data
             
             
        Movie_info = {'types':types_serializer.data,'genres':Genre_serializer.data,'contries':country_serializer.data,'years':year_serializer.data,'subs':subtitle_serializer.data}
        Movie_category = {"Hot_movies":Hot_movies_seralizer.data,'Series_movies':series_movies_data,'single_movies':movies_single_data,'rank_series':rank_series_seralizer.data,'rank_single':rank_single_seralizer.data}
        return Response({
            'Movie_info':Movie_info,
            'Movie_category':Movie_category
        })
class MovieCategory(APIView):
    serializer_class = MovieSerializer
    countries = CountryMovie.objects.all()
    years = YearMovie.objects.all()
    types = MovieType.objects.all()

    def get(self,request,name):
    
        try:          
            page_number = request.GET.get("page")
            print(page_number)
            movie_type = MovieType.objects.get(name__icontains=name)
            movie_category=Movie.objects.filter(type=movie_type)
            
            paginator = Paginator(movie_category, 5)  # Chia dữ liệu thành các trang, mỗi trang có 10 mục
            page_obj = paginator.get_page(page_number)
            print(len(list(page_obj)))
            page_obj_serializer = MovieSerializer(page_obj,many=True)
            print(paginator.num_pages)
            # Lấy tất cả các bộ phim có movie_type_id tương ứng với id của kiểu phim
            return Response({"movie_page":page_obj_serializer.data,'total_page':paginator.num_pages},status=status.HTTP_200_OK)
        except MovieType.DoesNotExist:
            # Trả về queryset rỗng nếu không tìm thấy kiểu phim
            return Movie.objects.none()
class DetailsMovie(generics.RetrieveAPIView):
       serializer_class = MovieSerializer
       def get_object(self):
            try:
                movie_name = self.kwargs['name']
                return Movie.objects.get(title_Vietnamese = movie_name)
            except Movie.DoesNotExist:
                raise Http404
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
class MovieEpisodeDetail(APIView):
    def get(self, request, type, name, episode):
        print(type)
        episode=episode.split("-")
        try:
            movie = Movie.objects.get(title_Vietnamese=name)
            episode_info = None
            print(episode)
            if type == 'Phim bộ' and episode[1].isdigit():
                episode_info = Episode.objects.get(movie__title_Vietnamese=name,title_episode=int(episode[1]))
                print(episode_info)
               
                count_episode = Episode.objects.filter(movie__title_Vietnamese = name).count()
                print("count:",count_episode)
                movie.view_count +=1
                movie.save()
                if episode_info:
            # Trả về thông tin tập phim dưới dạng JSON
                     return JsonResponse({
                    'id':episode_info.id,
                    'title_episode': episode_info.title_episode,
                    'video_file': episode_info.video_file.url,
                    'title_Vietnamese':movie.title_Vietnamese,
                    'title_English':movie.title_English,
                    'describe':movie.describe,
                    'episodes':count_episode,
                    'type':movie.type.name
                     })
            elif movie.type.name=="Phim lẻ":
                print(name)
                episode_info = Episode.objects.get(movie__title_Vietnamese=name)
                print(episode_info)
                video_url = episode_info.video_file.url
                print(episode_info.id)
                return JsonResponse({
                    'id':episode_info.id,
                    'title_Vietnamese':movie.title_Vietnamese,
                    'title_English':movie.title_English,
                    'describe':movie.describe,
                    'video_file':video_url
                })
        

        except Movie.DoesNotExist:
        # Trả về lỗi 404 nếu không tìm thấy phim
            return JsonResponse({'error': 'Movie not found'}, status=404)
class MovieHistoryAPIView(APIView):
    def post(self, request,username):
        id = request.data.get("id")
        duration_watched = request.data.get('duration_watched')
        print("user:"+username)
        print(id)
        print("duration:",duration_watched)
        movie_history = MovieHistory.objects.filter(user__username=username, episode_id=id)
        print(movie_history) 
        if not movie_history:
                user = get_object_or_404(CustomUser, username=username)
                print("user:",user)
                episode = get_object_or_404(Episode, id=id)
                print(episode)
                movie_history = MovieHistory.objects.create(user=user, episode=episode, duration_watched=duration_watched)
                return Response({'message': 'Movie history added successfully'}, status=status.HTTP_201_CREATED)
        else:
                # Nếu đã tồn tại, không thêm mới
                return Response({'message': 'Movie history already exists'}, status=status.HTTP_200_OK)
    def put(self, request,username):
        try:
            episode_id = request.data.get('id')
            duration_watched = request.data.get('duration_watched')
            
            # Kiểm tra xem user và episode_id đã tồn tại trong bảng MovieHistory chưa
            movie_history = MovieHistory.objects.filter(user__username=username, episode_id=episode_id).first()
            
            
                # Nếu đã tồn tại, cập nhật thời lượng đã xem
            movie_history.duration_watched = duration_watched
            movie_history.save()
            return Response({'message': 'Movie history updated successfully'}, status=status.HTTP_200_OK)
               
                
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def get(self, request,username):
        try:
            print(username)
            if not username:
                return Response({'error': 'Username not provided'}, status=status.HTTP_400_BAD_REQUEST)
            
            movie_history = MovieHistory.objects.filter(user__username=username)
            print(movie_history)
            serializer = MovieHistoryserilizer(movie_history, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
from django.http import JsonResponse
from django.db.models import Avg

class MovieRatingAPIView(APIView):
    def get(self,request,moviename):
        username = request.query_params.get('username')
        print(username)
        rating_movie = MovieReview.objects.filter(user__username=username,movie__title_Vietnamese=moviename).first()
        print(rating_movie)
        if rating_movie:
            Serializer_rating = MovieReviewserilizer(rating_movie)
            
            return Response(Serializer_rating.data,status=status.HTTP_200_OK)
        else:
            return Response({"message": "Chưa đánh giá."}, status=status.HTTP_200_OK)

        
    def post(self, request,moviename,):
        rating = request.data.get("rating")
        username = request.data.get("username")
        user = get_object_or_404(CustomUser, username=username)
        movie = get_object_or_404(Movie, title_Vietnamese=moviename)
        movie_rating, created = MovieReview.objects.get_or_create(user=user, movie=movie)
        movie_rating.rating = rating
        movie_rating.save()
        return Response({'data':"dfhdfhdh"}, status=status.HTTP_200_OK)


class MovieReview1(APIView):
    def get(self, request, moviename):
        print(moviename)
        total_rating = MovieReview.objects.filter(movie__title_Vietnamese=moviename).aggregate(total_rating=Avg('rating'))['total_rating']
        print(total_rating)
        
        # Kiểm tra xem total_rating có phải là None hay không
        if total_rating is None:
            total_rating = 0  # Đặt total_rating thành 0 nếu không có đánh giá nào
        
        # Biến kết quả thành một dictionary
        response_data = {'total_rating': int(total_rating)}

        # Trả về dữ liệu JSON
        return JsonResponse(response_data)
class CommentAPI(APIView):
    def get(self,request):
        try:
            titlemovie= request.query_params.get('titlemovie')
            # Tìm bộ phim dựa trên tên
            movie = Movie.objects.get(title_Vietnamese=titlemovie)
            # Lấy tất cả các bình luận của bộ phim
            comments = MovieComment.objects.filter(movie=movie)
            # Serialize dữ liệu
            serializer = CommentSerillizer(comments, many=True)
            # Trả về danh sách các bình luận của bộ phim
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            # Xử lý trường hợp không tìm thấy bộ phim
            return Response({"message": "Bộ phim không tồn tại"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Xử lý ngoại lệ nếu có lỗi xảy ra
            return Response({"message": "Đã xảy ra lỗi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    def post(self, request):
        username = request.data.get("username")
        titlemovie = request.data.get("titlemovie")
        comment = request.data.get("comment")
        print(username,"+",titlemovie,"+",comment)

        if not (username and titlemovie and comment):
            return Response({"message": "Thiếu thông tin"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUser.objects.get(username=username)
            movie = Movie.objects.get(title_Vietnamese=titlemovie)
            comment_obj, created = MovieComment.objects.get_or_create(user=user, movie=movie, comment=comment)

            if created:
                return Response({"message": "Bình luận thành công"}, status=status.HTTP_201_CREATED)
            else:
                return Response({"message": "Bình luận đã tồn tại"}, status=status.HTTP_200_OK)

        except CustomUser.DoesNotExist:
            return Response({"message": "Người dùng không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        except Movie.DoesNotExist:
            return Response({"message": "Bộ phim không tồn tại"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": "Đã xảy ra lỗi"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Create your views here.
