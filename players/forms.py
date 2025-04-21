from django import forms
from django.forms import inlineformset_factory
from .models import Player, PlayerCommonRecord

class PlayerForm(forms.ModelForm):
    MARRIAGE_CHOICES = [
        ('', '不明'),
        ('married', '既婚'),
        ('single', '独身'),
    ]

    is_married = forms.ChoiceField(
        choices=MARRIAGE_CHOICES,
        widget=forms.Select,
        required=False,
        label='婚姻状況'
    )

    class Meta:
        model = Player
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # 現在の選手の婚姻状況をフォームに反映
        if self.instance.is_married is not None:
            self.fields['is_married'].initial = 'married' if self.instance.is_married else 'single'

PlayerCommonRecordFormSet = inlineformset_factory(
    Player,
    PlayerCommonRecord,
    fields=('year', 'salary', 'currency'),  # 編集したいフィールド名
    extra=0, 
    can_delete=False
)