from django.http import JsonResponse, Http404, HttpResponseNotFound
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

    def render_to_response(self, context, **response_kwargs):
        obj = self.get_object()

        if not obj.published:
            raise Http404
        return super(MemoDetailView, self).render_to_response(context, **response_kwargs)


class MemoAPI(JSONResponseMixin, generic.View):
    model = Memo

    def post(self, request):
        item_id = request.POST.get("item_id")
        item = self.model.objects.get(id=item_id)

        operation = request.POST.get("operation")
        if operation == "remove":
            item.delete()
            return self.render_to_json_response({'deleted': True})

        return self.render_to_json_response({'deleted': False})


class MainPageView(JSONResponseMixin, generic.TemplateView):
    template_name = 'memo/main.html'
