from django import forms
import main.models as m
from django.utils.translation import gettext_lazy as _


# we are using this scrip to first import the comment model from
# models, and then use it to create a class for a form.
# we use the meta class and render the fields manually


class CommentForm(forms.ModelForm):
    class Meta:
        model = m.Comments
        fields = {'content', 'name', 'email', 'website'}
        widgets = {'content': forms.Textarea(attrs={'placeholder': 'Type your comment here...'}),
                   'name': forms.TextInput(attrs={'placeholder': 'Your name...'}),
                   'email': forms.TextInput(attrs={'placeholder': 'Your email...'}),
                   'website': forms.TextInput(attrs={'placeholder': 'Your website...'}),
                   }


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = m.Subscribe
        fields = '__all__'
        labels = {'email': _('')}
        widgets = {'email': forms.EmailInput(attrs={'placeholder': 'Enter your email here...'})}
