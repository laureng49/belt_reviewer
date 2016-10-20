from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User, Book, Review, Author
# Create your views here.
def index(request):
    return render(request, "belt_review/index.html")

def login(request):
    #either they're good at logging in or not
    if request.method == "POST":
        user = User.objects.login(request.POST)
        if not user:
            messages.error(request, "Invalid login credentials!")
        else:
            request.session['logged_user'] = user.id
            # don't need this, unless I'm calling for messages on my "home" page, but I shouldn't because I just have a welcome {{__ }} thang. : messages.success(request, "Welcome {}!".format(user.alias))
            return redirect('/home')
    return redirect('/')

def register(request):
    if request.method == "POST":
        form_errors = User.objects.validate_user_info(request.POST)

    #if there are errors, throw them into flash:
        if len(form_errors) > 0:
            for error in form_errors:
                messages.error(request, error)
        else:
            #register User
            User.objects.register(request.POST)
            messages.success(request, "You have Successfully registered! Please sign-in to continue")

    return redirect('/')

def home(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    books = Book.objects.all()
    # review = Review.objects.all()
    review = Review.objects.all().order_by("-id")[:3]

    context = {
        'user' : User.objects.get(id=request.session['logged_user']),
        'books': books,
        'review': review
    }
    return render(request, "belt_review/home.html", context)

def add(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    authors = Author.objects.all()
    print authors
    context = {}
    if authors:
        context = {
            "authors": authors
        }
    return render(request, "belt_review/add.html", context)

def add_book(request):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    if request.method == "POST":
        if request.POST['newauthor'] != "":
            print "we want to add an author"
            user = User.objects.get(id=request.session['logged_user'])
            author = Author.objects.create(name=request.POST['newauthor'])
            book = Book.objects.create(title=request.POST['title'], author=author)
            Review.objects.create(user=user, review=request.POST['review'], rating=request.POST['rating'], book=book)

        elif request.POST['author'] != "":
            print "we want to use a author already inside the db"
            user = User.objects.get(id=request.session['logged_user'])
            author = Author.objects.get(id=request.POST['author'])
            book = Book.objects.create(title=request.POST['title'], author=author)
            Review.objects.create(user=user, review=request.POST['review'], rating=request.POST['rating'], book=book)

        if request.POST['newauthor'] == "" and request.POST['author'] == "":
            messages.add_message(request, messages.WARNING, "Please add/select an Author")

        context = {
            "book": book
        }

        return redirect('books_page', book_id=book.id)

def books(request, book_id):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    logged_user = User.objects.get(id=request.session['logged_user'])
    # user = User.objects.get(id=book_id)
    book = Book.objects.get(id=book_id)
    reviews = Review.objects.filter(book_id=book_id)

    context = {
        "book": book,
        "reviews": reviews,
        "logged_user": logged_user,
        # "user": user
    }
    return render(request, "belt_review/books.html", context)

def add_review(request, book_id):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    if request.method == "POST":
        book = Book.objects.get(id=book_id)
        user = User.objects.get(id=request.session['logged_user'])

        Review.objects.create(rating=request.POST['rating'], review=request.POST['review'], book=book, user=user)


    return redirect('books_page', book_id=book_id)



def users(request, review_user_id):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')
    # logged_user = User.objects.get(id=request.session['logged_user'])
    user = User.objects.get(id=review_user_id)
    review_book_titles = Review.objects.filter(book_id=review_user_id)

    rating = Review.objects.filter(user_id=review_user_id)

    if rating > 0:
        rating = len(rating)

    # rating = Review.objects.filter(book_id=review_user_id)

    # books = Book.objects.all()
    # review = Review.objects.filter(user_id=user_id)
    #
    context = {
        "user": user,
        "review": review_book_titles,
        "rating": rating


    #     "logged_user": logged_user,
    }
    return render(request, "belt_review/users.html", context)

def delete(request, review_id):
    if "logged_user" not in request.session:
        messages.error(request, "Gotta login bro")
        return redirect('/')

    review = Review.objects.get(id=review_id)
    book_id = review.book.id

    #delete query
    review.delete()

    return redirect('books_page', book_id=book_id)


def logout(request):
    if 'logged_user' in request.session:
        request.session.pop('logged_user')
    return redirect('/')
