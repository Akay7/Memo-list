from django.conf.urls import url
from .views import MemoList
from .views import MemoDetailView, MemoAPI, CategoryList

urlpatterns = [
    url(r'^get_all/$', MemoList.as_view()),
    url(r'^category_all/$', CategoryList.as_view()),
    url(r'^(?P<pk>[0-9]+)$', MemoDetailView.as_view()),
    url(r'^api/$', MemoAPI.as_view()),
]