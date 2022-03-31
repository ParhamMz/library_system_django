from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm, UsernameField
from .models import UserInformations, LendBook
from django.core import validators
from django.core.validators import RegexValidator
from django.forms import SelectDateWidget
from jalali_date.fields import JalaliDateField
from jalali_date.widgets import AdminJalaliDateWidget
import jdatetime


class UserRegisterationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super(UserRegisterationForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "نام"
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['email'].label = "ایمیل"
        self.fields['username'].label = "نام کاربری"
        self.fields['password1'].label = "رمز عبور"
        self.fields['password2'].label = "تکرار رمز عبور"
        self.fields['password1'].widget.attrs['class'] = 'left-field'
        self.fields['password2'].widget.attrs['class'] = 'left-field'

    first_name = forms.CharField(widget=forms.TextInput(
        attrs={'class':'form-control only-persian fname-field', 
                'palceholder': 'نام خود را به فارسی وارد کنید'
        })
    )
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control only-persian lname-field',
    'palceholder': 'نام خانوادگی خود را به فارسی وارد کنید'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control email-field left-field','placeholder':'name@example.com'}))
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control only-english username-field left-field',}))
    # password1 = forms.CharField(widget=forms.PasswordInput(
    #     attrs={'type': 'password',
    #             'class': 'register-pass-field',
    #         }),
    # )
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={'type': 'password',
                'class': 'register-pass-field',
            }),
        help_text="<ul><li>برای تائید، رمز عبور را تکرار کنید.</li></ul>"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password1', 'password2']
# error_messages = {
#     'username': {
#         'unique': 'کاربری با این نام کاربری وجود دارد.',
#     },
#     'password_mismatch': "رمز عبور تکرار شده صحیح نمی‌باشد.",
# }


class UserInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        self.fields['national_code'].label = "کد ملی"
        self.fields['phone_no'].label = "شماره تلفن"
        self.fields['profile_pic'].label = "عکس پروفایل"
        self.fields['invited'].label = "کد دعوت"
        # self.fields['confirm_password'].label = "تکرار رمز عبور"


    # confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'left-field confirm-passw-field',}))
    birth_date = JalaliDateField(label='تاریخ تولد')
    invited = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control invited-field left-field',
        'placeholder': 'در صورت داشتن کد دعوت آن را وارد کنید'
        }),
        required=False
    )
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control only-number-input phone-field left-field',
            'placeholder': '09*********'}),
            validators=[RegexValidator(r'^[09]\d{10}$', message="شماره تلفن وارد شده معتبر نمی‌باشد.")]
    )
    national_code = forms.CharField(widget=forms.TextInput(attrs={
            'class':'form-control only-number-input national-field left-field',
            }), 
            validators=[RegexValidator(r'^\d{10}$', message="کد ملی وارد شده معتبر نمی‌باشد.")]
    )
    profile_pic = forms.ImageField(required=False, 
        widget=forms.TextInput(attrs={
            'class':'form-control pro-pic-field',
            'type': 'file'
            }
    ))
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])
    
    def clean_invited(self):
        if self.cleaned_data['invited']:
            try:
                invite_user = UserInformations.objects.get(invitation_code=self.cleaned_data['invited'])
            except UserInformations.DoesNotExist:
                raise forms.ValidationError('کد دعوت وارد شده صحیح نمی‌باشد. (حروف کوچک و بزرگ مهم هستند)')


    class Meta:
        model = UserInformations
        fields = ['national_code', 'birth_date', 'phone_no', 'invited', 'profile_pic']


class EditUserInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditUserInfoForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "نام"
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['email'].label = "ایمیل"
        self.fields['birth_date'].label = "تاریخ تولد"
        self.fields['phone_no'].label = "شماره تلفن"
        self.fields['profile_pic'].label = "عکس پروفایل"

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control only-persian fname-field', 'id': 'edit-inp-first-name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control only-persian lname-field', 'id': 'edit-inp-last-name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control email-field left-field', 'id': 'edit-inp-email', 'placeholder':'name@example.com'}))
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'class': 'date-filed', 'id': 'edit-inp-birth'}))
    phone_no = forms.CharField(
        widget=forms.TextInput(attrs={
            'class':'form-control only-number-input phone-field left-field',
            'id': 'edit-inp-phone-no',
            'placeholder': '09*********'}),
            validators=[RegexValidator(r'^[09]\d{10}$', message="شماره تلفن وارد شده معتبر نمی‌باشد.")]
    )
    
    profile_pic = forms.ImageField(required=False, 
        widget=forms.TextInput(attrs={
            'class':'form-control pro-pic-field',
            'id': 'edit-inp-profile-pic',
            'type': 'file'
        }
    ))
    botcatcher = forms.CharField(required=False, widget=forms.HiddenInput, validators=[validators.MaxLengthValidator(0)])

    class Meta:
        model = UserInformations
        fields = ['first_name', 'last_name', 'email', 'birth_date', 'phone_no', 'profile_pic']

class EditAdminInfoForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(EditAdminInfoForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].label = "نام"
        self.fields['last_name'].label = "نام خانوادگی"
        self.fields['email'].label = "ایمیل"
        

    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control only-persian fname-field', 'id': 'edit-inp-first-name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control only-persian lname-field', 'id': 'edit-inp-last-name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control email-field left-field', 'id': 'edit-inp-email', 'placeholder':'name@example.com'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class UserEditPassForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'left-field confirm-passw-field',}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'left-field',}))

    def __init__(self, *args, **kwargs):
        super(UserEditPassForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = "گذرواژه جدید"
        self.fields['confirm_password'].label = "تکرار گذرواژه "

    class Meta:
        model = User
        fields = ['password', 'confirm_password']
    
class LendingBookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(LendingBookForm, self).__init__(*args, **kwargs)
        self.fields['member'].label = "نام کاربری امانت گیرنده"
        self.fields['book'].label = "عنوان کتاب"
        self.fields['loan_date'].label = "تاریخ ثبت امانت"
        self.fields['member'].widget.attrs['class'] = 'left-field'
        self.fields['loan_date'].widget.attrs['class'] = 'date-field'
        self.fields['loan_date'].widget.attrs['style'] = 'text-align:center'

    loan_date = JalaliDateField(initial=jdatetime.date.today())

    class Meta:
        model = LendBook
        exclude = ('librarian', 'due_date',)
    