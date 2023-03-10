from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
import main.models as m
import main.forms as f


# before rendering the view, we fetch all the posts from the db using the model
# we put them in the context dict, and send them to be placed in a loop
def home(request):
    all_posts = m.Post.objects.all()

    # to get a featured post, first add the featured field to the model,
    # then query the posts by that field, get only the first one, and pass
    # it to the context dict to be rendered in the view
    # if no post is marked as featured, then nothing happens, and the context get a value NONE
    feature_post = None
    try:
        feature_post = m.Post.objects.filter(featured=True)[0]
    except IndexError:
        pass

    # creating the subscribe form in the index.
    # if the request is post, catch the form in the post method
    # if valid, save the info passed into the db,
    # set message from NONE to success, pass the message into the context to be rendered
    # reset the form so it is emptied and send the user back to the page
    subscribe_form = f.SubscribeForm()
    message = None
    if request.POST:
        subscribe_form = f.SubscribeForm(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            message = 'Successfully subscribed'
            subscribe_form = f.SubscribeForm()

    # this two queries are done using django query operations to get the 3 most popular and recent posts.
    # order_by is executed by passing the name of the field to query, but we use a - right at the start, to make sure
    # they are presented in descending order. the last part is a simple slice, from 0 to 3, to only get the first 3
    # results. an identical thing is done to the last updated field.
    # finally we pass this queries into the context dict to be rendered in the view
    popular = m.Post.objects.all().order_by('-count_view')[0:3]
    recent = m.Post.objects.all().order_by('-date')[0:3]
    context = {"posts": all_posts, 'popular': popular, 'recent': recent,
               'subscribe_form': subscribe_form, 'message': message, 'featured': feature_post}
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

    return render(request, 'main/pages/post.html', context=context)


# for this one we create a page where you can see posts with the same tags
def tag_page(request, slug):
    # first get the tag using the slug as the key
    tag = m.Tag.objects.filter(slug=slug)[0]
    # get all posts with the same tage
    posts_w_tag = m.Post.objects.filter(tags=tag).order_by('-count_view')

    # send both queries into the context dic to be rendered dynamically
    context = {'name': slug, 'tag': tag, 'posts': posts_w_tag}
    return render(request, 'main/pages/tag.html', context=context)


# for this one we create a page where you can see posts with the same tags
def author_page(request, slug):
    # first get the tag using the slug as the key
    profile = m.Profile.objects.filter(slug=slug)[0]
    # get all posts with the same tage
    posts_by_auth = m.Post.objects.filter(author=profile.user).order_by('-count_view')[0:3]

    # send both queries into the context dic to be rendered dynamically
    context = {'author': profile,  'posts': posts_by_auth}
    return render(request, 'main/pages/author.html', context=context)
