from django import forms

from .models import Comment, Post


class PostForm(forms.ModelForm):
    '''Form to create a new post.'''
    class Meta():
        model = Post
        fields = [
            'text',
            'group',
            'image',
        ]


class CommentForm(forms.ModelForm):
    '''Form to create a new comment.'''
    class Meta():
        model = Comment
        fields = [
            'text',
        ]
        widgets = {
            'text': forms.Textarea(
                attrs={
                    'rows': 5,
                },
            )
        }
