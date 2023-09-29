from django import forms
from myapp.models import Post,Comment

class PostForm(forms.ModelForm):
  class Meta:
    model = Post
    fields = ['title','content']
    # widgets = {
    #         'title': forms.TextInput(attrs={'class': 'form-control'}),
    #         'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
    #     }
    labels = {
            'title': '제목',
            'content': '내용',
        }  
class CommentForm(forms.ModelForm):
  class Meta:
    model = Comment
    fields = ['content']
    labels = {
            'content': '댓글 내용',
        }      