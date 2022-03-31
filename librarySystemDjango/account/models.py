from django.db import models
from django.contrib.auth.models import User
from random import choice
from book.models import Book
from django_jalali.db import models as jmodels
import jdatetime

# Create your models here.
def generate_invitation_code():
    mylist = []
    for i in range(48, 91):
        if chr(i).isalnum():
            mylist.append(chr(i))
    inv_code = ""
    for i in range(8):
        inv_code += str(choice(mylist))
    return inv_code

class UserInformations(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    national_code = models.CharField(max_length=10, unique=True)
    birth_date = jmodels.jDateField()
    phone_no = models.CharField(max_length=11)
    invitation_code = models.CharField(max_length=8, unique=True, default=generate_invitation_code)
    invited_people = models.PositiveIntegerField(default=0)
    current_invtd_ppl = models.PositiveIntegerField(default=0)
    dedicated_book = models.PositiveIntegerField(default=0)
    start_subs = jmodels.jDateTimeField(blank=True, null=True)
    end_subs = jmodels.jDateTimeField(blank=True, null=True)
    SUBS_CHOICES = (
        ("برنزی (یک ماهه)", "bronze(1 months)"),
        ("نقره‌ای (سه ماهه)", "silver(3 months)"),
        ("طلایی (یک ساله)", "golden(12 months)"),
    )
    subscription_type = models.CharField(max_length=20, choices=SUBS_CHOICES, blank=True, null=True)
    profile_pic = models.ImageField(upload_to='users_profile_pics', blank=True, null=True, default='users_profile_pics/empty-profile-picture-png-transparent-png.png')
    allowed_to_lend = models.BooleanField(default=True)
    lent_num = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.user.username

class UserFavoriteBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class SubscriptionRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    set_date = jmodels.jDateTimeField(null=True, blank=True)
    SUBS_CHOICES = (
        ("برنزی (یک ماهه)", "bronze(1 months)"),
        ("نقره‌ای (سه ماهه)", "silver(3 months)"),
        ("طلایی (یک ساله)", "golden(12 months)"),
    )
    subscription_type = models.CharField(max_length=20, choices=SUBS_CHOICES, blank=True, null=True)

    def __str__(self):
        return str(self.user)

class LendBook(models.Model):
    librarian = models.ForeignKey(User, limit_choices_to={'is_staff': True},
     on_delete=models.SET_NULL, null=True,
     related_name='library_admin'
    )
    member = models.ForeignKey(User, limit_choices_to={'is_staff': False},
     on_delete=models.CASCADE, related_name='library_member'
    )
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    loan_date = jmodels.jDateField(default=jdatetime.date.today())
    due_date = jmodels.jDateField()

    def __str__(self) -> str:
        return str(self.member)