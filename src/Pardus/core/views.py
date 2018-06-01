#
# Documentation Django sur l'écriture des vues (classique) :
# https://docs.djangoproject.com/fr/2.0/topics/http/views/
#

import datetime

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import CreateView, DetailView, ListView
from django.views.generic.edit import UpdateView, FormMixin

from core.forms import CommentForm, ContactForm, LoginForm, RegisterForm, SettingsForm
from core.models import Article, Category, Comment, ContactMessage


class Home(ListView):
    """
        Vue pour la page d'accueil

        Documentation Django de la vue générique "ListView" :
        https://docs.djangoproject.com/fr/2.0/ref/class-based-views/generic-display/#listview
    """

    model = Article
    template_name = "core/home.html"
    context_object_name = "articles"
    paginate_by = 5


class ArticleRead(FormMixin, DetailView):
    """
       Vue pour l'affichage d'un article

       Documentation Django de la vue générique "DetailView" :
       https://docs.djangoproject.com/fr/2.0/ref/class-based-views/generic-display/#listview

       Documentation Django de l'utilisation de la vue générique "DetailView" avec la mixin "FormMixin" :
       https://docs.djangoproject.com/fr/2.0/topics/class-based-views/mixins/#using-formmixin-with-detailview
    """

    model = Article
    form_class = CommentForm
    template_name = "core/article.html"
    context_object_name = "article"

    def get_success_url(self):
        """
            Surcharge de la méthode "get_sucess_url" de la mixin "FormMixin"

            Documentation Django de la méthode "get_sucess_url" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_success_url
        """

        return reverse("article_read", kwargs={"id": self.object.id, "slug": self.object.slug})

    def get_context_data(self, **kwargs):
        """
            Surcharge de la méthode "get_context_data"

            Retourne en plus du contexte par défaut :
            - Le formulaire CommentForm
            - Tous les objets Comment

            Documentation Django de la méthode "get_content_data" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_context_data

            Documentation Django sur la surcharge de la méthode "get_context_data" :
            https://docs.djangoproject.com/fr/2.0/topics/class-based-views/generic-display/#adding-extra-context
        """

        context = super(ArticleRead, self).get_context_data(**kwargs)
        context["form"] = self.get_form()
        context["comments"] = Comment.objects.filter(article=self.object)
        return context

    def post(self, request, *args, **kwargs):
        """
            Surcharge de la méthode "post"

            Retourne :
            - Les données du formulaire CommentForm si les données sont valides
            - Les données (non-exploitées) et les erreurs du formulaire CommentForm si les données sont invalides

            Documentation Django de la méthode "post" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.ProcessFormView.post
        """

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        """
            Surcharge de la méthode "form_valid"

            Créé un commentaire avec la méthode "create" de Comment.objects à partir des données valides du formulaire
            CommentForm

            Documentation Django de la méthode "form_valid" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.form_valid
        """

        Comment.objects.create(article=self.object, author=self.request.user, content=form.cleaned_data["content"])
        return super(ArticleRead, self).form_valid(form)


class DateFilter(ListView):
    """
        Vue pour la page d'articles filtrés par date
    """

    model = Article
    template_name = "core/date_filter.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        """
            Surcharge de la méthode "get_queryset"

            Retourne :
            - Tous les articles filtrés par l'année et le mois de la date spécifiée dans l'URL

            Documentation Django de la méthode "get_queryset" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_queryset
        """

        return Article.objects.filter(date__year=self.kwargs["year"], date__month=self.kwargs["month"])

    def get_context_data(self, **kwargs):
        """
            Surcharge de la méthode "get_context_data"

            Retourne en plus du contexte par défaut :
            - La date de type datetime
        """

        context = super(DateFilter, self).get_context_data(**kwargs)
        date = str(self.kwargs["year"]) + "-" + str(self.kwargs["month"])
        context["date"] = datetime.datetime.strptime(date, "%Y-%m")
        return context


class Categories(ListView):
    """
        Vue pour la page des catégories
    """

    model = Category
    template_name = "core/categories.html"
    context_object_name = "categories"
    paginate_by = 0


class CategoriesFilter(ListView):
    """
        Vue pour la page d'articles filtrés par catégorie
    """

    model = Article
    template_name = "core/categories_filter.html"
    context_object_name = "articles"
    paginate_by = 5

    def get_queryset(self):
        """
            Surcharge de la méthode "get_queryset"

            Retourne :
            - Tous les articles filtrés par la catégorie spécifiée dans l'URL
        """

        return Article.objects.filter(categories__id=self.kwargs["id"])

    def get_context_data(self, **kwargs):
        """
            Surcharge de la méthode "get_context_data"

            Retourne en plus du contexte par défaut :
            - La catégorie spécifié dans l'URL de type Category
        """

        context = super(CategoriesFilter, self).get_context_data(**kwargs)
        context["category"] = Category.objects.get(id=self.kwargs["id"])
        return context


class Contact(CreateView):
    """
        Vue pour la page de contact

        Documentation Django de la vue générique "CreateView" :
        https://docs.djangoproject.com/fr/2.0/ref/class-based-views/generic-editing/#django.views.generic.edit.CreateView
    """

    model = ContactMessage
    form_class = ContactForm
    template_name = "core/contact.html"
    success_url = "/contact/"

    def get_initial(self):
        """
            Surcharge de la méthode "get_initial"

            Retourne en plus de l'initial par défaut :
            - Pré-remplis les champs "first_name" et "last_name" si un utilisateur est connecté et qu'il a spécifié ces
              paramètres
            - Pré-remplis le champ "email" si un utilisateur est connecté

            Documentation Django sur la méthode "get_initial" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-editing/#django.views.generic.edit.FormMixin.get_initial
        """

        initial = super(Contact, self).get_initial()
        if self.request.user.is_authenticated:
            user = self.request.user

            if user.first_name:
                initial["first_name"] = user.first_name
            if user.last_name:
                initial["last_name"] = user.last_name
            initial["email"] = user.email

        return initial

    def get_success_url(self):
        messages.success(self.request, "Le message a été envoyé avec succès.")
        return super(Contact, self).get_success_url()


class Login(LoginView):
    """
        Vue pour la page de connexion

        Documentation Django de la vue générique "LoginView" :
        https://docs.djangoproject.com/fr/2.0/topics/auth/default/#django.contrib.auth.views.LoginView
    """

    authentication_form = LoginForm
    template_name = "core/login.html"
    redirect_authenticated_user = True


class Register(CreateView):
    """
       Vue pour la page de connexion
    """

    model = User
    form_class = RegisterForm
    template_name = "core/register.html"
    success_url = "/"

    def get(self, request, *args, **kwargs):
        """
            Surcharge de la méthode "get"

            Retourne :
            - Redirige vers la page d'accueil si un utilisateur connecté accède à la page
        """

        if self.request.user.is_authenticated:
            return redirect(reverse("home"))

        return super(Register, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        """
            Surcharge de la méthode "form_valid"

            Connecte l'utilisateur après son inscription
        """

        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user_login = authenticate(username=username, password=password)
        login(self.request, user_login)

        return super(Register, self).form_valid(form)


class Profile(ListView):
    """
        Vue pour la page de profil d'un utilisateur
    """

    model = Article
    template_name = "core/profile.html"
    context_object_name = "articles"
    paginate_by = 1

    def get(self, request, *args, **kwargs):
        if not self.request.user.is_authenticated:
            if not kwargs["id"]:
                return redirect("/login/?next=/profile/")
        return super(Profile, self).get(request, *args, **kwargs)

    def get_profile(self):
        """
            Méthode créée

            Retourne :
            - L'utilisateur spécifié dans l'URL si c'est le cas
            - L'utilisateur connecté si aucun utilisateur n'est spécifié dans l'URL
        """

        if self.request.user.id:
            if self.kwargs["id"]:
                return get_object_or_404(User, id=self.kwargs["id"])
            else:
                return get_object_or_404(User, id=self.request.user.id)
        else:
            if self.kwargs["id"]:
                return get_object_or_404(User, id=self.kwargs["id"])

    def get_queryset(self):
        """
            Surcharge de la méthode "get_queryset"

            Retourne :
            - Tous les articles filtrés par l'utilisateur (auteur) spécifié dans l'URL
        """

        return Article.objects.filter(author__id=self.get_profile().id)

    def get_context_data(self, **kwargs):
        """
            Surcharge de la méthode "get_context_data"

            Retourne en plus du contexte par défaut :
            - Tous les articles filtrés par l'utilisateur (auteur) spécifié dans l'URL
        """

        context = super(Profile, self).get_context_data(**kwargs)
        context["user"] = User.objects.get(id=self.get_profile().id)
        return context


class Settings(LoginRequiredMixin, UpdateView):
    """
        Vue pour la page des paramètres utilisateurs
    """

    model = User
    form_class = SettingsForm
    template_name = "core/settings.html"

    def get_initial(self):
        """
            Surcharge de la méthode "get_initial"

            Retourne en plus de l'initial par défaut :
            - Vide le champ pré-remplis "email"
        """

        initial = super(Settings, self).get_initial()
        initial["email"] = None
        return initial

    def get_object(self, queryset=None):
        """
            Surcharge de la méthode "get_initial"

            Retourne :
            - L'utilisateur connecté

            Documentation Django sur la méthode "get_object" :
            https://docs.djangoproject.com/fr/2.0/ref/class-based-views/mixins-single-object/#django.views.generic.detail.SingleObjectMixin.get_object
        """

        return get_object_or_404(User, pk=self.request.user.id)

    def get_success_url(self):
        """
            Surcharge de la méthode "get_success_url"

            Retourne :
            - Redirige vers la page "settings"
        """

        messages.success(self.request, "Les paramètres ont été sauvegardés avec succès.")
        return reverse("settings")


def search(request):
    """
        Vue (classique) pour la page de recherche

        Documentation Django sur l'écriture de vues :
        https://docs.djangoproject.com/fr/2.0/topics/http/views/
    """

    search_text = request.GET.get("search", "")
    articles = Article.objects.filter(title__contains=search_text)
    categories = Category.objects.filter(name__contains=search_text)
    users = User.objects.filter(
        Q(username__contains=search_text) | Q(first_name__contains=search_text) | Q(last_name__contains=search_text))

    return render(request, "core/search.html", locals())
