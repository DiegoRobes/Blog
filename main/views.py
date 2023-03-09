from django.shortcuts import render
import main.models as m


# Create your views here.

def home(request):
    all_posts = m.Post.objects.all()
    context = {"posts": all_posts}
    return render(request, 'main/index.html', context=context)


def post_page(request, slug):
    post = m.Post.objects.get(slug=slug)
    if post.count_view is None:
        post.count_view = 1
    else:
        post.count_view += 1
    post.save()
    context = {'post': post}
    print(post.image.url)
    return render(request, 'main/post.html', context=context)


