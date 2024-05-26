from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
# Create your models here.

now = timezone.now()

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.

now = timezone.now()

# Create your models here.

class Quizz(models.Model):
    title = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    # user_take = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usertaker')
    # deadline = models.DateField()
    # time_limit = models.IntegerField()
    # takers = models.IntegerField(blank=True)
    
class Questions(models.Model):
    name = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    question = models.TextField(blank=True)
    answer = models.TextField()
    
class Lesson(models.Model):
    title = models.TextField()
    description = models.TextField()
    file = models.FileField(upload_to='files', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'pdf', 'word', 'ppt', 'excel'])],)
    upload_date = models.DateTimeField(default=now)
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    

class Score(models.Model):
    score = models.IntegerField()
    taker = models.ForeignKey(User, on_delete=models.CASCADE)
    quiz = models.ForeignKey(Quizz, on_delete=models.CASCADE)
    
    
    
class Forum(models.Model):
    title = models.CharField(max_length=10000)
    file = models.FileField(
        upload_to='media/announcement',
        validators=[ 
            FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'pdf', 'word', 'ppt', 'xlsx', 'csv', 'gif'])
        ],
        null=True,  # Allow null values
        blank=True  # Also allow empty values (in forms)
    )
    upload_date = models.DateTimeField(default=now)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Comments(models.Model):
    post = models.ForeignKey(Forum, on_delete=models.CASCADE)
    commentors = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    comment_date = models.DateTimeField(default=now)
    
class Announcement(models.Model):
    title = models.CharField(max_length=10000)
    # file = models.FileField(upload_to='media/event', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpeg', 'jpg', 'pdf', 'word', 'ppt', 'xlsx', 'csv', 'gif'])],)
    upload_date = models.DateTimeField(default=now)
    description = models.TextField()
    uploader = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.IntegerField()