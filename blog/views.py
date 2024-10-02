from django.shortcuts import render
from django.shortcuts import get_object_or_404, render
from .models import Post
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect
from django.views.decorators.http import require_POST
from .forms import CommentForm, EmailPostForm, SearchForm
from django.core.mail import send_mail
from decouple import config
from taggit.models import Tag
from django.contrib.postgres.search import TrigramSimilarity

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

def post_list(request, tag_slug = None):
    posts = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        post_list = post_list.filter(tags__in=[tag])
    paginator = Paginator(posts, 3)
    page_number = request.GET.get('page', 1)
    for i in paginator:
        print (i)
    try:
        posts = paginator.page(page_number)
    except PageNotAnInteger:
        posts = paginator.page(1)
        return redirect(f"{request.path}?page=1")
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
        return redirect(f"{request.path}?page={paginator.num_pages}")
    return render(
        request,
        'blog/post/list.html',
        {'posts': posts}
    )


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post,
        publish__year=year,
        publish__month=month,
        publish__day=day,
        slug=post,
    )
    comments = post.comments.filter(active=True)
    form = CommentForm()
    return render(
        request,
        'blog/post/detail.html',
        {
            'post': post,
            'comments': comments,
            'form': form
        },
    )

@require_POST
def post_comment(request, post_id):
    post = get_object_or_404(
        Post,
        id=post_id,
        status="PB"
    )
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the post to the comment
        comment.post = post
        # Save the comment to the database
        comment.save()
    return render(
        request,
        'blog/post/comment.html',
        {
            'post': post,
            'form': form,
            'comment': comment
        },
    )

def post_share(request, post_id):                                                       

    post = get_object_or_404(
        Post,
        id=post_id,
        status="PB"
    )
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )
            print(post_url)
            subject = (
                f"Sheriff recommends you read {post.title}"
            )
            message = (
                f"Read {post.title} at {post_url}\n\n"
                f"{cd['name']}'s comments: {cd['comments']}"
            )
            send_mail(
                subject=subject,
                message=message,
                from_email=config('DEFAULT_FROM_EMAIL'),
                recipient_list=[cd['email']],
            )
            sent = True
    else:
        form = EmailPostForm()
    return render(
        request,
         'blog/post/share.html',
        {
            'post': post,
            'form': form,
            'sent': sent
        },
    )


def post_search(request):
    form = SearchForm()
    query = None
    results = []

    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = (
                Post.published.annotate(
                    similarity=TrigramSimilarity('title', query),
                )
                .filter(similarity__gt=0.1)
                .order_by('-similarity')
            )

    return render(
        request,
        'blog/post/search.html',
        {
            'form': form,
            'query': query,
            'results': results
        },
    )
