from django import forms
from final.models import diary_image

class DiaryImageForm(forms.ModelForm):
    class Meta:
        model = diary_image  # 사용할 모델
        fields = ['subject', 'content', 'username']
        labels = {
            'subject': '작성일자',
            'content': '일기',
            'username': '작성자',
        }