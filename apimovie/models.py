from django.db import models
from django.db import models
from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length = 20)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return f'{self.email}-{self.username}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
class Customtoken(models.Model):
      user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
      token = models.CharField(max_length=255,null=False)
      def __str__(self):
           return f'{self.user}-{self.token}'
class MovieType(models.Model):
      name = models.CharField(max_length=50,unique=True)

      def __str__(self):
            return self.name
class GenreMovie(models.Model):
      name = models.CharField(max_length=50,unique=True)
      def __str__(self):
            return self.name


class YearMovie(models.Model):
      name = models.IntegerField(unique=True)
      def __str__(self):
            return str(self.name)
class Director(models.Model):
      name = models.CharField(max_length=40,unique=True)
      def __str__(self):
            return self.name
class Actor(models.Model):
      name = models.CharField(max_length=40,unique=True)
      def __str__(self):
            return self.name
      
class CountryMovie(models.Model):
      name = models.CharField(max_length=40,unique=True)
      def __str__(self):
            return self.name 
class Subtitle(models.Model):
      name = models.CharField(max_length=40,unique=True)
      def __str__(self):
            return self.name
class Movie(models.Model):
      title_Vietnamese = models.CharField(max_length=50,unique=True)
      title_English = models.CharField(max_length=50)
      type = models.ForeignKey(MovieType,on_delete=models.CASCADE,related_name='movie')
      genres = models.ManyToManyField(GenreMovie)
      Year = models.ForeignKey(YearMovie,on_delete=models.CASCADE,related_name='movie')
      country = models.ForeignKey(CountryMovie,on_delete=models.CASCADE,related_name='movie')
      subtitle = models.ForeignKey(Subtitle,on_delete=models.CASCADE,related_name='movie')
      actor = models.ManyToManyField(Actor,blank=True,null=True,related_name='movie')
      director = models.ForeignKey(Director,on_delete=models.CASCADE,related_name='movie')
      describe = models.TextField()
      duration = models.CharField(max_length=20)
      count_episode = models.IntegerField(default=1)
      image = models.ImageField(upload_to="images")
      create_at = models.DateField(auto_now_add=True)
      view_count = models.IntegerField(default=0)
      def __str__(self):
            
           return f'{self.title_Vietnamese}-{self.title_English}-{self.type.name}'
class Episode(models.Model):
      id = models.AutoField(primary_key=True) 
      movie = models.ForeignKey(Movie,on_delete=models.CASCADE,related_name="episodes")
      title_episode = models.IntegerField(default=1,blank=True)
      video_file = models.FileField(upload_to="videos")
      video_at = models.DateTimeField(auto_now_add=True)
      def __str__(self):
              return f'{self.movie.title_Vietnamese}-{self.title_episode}'
      
class MovieHistory(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.Case)
    episode = models.ForeignKey(Episode,on_delete=models.Case)
    duration_watched = models.FloatField(null=True,default=0, help_text="Thời lượng xem của người dùng cho tập phim (đơn vị: giây)")
    watched_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} - {self.episode} - {self.duration_watched} giây"
class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    rating = models.IntegerField(default=0) 
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('movie', 'user')  # Đảm bảo mỗi người dùng chỉ có một đánh giá cho mỗi bộ phim

    def __str__(self):
        return f"{self.movie.title_Vietnamese} - {self.user.username}"
         
class MovieComment(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE) 
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return f"{self.movie.title_Vietnamese} - {self.user.username}"
    
# Create your models here.

