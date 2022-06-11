from django.shortcuts import render

# Create your views here.

from .models import Book, Author, BookInstance, Genre


def index(request):
    """View function for home page of site."""
    # Generate counts of some of the main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    # Available copies of books
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()  # The 'all()' is implied by default.

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits+1

    # Render the HTML template index.html with the data in the context variable.
    return render(
        request,
        'index.html',
        context={'num_books': num_books, 'num_instances': num_instances,
                 'num_instances_available': num_instances_available, 'num_authors': num_authors,
                 'num_visits': num_visits},
    )


from django.views import generic


class BookListView(generic.ListView):
    """Generic class-based view for a list of books."""
    model = Book
    paginate_by = 10



class BookDetailView(generic.DetailView):
    """Generic class-based detail view for a book."""
    model = Book


class AuthorListView(generic.ListView):
    """Generic class-based list view for a list of authors."""
    model = Author
    paginate_by = 10



class AuthorDetailView(generic.DetailView):
    """Generic class-based detail view for an author."""
    model = Author


from django.contrib.auth.mixins import LoginRequiredMixin


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


# Added as part of challenge!
from django.contrib.auth.mixins import PermissionRequiredMixin


class LoanedBooksAllListView(PermissionRequiredMixin, generic.ListView):
    """Generic class-based view listing all books on loan. Only visible to users with can_mark_returned permission."""
    model = BookInstance
    permission_required = 'catalog.can_mark_returned'
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')


from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
import datetime
from django.contrib.auth.decorators import login_required, permission_required

# from .forms import RenewBookForm
from catalog.forms import RenewBookForm


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    """View function for renewing a specific BookInstance by librarian."""
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('all-borrowed'))

    # If this is a GET (or any other method) create the default form
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Author


class AuthorCreate(PermissionRequiredMixin, CreateView):
    model = Author
    fields = ['first_name', 'last_name', 'date_of_birth', 'date_of_death']
    initial = {'date_of_death': '11/06/2020'}
    permission_required = 'catalog.can_mark_returned'


class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    model = Author
    fields = '__all__' # Not recommended (potential security issue if more fields added)
    permission_required = 'catalog.can_mark_returned'


class AuthorDelete(PermissionRequiredMixin, DeleteView):
    model = Author
    success_url = reverse_lazy('authors')
    permission_required = 'catalog.can_mark_returned'


# Classes created for the forms challenge
class BookCreate(PermissionRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookUpdate(PermissionRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'summary', 'isbn', 'genre', 'language']
    permission_required = 'catalog.can_mark_returned'


class BookDelete(PermissionRequiredMixin, DeleteView):
    model = Book
    success_url = reverse_lazy('books')
    permission_required = 'catalog.can_mark_returned'


from django.core.paginator import Paginator
from django.core.cache import cache
import requests
from .forms import SearchCocktailForm

@login_required
def SearchCocktail(request):
    args = {}
    # keyword = request.GET.get('keyword')
    # if keyword is not None and keyword != "":
    #     cocktails = cache.get('SearchCocktail_%s' % keyword)
    #     if not cocktails:
    #         response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php', params={'s': keyword})
    #         searchresult = response.json()
    #         cocktails = searchresult['drinks']
    #         cache.set('SearchCocktail_%s' % keyword , cocktails, 120)
    #     if cocktails:
    #         paginator = Paginator(cocktails, 2)
    #         page_number = request.GET.get('page')
    #         if page_number is None:
    #             page_number = 1
    #         page_obj = paginator.get_page(page_number)
    #         page_obj.adjusted_elided_pages = paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1)
    #         is_paginated = True if paginator.num_pages > 1 else False
    #         #print(len(list(paginator.get_elided_page_range(page_number, on_each_side=2, on_ends=1))), file=sys.stderr)
    #         # print(page_obj, file=sys.stderr)
    #         # print(page_obj.object_list, file=sys.stderr)
    #         if page_obj.has_other_pages():
    #             args['is_custom_paginated'] = True
    #             args['current_get_value'] = [{'keyword' : keyword}]
    #         args['page_obj'] = page_obj
    #     form = SearchCocktailForm(initial={'keyword': keyword, })
    if request.method == 'POST':
        form = SearchCocktailForm(request.POST)
        # print('is POST', file=sys.stderr)
        if form.is_valid():
            # print('is_valid', file=sys.stderr)
            keyword = form.cleaned_data['keyword']
            # print(keyword, file=sys.stderr)
            page = form.cleaned_data['page']
            # print(page, file=sys.stderr)
            cocktails = cache.get('SearchCocktail_%s' % keyword)
            if not cocktails:
                response = requests.get('https://www.thecocktaildb.com/api/json/v1/1/search.php', params={'s': keyword})
                cocktails = response.json()['drinks']
                cache.set('SearchCocktail_%s' % keyword , cocktails, 120)
            if cocktails:
                paginator = Paginator(cocktails, 3)
                page_obj = paginator.get_page(page)
                args['page_obj'] = page_obj
                args['is_paginated'] = True if paginator.num_pages > 1 else False
                args['cocktail_list'] = page_obj.object_list
                form = SearchCocktailForm(initial={'keyword': keyword, 'page': page , })
            else:
                form = SearchCocktailForm(initial={'keyword': keyword,})
        # else:
        #     print(form.errors, file=sys.stderr)
    else:
        form = SearchCocktailForm()
    args['form'] = form
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'catalog/SearchCocktail.html', args)