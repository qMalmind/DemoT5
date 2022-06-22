from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from demo.models import User


def lenght_password(password):
    if len(password) < 6:
        raise ValidationError('Длина пароля должна быть неменьше шести символов')


class RegisterUserForm(forms.ModelForm):
    name = forms.CharField(label='Имя', error_messages={
        'required': 'Данное поле обязательно'
    }, required=True, validators=[RegexValidator("^[а-яА-Я- ]+$", message='Допустима только латиница и пробел')],
                           widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'имя'}))

    surname = forms.CharField(label='Фамилия', error_messages={
        'required': 'Данное поле обязательно'
    }, required=True, validators=[RegexValidator("^[а-яА-Я- ]+$", message='Допустима только латиница и пробел')],
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'фамилия'}))

    patronymic = forms.CharField(label='Отчество', required=False, validators=[
        RegexValidator("^[а-яА-Я- ]+$", message='Допустима только латиница и пробел')],
                                 widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'отчество'}))

    username = forms.CharField(label='Логин', error_messages={
        'required': 'Данное поле обязательно',
        'unique': 'Данное поле не уникально'
    }, required=True, validators=[
        RegexValidator("^[a-zA-Z0-9-_]+$", message="Разрешены латиница, цифры и знак нижнего подчёркивания")],
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'логин'}))

    email = forms.CharField(label='Почта', error_messages={
        'required': 'Данное поле обязательно',
        'unique': 'Данное поле не уникально'
    }, required=True, widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'почта'}))

    password1 = forms.CharField(label='Пароль', error_messages={
        'required': 'Данное поле обязательно'
    }, required=True, validators=[lenght_password],
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'пароль'}))

    password2 = forms.CharField(label='Повторите пароль', error_messages={
        'required': 'Данное поле обязательно'
    }, required=True, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'ещё пароль'}))

    rules = forms.BooleanField(label='Пользовательское соглашение',
                               widget=forms.CheckboxInput(attrs={'class': 'form-control'}), initial=True,
                               error_messages={
                                   'required': 'Данное поле обязательно',
                               })

    def clean(self):
        super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password2 and password1 and password1 != password2:
            raise ValidationError({
                'password2': ValidationError('Пароли не совподают')
            })

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get('password1'))

        if user:
            user.save()

        return user

    class Meta:
        model = User
        fields = ('name', 'surname', 'patronymic', 'username', 'email', 'password1', 'password2', 'rules')


class OrderAdminForm(forms.ModelForm):
    def clean(self):
        super().clean()
        status = self.cleaned_data.get('status')
        reject_reason = self.cleaned_data.get('reject_reason')

        if status == 'canceled' and not reject_reason:
            raise ValidationError({
                'reject_reason': "При отмене заказа нужно указать причину отмены"
            })

        if self.instance.status != 'new':
            raise ValidationError({
                'status': 'Статус можно менять только у новых заказов'
            })
