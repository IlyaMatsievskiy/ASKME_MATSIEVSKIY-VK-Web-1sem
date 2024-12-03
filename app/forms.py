from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from app.models import Profile, Question, Answer


class LoginForm(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True) #чтобы пароль не было видно при вводе

    def clean_username(self):
        return self.cleaned_data['username'].lower().strip() #убираем лишние пробелы и делаем все буквы строчными


class SignUpForm(forms.ModelForm):
    # Замена
    password = forms.CharField(widget=forms.PasswordInput)

    # Новое поле
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'formFile',}))

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password')

    #вызывается автоматически при form.is_valid()
    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirmation']:
            # raise ValidationError('Passwords do not match')
            self.add_error('password', '')  # комментарий к ошибке не выводим
            self.add_error('password_confirmation', 'Passwords do not match')

        return data

    def clean_email(self):
        email = self.cleaned_data['email']
        if not email:
            raise ValidationError('Email is required')
        if User.objects.filter(email=email).exists():
            raise ValidationError('This email already exists')
        return email

    def clean_username(self):
        username = self.cleaned_data['username']
        if not username:
            raise ValidationError('Username is required')
        if User.objects.filter(username=username).exists():
            raise ValidationError('This username already exists')
        return username

    def clean_nickname(self):
        nickname = self.cleaned_data['nickname']
        if Profile.objects.filter(nickname=nickname).exists():
            raise ValidationError('This nickname already exists')
        return nickname

    def save(self, commit=True):
        user = super().save(commit=False)

        user.set_password(self.cleaned_data['password'])

        user.save()

        Profile.objects.create(
            user=user,
            nickname=self.cleaned_data.get('nickname', ''),
            avatar=self.cleaned_data.get('avatar', None),
        )

        return user

class SettingsForm(forms.ModelForm):
    # Замена
    password = forms.CharField(widget=forms.PasswordInput)

    # Новое поле
    password_confirmation = forms.CharField(widget=forms.PasswordInput)
    nickname = forms.CharField()
    avatar = forms.ImageField(
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'id': 'formFile', }))

    class Meta:
        model = User
        fields = ('username', 'email', 'nickname', 'password')

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance', None)
        super().__init__(*args, **kwargs)

        #можно сделать так, чтобы нельзя было менять это поле, также можно сделать и с паролем
        #в образце не было указано, что можно менять логин и пароль, но мне кажется это полезная функция
        #если учесть, что в будущем для смены этих данных будет введена аутентификация по почте
        # self.fields['username'].disabled = True
        if instance:
            # Получаем профиль, если он существует
            profile = getattr(instance, 'profile', None)
            if profile:
                self.initial['nickname'] = profile.nickname
                self.initial['avatar'] = profile.avatar

    def clean(self):
        data = super().clean()
        if data['password'] != data['password_confirmation']:
            # raise ValidationError('Passwords do not match')
            self.add_error('password', '')  # комментарий к ошибке не выводим
            self.add_error('password_confirmation', 'Passwords do not match')

        return data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise ValidationError('Email is required')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('This email already exists')
        return email

    def save(self, commit=True):
        user = super().save(commit=False)

        user.email = self.cleaned_data.get('email')

        if self.cleaned_data.get('password'):
            user.set_password(self.cleaned_data['password'])

        user.save()

        profile = user.profile  # Получаем существующий профиль
        profile.nickname =self.cleaned_data.get('nickname', '')
        profile.avatar = self.cleaned_data.get('avatar', None)

        profile.save()

        return user

class AskForm(forms.ModelForm):
    title = forms.CharField(required=True)
    text = forms.CharField(required=True, widget=forms.Textarea(attrs={'rows': 4, 'cols': 40}))
    tags = forms.CharField(required=False)

    class Meta:
        model = Question  # Указываем модель, с которой работает форма
        fields = ['title', 'text', 'tags']

    def clean(self):
        data = super().clean()
        return data #в данном случае не нужен, но можно оставить для переопределения в будущем


class AnswerForm(forms.ModelForm):
    content = forms.CharField(required=True, widget=forms.Textarea(attrs={'placeholder': 'Enter your answer here..',
            'rows': 4,
            'cols': 40,
            'class': 'form-control'}), label='')

    class Meta:
        model = Answer  # Указываем модель, с которой работает форма
        fields = ['content']

    def clean(self):
        data = super().clean()
        return data #в данном случае не нужен, но можно оставить для переопределения в будущем



