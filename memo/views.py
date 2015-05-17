from django.http import JsonResponse
from django.views import generic
from .models import Memo


class JSONResponseMixin(object):
    """
    A mixin that can be used to render a JSON response.
    """
    def render_to_json_response(self, context, **response_kwargs):
        """
        Returns a JSON response, transforming 'context' to make the payload.
        """
        return JsonResponse(
            self.get_data(context),
            **response_kwargs
        )

    def get_data(self, context):
        """
        Returns an object that will be serialized as JSON by json.dumps().
        """
        # Note: This is *EXTREMELY* naive; in reality, you'll need
        # to do much more complex handling to ensure that arbitrary
        # objects -- such as Django model instances or querysets
        # -- can be serialized as JSON.

        if 'object_list' in context:
            return {"data": [i.as_dict() for i in context['object_list']]}
        return context


class MemoListJSON(JSONResponseMixin, generic.ListView):
    model = Memo

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)


class MemoDetailView(generic.DetailView):
    model = Memo
    template_name = 'memo/memo.html'


class MainPageView(generic.TemplateView):
    template_name = 'memo/main.html'
