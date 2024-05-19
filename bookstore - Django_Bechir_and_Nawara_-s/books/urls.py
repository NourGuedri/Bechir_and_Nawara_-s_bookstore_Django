from django.urls import path
from . import admin_views,student_views


urlpatterns = [

    # admin views
    path('admin',admin_views.admin_index,name='admin_index'),
    path('admin/authors', admin_views.admin_list_authors, name='admin_authors'),
    path('admin/new_book',admin_views.admin_new_book,name='admin_new_book'),
    path('admin/new_author',admin_views.admin_new_author,name='admin_new_author'),
    path('admin/delete_book/<int:book_id>',admin_views.admin_delete_book,name='admin_delete_book'),
    path('admin/delete_author/<int:author_id>',admin_views.admin_delete_author,name='admin_delete_author'),
    path('admin/edit_book/<int:book_id>',admin_views.admin_edit_book,name='admin_edit_book'),
    path('admin/edit_author/<int:author_id>',admin_views.admin_edit_author,name='admin_edit_author'),
    path('admin/borrowings',admin_views.admin_return_book,name='admin_borrowings'),

    # user views
    path('student',student_views.student_index,name='student_index'),
    path('student/borrow/<int:book_id>',student_views.student_borrow,name='student_borrow')


]