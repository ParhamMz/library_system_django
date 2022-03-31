from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.urls import reverse
from .models import UserFavoriteBook, UserInformations, SubscriptionRecord, LendBook
from book.models import Book
from .forms import (UserInfoForm, UserRegisterationForm,
                    EditUserInfoForm, EditAdminInfoForm,
                    UserEditPassForm, LendingBookForm)
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordResetForm
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
from dateutil.relativedelta import relativedelta
import urllib
import json
import datetime
import jdatetime
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.contrib import messages


# Create your views here.
def register(request):
    registered = False
    if request.method == 'POST':
        user_form = UserRegisterationForm(request.POST)
        profile_form = UserInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            if request.POST['invited']:
                try:
                    invite_user = UserInformations.objects.get(invitation_code=request.POST['invited'])
                    CHOICES_SUBS = dict(map(reversed, UserInformations.SUBS_CHOICES))
                    if invite_user:
                        invite_user.invited_people += 1
                        invite_user.current_invtd_ppl += 1
                        if invite_user.current_invtd_ppl == 3:
                            invite_user.subscription_type = CHOICES_SUBS['bronze(1 months)']
                            current_time = jdatetime.datetime.now()
                            invite_user.start_subs = current_time
                            future_date = current_time.togregorian() + relativedelta(months=1)
                            invite_user.end_subs = future_date
                            invite_user.current_invtd_ppl = 0
                            new_sub_record = SubscriptionRecord(user=invite_user.user, set_date=current_time, subscription_type=CHOICES_SUBS['bronze(1 months)'])
                            new_sub_record.save()
                        invite_user.save()
                except UserInformations.DoesNotExist:
                    pass

            user = user_form.save()
            # user.set_password(user.password)

            # user.save()

            # Now extra info
            profile = profile_form.save(commit=False)

            # Set One to One relationship between UserForm and UserProfileInfoForm
            profile.user = user
            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()
            
            new_username = request.POST['username']
            new_password = request.POST['password1']
            print('\nTHIS IS USERPASS ' + new_username + new_password)
            new_user = authenticate(request, username=new_username, password=new_password)
            print('\nTHIS IS USER ' + str(new_user))

            if new_user:
                login(request, new_user)
            registered = True
            return redirect('/')
    else:
        user_form = UserRegisterationForm()
        profile_form = UserInfoForm()

    context = {
        'user_form': user_form,
        'pro_form': profile_form,
        'registered': registered
    }

    return render(request, 'account/registeration.html', context=context)

def user_login(request):
    if request.method == 'POST':
        # parameters in parenthesis are "name" of our input forms in html doc
        username = request.POST['username'] 
        password = request.POST['password'] 
        user = authenticate(request, username=username, password=password)

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.RECAPTCHA_PRIVATE_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''


        if user:
            if result['success']:
                login(request, user)
                return redirect('/')
            else:
                messages.error(request, 'Recaptcha Error')
        else:
            messages.error(request, 'اطلاعات کاربری صحیح نمی‌باشد.')

    
    return render(request, 'account/loginPage.html', {})

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home_page'))

def password_reset(request):
    if request.method == "POST":
        domain = request.headers['Host']
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            # You can use more than one way like this for resetting the password.
            # ...filter(Q(email=data) | Q(username=data))
            # but with this you may need to change the password_reset form as well.
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "admin/accounts/password/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': domain,
                        'site_name': 'Interface',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/core/password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request, 'account/password_reset_form.html', {'password_reset_form': password_reset_form})

@user_passes_test(lambda u: u.is_superuser)
def promote_into_staff(request, the_username):
    user = User.objects.get(username=the_username)

    if request.method == 'POST':
        
        try:
            UserInformations.objects.get(user=user).delete()
            UserFavoriteBook.objects.get(user=user).delete()
            SubscriptionRecord.objects.get(user=user).delete()
        except UserFavoriteBook.DoesNotExist:
            pass
        except SubscriptionRecord.DoesNotExist:
            pass
        user.is_staff = True
        user.save()
        return HttpResponseRedirect(reverse('account:users_list_page'))
    context = {
        'user': user,
    }
    return render(request, 'account/promotionPage.html', context)

@login_required
def user_profile(request):
    # ADMIN
    if request.user.is_staff:
        admin_info_form = EditAdminInfoForm(request.POST or None)
        if request.method == 'POST':
            user = request.user
            if admin_info_form.is_valid():
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()
                messages.success(request, 'اطلاعات شما با موفقیت تغییر یافت.')

        context = {
            'admin_form': admin_info_form,
        }
    # MEMBER
    else:
        user = request.user
        user_info = UserInformations.objects.get(user=request.user)
        user_edit_form = EditUserInfoForm(request.POST or None)
        have_subs = False
        first_time = jdatetime.datetime.now() # IRI time zone
        end_time = 0
        if user_info.end_subs:
            have_subs = True
            later_time = user_info.end_subs
            end_time = later_time.togregorian().timestamp() * 1000 // 1


            difference = (((later_time.year - first_time.year) * 31536000) 
            + ((later_time.month - first_time.month) * 2628288)
            + ((later_time.day - first_time.day) * 86400)
            + ((later_time.hour - first_time.hour) * 3600)
            + ((later_time.minute - first_time.minute) * 60)
            + ((later_time.second - first_time.second)))


            if difference <= 0:
                user_info.subscription_type = None
                user_info.end_subs = None
                user_info.start_subs = None
                have_subs = False
                user_info.save()
        
        # UPDATING PROFILE
        if request.method == 'POST':
            if user_edit_form.is_valid():
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.email = request.POST['email']
                user.save()

                user_info.birth_date = request.POST['birth_date']
                user_info.phone_no = request.POST['phone_no']
                if 'profile_pic' in request.FILES:
                    user_info.profile_pic = request.FILES['profile_pic']
                
                user_info.save()
                messages.success(request, 'اطلاعات شما با موفقیت تغییر یافت.')
                return HttpResponseRedirect(reverse('account:profile_page'))

        context = {
            'user_info': user_info,
            'user_edit_form': user_edit_form,
            'have_sub': have_subs,
            'end_sub_time': end_time,
        }
    return render(request, 'account/userProfile.html', context)

@login_required
def delete_profile_pic(request, member_username):
    user = User.objects.get(username=member_username)
    the_user = user.userinformations
    the_user.profile_pic = 'users_profile_pics/empty-profile-picture-png-transparent-png.png'
    the_user.save()
    messages.success(request, 'اطلاعات شما با موفقیت تغییر یافت.')

    return redirect('account:profile_page')

@login_required
def edit_password(request):
    user = request.user
    edit_pass_form = UserEditPassForm(request.POST or None)
    if request.method == 'POST':
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']

        if len(password1) < 8 or len(password1) > 16:
            edit_pass_form.add_error('password', 'طول رمز عبور باید ۸ تا ۱۶ کاراکتر باشد.')
        elif password1 != password2:
            edit_pass_form.add_error('confirm_password', 'رمز عبور تکرار شده صحیح نمی‌باشد.')
        if edit_pass_form.is_valid():
            new_password = request.POST['password']
            user.set_password(request.POST['password'])
            user.save()
            new_user = authenticate(request, username=user.username, password=new_password)
            if new_user:
                login(request, new_user)
                return redirect('account:profile_page')
    return render(request, 'account/editPassPage.html', {'edit_pass_form':edit_pass_form})

@staff_member_required
def list_admins(request):
    admins = User.objects.all().filter(is_staff=True)
    context = {
        'admins': admins,
    }
    return render(request, 'account/allAdmins.html', context)

@login_required
def delete_user_acc(request):
    user = request.user
    by_admin = False
    if request.method == 'POST':
        user.delete()
        return redirect('/')
    return render(request, 'account/deletePage.html', {'by_admin':by_admin})

@staff_member_required
def list_users(request):
    user = request.user
    query = request.GET.get('searched_name')
    if query:
        all_users = UserInformations.objects.filter(national_code__contains=query) 
        if not all_users:
            all_users = None
    else:
        all_users = UserInformations.objects.all()

    context = {
        'all_users': all_users,
    }
    return render(request, 'account/allUsersPage.html', context)

@staff_member_required
def delete_user_by_admin(request, username_to_del):
    by_admin = True
    user = User.objects.get(username=username_to_del)

    if request.method == 'POST':
        user.delete()
        return redirect('account:profile_page')
    return render(request, 'account/deletePage.html', {'by_admin':by_admin, 'the_user':user})

@staff_member_required
def set_subscription(request, username_to_buy):
    if request.method == 'POST':
        sub_type = request.POST['subs-selection']
        user = User.objects.get(username=username_to_buy)
        the_user = user.userinformations
        CHOICES_SUBS = dict(map(reversed, UserInformations.SUBS_CHOICES))
        
        if sub_type == '1':
            the_user.subscription_type = CHOICES_SUBS['bronze(1 months)']
            current_time = jdatetime.datetime.now()
            the_user.start_subs = current_time
            future_date = current_time.togregorian() + relativedelta(months=1)
            the_user.end_subs = future_date
            new_sub_record = SubscriptionRecord(user=the_user.user, set_date=current_time, subscription_type=CHOICES_SUBS['bronze(1 months)'])
            new_sub_record.save()
        elif sub_type == '3':
            the_user.subscription_type = CHOICES_SUBS['silver(3 months)']
            current_time = jdatetime.datetime.now()
            the_user.start_subs = current_time
            future_date = current_time.togregorian() + relativedelta(months=3)
            the_user.end_subs = future_date
            new_sub_record = SubscriptionRecord(user=the_user.user, set_date=current_time, subscription_type=CHOICES_SUBS['silver(3 months)'])
            new_sub_record.save()
        elif sub_type == '12':
            the_user.subscription_type = CHOICES_SUBS['golden(12 months)']
            current_time = jdatetime.datetime.now()
            the_user.start_subs = current_time
            future_date = current_time.togregorian() + relativedelta(months=12)
            the_user.end_subs = future_date
            new_sub_record = SubscriptionRecord(user=the_user.user, set_date=current_time, subscription_type=CHOICES_SUBS['golden(12 months)'])
            new_sub_record.save()
        num = request.POST['dedicate-field']
        the_user.dedicated_book = num
        the_user.save()
        messages.success(request, 'تغییرات با موفقیت اعمال شد.')
            
    return HttpResponseRedirect(reverse('account:users_list_page'))

@staff_member_required
def dedicate_book(request, member_username):
    user = User.objects.get(username=member_username)
    the_user = user.userinformations

    if request.method == 'POST':
        num = request.POST['dedicate-field']
        the_user.dedicated_book = num
        the_user.save()
        messages.success(request, 'تغییرات با موفقیت اعمال شد.')

    return HttpResponseRedirect(reverse('account:users_list_page'))

@login_required
def show_subscription(request):
    return render(request, 'account/buySubsPage.html')

@login_required
def buy_subscription(request, subs_type, num_month):
    user = request.user
    user_info  = UserInformations.objects.get(user=user)
    CHOICES_SUBS = dict(map(reversed, UserInformations.SUBS_CHOICES))

    if request.method == 'POST':
        user_info.subscription_type = CHOICES_SUBS[subs_type]
        current_time = jdatetime.datetime.now()
        user_info.start_subs = current_time
        future_date = current_time.togregorian() + relativedelta(months=num_month)
        user_info.end_subs = future_date
        new_sub_record = SubscriptionRecord(user=user, set_date=current_time, subscription_type=CHOICES_SUBS[subs_type])
        new_sub_record.save()
        user_info.save()
        return HttpResponseRedirect(reverse('account:profile_page'))

    return render(request, 'account/bankPage.html')

@staff_member_required
def delete_subscription(request, the_username):
    temp = User.objects.get(username=the_username)
    the_user = UserInformations.objects.get(user=temp)
    the_user.subscription_type = None
    the_user.end_subs = None
    the_user.start_subs = None
    the_user.save()
    messages.success(request, 'تغییرات با موفقیت اعمال شد.')
    return HttpResponseRedirect(reverse('account:users_list_page'))

@login_required
def show_favorite_books(request):
    user = request.user

    query = request.GET.get('searched_name')
    if query:
        try:
            searched_book = Book.objects.get(title__icontains=query)
            favorites = UserFavoriteBook.objects.filter(user=user).filter(title=searched_book.id)
        except Book.DoesNotExist:
            favorites = None
        if not favorites:
            favorites =  None
    else:
        favorites = UserFavoriteBook.objects.filter(user=user)
    
    context = {
        'favorites': favorites,
    }
    
    return render(request, 'account/favoriteBooks.html', context)

@login_required
def del_from_favorites(request, book_title):
    book_to_del = Book.objects.get(title=book_title)
    UserFavoriteBook.objects.get(title=book_to_del.id).delete()
    return HttpResponseRedirect(reverse('account:favorite_page'))

@staff_member_required
def list_books(request):
    query = request.GET.get('searched_name')
    if query:
        books = Book.objects.filter(title__icontains=query) 
        if not books:
            books = None
    else:
        books = Book.objects.all()
    context = {
        'books': books,
    }
    return render(request, 'account/allBooksPage.html', context)

@staff_member_required
def del_book(request, book_title):
    the_book = Book.objects.get(title=book_title)
    if request.method == 'POST':
        the_book.delete()
    return render(request, 'account/deleteBPage.html', {'the_book':the_book})

@login_required
def show_subs_record(request):    
    # ADMIN
    if request.user.is_staff:
        query = request.GET.get('searched_name')
        user_info = None
        no_record = False
        if query:
            try:
                the_user = User.objects.get(username=query)
                user_info = UserInformations(user=the_user)
                subs_records = SubscriptionRecord.objects.all().filter(user=the_user).order_by('-set_date')
            except User.MultipleObjectsReturned:
                subs_records = None
            except User.DoesNotExist:
                subs_records = None
            if not subs_records:
                subs_records = []
                no_record = True
        else:
            subs_records = SubscriptionRecord.objects.all().order_by('-set_date')
        context = {
            'subs_records': zip(range(50), subs_records),
            'no_record': no_record,
            'user_info': user_info,
        }
    # MEMBER
    else:
        
        subs_records = SubscriptionRecord.objects.all().filter(user=request.user).order_by('-set_date')
        context = {
            'subs_records': zip(range(50), subs_records),
        }
    return render(request, 'account/allSubsRecords.html', context)

@staff_member_required
def book_lending(request):
    lending_form = LendingBookForm(request.POST or None)
    if request.method == 'POST':
        if lending_form.is_valid():
            librarian = request.user
            member = lending_form.cleaned_data['member']
            book = lending_form.cleaned_data['book']
            loan_date = lending_form.cleaned_data['loan_date']
            member_info = UserInformations.objects.get(user=member)
            if member_info.allowed_to_lend:
                due_date = loan_date + relativedelta(days=7)
                new_record = LendBook(librarian=librarian, member=member, book=book, loan_date=loan_date, due_date=due_date)
                new_record.save()
                member_info.lent_num += 1
                if member_info.lent_num == 3:
                    member_info.allowed_to_lend = False
                member_info.save()
                return redirect('account:loan_list_page')
            else:
                messages.error(request, 'کاربر در حال حاضر مجاز به امانت گرفتن کتاب نمی‌باشد.')
        else:
            messages.error(request, 'خطا در ثبت اطلاعات')
    
    context = {
        'lending_form': lending_form,
    }
    return render(request, 'account/lendBPage.html', context)

@staff_member_required
def list_lent_books(request):
    query = request.GET.get('searched_name')
    if query:
        all_records = LendBook.objects.filter(member__username__icontains=query)
        #                                     foreignKey__field__lookup
        if not all_records:
            all_records = None
    else:
        all_records = LendBook.objects.all()

    context = {
        'all_records': all_records,
    }
    return render(request, 'account/allLentBPage.html', context)

@staff_member_required
def return_book(request, member_username, book_title):
    loan = LendBook.objects.filter(member__username=member_username).filter(book__title=book_title)
    member_info = UserInformations.objects.get(user__username=member_username)
    loan.delete()
    member_info.lent_num -= 1
    if member_info.lent_num < 3:
        member_info.allowed_to_lend = True
    member_info.save()
    messages.success(request, 'عملیات با موفقیت انجام شد.')
    return redirect('account:loan_list_page')