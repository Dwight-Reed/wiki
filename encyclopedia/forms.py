from django import forms

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        "placeholder": "Content",
        # TODO: move to styles.css
        "style": "width: 100%; max-height: 100%;",
        "rows": "100",
        "class": "form-control",
        }), label="")

class NewPageForm(EditForm):
    title = forms.CharField(widget=forms.TextInput(attrs={"placeholder": "Title"}), label="")

    # place title before content
    field_order = ["title", "content"]

    # TODO: remove
    # check if page already exists
    # def clean(self):
    #     cleaned_data = super().clean()
    #     title = cleaned_data.get("title")

    #     if util.get_entry(title):
    #         self.add_error("title", f'Page "{title}" already exists')


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "username",
        "class": "form-control",
    }),
        label="",
    )

    password = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "password",
        "class": "form-control",
        "type": "password",
    }),
        label="",
    )

class RegisterForm(LoginForm):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        "placeholder": "email",
        "class": "form-control",
    }),
        label="",
    )
    confirm = forms.CharField(widget=forms.TextInput(attrs={
        "placeholder": "confirm password",
        "class": "form-control",
        "type": "password",
    }),
        label="",
    )
    field_order = ["username", "email", "password", "confirm"]
