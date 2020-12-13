from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView

from recipes.utils import validate_session_basket
from users.forms import CreationForm


class SignUpView(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'


class CustomLoginView(LoginView):
    def form_valid(self, form):
        basket_for_session = self.request.session.get('basket')
        if basket_for_session:
            recipes_list = validate_session_basket(self.request,
                                                   basket_for_session)
            user = form.get_user()
            for recipe in recipes_list:
                user.basket.append(recipe)
            try:
                self.request.session.pop('basket')
                self.request.session.pop('basket_len')
            except KeyError:
                pass

        return super().form_valid(form)
