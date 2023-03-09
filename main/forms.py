from django import forms
from main.models import Comments


# we are using this scrip to first import the comment model from
# models, and then use it to create a class for a form.
# we use the meta class and render the fields manually


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = {'content', 'name', 'email',  'website'}
        widgets = {'content': forms.Textarea(attrs={'placeholder': 'Type your comment here...'}),
                   'name': forms.TextInput(attrs={'placeholder': 'Your name...'}),
                   'email': forms.TextInput(attrs={'placeholder': 'Your email...'}),
                   'website': forms.TextInput(attrs={'placeholder': 'Your website...'}),
                   }
