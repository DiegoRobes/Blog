from django.shortcuts import render
import main.models as m


# Create your views here.
def post_page(request, slug):
    post = m.Post.objects.get(slug=slug)
    context = {'post': post}
    return render(request, 'main/post.html', context=context)
