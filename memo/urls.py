from django.conf.urls import url
from .views import MemoDetailView

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)$', MemoDetailView.as_view()),
]