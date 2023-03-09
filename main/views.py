from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import main.models as m
import main.forms as f


# before rendering the view, we fetch all the posts from the db using the model
# we put them in the context dict, and send them to be placed in a loop
def home(request):
    all_posts = m.Post.objects.all()
    context = {"posts": all_posts}
    return render(request, 'main/index.html', context=context)


# we take the slug from the post we click asa an argument, check the html,
# and use it to filter the corresponding post from the db. we also do some basic
# operations to increase the views counter.
# finally, we import and pass the comment form to be rendered in the template

def post_page(request, slug):
    post = m.Post.objects.get(slug=slug)
    comments = m.Comments.objects.filter(post=post, parent=None)
    form = f.CommentForm()
    # in this block we capture the info from the form, but we dont actually save it into the db
    # the reason is that from the form we get some content, the model asks for more fields
    # like post, but we don't get it from the form, so we solve it before doing the commit to the db
    # first we intercept the request, we find the post to which the comment belongs by using a hidden input containing
    # the post id in the form, we assign that post to the comment, and finally we commit to the db. yeah, convoluted.
    if request.POST:
        comment_form = f.CommentForm(request.POST)
        if comment_form.is_valid():
            parent_object = None
            # catching, mapping and saving replies to comments:
            # check if the form has the hidden arg parent, meaning, it is a reply.
            if request.POST.get('parent'):
                # if so, catch it and use it to fetch the comment with the same id
                parent = request.POST.get('parent')
                parent_object = m.Comments.objects.get(id=parent)
                # if you find a comment with the same id, it means you got the parent for the reply
                if parent_object:
                    # if there is a parent, pre-save the submitted form. no commit yet
                    comment_reply = comment_form.save(commit=False)
                    # make sure to include the id of the parent object, or parent comment, in the package
                    # before committing th reply
                    comment_reply.parent = parent_object
                    # also, map the relpy to its comment, sorta like its grandparent
                    comment_reply.post = post
                    # only when all that info is in the package, we commit into the db
                    comment_reply.save()
                    return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

            else:
                to_save = comment_form.save(commit=False)
                post_id = request.POST.get('post_id')
                post = m.Post.objects.get(id=post_id)
                to_save.post = post
                to_save.save()
                # this next method to redirect the user is made, so they can refresh the page without posting a comment
                # multiple times. this happens bc when we redirect the user with the Http method, the request from
                # the form gets deactivated
                return HttpResponseRedirect(reverse('post_page', kwargs={'slug': slug}))

    if post.count_view is None:
        post.count_view = 1
    else:
        post.count_view += 1
    post.save()
    context = {'post': post, 'form': form, 'comments': comments}

    return render(request, 'main/post.html', context=context)
