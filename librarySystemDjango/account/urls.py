from . import views
from book import views as book_view
from django.urls import path, include

app_name = 'account'

urlpatterns = [
    path('register/', views.register, name='register_page'),
    path('login/', views.user_login, name='login_page'),
    path('logout/', views.user_logout, name='logout_page'),
    path('myprofile/', views.user_profile, name='profile_page'),
    path('myprofile/delete-profile/<str:member_username>/', views.delete_profile_pic, name='del_pic_page'),
    path('myprofile/edit-password/', views.edit_password, name='edit_pass_page'),
    path('myprofile/mybooks/', views.show_favorite_books, name='favorite_page'),
    path('myprofile/mybooks/delete/<str:book_title>', views.del_from_favorites, name='del_favorite_page'),
    path('myprofile/services/', views.show_subscription, name='subs_services_page'),
    path('myprofile/subscription-records/', views.show_subs_record, name='subs_records_page'),
    path('bank/shaparak/<str:subs_type>/<int:num_month>', views.buy_subscription, name='bank_page'),
    path('myprofile/del-account', views.delete_user_acc, name='delete_page'),
    path('list-admins/', views.list_admins, name='admins_list_page'),
    path('list-users/', views.list_users, name='users_list_page'),
    path('list-users/<str:member_username>/', views.dedicate_book, name='add_dedicated_page'),
    path('list-users/delete-sub/<str:the_username>/', views.delete_subscription, name='delete_subs'),
    path('list-books/', views.list_books, name='books_list_page'),
    path('del-book/<str:book_title>/', views.del_book, name='delete_book'),
    path('lend-book/', views.book_lending, name='lend_book'),
    path('list_loans/', views.list_lent_books, name='loan_list_page'),
    path('list_loans/return/<member_username>/<book_title>/', views.return_book, name='return_loan'),
    path('update-book/<str:book_title>/', book_view.update_book, name='update_book'),
    path('del-user/<slug:username_to_del>/', views.delete_user_by_admin, name='delete_user'),
    path('buy-sub/<slug:username_to_buy>/', views.set_subscription, name='buysub_page'),
    path('promote/<str:the_username>/', views.promote_into_staff, name='promotion_page'),
]