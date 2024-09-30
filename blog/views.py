from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

# from django.utils import timezone
# from django.contrib.auth import get_user_model
# User = get_user_model()
# author = User.objects.first() 
# for i in range(30):
#         Post.objects.create(
#             title=f"Test Post {i}",
#             slug=f"test-post-{i}",
#             author=author,
#             body=f"This is a test body content for post {i}",
#             publish=timezone.now(),
#             status='PB'
#         )

def post_list(request):
    posts = Post.published.all()
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    print(page_number)
    for i in paginator:
        print (i)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        # If page_number is not an integer get the first page
        posts = paginator.page(1)
    except EmptyPage:
        # If page_number is out of range get last page of results
        posts = paginator.page(paginator.num_pages)
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        status = "PB",
        slug=post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
    )
    return render(
        request,
        'blog/post/detail.html',
        {'post': post}
    )
