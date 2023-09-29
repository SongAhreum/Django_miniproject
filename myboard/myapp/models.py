from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_post')
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_post')
    def __str__(self):
        return self.title # 게시물의 제목을 문자열로 반환


# 댓글
class Comment(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='author_comment')
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    voter = models.ManyToManyField(User, related_name='voter_comment')
    
    def __str__(self):
        return self.content
    
'''
역방향 참조(user와 연결된 필드가 1개일경우(author)) 
user = User.objects.get(id=특정_사용자의_ID)
posts_written_by_user = user.post_set.all()
user = User.objects.get(id=특정_사용자의_ID)
comments_written_by_user = user.comment_set.all()

related_name를 사용한 역방향참조
voter필드를 추가한후 user와 연결된 필드가 2개 user.모델명_set.all()로 가져오는데 이렇게 가져온내용이 author,voter의 구별이안되서 에러남
user = User.objects.get(id=특정_사용자의_ID)
posts_written_by_user = user.author_post.all()
user = User.objects.get(id=특정_사용자의_ID)
comments_written_by_user = user.author_comment.all()
'''