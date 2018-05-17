#
# Documentation Django sur les modèles :
# https://docs.djangoproject.com/fr/2.0/topics/db/models/
#

import os
from uuid import uuid4

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class ContactMessage(models.Model):
    """
        Modèle pour les messages envoyés par le formulaire de contact
    """

    first_name = models.CharField(max_length=30, verbose_name="Prénom")
    last_name = models.CharField(max_length=30, verbose_name="Nom")
    email = models.EmailField(max_length=100, verbose_name="Adresse e-mail")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date d'envoi")
    subject = models.CharField(max_length=200, verbose_name="Sujet")
    message = models.TextField(verbose_name="Message")

    def __str__(self):
        """
            Documentation Django sur la méthode "__str__" :
            https://docs.djangoproject.com/fr/2.0/ref/models/instances/#str
        """

        return self.email

    class Meta:
        """
            Documentation Django sur la classe Meta (Modèle) :
            https://docs.djangoproject.com/fr/2.0/topics/db/models/#meta-options
        """

        verbose_name = "message"
        ordering = ["-date"]


def category_image(instance, file_name):
    """
        Fonction pour générer le chemin des images des catégories

        Récupère l'instance et affecte la valeur à une variable avec la propriété "name" de l'instance si elle est disponible,
        sinon affecte un UUID généré, puis retourne la variable
    """

    upload_to = "categories/"
    # Récupère l'extension du fichier (JPG, PNG, ...)
    file_type = file_name.split(".")[-1]
    if instance.name:
        file_name = "{}.{}".format(instance.name, file_type)
    else:
        file_name = "{}.{}".format(uuid4().hex, file_type)
    # Défini le chemin complet depuis la racine du projet
    file_path = "uploads/" + upload_to + file_name
    # Vérifie si un fichier existe déja et si oui, le supprime
    if os.path.isfile(file_path):
        os.remove(file_path)
    return os.path.join(upload_to, file_name)


class Category(models.Model):
    """
        Modèle pour les catégories
    """

    name = models.CharField(max_length=40, verbose_name="Nom")
    image = models.ImageField(upload_to=category_image, verbose_name="Image de fond", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "catégorie"
        ordering = ["name"]


def article_image(instance, file_name):
    """
        Fonction pour générer le chemin des images des articles

        Récupère l'instance et affecte la valeur à une variable avec la propriété "slug" de l'instance si elle est disponible,
        sinon affecte un UUID généré, puis retourne la variable
    """

    upload_to = "articles/"
    # Récupère l'extension du fichier (JPG, PNG, ...)
    file_type = file_name.split(".")[-1]
    if instance.title:
        file_name = "{}.{}".format(instance.title, file_type)
    else:
        file_name = "{}.{}".format(uuid4().hex, file_type)
    # Défini le chemin complet depuis la racine du projet
    file_path = "uploads/" + upload_to + file_name
    # Vérifie si un fichier existe déja et si oui, le supprime
    if os.path.isfile(file_path):
        os.remove(file_path)
    return os.path.join(upload_to, file_name)


class Article(models.Model):
    """
        Modèle pour les articles
    """

    title = models.CharField(max_length=200, verbose_name="Titre")
    slug = models.SlugField(max_length=200, verbose_name="Slug", blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Auteur")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    categories = models.ManyToManyField(Category, verbose_name="Catégories")
    image = models.ImageField(upload_to=article_image, verbose_name="Image de fond", blank=True)
    content = models.TextField(verbose_name="Contenu")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
            Surcharge de la méthode "save" :

            Créé un slug (texte identificateur) en fonction du titre si ce dernier n'est pas déjà défini

            Documentation Django sur la surcharge des méthodes de modèles :
            https://docs.djangoproject.com/fr/2.0/topics/db/models/#overriding-model-methods
        """

        if not self.slug:
            self.slug = slugify(self.title)
        super().save()

    class Meta:
        verbose_name = "article"
        ordering = ["-date"]


class Comment(models.Model):
    """
        Modèle pour les commentaires
    """

    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="Article")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Utilisateur")
    date = models.DateTimeField(auto_now_add=True, verbose_name="Date")
    content = models.TextField()

    def __str__(self):
        return self.article.title

    class Meta:
        verbose_name = "commentaire"
        ordering = ["-date"]
