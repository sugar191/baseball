from django import forms
from django.forms import inlineformset_factory
from players.models import Player
from records.models import PlayerCommonRecord
from games.models import Game
from teams.models import Team, TeamSeason
from transfers.models import Transfer


class PlayerForm(forms.ModelForm):
    MARRIAGE_CHOICES = [
        (None, "不明"),
        (True, "既婚"),
        (False, "独身"),
    ]

    favorite_team = forms.ModelChoiceField(
        label="ファン球団",
        empty_label="選択してください",
        queryset=Team.objects.filter(is_select=True),  # ここでquerysetを指定
        required=False,
    )

    is_married = forms.TypedChoiceField(
        choices=MARRIAGE_CHOICES,
        coerce=lambda x: {
            "True": True,
            "1": True,
            "False": False,
            "0": False,
            "None": None,
            "": None,
        }.get(x, None),
        widget=forms.Select,
        required=False,
        label="婚姻状況",
        empty_value=None,
    )

    class Meta:
        model = Player
        exclude = ["created_at"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # すでにModelChoiceFieldでquerysetを設定しているので、ここで再設定する必要はありません
        # もし別の動的な処理が必要ならば、__init__内で変更することもできます。
        if self.instance.is_married is not None:
            self.fields["is_married"].initial = str(int(self.instance.is_married))
        else:
            self.fields["is_married"].initial = ""


class PlayerCommonRecordForm(forms.ModelForm):
    class Meta:
        model = PlayerCommonRecord
        fields = ("season", "salary", "currency")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["salary"].widget.attrs.update({"style": "width: 100px;"})


PlayerCommonRecordFormSet = inlineformset_factory(
    Player,
    PlayerCommonRecord,
    form=PlayerCommonRecordForm,  # ← ここで指定
    fields=("season", "salary", "currency"),  # 編集したいフィールド名
    extra=0,
    can_delete=False,
)


class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = "__all__"  # 全項目編集可能にする場合


class TransferForm(forms.ModelForm):
    class Meta:
        model = Transfer
        fields = "__all__"  # 全項目編集可能にする場合


class TeamSeasonEditForm(forms.ModelForm):
    class Meta:
        model = TeamSeason
        fields = ["sort_order", "win", "lose", "draw"]
