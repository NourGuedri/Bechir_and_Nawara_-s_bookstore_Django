from django.shortcuts import render, redirect
from .models import Book, Author, Borrowing
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# Create your views here.
def admin_index(request):
    # check if user is staff
    if not request.user.is_authenticated:
        return redirect('login')
    if not request.user.is_staff:
        return redirect('student_index')
    

    all_books = Book.objects.all()

    return render(request, 'index.html', {'all_books': all_books})


def admin_new_book(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user.is_staff:
        return redirect('student_index')
    if request.method == 'POST':
        title = request.POST.get('title')
        authors = request.POST.getlist('authors')
        cover = request.FILES.get('cover')  # Get the uploaded file

        # get the authors from the list of authors
        book = Book.objects.create(title=title, cover_picture=cover)  # Save the uploaded file
        for author_id in authors:
            author = Author.objects.get(id=author_id)
            book.authors.add(author)
        book.save()
        return redirect('admin_index')
    authors = Author.objects.all()
    # orderby name of author in alphabetical order
    authors = sorted(authors, key=lambda x: x.name)
    return render(request, 'new_book.html', {'authors': authors})

def admin_new_author(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user.is_staff:
        return redirect('student_index')
    if request.method == 'POST':
        name = request.POST.get('name')
        author = Author.objects.create(name=name)
        return redirect('admin_authors')

    return render(request, 'new_author.html')


def admin_delete_book(request, book_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user.is_staff:
        return redirect('student_index')
    book = Book.objects.get(id=book_id)
    book.delete()
    return redirect('admin_index')

def admin_list_authors(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user.is_staff:
        return redirect('student_index')
    authors = Author.objects.all()
    return render(request, 'authors.html', {'authors': authors})


def admin_delete_author(request, author_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user.is_staff:
        return redirect('student_index')
    author = Author.objects.get(id=author_id)
    author.delete()
    return redirect('admin_authors')

def admin_edit_book(request , book_id):
    if not request.user.is_authenticated:
        return redirect('login')
    
    if not request.user.is_staff:
        return redirect('student_index')
    book = Book.objects.get(id=book_id)
    if request.method == 'POST':
        title = request.POST.get('title')
        authors = request.POST.getlist('authors')
        book.title = title
        book.authors.clear()
        for author_id in authors:
            author = Author.objects.get(id=author_id)
            book.authors.add(author)
        book.save()
        return redirect('admin_index')
    authors = Author.objects.all()
    authors = sorted(authors, key=lambda x: x.name)
    return render(request, 'edit_book.html', {'authors': authors, 'book': book})

def admin_edit_author(request, author_id):
    if not request.user.is_staff:
        return redirect('student_index')
    author = get_object_or_404(Author, pk=author_id)
    
    if request.method == 'POST':
        name = request.POST.get('name')
        if name:  # Check if name is not empty
            author.name = name
            author.save()
            return redirect('admin_authors')
        else:
            messages.error(request, 'Name field cannot be empty.')
    return render(request, 'edit_author.html', {'author': author})

def admin_return_book(request):
    user = request.user

    if not user.is_authenticated:
            return redirect('login')
    if not user.is_staff:
        return redirect('student_index')
    if request.method == 'POST':
        borrowing_id = request.POST.get('borrow_id')
        borrowing = Borrowing.objects.get(id=borrowing_id)
        borrowing.is_returned = True
        borrowing.save()
        return redirect('admin_borrowings')    




    date_borrowed = request.GET.get('date_borrowed')
    book_name = request.GET.get('search')

    date_borrowed_start = request.GET.get('date_borrowed_start')
    date_borrowed_end = request.GET.get('date_borrowed_end')
    if date_borrowed:
        
        borrowings = Borrowing.objects.filter(date_borrowed__date=date_borrowed)

    else:
        borrowings = Borrowing.objects.filter(is_returned=False)
    

    if book_name:
        borrowings = borrowings.filter(book__title__icontains=book_name)
    else:
        borrowings = borrowings


    if date_borrowed_start and date_borrowed_end:
        borrowings = borrowings.filter(date_borrowed__range=[date_borrowed_start, date_borrowed_end])

    return render(request, 'borrowings.html', {'borrowings': borrowings})
    