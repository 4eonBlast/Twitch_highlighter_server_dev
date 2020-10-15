from django import forms

from .models import User


class RegisterForm (forms.ModelForm):

    # widget = HTML 입력요소
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['email', 'username']

    def clean_confirm_password(self):
        cd = self.cleaned_data
        if cd['password'] != cd['confirm_password']:
            raise forms.ValidationError('비밀번호가 일치하지 않습니다')

        return cd['confirm_password']
