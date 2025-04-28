from django.contrib import admin
from django import forms
from django.forms import HiddenInput
from django.db import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.forms import CheckboxSelectMultiple
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email', 'username','password', 'is_staff', 'is_admin', 'date_joined')
    search_fields = ('email', 'username')
    readonly_fields = ('date_joined', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(CustomUser, CustomUserAdmin)
# Đăng ký các mô hình vào trang admin
@admin.register(MovieType)
class MovieTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(GenreMovie)
class GenreMovieAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(YearMovie)
class YearMovieAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(Director)
class DirectorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(CountryMovie)
class CountryMovieAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(Subtitle)
class SubtitleAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ['name']

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    def get_actors(self, obj):
        return ", ".join([actor.name for actor in obj.actor.all()])
    get_actors.short_description = 'actor'

    list_display = ('id','title_Vietnamese', 'title_English', 'type', 'Year', 'country', 'get_actors', 'subtitle', 'director', 'describe', 'count_episode', 'create_at', 'view_count', 'image')

    search_fields = ['title_Vietnamese', 'title_English', 'describe']
    list_filter = ('type', 'Year', 'country', 'subtitle', 'director', 'genres')
    formfield_overrides = {
        models.ManyToManyField: {'widget': CheckboxSelectMultiple},
    }
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == "genres":
            kwargs["widget"] = CheckboxSelectMultiple
        else:
            kwargs["widget"] = None
        return super().formfield_for_manytomany(db_field, request, **kwargs)
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        try:
            if obj and obj.type.name == "Phim lẻ":
                form.base_fields['count_episode'].widget = forms.HiddenInput()
        except KeyError:
            pass
        return form
class EpisodeMovieForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EpisodeMovieForm, self).__init__(*args, **kwargs)
        self.fields['movie'].queryset = Movie.objects.filter(type__name='Phim lẻ', episodes__isnull=False)
        if not self.instance.pk:
            self.fields['movie'].queryset = Movie.objects.exclude(type__name='Phim lẻ', episodes__isnull=False)
            
    class Meta:
        model = Episode
        fields = ['movie','title_episode', 'video_file']
    def clean(self):
        cleaned_data = super().clean()
        title_episode = cleaned_data.get('title_episode')
        movie = cleaned_data.get('movie')
        all_movie_titles = Episode.objects.values_list('movie__title_Vietnamese', flat=True).distinct()
        print(movie.type.name)
        title_episode = cleaned_data.get('title_episode')
        if movie.type.name == "Phim bộ":
            if title_episode and movie and title_episode > movie.count_episode or title_episode<=0:
                raise forms.ValidationError("Số tập mới vượt quá số tập hiện có của bộ phim hoặc tập mới  nhở hơn 0")
        else:
            if movie.title_Vietnamese in all_movie_titles and movie.pk is None:

                    raise forms.ValidationError("tên phim đã xuất hiện trong model hoặc tâp lớn hơn hoặc bằng không  ")

        return cleaned_data

class EpisodeMovieAdmin(admin.ModelAdmin):
   
        
    form = EpisodeMovieForm
    list_display = ('id','movie', 'title_episode', 'video_file', 'video_at')
    search_fields = ['movie__title_Vietnamese', 'movie__title_English']
    list_filter = ('movie__title_Vietnamese', 'movie__title_English')
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.movie.type.name == "Phim lẻ":
            form.base_fields['title_episode'].widget = HiddenInput()
        return form
admin.site.register(Episode,EpisodeMovieAdmin) 
@admin.register(MovieHistory)
class WatchMovieAdmin(admin.ModelAdmin):
    list_display = ('user', 'episode', 'duration_watched', 'watched_at')
    search_fields = ['user__username', 'episode__id']
    list_filter = ('user', 'episode')

@admin.register(MovieReview)
class MovieReviewAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'rating', 'created_at')
    search_fields = ['movie__title_Vietnamese', 'movie__title_English', 'user__username']
    list_filter = ('movie', 'user', 'rating')

# Đăng ký mô hình MovieComment
@admin.register(MovieComment)
class MovieCommentAdmin(admin.ModelAdmin):
    list_display = ('movie', 'user', 'comment', 'created_at')
    search_fields = ['movie__title_Vietnamese', 'user__username']  # Tìm kiếm theo tiêu đề phim và tên người dùng
    list_filter = ['created_at']  # Bộ lọc theo thời điểm tạo
@admin.register(Customtoken)
class CustomTokenadmin(admin.ModelAdmin):
    
    list_display = ('user', 'token')
    search_fields = ['user']  # Tìm kiếm theo tiêu đề phim và tên người dùng
    list_filter = ['user'] 
from django.contrib import admin
from django.contrib.auth.models import Group, User


# Register your models here.

# Register your models here.
