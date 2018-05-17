#
# Documentation Django sur les processeurs de contexte :
# https://docs.djangoproject.com/fr/2.0/topics/templates/#context-processors
#
# Documentation Django sur la création d'un processeur de contexte personnalisé :
# https://docs.djangoproject.com/fr/2.0/ref/templates/api/#writing-your-own-context-processors
#

from core.models import Category


def get_categories(request):
    """
        Retourne tous les objets Category
    """

    categories = Category.objects.all()[:5]
    return {"get_categories": categories}
