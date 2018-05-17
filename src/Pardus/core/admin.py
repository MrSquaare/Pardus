#
# Documentation Django sur la gestion de l'administration :
# https://docs.djangoproject.com/fr/2.0/ref/contrib/admin/
#

from django.contrib import admin
from django.utils.text import Truncator

from core.models import Article, Category, Comment, ContactMessage


class ContactMessageAdmin(admin.ModelAdmin):
    """
        Gestion du modèle ContactMessage pour django-admin
    """

    list_display = ("email", "first_name", "last_name", "date", "subject", "message_display")
    ordering = ("date",)
    search_fields = ("email", "subject")
    readonly_fields = ("first_name", "last_name", "email", "date", "subject", "message")

    def message_display(self, contact_message):
        """
            Fonction pour prévisualiser le contenu d'un message

            Récupère la propriété "message" d'un objet ContactMessage et retourne le texte tronqué
        """

        return Truncator(contact_message.message).chars(30, truncate="...")

    message_display.short_description = "Message"

    fieldsets = (
        ("Général", {
            "description": "Informations générales du message",
            "fields": ("first_name", "last_name", "email", "date")
        }),
        ("Message", {
            "description": "Contenu du message",
            "fields": ("subject", "message")
        })
    )


class CategoryAdmin(admin.ModelAdmin):
    """
        Gestion du modèle Category pour django-admin
    """

    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)

    fieldsets = (
        ("Général", {
            "description": "Informations générales de la catégorie",
            "fields": ("name", "image")
        }),
    )


class ArticleAdmin(admin.ModelAdmin):
    """
        Gestion du modèle Article pour django-admin
    """

    list_display = ("title", "author", "date", "categories_display", "content_display")
    list_filter = ("author", "categories__name")
    date_hierarchy = "date"
    ordering = ("date",)
    search_fields = ("title",)
    prepopulated_fields = {"slug": ("title",)}

    def categories_display(self, article):
        """
            Fonction pour voir les catégories d'un article

            Récupère tout les objects Category liés à un objet Article à l'aide d'une boucle for et retourne une chaine
            de texte
        """
        return ", ".join([category.name for category in article.categories.all()])

    def content_display(self, article):
        """
            Fonction pour prévisualiser le contenu d'un article

            Récupère la propriété "content" d'un objet Article et retourne le texte tronqué
        """

        return Truncator(article.content).chars(30, truncate="...")

    categories_display.short_description = "Catégories"
    content_display.short_description = "Aperçu de l'article"

    fieldsets = (
        ("Général", {
            "description": "Informations générales de l'article",
            "fields": ("title", "author", "categories", "image")
        }),
        ("Contenu", {
            "description": "Contenu de l'article",
            "fields": ("content",)
        }),
        ("Avancé", {
            "classes": ("collapse",),
            "fields": ("slug",)
        })
    )


class CommentAdmin(admin.ModelAdmin):
    """
        Gestion du modèle Comment pour django-admin
    """

    list_display = ("article", "author", "date", "content_display")
    list_filter = ("article", "author")
    date_hierarchy = "date"
    ordering = ("date",)
    search_fields = ("content_display",)
    readonly_fields = ("article", "author")

    def content_display(self, article):
        """
            Fonction pour prévisualiser le contenu d'un commentaire

            Récupère la propriété "content" d'un objet Comment et retourne le texte tronqué
        """

        return Truncator(article.content).chars(30, truncate="...")

    content_display.short_description = "Aperçu du commentaire"

    fieldsets = (
        ("Général", {
            "description": "Informations générales du commentaire",
            "fields": ("article", "author")
        }),
        ("Contenu", {
            "description": "Contenu du commentaire",
            "fields": ("content",)
        })
    )


admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Article, ArticleAdmin)
admin.site.register(Comment, CommentAdmin)
