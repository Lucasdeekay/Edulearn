from django import forms
from .models import countries, states, Student, subjects

try:
    all_students = Student.objects.all()
except Exception:
    all_students = ''


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Username",
                "required": "",
            }
        )
    )

    password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "required": "",
            }
        )
    )

    role = forms.BooleanField(
        label="Staff",
        required=False,
        initial=False,
        widget=forms.CheckboxInput(
            attrs={
                "placeholder": "Staff",
            }
        ),
        help_text="Please check the box if you are a staff"
    )

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        username = cleaned_data.get("username")
        password = cleaned_data.get("password")
        role = cleaned_data.get("role")
        if not username or not password:
            raise forms.ValidationError("Field cannot be empty")
        elif len(password) < 8:
            raise forms.ValidationError("Password cannot be less than 8 characters")


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=50,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "Email",
                "required": "",
            }
        )
    )

    def clean(self):
        cleaned_data = super(ForgotPasswordForm, self).clean()
        email = cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Field cannot be empty")


class PasswordRetrievalForm(forms.Form):
    password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "required": "",
            }
        )
    )

    def clean(self):
        cleaned_data = super(PasswordRetrievalForm, self).clean()
        password = cleaned_data.get("password")
        if not password:
            raise forms.ValidationError("Field cannot be empty")
        elif len(password) < 8:
            raise forms.ValidationError("Password cannot be less than 8 characters")


class ChangePasswordForm(forms.Form):
    password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "required": "",
            }
        )
    )

    confirm_password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "required": "",
            }
        )
    )

    def clean(self):
        cleaned_data = super(ChangePasswordForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not confirm_password or not password:
            raise forms.ValidationError("Field cannot be empty")
        elif len(password) < 8 or len(confirm_password) < 8:
            raise forms.ValidationError("Password cannot be less than 8 characters")
        elif password != confirm_password:
            raise forms.ValidationError("Password do not match")


class RegistrationForm(forms.Form):
    last_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name/Surname',
                'required': '',
            }
        )
    )
    first_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'required': '',
            }
        )
    )
    middle_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Middle Name',
                'required': '',
            }
        )
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'required': '',
            }
        )
    )
    sex = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select Sex...'), ('Male', 'Male'), ('Female', 'Female')],
            attrs={
                'required': '',
            }
        )
    )
    dob = forms.CharField(
        help_text="Select your date of birth",
        widget=forms.DateInput(
            attrs={
                'required': '',
                'type': 'date',
            }
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Phone Number',
                'required': '',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'required': '',
            }
        )
    )
    address = forms.CharField(
        max_length=256,
        help_text='Maximum of 256 characters',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter address',
                'required': '',
                'rows': 4,
                'cols': 15,
            }
        )
    )
    religion = forms.CharField(
        max_length=20,
        widget=forms.Select(
            choices=[('', 'Select Religion...'), ('Christianity', 'Christianity'), ('Islam', 'Islam')],
            attrs={
                'required': '',
            }
        )
    )
    country = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select Country...')] + [(x, x) for x in countries],
            attrs={
                'required': '',
            }
        )
    )
    state_of_origin = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select State of Origin...')] + [(x, x) for x in states],
            attrs={
                'required': '',
            }
        )
    )
    state_of_residence = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select State of Residence...')] + [(x, x) for x in states],
            attrs={
                'required': '',
            }
        )
    )
    role = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select Role...'), ('Student', 'Student'), ('Teacher', 'Teacher')],
            attrs={
                'required': '',
            }
        )
    )
    password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Password",
                "required": "",
            }
        )
    )
    confirm_password = forms.CharField(
        max_length=25,
        widget=forms.PasswordInput(
            attrs={
                "placeholder": "Confirm Password",
                "required": "",
            }
        )
    )


    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        middle_name = cleaned_data.get('middle_name')
        username = cleaned_data.get('username')
        sex = cleaned_data.get('sex')
        dob = cleaned_data.get('dob')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        address = cleaned_data.get('address')
        religion = cleaned_data.get('religion')
        country = cleaned_data.get('country')
        state_of_origin = cleaned_data.get('state_of_origin')
        state_of_residence = cleaned_data.get('state_of_residence')
        role = cleaned_data.get('role')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if not last_name or not first_name or not middle_name or not username or not sex or not dob or \
                not phone_number or not email or not address or not religion or not country or not state_of_origin\
                or not state_of_residence or not password or not confirm_password or not role:
            raise forms.ValidationError("Field cannot be empty")
        elif len(last_name) < 2 or len(last_name) > 50:
            raise forms.ValidationError("Last Name must be between 2-50")
        elif len(first_name) < 2 or len(first_name) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(middle_name) < 2 or len(middle_name) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(username) < 2 or len(username) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(password) < 8:
            raise forms.ValidationError("Password cannot be less than 8 characters")
        elif password != confirm_password:
            raise forms.ValidationError("Password does not match")


class ProfileForm(forms.Form):
    last_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name/Surname',
            }
        )
    )
    first_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
            }
        )
    )
    middle_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Middle Name',
            }
        )
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
            }
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Phone Number',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
            }
        )
    )
    address = forms.CharField(
        max_length=256,
        help_text='Maximum of 256 characters',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter address',
                'rows': 4,
                'cols': 15,
            }
        )
    )
    image = forms.ImageField(
        max_length=250,
        help_text="Image must not be more than 10mb",
        widget=forms.FileInput(
            attrs={
                'class': 'input',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ProfileForm, self).clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        middle_name = cleaned_data.get('middle_name')
        username = cleaned_data.get('user_id')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        address = cleaned_data.get('address')
        image = cleaned_data.get('image')
        if not last_name or not first_name or not middle_name or not username or not phone_number or not email \
                or not address or not image:
            raise forms.ValidationError("Field cannot be empty")
        elif len(last_name) < 2 or len(last_name) > 50:
            raise forms.ValidationError("Last Name must be between 2-50")
        elif len(first_name) < 2 or len(first_name) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(middle_name) < 2 or len(middle_name) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(username) < 2 or len(username) > 50:
            raise forms.ValidationError("First Name must be between 2-50")


class SelectSessionPeriodForm(forms.Form):
    session_period = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[
                ('', 'Select Session Period...'),] + [(f'{x}/{x+1}', f'{x}/{x+1}') for x in range(2020, 2050)],
            attrs={
                'required': '',
            }
        )
    )

    session_term = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[
                ('', 'Select Session Term...'),
                ('1st', '1st'),
                ('1st Mid-Term', '1st Mid-Term'),
                ('2nd', '2nd'),
                ('2nd Mid-Term', '2nd Mid-Term'),
            ],
            attrs={
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(SelectSessionPeriodForm, self).clean()
        session_period = cleaned_data.get('session_period')
        session_term = cleaned_data.get('session_term')


class SelectSessionPeriodAndStudentForm(SelectSessionPeriodForm):
    student = forms.CharField(
        max_length=256,
        widget=forms.Select(
            choices=[('', 'Select Student...')] + [(x.person, x.person) for x in tuple(Student.objects.all())],
            attrs={
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(SelectSessionPeriodForm, self).clean()
        student = cleaned_data.get('student')


class StudentRegistrationForm(forms.Form):
    last_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Last Name/Surname',
                'required': '',
            }
        )
    )
    first_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'First Name',
                'required': '',
            }
        )
    )
    middle_name = forms.CharField(
        max_length=50,
        help_text="Characters must be between 2-50",
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Middle Name',
                'required': '',
            }
        )
    )
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username',
                'required': '',
            }
        )
    )
    sex = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select Sex...'), ('Male', 'Male'), ('Female', 'Female')],
            attrs={
                'required': '',
            }
        )
    )
    dob = forms.CharField(
        help_text="Select your date of birth",
        widget=forms.DateInput(
            attrs={
                'required': '',
                'type': 'date',
            }
        )
    )
    phone_number = forms.CharField(
        max_length=20,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Phone Number',
                'required': '',
            }
        )
    )
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'placeholder': 'Email',
                'required': '',
            }
        )
    )
    address = forms.CharField(
        max_length=256,
        help_text='Maximum of 256 characters',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter address',
                'required': '',
                'rows': 4,
                'cols': 15,
            }
        )
    )
    religion = forms.CharField(
        max_length=20,
        widget=forms.Select(
            choices=[('', 'Select Religion...'), ('Christianity', 'Christianity'), ('Islam', 'Islam')],
            attrs={
                'required': '',
            }
        )
    )
    country = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select Country...')] + [(x, x) for x in countries],
            attrs={
                'required': '',
            }
        )
    )
    state_of_origin = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select State of Origin...')] + [(x, x) for x in states],
            attrs={
                'required': '',
            }
        )
    )
    state_of_residence = forms.CharField(
        max_length=10,
        widget=forms.Select(
            choices=[('', 'Select State of Residence...')] + [(x, x) for x in states],
            attrs={
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(StudentRegistrationForm, self).clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        middle_name = cleaned_data.get('middle_name')
        username = cleaned_data.get('username')
        sex = cleaned_data.get('sex')
        dob = cleaned_data.get('dob')
        phone_number = cleaned_data.get('phone_number')
        email = cleaned_data.get('email')
        address = cleaned_data.get('address')
        religion = cleaned_data.get('religion')
        country = cleaned_data.get('country')
        state_of_origin = cleaned_data.get('state_of_origin')
        state_of_residence = cleaned_data.get('state_of_residence')
        if not last_name or not first_name or not middle_name or not username or not sex or not dob or \
                not phone_number or not email or not address or not religion or not country or not state_of_origin\
                or not state_of_residence:
            raise forms.ValidationError("Field cannot be empty")
        elif len(last_name) < 2 or len(last_name) > 50:
            raise forms.ValidationError("Last Name must be between 2-50")
        elif len(first_name) < 2 or len(first_name) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(middle_name) < 2 or len(middle_name) > 50:
            raise forms.ValidationError("First Name must be between 2-50")
        elif len(username) < 2 or len(username) > 50:
            raise forms.ValidationError("First Name must be between 2-50")


class StudentAssessmentForm(forms.Form):
    student = forms.CharField(
        max_length=256,
        widget=forms.Select(
            choices=[('', 'Select Student...')] + [(x.person, x.person) for x in tuple(Student.objects.all())],
            attrs={
                'required': '',
            }
        )
    )
    report = forms.CharField(
        max_length=500,
        help_text='Maximum of 500 characters',
        widget=forms.Textarea(
            attrs={
                'required': '',
                'rows': 4,
                'cols': 15,
            }
        )
    )
    attentiveness = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(StudentAssessmentForm, self).clean()
        student = cleaned_data.get('student')
        report = cleaned_data.get('report')
        attentiveness = cleaned_data.get('attentiveness')


class ResultForm(forms.Form):
    student = forms.CharField(
        max_length=256,
        widget=forms.Select(
            choices=[('', 'Select Student...')] + [(x.person, x.person) for x in tuple(Student.objects.all())],
            attrs={
                'required': '',
            }
        )
    )
    subject = forms.CharField(
        max_length=256,
        widget=forms.Select(
            choices=[('', 'Select Subject...')] + [(x, x) for x in subjects],
            attrs={
                'required': '',
            }
        )
    )
    score = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(ResultForm, self).clean()
        student = cleaned_data.get('student')
        subject = cleaned_data.get('subject')
        score = cleaned_data.get('score')


class MessageForm(forms.Form):
    message = forms.CharField(
        max_length=1000,
        help_text='Maximum of 1000 characters',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter message',
                'required': '',
                'rows': 4,
                'cols': 15,
            }
        )
    )
    student = forms.CharField(
        max_length=256,
        widget=forms.Select(
            choices=[('', 'Select Student...')] + [(x.person, x.person) for x in tuple(Student.objects.all())],
            attrs={
                'required': '',
            }
        )
    )

    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        message = cleaned_data.get('message')
        student = cleaned_data.get('student')


class ReplyForm(forms.Form):
    reply = forms.CharField(
        max_length=1000,
        help_text='Maximum of 1000 characters',
        widget=forms.Textarea(
            attrs={
                'placeholder': 'Enter reply...',
                'required': '',
                'rows': 4,
                'cols': 15,
            }
        )
    )

    def clean(self):
        cleaned_data = super(MessageForm, self).clean()
        reply = cleaned_data.get('reply')
