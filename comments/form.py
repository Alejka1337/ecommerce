from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    message = forms.CharField(
        min_length=5,
        max_length=600,
        widget=forms.Textarea(
            attrs={"rows": 3, "placeholder": "Комментарий..."},
        ),
        label="",
    )

    name = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "placeholder": "Имя"}, ),
                           label="")

    email = forms.CharField(widget=forms.Textarea(attrs={"rows": 1, "placeholder": "Email"}, ),
                            label="")

    class Meta:
        model = Comment
        fields = ['name', 'email', 'message']

