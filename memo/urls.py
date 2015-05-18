from django.conf.urls import url
from .views import MemoListJSON
from .views import MemoDetailView, MemoDeleteView

urlpatterns = [
    url(r'^get_all/$', MemoListJSON.as_view()),
    url(r'^(?P<pk>[0-9]+)$', MemoDetailView.as_view()),
    url(r'^(?P<pk>[0-9]+)/del$', MemoDeleteView.as_view()),
]