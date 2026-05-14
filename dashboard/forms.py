from django import forms
from accounts.models import Course,Session,Institution,Student,Result,Certificate,Chairman
import random

class CourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = ['name', 'duration', 'exam_fee', 'cert_type', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter course name'
            }),

            'duration': forms.Select(attrs={
                'class': 'form-control'
            }),

            'cert_type': forms.Select(attrs={
                'class': 'form-control'
            }),

            'exam_fee': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '1', 
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  
                'placeholder': 'Short description'
            }),
        }

class SessionForm(forms.ModelForm):
    class Meta:
        model = Session
        fields = ['name', 'start_date', 'end_date', 'exam_date', 'status']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'end_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'exam_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class InstitutionForm(forms.ModelForm):
    class Meta:
        model = Institution
        fields = [
            'name',  'director',
            'mobile', 'email',
            'district', 'upazila', 'address'
        ]
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'director': forms.TextInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'district': forms.TextInput(attrs={'class': 'form-control'}),
            'upazila': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  
                'placeholder': 'Short description'
            }),
        }




class StudentForm(forms.ModelForm):
    profile_image = forms.ImageField(required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['session'].required = True
        if user and hasattr(user, 'profile'):

            if user.profile.role == 'institution':
                self.fields['institution'].queryset = Institution.objects.filter(
                    id=user.profile.institution.id
                )
                self.fields['institution'].initial = user.profile.institution
                self.fields['institution'].disabled = True

            # ✅ ADMIN USER: show ALL active institutions
            elif user.profile.role == 'admin':
                self.fields['institution'].queryset = Institution.objects.filter(is_active=True)

            # (optional safety)
            else:
                self.fields['institution'].queryset = Institution.objects.none()
    
    def clean_session(self):
        session = self.cleaned_data.get('session')
        if not session:
            raise forms.ValidationError("Session is required.")
        return session
    
    class Meta:
        model = Student
        fields = [
            'full_name',
            'father_name',
            'mother_name',
            'dob',
            'gender',
            'email',
            'blood_group',
            'mobile',
            'nid_no',
            'religion',
            'nationality',
            'present_address',
            'permanent_address',
            'education',
            'session',
            'institution',
            'courses',
            'reg_book_no',
            'admissionDate'
        ]

        widgets = {
            'full_name': forms.TextInput(attrs={'class': 'form-control'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control'}),
            'mother_name': forms.TextInput(attrs={'class': 'form-control'}),
            'dob': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'blood_group': forms.Select(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'nid_no': forms.TextInput(attrs={'class': 'form-control'}),
            'education': forms.TextInput(attrs={'class': 'form-control'}),
            'reg_book_no': forms.TextInput(attrs={'class': 'form-control'}),
            'nationality': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'courses': forms.Select(attrs={'class': 'form-control'}),
            'present_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  
                'placeholder': 'Present Address'
            }),
            'permanent_address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,  
                'placeholder': 'Permanent Address'
            }),
        }


class StudentEditForm(StudentForm):
    class Meta(StudentForm.Meta):
        fields = StudentForm.Meta.fields + ['is_active']



class ResultForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['student'].queryset = Student.objects.none()

        if user and hasattr(user, 'profile'):
            if user.profile.role == 'institution':
                self.fields['student'].queryset = Student.objects.filter(
                    institution=user.profile.institution
                )
            elif user.profile.role == 'admin':
                self.fields['student'].queryset = Student.objects.all()
    def clean(self):
        cleaned_data = super().clean()

        written = cleaned_data.get("written_mark") or 0
        practical = cleaned_data.get("practical_mark") or 0
        viva = cleaned_data.get("viva_mark") or 0

        total = written + practical + viva

        if total > 100:
            raise forms.ValidationError("Total marks cannot exceed 100")

        return cleaned_data
    class Meta:
        model = Result
        fields = [
            'student',
            'course',
            'session',
            'written_mark',
            'practical_mark',
            'viva_mark',
            'exam_date',
            'is_published'
        ]

        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'course': forms.Select(attrs={'class': 'form-control'}),
            'session': forms.Select(attrs={'class': 'form-control'}),
            'written_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'practical_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'viva_mark': forms.TextInput(attrs={'class': 'form-control'}),
            'exam_date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }



class CertificateForm(forms.ModelForm):

    class Meta:
        model = Certificate
        fields = ['result','issue_date']
        widgets = {
            'result': forms.Select(attrs={'class': 'form-control', 'id': 'id_result'}),
            'issue_date':forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            })
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        qs = Result.objects.select_related('student', 'course', 'session', 'student__institution')
        qs = qs.filter(is_published=True)
        # ONLY PASSED STUDENTS
        qs = qs.filter(
            grade__in=['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'D']
        )

        # institution restriction
        if user and user.profile.role == 'institution':
            qs = qs.filter(student__institution=user.profile.institution)

        # exclude already certified
        qs = qs.exclude(certificate__isnull=False)

        self.fields['result'].queryset = qs


class ChairmanForm(forms.ModelForm):
    class Meta:
        model = Chairman
        fields = ['sign_image','certificate_bg','admitcard_bg','registration_bg','idcard_bg', 'is_active']

        widgets = {
            'sign_image': forms.FileInput(attrs={
                'id': 'id_sign_image',
                'accept': 'image/*'
            }),
            'certificate_bg': forms.FileInput(attrs={
                'id': 'id_certificate_bg',
                'accept': 'image/*'
            }),
            'admitcard_bg': forms.FileInput(attrs={
                'id': 'id_admitcard_bg',
                'accept': 'image/*'
            }),
            'registration_bg': forms.FileInput(attrs={
                'id': 'id_registration_bg',
                'accept': 'image/*'
            }),
            'idcard_bg': forms.FileInput(attrs={
                'id': 'id_idcard_bg',
                'accept': 'image/*'
            }),
        }

class CertificateEditForm(forms.ModelForm):

    class Meta:
        model = Certificate
        fields = ['serial_no', 'issue_date']
        widgets = {
            'issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'serial_no': forms.TextInput(attrs={'class': 'form-control'}),
        }