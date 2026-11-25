from django import forms
from django.utils import timezone

from .models import Activity


class ActivityForm(forms.ModelForm):
    """活动的 ModelForm：新增页和编辑页共用"""

    class Meta:
        model = Activity
        fields = ['title', 'start_time', 'location', 'description']
        widgets = {
            # datetime-local 需要的格式：2026-11-26T15:00
            'start_time': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ['%Y-%m-%dT%H:%M']
        self.fields['start_time'].error_messages['invalid'] = '请输入正确的开始时间。'

    def clean_start_time(self):
        """开始时间不得早于当前时间"""
        start_time = self.cleaned_data['start_time']
        # 去掉秒，避免“选当前这一分钟”被误判为过去
        now = timezone.now().replace(second=0, microsecond=0)
        if start_time < now:
            raise forms.ValidationError('开始时间不能早于当前时间。')
        return start_time
