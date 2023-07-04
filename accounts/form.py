from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import  MyUser
 
 
class RegisterForm(UserCreationForm):
 
    # 入力を必須にするため、required=Trueで上書き
    username = forms.CharField(required=True, label="ユーザID")
    nickname = forms.CharField(required=True, label="ニックネーム")
    
    class Meta:
        model = MyUser
    
        fields = (
        "nickname","username", "password1", "password2"
        )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
        self.fields['nickname'].widget.attrs['class'] = 'form-control'
        self.fields['nickname'].widget.attrs['placeholder'] = 'お名前'
    
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'ユーザID'
    
        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'パスワード'
    
        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'パスワード（確認）'

class SettingUserForm(forms.ModelForm):
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type":"date"}),
        label="生年月日",
        required=False
    )

    class Meta:
        model = MyUser
    
        fields = (
            "nickname","date_of_birth","introduction"
        )