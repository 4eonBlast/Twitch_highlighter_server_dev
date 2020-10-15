from django import forms
from .models import Videos


class VidInputForm(forms.Form):
    vid_url = forms.CharField(
        max_length=128, label='Twitch replay url input', widget=forms.URLInput)
