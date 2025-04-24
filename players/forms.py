from django import forms
from django.forms import inlineformset_factory
from .models import Player, PlayerCommonRecord

class PlayerCommonRecordForm(forms.ModelForm):
    class Meta:
        model = PlayerCommonRecord
        fields = ('year', 'salary', 'currency')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['year'].widget.attrs.update({'style': 'width: 50px;'})
        self.fields['salary'].widget.attrs.update({'style': 'width: 100px;'})

class PlayerForm(forms.ModelForm):
    MARRIAGE_CHOICES = [
        (None, '不明'),
        (True, '既婚'),
        (False, '独身'),
    ]

    is_married = forms.TypedChoiceField(
        choices=MARRIAGE_CHOICES,
        coerce=lambda x: {
            'True': True,
            'False': False,
            'None': None,
            '': None,
        }.get(x, None),
        widget=forms.Select,
        required=False,
        label='婚姻状況',
        empty_value=None
    )

    class Meta:
        model = Player
        exclude = ['created_at']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # instanceの値（0, 1, None）を文字列に変換して初期値に設定
        if self.instance.is_married is not None:
            self.fields['is_married'].initial = str(int(self.instance.is_married))
        else:
            self.fields['is_married'].initial = ''

    def clean_is_married(self):
        value = self.cleaned_data.get('is_married')
        if value == '':
            return None
        return bool(int(value))

PlayerCommonRecordFormSet = inlineformset_factory(
    Player,
    PlayerCommonRecord,
    form=PlayerCommonRecordForm,  # ← ここで指定
    fields=('year', 'salary', 'currency'),  # 編集したいフィールド名
    extra=0, 
    can_delete=False
)