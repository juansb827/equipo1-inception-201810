# -*- coding: utf-8 -*-

from cloudinary.forms import CloudinaryJsFileField
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from models import Category, Profile


class UserForm(ModelForm):
    username = forms.CharField(max_length=50, label="Usuario")
    first_name = forms.CharField(max_length=30, label="Nombres")
    last_name = forms.CharField(max_length=30, label="Apellidos")
    email = forms.EmailField(label="Correo electrónico")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar Contraseña")
    country = forms.CharField(max_length=30, label="Pais")
    city = forms.CharField(max_length=30, label="Ciudad")
    address = forms.CharField(max_length=50, label="Direccion")
    image = CloudinaryJsFileField(label="Foto", required=False, options={
        'allowed_formats': ['jpg', 'png']
    })

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'password', 'password2', 'address', 'country', 'city',
                  'preferences', 'image']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields["preferences"].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["preferences"].help_text = ""
        self.fields["preferences"].queryset = Category.objects.all()
        self.fields["preferences"].label = "Preferencias"
        self.fields["preferences"].required = False
        self.fields["city"].label = "Ciudad"

    def clean_preferences(self):
        preferences = self.cleaned_data['preferences']
        if len(preferences) < 1:
            raise forms.ValidationError('Debe seleccionar almenos una preferencia.')
        return preferences

    def clean_image(self):
        image = self.cleaned_data['image']
        if image is None:
            raise forms.ValidationError('Debe seleccionar una imagen')
        return image

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError('El usuario ya se encuentra en uso.')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError('El email ya se encuentra en uso.')
        return email

    def clean_password2(self):
        password = self.cleaned_data['password']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return password


class EditUserForm(UserForm):
    old_password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña Anterior")
    password = forms.CharField(widget=forms.PasswordInput(), label="Nueva Contraseña (Opcional)", required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar Nueva Contraseña (Opcional)",
                                required=False)

    class Meta:
        model = Profile
        fields = ['username', 'first_name', 'last_name', 'email', 'old_password', 'password', 'password2', 'address',
                  'country', 'city',
                  'preferences', 'image']

    def clean(self):
        print "big_clean1 "
        cleaned_data = super(EditUserForm, self).clean()
        print "big_clean2 "
        old_password = cleaned_data['old_password']
        password = cleaned_data['password']
        if old_password:
            print "old pass", old_password
            print "cechk", self.user.check_password(old_password)
            if not self.user.check_password(old_password):
                raise forms.ValidationError('Contraseña incorrecta.')
            if password and old_password == password:
                raise forms.ValidationError('La nueva contraseña debe ser diferente a la anterior.')
        return cleaned_data

    def clean_username(self):
        if self.cleaned_data["username"] != self.user.username:
            return super(EditUserForm, self).clean_username()
        return self.cleaned_data["username"]

    def clean_email(self):
        if self.cleaned_data["email"] != self.user.email:
            return super(EditUserForm, self).clean_email()
        return self.cleaned_data["email"]

    def clean_password2(self):
        new_password = self.cleaned_data["password"]
        if new_password:
            return super(EditUserForm, self).clean_password2()
        return new_password


class LoginForm(ModelForm):
    username = forms.CharField(max_length=50, label="Usuario")
    password = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")

    class Meta:
        model = Profile
        fields = ['username', 'password']

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data['username']
        return username
