from django import forms
from django.core.exceptions import ValidationError

from .models import *


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "type": "text",
            "name": "username",
            "class": "form-control",
            "aria-describedby": "usernameHelp"
        }
    ))
    password = forms.CharField(min_length=4, widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "name": "password",
            "class": "form-control",
            "id": "exampleInputPassword1"
        }
    ))

class RegisterForm(forms.ModelForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={
            "type": "text",
            "name": "username",
            "class": "form-control",
            "aria-describedby": "usernameHelp"
        }
    ))
    email = forms.CharField(widget=forms.EmailInput(
        attrs={
            "type": "text",
            "name": "email",
            "class": "form-control",
            "aria-describedby": "usernameHelp"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control"
        }
    ))
    password_check = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "type": "password",
            "class": "form-control"
        }
    ))
    avatar = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            "type": "file",
            "class": "form-control",
            "id": "customFile"
        }
    ))
    def clean(self):
        password = self.cleaned_data['password']
        password_check = self.cleaned_data['password_check']
        if password != password_check:
            raise ValidationError('Passwords do not match')        # Пароли не совпадают
    def clean_username(self):
        username = self.cleaned_data['username']
        user = User.objects.filter(username=username)
        if len(user) != 0:
            raise ValidationError('A user with this username already exists')   # Пользователь с таким username уже существует
        return username
    def clean_email(self):
        email = self.cleaned_data['email']
        user_email = User.objects.filter(email=email)
        if len(user_email) != 0:
            raise ValidationError('A user with such an email already exists')   # Пользователь с таким email уже существует
        return email
    def save(self, **kwargs):
        self.cleaned_data.pop('password_check')
        user = User.objects.create_user(username=self.cleaned_data["username"], email=self.cleaned_data["email"], password=self.cleaned_data["password"])
        profile = Profile(user=user)
        received_avatar = self.cleaned_data["avatar"]
        if received_avatar:
            profile.avatar = received_avatar
        profile.save()
        return user
    class Meta:
        model = User
        fields = ["username", "email", "password"]

class QuestionForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "Header field",
            "rows": "3"
        }
    ))
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-text-height form-control",
            "placeholder": "Reveal the essence of the question",
            "rows": "3"
        }
    ))
    tags = forms.CharField(widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "placeholder": "#C++#HTML#CSS"
        }
    ))
    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(QuestionForm, self).__init__(*args, **kwargs)
    def clean_tags(self):
        data = self.cleaned_data['tags']
        kol = 0
        for i in data:
            if (i == "#"):
                kol += 1
        if kol > 3:
            raise ValidationError('The number of tags is no more than 3')       # Количество тэгов должно быть не более 3
        if kol == 0:
            raise ValidationError('Fill in the field')                          # Необходимо добавить тэг
        for i in data:
            if not (i == "#" or i.isalpha() or ("0" <= i <= "9") or i == "-" or i == "_"):
                raise ValidationError('Tags can only contain numbers and Latin letters')    # Теги могут содержать только цифры и латинские буквы
            # A tag can consist solely of lowercase alphanumeric characters, dashes, and underscores, without 2 or more dashes in a row (underscores are allowed). In addition, the tag can't start or end with a hyphen
        return data
    def clean_title(self):
        data = self.cleaned_data['title']
        if len(data) == 0:
            raise ValidationError('It is necessary to fill in the Title field') # Необходимо заполнить поле Title
        return data
    def clean_content(self):
        data = self.cleaned_data['content']
        if len(data) == 0:
            raise ValidationError('It is necessary to fill in the Content field') # Необходимо заполнить поле Content
        return data
    def save(self, **kwargs):
        user = Profile.objects.all().get(user=self.user)
        question = Question.objects.create(title=self.cleaned_data['title'],
                                           content=self.cleaned_data['content'],
                                           user=user)
        returnedQueryset = self.cleaned_data.get('tags')
        if returnedQueryset[0] != "#":
            raise ValidationError('Не хватает # в начале')
        returnedQueryset = returnedQueryset[1:len(returnedQueryset)]
        tag = ""
        list_tag = []
        for i in range(len(returnedQueryset)):
            if returnedQueryset[i] == "#":
                if not Tag.objects.filter(tag=tag).exists():
                    t = Tag(tag=tag)
                    t.save()
                list_tag.append(Tag.objects.get(tag=tag))
                tag = ""
            else:
                tag += returnedQueryset[i]
        if not Tag.objects.filter(tag=tag).exists():
            t = Tag(tag=tag)
            t.save()
        list_tag.append(Tag.objects.get(tag=tag))
        for member in list_tag:
            question.tags.add(member)
        if question is not None:
            question.save()
        return question
    class Meta:
        model = Question
        fields = ["title", "content", "tags"]

class AnswerForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(
        attrs={
            "class": "form-control",
            "placeholder": "Enter your answer here..",
            "rows": "4"
        }
    ))
    def __init__(self, user, question_id, *args, **kwargs):
        self.user = user
        self.question_id = question_id
        super(AnswerForm, self).__init__(*args, **kwargs)
    def save(self, **kwargs):
        user = Profile.objects.all().get(user=self.user)#self.user.id)
        question = Question.objects.all().get(pk=self.question_id)
        answer = Answer.objects.create(content=self.cleaned_data['content'],
                                       question=question,
                                       user=user)
        if answer is not None:
            answer.save()
        return answer
    class Meta:
        model = Answer
        fields = ["content"]

class ProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False, widget=forms.FileInput(
        attrs={
            "type": "file",
            "class": "form-control",
            "id": "customFile"
        }
    ))
    username = forms.CharField(max_length=250, widget=forms.TextInput(
        attrs={
            "class": "form-control",
            "rows": "4"
        }
    ))
    email = forms.EmailField(widget=forms.EmailInput(
        attrs={
            "type": "email",
            "class": "form-control",
            "id": "exampleInputEmail1",
            "aria-describedby": "emailHelp",
        }
    ))
    def save(self, **kwargs):
        user = super().save(**kwargs)
        profile = user.profile
        received_avatar = self.cleaned_data["avatar"]
        if received_avatar:
            profile.avatar = received_avatar
            profile.save()
        return user
    def clean_username(self):
        username = self.cleaned_data["username"]
        user_ = User.objects.filter(username=username)
        if len(user_) != 0 and self.instance.username != username:
            raise ValidationError("Such a username is already taken") # Такой username уже занят
        return username
    def clean_email(self):
        email = self.cleaned_data["email"]
        user_email = User.objects.filter(email=email)
        if len(user_email) != 0 and self.instance.email != email:
            raise ValidationError("Such a email is already taken") # Такой email уже занят
        return email
    class Meta:
        model = User
        fields = ["username", "email"]