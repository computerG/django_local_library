from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import get_object_or_404, render

from .models import Book, Author, BookInstance, Genre
from django.views import generic

import datetime

from django.views.generic.edit import CreateView, UpdateView, DeleteView


from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

from catalog.forms import RenewalBookForm
# Create your views here.

def index (request):
    '''View function for the home page of site'''
        #Generrate counts of some of the main objects
    
    #Number of visits to the home page
    num_visits = request.session.get('num_visits',0)
    request.session['num_visits'] = num_visits + 1

    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()


    #Available books (status='a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    #The all() is implie by default.

    num_authors =Author.objects.count()

    context = {
        'num_visits':num_visits,
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors

    }

    return render(request,'catalog/index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by= 2
    context_book_list = 'book_list'
    queryset = Book.objects.all()
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get the 5 books containing the title war
    template_name = 'catalog/book_list.html' #the template location


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = 'catalog/book_detail.html'

class AuthorListView(generic.ListView):
    model = Author
    paginate_by= 2
    context_author_list = 'author_list'
    queryset = Author.objects.all()
    #queryset = Book.objects.filter(title__icontains='war')[:5] # Get the 5 books containing the title war
    template_name = 'catalog/author_list.html' #the template location

class AuthorDetailView(generic.DetailView):
    model = Author
   
    template_name = 'catalog/author_detail.html'

class LoanedBooksByUserListView(LoginRequiredMixin,generic.ListView):

    """Generic class-based view listing books on loan to current user"""

    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):

        return (
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )

class BooksBorrowedListView(LoginRequiredMixin,PermissionRequiredMixin,generic.ListView):

    """Generic class-based view listing books on loan to current user"""
    permission_required = 'catalog.can_mark_returned'
   
    model = BookInstance
    template_name = 'catalog/book_borrowed_list.html'
    paginate_by = 10

    def get_queryset(self):

        return (
            BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
        )


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewalBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('borrowed-books'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class AuthorCreate(CreateView):
    model = Author
    fields = ['first_name', 'last_name','date_of_birth', 'date_of_death']
    initial = {'date_of-death': '11/06/2020'}

class AuthorUpdate(UpdateView):
    model = Author
    fields = ['first_name', 'last_name','date_of_birth', 'date_of_death']

class AuthorDelete(DeleteView):
    model = Author
    success_url = reverse_lazy('authors')


class BookCreate(CreateView):
    model = Book
    fields = ['title', 'author','summary', 'isbn','genre']
    

class BookUpdate(UpdateView):
    model = Book
    fields = ['title', 'author','summary', 'isbn','genre']

class BookDelete(DeleteView):
    model = Book
    success_url = reverse_lazy('books')
