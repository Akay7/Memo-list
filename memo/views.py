from django.views import generic
from .models import Memo


class MemoDetailView(generic.DetailView):
    model = Memo
    template_name = 'memo/memo.html'