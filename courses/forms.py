from django import forms
from core.models import Comment

# Form to save user comment on an post
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment

        fields = ['content']

        widgets = {
            'content': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Give your opinion...'
            }),
        }

class ReplyCommentForm(forms.ModelForm):
    
    class Meta:
        model = Comment

        fields = ['content']

        widgets = {
            'context': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Reply your thoughts...'
            }),
        }
        