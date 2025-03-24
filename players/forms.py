from django import forms
from .models import Player

class PlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name']  # 登録する項目（ここでは名前だけ）

    name = forms.CharField(required=True)