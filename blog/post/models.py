from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone

User = get_user_model()


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=250,
                            unique_for_date='publish')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                              choices=STATUS_CHOICES,
                              default='draft')
    image = models.ImageField(upload_to='posts',
                              null=True,
                              blank=True)

    class Meta:
        ordering = ('-publish', )

    def __str__(self):
        return self.title

    def avr_rating(self):
        summ = 0
        ratings = Rating.objects.filter(post=self)
        for rating in ratings:
            summ += rating.rate
        if len(ratings) > 0:
            return round(summ / len(ratings), 2)
        else:
            return 'No rate'


class Comment(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='comments')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.post} --> {self.user}'


class Rating(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    rate = models.DecimalField(max_digits=3,
                               decimal_places=2,
                               validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        unique_together = (('user', 'post'), )
        index_together = (('user', 'post'), )


class Like(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='likes')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='likes')
    is_liked = models.BooleanField(default=False)


class Favourite(models.Model):
    post = models.ForeignKey(Post,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='favourites')
    is_favourite = models.BooleanField(default=False)
