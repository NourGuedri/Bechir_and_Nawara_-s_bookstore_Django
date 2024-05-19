from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta


# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)

    def delete(self, *args, **kwargs):
        for book in self.book_set.all():
            book.delete()
        super().delete(*args, **kwargs)
        
    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author)
    cover_picture = models.ImageField(upload_to='covers/', null=True, blank=True)
    def __str__(self):
        return self.title   
    
    def available(self):
        # check for the the book in Borrowing table and use returned method
        borrowings = Borrowing.objects.filter(book=self)
        for borrowing in borrowings:
            print("borrowomasd;lahsdlkjashdkljas")
            print(borrowing.returned())
            if not borrowing.returned():
                return False
        return True 
    

    
class Borrowing (models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    date_borrowed = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.return_date:
            self.return_date = self.date_borrowed + timedelta(days=15)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.book.title+" borrowed by "+self.borrower.username
    def returned(self):
        return self.is_returned
