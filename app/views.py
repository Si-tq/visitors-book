from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import render
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.http import is_safe_url
from django.views import generic
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters

from .forms import CreatePost, CustomUserCreationForm
from .models import Post


class UserDetail(generic.DetailView):
    """
    User profile view.
    """
    model = Post
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        """
        Context data overridden.
        """

        context = super(UserDetail, self).get_context_data(**kwargs)

        try:
            user = User.objects.get(pk=self.kwargs.get("pk"))
            post = Post.objects.filter(author=user, status=1)
        except User.DoesNotExist:
            user = None
            post = None

        context["post_list"] = post

        context["user"] = user

        return context


class PostList(generic.ListView):
    """
    View for all posts.
    """

    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        """
        Context data overridden.
        """
        context = super(PostList, self).get_context_data(**kwargs)
        context['form'] = CreatePost()

        return context

    def post(self, request, *args, **kwargs):
        form = CreatePost(request.POST)
        queryset = self.get_queryset()

        if form.is_valid():
            instance = form.save(commit=False)
            instance.title = request.POST.get('title')
            instance.slug = slugify(request.POST.get('title'))
            instance.content = request.POST.get('content')
            instance.author = request.user
            instance.status = 0
            instance.save()
            messages.success(request, 'Post added! Need to wait for admin acceptation to see it live!')
            reload_time = 1
        else:
            form = CreatePost()
            messages.error(request, "Error with adding a post! Probably post with this title exists.")
            reload_time = None
        return render(request, self.template_name, {'post_list': queryset, 'form': form, 'reload_time': reload_time})


class PostDetail(generic.DetailView):
    """
    View for post detail.
    """

    slug_field = 'slug'
    model = Post
    template_name = 'post_detail.html'


class SearchView(generic.ListView):
    """
    Search view.
    """

    template_name = "search_results.html"
    model = Post
    context_object_name = "posts"
    paginate_by = 10

    def get_search_query(self):
        """
        Returns search query from input.
        """

        return self.request.GET.get("search_query", [])

    def get_context_data(self, **kwargs):
        """
        Overridden context data.
        """

        context = super(SearchView, self).get_context_data()

        context["search_query"] = self.get_search_query()
        context["is_search_results"] = True

        return context

    def get_queryset(self):
        """
        Returns search result if search input used.
        """

        search_query = self.get_search_query()

        if search_query:
            queryset = (
                self.model.objects.filter(
                    Q(content__icontains=search_query) |
                    Q(author__username__icontains=search_query) |
                    Q(title__icontains=search_query)
                )
                    .select_related("author")
                    .order_by("-pk")
            )
        else:
            queryset = self.model.objects.none()

        return queryset


class SignUpView(generic.edit.CreateView):
    """
    Signup view.
    """

    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


class LoginView(generic.FormView):
    """
    Login view.
    """
    success_url = ''
    form_class = AuthenticationForm
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        auth_login(self.request, form.get_user())

        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, allowed_hosts=self.request.get_host()):
            redirect_to = self.success_url

        return redirect_to


class LogoutView(generic.RedirectView):
    """
    Logout view.
    """

    url = 'login/'

    def get(self, request, *args, **kwargs):
        auth_logout(request)
        return super(LogoutView, self).get(request, *args, **kwargs)
