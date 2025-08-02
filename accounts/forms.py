from .models import UserProfile
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SingUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=254, help_text='Ejemplo: ejemplo@hotmail.com')

    model = User
    class Meta(UserCreationForm.Meta):
        fields = ['username','first_name', 'last_name', 'email' ]

        def clean_email(self):
            email = self.cleaned_data.get('email')
            if User.objects.filter(email__iexact=email).exists():
                raise forms.ValidationError("Ya existe un usuario con ese correo electrónico."
                                            "¿Olvidaste tu contraseña? Puedes restablecer el "
                                            "acceso a tu cuenta")
            return email


class ProfileCreate(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ['user', 'id']
        widgets = { 'text': forms.Textarea(attrs={'rows': 2})}