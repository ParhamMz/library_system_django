from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from .forms import AddBookForm
from account.forms import UserEditPassForm
from .models import Book, Category
from account.models import UserFavoriteBook, UserInformations
from librarySystemDjango.settings import MEDIA_DIR
import mimetypes
from django.contrib import messages


# Create your views here.
def main_book_page(request):
    user = request.user
    categories = Category.objects.all()
    srch_base_que = request.GET.get('search-base')
    searched_book_que = request.GET.get('book-info')
    free_que = request.GET.get('free-checkbox')
    premium_que = request.GET.get('premium-checkbox')
    available_que = request.GET.get('available-checkbox')
    category_que = request.GET.get('categories-radio-btn')
    
    books = None

    if available_que:
        available_que = True
        books = Book.objects.filter(available=True)
    else:
        books = Book.objects.all()

    if free_que and premium_que:
        free_que = True
        premium_que = True
    elif free_que:
        free_que = True
    elif premium_que:
        free_que = False
    else:
        free_que = True
        premium_que = True

    if srch_base_que and searched_book_que:
        if srch_base_que == 'title':
            if free_que and premium_que: 
                if category_que:   
                    books = books.filter(category__name=category_que).filter(title__contains=searched_book_que)
                else:
                    books = books.filter(title__contains=searched_book_que)
            else:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(title__contains=searched_book_que).filter(free=free_que)
                else:
                    books = books.filter(title__contains=searched_book_que).filter(free=free_que)

        elif srch_base_que == 'author':
            if free_que and premium_que:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(author__contains=searched_book_que)
                else:
                    books = books.filter(author__contains=searched_book_que)
            else:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(author__contains=searched_book_que).filter(free=free_que)
                else:
                    books = books.filter(author__contains=searched_book_que).filter(free=free_que)
        
        elif srch_base_que == 'translator':
            if free_que and premium_que:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(translator__contains=searched_book_que)
                else:
                    books = books.filter(translator__contains=searched_book_que)
            else:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(translator__contains=searched_book_que).filter(free=free_que)
                else:
                    books = books.filter(translator__contains=searched_book_que).filter(free=free_que)
        
        elif srch_base_que == 'publisher':
            if free_que and premium_que:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(publisher__contains=searched_book_que)
                else:
                    books = books.filter(publisher__contains=searched_book_que)
            else:
                if category_que:   
                    books = books.filter(category__name=category_que).filter(publisher__contains=searched_book_que).filter(free=free_que)
                else:
                    books = books.filter(publisher__contains=searched_book_que).filter(free=free_que)
    elif category_que:
        if free_que and premium_que:
            books = books.filter(category__name=category_que)
        else:
            books = books.filter(free=free_que).filter(category__name=category_que)
    else:
        if not (free_que and premium_que):
            books = books.filter(free=free_que)
    
    if books:
        if available_que:
            books = books.filter(available=available_que)
    else:
        books = Book.objects.filter(available=available_que)


    paginator = Paginator(books, 6) # Show 25 contacts per page.
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'is_book': books,
        'page_obj': page_obj,
        'categories': categories,
    }

    return render(request, 'book/booksMain.html', context)

@staff_member_required
def add_book(request):
    edit_pass_form = UserEditPassForm(request.POST or None)

    if request.method == 'POST':
        add_form = AddBookForm(request.POST)
        if add_form.is_valid():
            the_book = add_form.save(commit=False)

            if 'book_imgs' in request.FILES:
                the_book.book_imgs = request.FILES['book_imgs']

            if 'book_pdf' in request.FILES:
                the_book.book_pdf = request.FILES['book_pdf']

            the_book.save()

            return HttpResponseRedirect(reverse('books:main_books_page'))
    else:
        add_form = AddBookForm()

    context = {
        'add_form': add_form,
        'edit_pass_form': edit_pass_form,
    }

    return render(request, 'book/addBPage.html', context)

def book_info(request, book_title):
    the_book = Book.objects.get(title=book_title)
    alike_books = Book.objects.filter(category__name=the_book.category).exclude(title=book_title)
    is_favorite = False
    user = None
    user_profile = None
    if request.user.is_authenticated:
        user = request.user
        if not user.is_staff:
            user_profile = UserInformations.objects.get(user=user)
        user_favorite = UserFavoriteBook.objects.filter(title=the_book.id).filter(user=user)
        if user_favorite:
            is_favorite = True
        else:
            is_favorite = False
            
    if request.method == 'POST':
        if is_favorite:
            user_favorite.delete()
        else:
            new_obj = UserFavoriteBook(user=user, title=the_book)
            new_obj.save()
        return redirect('/books/book/{book_title}/'.format(book_title=book_title))
    context = {
        'loggedin_user': user,
        'user_profile': user_profile,
        'the_book': the_book,
        'alike_books': alike_books,
        'is_favorite': is_favorite,
    }
    return render(request, 'book/bookInfo.html', context)

def download_file(request, filename):
    if filename != '':
        # Define Django project base directory
        # BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # Define the full file path
        filename = filename.replace('/', '\\')
        filepath = MEDIA_DIR + '\\' + filename
        # Open the file for reading content
        path = open(filepath, 'rb')
        # Set the mime type
        mime_type, _ = mimetypes.guess_type(filepath)
        # Set the return value of the HttpResponse
        response = HttpResponse(path, content_type=mime_type)
        # Set the HTTP header for sending to browser
        response['Content-Disposition'] = "attachment; filename=%s" % filename
        # Return the response value
        return response
    else:
        # Load the template
        return render(request, 'book/bookInfo.html', {})

@staff_member_required
def update_book(request, book_title):
    edit_pass_form = UserEditPassForm(request.POST or None)

    the_book = Book.objects.get(title=book_title)
    update_form = AddBookForm(request.POST or None, instance=the_book)
    if request.method == 'POST':
        if update_form.is_valid():
            the_book = update_form.save(commit=False)

            if 'book_imgs' in request.FILES:
                the_book.book_imgs = request.FILES['book_imgs']

            if 'book_pdf' in request.FILES:
                the_book.book_pdf = request.FILES['book_pdf']

            the_book.save()
            messages.success(request, 'تغییرات با موفقیت اعمال شد.')
            return HttpResponseRedirect(reverse('account:books_list_page'))

    context = {
        'update_form': update_form,
        'edit_pass_form': edit_pass_form,
    }
    return render(request, 'book/updateBPage.html', context)