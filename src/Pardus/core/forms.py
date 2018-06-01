#
# Documentation Django sur les formulaires :
# https://docs.djangoproject.com/fr/2.0/topics/db/models/
#

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User

from core.models import Comment, ContactMessage


class ContactForm(forms.ModelForm):
    """
        Formulaire pour la page de contact
    """

    class Meta:
        model = ContactMessage
        fields = ["first_name", "last_name", "email", "subject", "message"]
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@service.com", "value": ""}),
            "subject": forms.TextInput(attrs={"class": "form-control", "placeholder": "Sujet"}),
            "message": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Entrez votre commentaire ici...", "rows": 3})
        }


class LoginForm(AuthenticationForm):
    """
        Formulaire pour la page de connexion
    """

    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}), max_length=30,
        label="Nom d'utilisateur")
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}),
        label="Mot de passe")
    remember_me = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}),
                                     label="Se souvenir de moi", required=False)


class RegisterForm(forms.ModelForm):
    """
        Formulaire pour la page d'inscription
    """

    class Meta:
        model = User
        fields = ["username", "email", "password"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom d'utilisateur"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@service.com"}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"})
        }

    email_confirm = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@service.com"}), max_length=100,
        label="Confirmer l'adresse e-mail")
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}),
        label="Confirmer le mot de passe")
    terms = forms.BooleanField(widget=forms.CheckboxInput(attrs={"class": "custom-control-input"}))

    def clean_email_confirm(self):
        """
            Fonction pour vérifier que le contenu du champ de l'adresse email et du champ de confirmation sont valides et
            cohérents

            Retourne une erreur si le contenu du champ "email" et du champ "email_confirm" n'ont pas la même valeur
        """

        email = self.cleaned_data.get("email")
        email_confirm = self.cleaned_data.get("email_confirm")

        if email and email_confirm and email_confirm != email:
            self.add_error(
                "email_confirm",
                "L'email ne correspond pas"
            )

        return email_confirm

    def clean_password_confirm(self):
        """
            Fonction pour vérifier que le contenu du champ du mot de passe et du champ de confirmation sont valides et
            cohérents

            Retourne une erreur si le contenu du champ "password" et du champ "password_confirm" n'ont pas la même valeur
        """

        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm and password_confirm != password:
            self.add_error(
                "password_confirm",
                "Le mot de passe ne correspond pas"
            )

        return password_confirm

    def save(self, commit=True):
        """
            Surcharge de la méthode "save"

            Récupère l'objet User à l'aide de la méthode "save" sans envoyer les données, défini le mot de passe de
            l'utilisateur, sauvegarde les données et retourne l'objet User

            L'utilisation de la méthode "set_password" pour définir le mot de passe d'un objet User est obligatoire : en
            effet, le mot de passe est hashé pour ne pas qu'il ai une valeur visible dans la base de données, voir
            documentation sur le hashage des mots de passes : https://docs.djangoproject.com/fr/2.0/topics/auth/passwords/

            Documentation Django sur la méthode "save" :
            https://docs.djangoproject.com/fr/2.0/topics/forms/modelforms/#the-save-method
        """

        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])

        if commit:
            user.save()

        return user


class CommentForm(forms.ModelForm):
    """
        Formulaire pour l'entrée de commentaires
    """

    class Meta:
        model = Comment
        fields = ["content", ]
        widgets = {
            "content": forms.Textarea(
                attrs={"class": "form-control", "placeholder": "Entrez votre commentaire ici...", "rows": 3})
        }


class SettingsForm(forms.ModelForm):
    """
        Formulaire pour la page des paramètres utilisateurs
    """

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password"]
        labels = {
            "email": "Nouvelle adresse e-mail",
            "password": "Nouveau mot de passe"
        }
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Prénom"}),
            "last_name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Nom"}),
            "email": forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@service.com", "value": ""}),
            "password": forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"})
        }

    username = forms.CharField(disabled=True)
    email_confirm = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control", "placeholder": "email@service.com"}), max_length=100,
        label="Confirmer la nouvelle adresse e-mail", required=False)
    password_confirm = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}),
        label="Confirmer le nouveau mot de passe", required=False)
    password_save = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "placeholder": "Mot de passe"}),
        label="Mot de passe actuel")

    def __init__(self, *args, **kwargs):
        super(SettingsForm, self).__init__(*args, **kwargs)
        self.fields["password"].required = False

    def clean_email_confirm(self):
        """
            Fonction pour vérifier que le contenu du champ de l'adresse email et du champ de confirmation sont valides et
            cohérents si le champ de l'adresse email est défini

            Retourne une erreur si le contenu du champ "email" et du champ "email_confirm" n'ont pas la même valeur
        """

        email = self.cleaned_data.get("email")
        email_confirm = self.cleaned_data.get("email_confirm")

        if email and email_confirm != email:
            self.add_error(
                "email_confirm",
                "L'email ne correspond pas"
            )

        return email_confirm

    def clean_password_confirm(self):
        """
            Fonction pour vérifier que le contenu du champ du mot de passe et du champ de confirmation sont valides et
            cohérents si le champ du mot de passe est défini

            Retourne une erreur si le contenu du champ "password" et du champ "password_confirm" n'ont pas la même valeur
        """

        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        if password and password_confirm != password:
            self.add_error(
                "password_confirm",
                "Le mot de passe ne correspond pas"
            )

        return password_confirm

    def clean_password_save(self):
        """
            Fonction pour vérifier que le contenu du champ du mot de passe et le mot de passe actuel de l'utilisateur sont
            valides et cohérents

            Retourne une erreur si le contenu du champ "password_save" et du mot de passe actuel de l'utilisateur n'ont
            pas la même valeur
        """

        if not self.instance.check_password(self.cleaned_data["password_save"]):
            self.add_error(
                "password_save",
                "Le mot de passe ne correspond pas au mot de passe actuel"
            )

    def save(self, commit=True):
        """
            Surcharge de la méthode "save"

            Récupère l'objet User à l'aide de la méthode "save" sans envoyer les données, puis :
            - Défini la propriété "first_name" de l'objet User si le champ "first_name" est défini
            - Défini la propriété "last_name" de l'objet User si le champ "last_name" est défini
            - Défini la propriété "email" de l'objet User si le champ "email" est défini
            - Défini le mot de passe de l'objet User si le champ "password" est défini
            - Puis,
            sauvegarde les données et retourne l'objet User
        """

        user = super(SettingsForm, self).save(commit=False)

        if self.cleaned_data["first_name"]:
            user.save(update_fields=["first_name"])
        if self.cleaned_data["last_name"]:
            user.save(update_fields=["last_name"])
        if self.cleaned_data["email"]:
            user.save(update_fields=["email"])
        if self.cleaned_data["password"]:
            user.set_password(self.cleaned_data["password"])
            user.save(update_fields=["password"])

        return user
