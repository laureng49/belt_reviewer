from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^home$', views.home),
    url(r'^logout$', views.logout),
    url(r'^add$', views.add),
    url(r'^add_book$', views.add_book),
    url(r'^books/(?P<book_id>\d+)$', views.books, name="books_page"),

    url(r'^users/(?P<review_user_id>\d+)$', views.users),

    url(r'^add_review/(?P<book_id>\d+)$', views.add_review),
    url(r'^delete/(?P<review_id>\d+)$', views.delete),

]



# urlpatterns = [
#     url(r'^$', views.index),
#     url(r'^process_course$', views.process_course),
#     # url(r'^comment_show$', views.comment_show),
#     url(r'^delete/(?P<course_id>\d+)$', views.delete),
#     url(r'^final/(?P<course_id>\d+)$', views.final),
#     url(r'^edit/(?P<course_id>\d+)$', views.edit),
#     url(r'^edit_final/(?P<course_id>\d+)$', views.edit_final),
    # url(r'^comment/(?P<course_id>\d+)$', views.comment, name="comments_page"),
    # url(r'^comment_process/(?P<course_id>\d+)$', views.comment_process),
