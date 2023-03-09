from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100, default="")
    slug = models.SlugField(max_length=200, unique=True)

    # this one creates a slug for any new entry on the tag models
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slugify(self.name)
        return super(Tag, self).save(self, *args, **kwargs)

    def __str__(self):
        return self.name


# in this one we are going to create a manytomany relationship,
# using the model TAG as the key.
# then we create a field to make a count of times the post is
# opened
class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    last_updated = models.DateField(auto_now=True)
    slug = models.SlugField(max_length=20, unique=True)
    image = models.ImageField(null=True, blank=True, upload_to='images/')
    tags = models.ManyToManyField(Tag, blank=True, related_name='post')
    count_view = models.IntegerField(null=True, blank=True)


# model to store comments in the db, and the link them to a specific
# post using a foreign key. in the last field we are going to check
# the user who makes the comment by using the USER model from django
# more on that later
class Comments(models.Model):
    content = models.TextField()
    date = models.DateField(auto_now=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    website = models.CharField(max_length=500)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

