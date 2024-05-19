from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Book, Author, Borrowing
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta

def student_index(request):
        # check if user is staff
    if not request.user.is_authenticated:
        return redirect('login')
    all_books = Book.objects.all()
    # date_to_be_returned contains nows date + 15 days
    return_date = timezone.now() + timedelta(days=15)
    context = {
        'all_books': all_books,
        'return_date': return_date,
    }
    return render(request, 'student/index.html',context)



def student_borrow(request,book_id):
    try:
        book = get_object_or_404(Book, pk=book_id)
        # check if the book is available
        if book.available():
            # create a new borrowing
            borrowing = Borrowing(book=book, borrower=request.user, date_borrowed=timezone.now())
            borrowing.save()
            messages.success(request, 'Book borrowed successfully')
        else:
            messages.error(request, 'Book is not available')

        return redirect('student_index')
    except Exception as e:
        return HttpResponse(f"An error occurred: {e}")