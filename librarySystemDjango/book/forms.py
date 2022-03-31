from .models import Book, Category
from django import forms
from django.core import validators
from django.core.validators import RegexValidator

class AddBookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(AddBookForm, self).__init__(*args, **kwargs)
        self.fields['title'].label = "عنوان"
        self.fields['author'].label = "نویسنده"
        self.fields['translator'].label = "مترجم"
        self.fields['publisher'].label = "نام انتشارات"
        self.fields['category'].label = "دسته بندی"
        self.fields['pages'].label = "تعداد صفحات"
        self.fields['publication_year'].label = "سال انتشار"
        self.fields['available_numbers'].label = "تعداد موجود"
        self.fields['book_imgs'].label = "عکس جلد"
        self.fields['free'].label = "رایگان"
        self.fields['book_pdf'].label = "فایل الکترونیکی کتاب"

    pages = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control left-field',}))
    publication_year = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control left-field',}))
    available_numbers = forms.IntegerField(widget=forms.NumberInput(attrs={'class':'form-control left-field',}))
    title = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control title-field'}))
    author = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control author-field',}))
    translator = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control translator-field',}), required=False)
    publisher = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control publisher-field'}))
    book_imgs = forms.ImageField(widget=forms.FileInput(attrs={'class':'form-control book-imgs-field',}), required=False)
    book_pdf = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control book-pdf-field',}), required=False)


    class Meta:
        model = Book
        exclude = ('available', 'lent_by')