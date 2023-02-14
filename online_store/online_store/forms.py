from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    username = forms.CharField(required=True, min_length=4, max_length=50, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'id': 'username'
    }))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'id': 'email',
        'placeholder': 'example@onlinestore.com'
    }))
    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'class': 'form-control'
    }))
    password2 = forms.CharField(label='Confirmar password', required=True, widget=forms.PasswordInput(attrs={
        'class':'form-control'
    }))

    def clean_username(self):
        username = self.cleaned_data.get('username')

        #Valida si exite el usuario ingresado por usuario
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('El usuario ya existe')
        
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')

        #Valida si exite el email ingresado por el usuario
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('El email ya existe')
        
        return email

    def clean(self):#Valida campo o atributos que dependan unos de otros
        cleaned_data = super().clean()

        if cleaned_data.get('password2') != cleaned_data.get('password'):
            self.add_error('password2', 'Los password no coinciden')

    def save(self):
        return User.objects.create_user(
            self.cleaned_data.get('username'),
            self.cleaned_data.get('email'),
            self.cleaned_data.get('password'),
        )