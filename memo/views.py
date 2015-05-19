from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse, Http404
from django.views import generic
from .models import Memo, Category


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
            if context['object_list'] is None:
                return {'data': [], 'success': True}
            return {"data": [i.as_dict() for i in context['object_list']], 'success': True}

        return context


class MemoList(JSONResponseMixin, generic.ListView):
    model = Memo

    def get_queryset(self):
        if self.request.user.id:
            return self.model.objects.filter(owner=self.request.user)

    def render_to_response(self, context, **response_kwargs):
        return self.render_to_json_response(context, **response_kwargs)

class CategoryList(JSONResponseMixin, generic.ListView):
    model = Category

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
        if request.user.is_authenticated():
            values = {key: request.POST[key] for key in
                      ["id", "title", "text", "created", "category", "chosen", "published"]
                      if request.POST.get(key, None) is not None and request.POST[key] != ''}
            values.update({key: True for key in ["chosen", "published"]
                           if values.get(key, None) == 'on'})
            values.update({key: Category.objects.get() for key in ["category"]
                           if request.POST.get(key, None)})
            values.update({'owner': request.user})

            if values.get('id', None) and self.model.objects.filter(
                    id=values['id'], owner=request.user).first():
                operation = request.POST.get("operation")
                if operation == "remove":
                    self.model.objects.get(id=values['id']).delete()
                    return self.render_to_json_response({'success': True})
                if operation == "read":
                    obj = self.model.objects.get(id=values['id'])
                    print(obj.as_dict())
                    return self.render_to_json_response({'data': obj.as_dict(), 'success': True})
                else:
                    self.model.objects.filter(id=values['id']).update(**values)
                    return self.render_to_json_response({'success': True})

            elif values.get('id', None):
                return self.render_to_json_response({
                    'success': False,
                    'errormsg': "You can't get access to items of another user"
                })

            else:
                a = self.model(**values)
                a.save()
                print(type(a))
                return self.render_to_json_response({'success': True})
        else:
            return self.render_to_json_response({
                'success': False, 'errormsg': 'You not authenticated!'
            })

class AuthAPI(JSONResponseMixin, generic.View):
    def post(self, request):
        operation = request.POST.get("operation")
        username = request.POST.get('username')
        password = request.POST.get('password')

        if operation == "login":
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return self.render_to_json_response(
                        {'username': username, 'success': True}
                    )
            return self.render_to_json_response(
                {'username': username, 'success': False,
                 'errormsg': 'Please input correct User name and Login'}
            )
        if operation == "logout":
            logout(request)
            return self.render_to_json_response(
                {'success': True}
            )

        if operation == "register":
            try:
                User.objects.get(username=username)
                return self.render_to_json_response({
                    'username': username, 'success': False,
                    'errormsg': 'User with this name already registered'
                })
            except ObjectDoesNotExist:
                user = User.objects.create_user(
                    username=username, password=password)
                user.save()
                return self.render_to_json_response(
                    {'username': username, 'success': True}
                )


class MainPageView(JSONResponseMixin, generic.TemplateView):
    template_name = 'memo/main.html'
