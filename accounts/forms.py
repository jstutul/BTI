from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile,Institution

User = get_user_model()


# =========================
# 1. SIGNUP FORM
# =========================
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    # Profile fields (not in User model)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'email',
            'password1',
            'password2'
        )


# =========================
# 2. USER PROFILE UPDATE
# =========================
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            else:
                field.widget.attrs.update({'class': 'form-control'})


# =========================
# 3. PROFILE FORM
# =========================
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','sign_image'] 

        widgets = {
            'profile_image': forms.FileInput(attrs={'class': 'form-control','id': 'profileImageInput'}),
            'sign_image': forms.FileInput(attrs={'class': 'form-control','id': 'signImageInput'}),
        }

class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = ['name', 'director', 'mobile', 'email', 'address','district','upazila']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'upazila': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  
                'placeholder': 'Short description'
            }),
        }

# =========================
# 4. ADMIN BALANCE UPDATE
# =========================
class UserAdminBalanceForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('balance',)


