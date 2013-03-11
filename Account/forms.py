from django.contrib.auth.models import User

__author__ = 'Behnam'

from django.utils.translation import ugettext_lazy as _
from django import forms


class Change_password_form(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'password_incorrect': _("Your old password was entered incorrectly. "
                                "Please enter it again."),
    }

    old_password = forms.CharField(label="Old password",
                                   widget=forms.PasswordInput, initial='Password')

    new_password1 = forms.CharField(label=_("Password"),
                                    widget=forms.PasswordInput, initial='Password')

    new_password2 = forms.CharField(label=_("Password (again)"),
                                    widget=forms.PasswordInput, initial='Password',
                                    help_text=_("Enter the same password as above, for verification."))


    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Change_password_form, self).__init__(*args, **kwargs)

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data["old_password"]
        if not self.user.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'])
        return old_password


    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2


    def save(self, commit=True):
        self.user.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.user.save()
        return self.user


class Change_user_password_form(forms.Form):
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
        'username_not_exists': _("Username doesn't exist"),
        'admin_password': _("You can't change your password from this part"),
    }

    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput)

    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)

    password2 = forms.CharField(label=_("Password (again)"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Change_user_password_form, self).__init__(*args, **kwargs)


    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if username == self.user.username:
                raise forms.ValidationError(
                    self.error_messages['admin_password']
                )
            try:
                self.user = User.objects.get(username__exact=username)
            except:
                raise forms.ValidationError(
                    self.error_messages['username_not_exists']
                )
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        return self.user


class Delete_user_form(forms.Form):
    error_messages = {
        'username_not_exists': _("Username doesn't exist"),
        'admin_password': _("You can't delete your self"),
    }

    username = forms.CharField(label=_("Username"),
                               widget=forms.TextInput)

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(Delete_user_form, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            if username == self.user.username:
                raise forms.ValidationError(
                    self.error_messages['admin_password']
                )
            try:
                self.user = User.objects.get(username__exact=username)
            except:
                raise forms.ValidationError(
                    self.error_messages['username_not_exists']
                )
        return username


    def save(self, commit=True):
        self.user.delete()
        return self.user


class show_user_form(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email', 'groups', 'is_staff', 'is_active', 'is_superuser',
            'last_login', 'date_joined')
        exclude = ('id', 'password', 'user_permissions')


class edit_user_form(forms.ModelForm):
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
    }

    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(edit_user_form, self).__init__(*args, **kwargs)


    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        if username == self.user.username:
            return username

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name", "email", "is_active")
        exclude = ('id', )


class Create_user_form(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'duplicate_username': _("A user with that username already exists."),
        'password_mismatch': _("The two password fields didn't match."),
    }
    username = forms.RegexField(label=_("Username"), max_length=30,
                                regex=r'^[\w.@+-]+$',
                                help_text=_("Required. 30 characters or fewer. Letters, digits and "
                                            "@/./+/-/_ only."),
                                error_messages={
                                    'invalid': _("This value may contain only letters, numbers and "
                                                 "@/./+/-/_ characters.")})
    password1 = forms.CharField(label=_("Password"),
                                widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
                                widget=forms.PasswordInput,
                                help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = User
        fields = (
            "username", "password1", "password2", "first_name", "last_name", "email", "groups", "is_staff", "is_active",
            "is_superuser")

    def clean_username(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        username = self.cleaned_data["username"]
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'])
        return password2

    def save(self, commit=True):
        user = super(Create_user_form, self).save(commit=commit)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
