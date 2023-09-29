from django.shortcuts import HttpResponse, render,get_object_or_404,redirect, resolve_url
from django.http import HttpResponseNotAllowed
from django.utils import timezone
from django.views.generic import ListView
from .models import Post,Comment
from .forms import PostForm,CommentForm
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.


# class PostListView(ListView):
#     model = Post
#     template_name = 'myapp/post_list.html'
#     context_object_name = 'post_list'
#     ordering = ['-created_at']
#     paginate_by = 10

#     def get_queryset(self):
#         return Post.objects.order_by('-created_at') 

def index(request):
    page = request.GET.get('page', '1') 
    post_list = Post.objects.order_by('-created_at')
    paginator = Paginator(post_list, 10) #페이지당 10개씩
    page_obj = paginator.get_page(page)
    context = {'post_list':page_obj}
    return render(request,'myapp/post_list.html',context)

def detail(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    context = {'post':post}
    return render(request,'myapp/post_detail.html',context) 

'''
게시글 작성버튼을 누르면 get으로 request전달
form = PostForm()생성후, return render(request,'myapp/post_form.html',{'form':form})
post_form에서 form형식에맞는 내용작성 후 post로 request 재 전달(post_form의 form태그 action지정 안함,post_form.html은 create,modify등 form에해당하는 작업수행할 시에 공통으로 사용할 것이기 때문)
유효성검사이후 save(),redirect
'''
@login_required(login_url='common:login')
def post_create(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST) 
        if form.is_valid():
            post = form.save(commit=False) # 임시 저장
            post.author = request.user
            # post.created_at = timezone.now() --auto_now_add=True설정해서 괜찮을듯
            post.save() #저장
            return redirect('myapp:index')
    else:
        form = PostForm()    
    context ={'form':form}       
    #is_valid()가 폼 유효성 검사를 수행하고, 만약 폼이 유효하지 않은 경우 해당 폼 객체에 오류 메시지를 저장     
    return render(request,'myapp/post_form.html',{'form':form})

'''
게시글수정버튼 -> get으로 request전달 -> form = PostForm(instance=post) -> request와form을 myapp/post_form.html로 전달
post_form.html에서 post로 request 재 전달 -> PostForm(request.POST,instance=post) -> 유효성검사 -> save(),redirect
post_form.html form태그 action지정안함(view에 여러함수에서 재사용하려고)
'''
@login_required(login_url='common:login')
def post_modify(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    if request.user != post.author:
        messages.error(request,'수정권한이 없습니다.') #필드오류:입력값이 필드형식과불일치시/넌필드오류: 필드오류이외 발생.
        return redirect('myapp:detail',post_id=post.id)
    if request.method == "POST":
        form = PostForm(request.POST,instance=post) #해당인스턴스기준으로 생성하지만, request.POST로 덮어쓰기
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = timezone.now() #수정시간
            post.save()
            return redirect('myapp:detail',post_id=post.id)
    else:
        form = PostForm(instance=post) 
    context = {'form':form}              
    return render(request,'myapp/post_form.html',context)

@login_required(login_url='common:login')
def post_delete(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    if request.user != post.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('myapp:detail', post_id=post.id)
    post.delete() #model에서 해당데이터객체 삭제 함수
    return redirect('myapp:index')

@login_required(login_url='common:login')
def comment_create(request,post_id):
    post = get_object_or_404(Post,pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post # 게시물 정보를 코멘트에 할당
            comment.author = request.user # author 속성에 로그인 계정 저장
            comment.save()
            # return redirect('myapp:detail',post_id=post.id)
            return redirect('{}#comment_{}'.format(resolve_url('myapp:detail',post_id=post.id),comment.id))
            #/myapp/detail/123#comment_4와같이 리다이렉트 :해시 프래그먼트 
    else:
        # @login_required(login_url='common:login')로 로그인페이지를 거쳐 해당 함수에 들어오면 get으로 접근하는거라 수정(input hidden타입, 다음로그인수행후 다음 url지정)
        # return HttpResponseNotAllowed('Only POST is possible.') #comment는 post로만 요청될것이기 때문에 오류발생시킴
        form = CommentForm()
    # post.comment_set.create(content=request.POST.get('content'))
    context = {'post':post,'form':form}
    return render(request,'myapp/post_detail.html',context)#form.is_valid()실패한경우 form에 에러메세지를 담아 리턴
    # comment = Comment(post=post,content=request.POST.get('content'))
    # comment.save()
    # return redirect('myapp:detail',post_id=post.id)

'''
comment수정을누르면 get으로 request전달
myapp/comment_form.html 에서 form작성후 post로 request 재전달(그래서 comment_form.html에서 form태그 action지정 안함 )
post로 전달된 request의 유효성체크 후 save(), redirect
'''    
@login_required(login_url='common:login')
def comment_modify(request,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '수정권한이 없습니다')
        return redirect('myapp:detail', post_id=comment.post.id)
    if request.method =="POST":
        form = CommentForm(request.POST,instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.updated_at = timezone.now()
            comment.save()
            # return redirect('myapp:detail',post_id = comment.post.id)
            return redirect('{}#comment_{}'.format(resolve_url('myapp:detail',post_id=comment.post.id),comment.id))
    else:
        form = CommentForm(instance=comment)
    context = {'comment':comment,'form':form}
    return render(request,'myapp/comment_form.html',context)  
    
@login_required(login_url='common:login')
def comment_delete(request,comment_id):      
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '삭제권한이 없습니다')
    else:
        comment.delete()
    return redirect('myapp:detail',post_id=comment.post.id)  

@login_required(login_url='common:login')
def post_vote(request,post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user == post.author:
        messages.error(request, '내가 작성한 글은 추천할 수 없습니다')
    else:
        post.voter.add(request.user)
    return redirect('myapp:detail', post_id=post.id)        

@login_required(login_url='common:login')
def comment_vote(request,comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user == comment.author:
        messages.error(request, '내가 작성한 글은 추천할 수 없습니다')
    else:
        comment.voter.add(request.user)
    return redirect('{}#comment_{}'.format(resolve_url('myapp:detail',post_id=comment.post.id),comment.id))        