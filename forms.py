from django import forms
from review.models import Review


class ReviewForm(forms.ModelForm):

    class Meta:

        CHOICES = [
            (0, '☆☆☆☆☆'),
            (1, '★☆☆☆☆'),
            (2, '★★☆☆☆'),
            (3, '★★★☆☆'),
            (4, '★★★★☆'),
            (5, '★★★★★')
        ]

        model = Review  # 사용할 모델
        fields = ['movie', 'title', 'star', 'content']  # ReviewForm에서 사용할 Review 모델의 속성
        widgets = {
            'movie': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'star': forms.Select(attrs={'class': 'form-select'}, choices=CHOICES),
        }
        labels = {
            'movie': '영화명',
            'title': '제목',
            'content': '내용',
            'star': '별점',
        }

    def __init__(self, *args, **kwargs):
        kwargs.setdefault("label_suffix", "")
        super(ReviewForm, self).__init__(*args, **kwargs)

