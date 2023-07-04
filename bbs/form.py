from django import forms
from bbs.models import Post
 

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
    
        fields = (
        'text',
        )
        labels = {
        "text":"投稿する"
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['text'].widget.attrs['class'] = 'form-control'
        self.fields['text'].widget.attrs['id'] = 'post_text'
        self.fields['text'].widget.attrs['placeholder'] = '内容'
        self.fields['text'].widget.attrs['rows'] = 3