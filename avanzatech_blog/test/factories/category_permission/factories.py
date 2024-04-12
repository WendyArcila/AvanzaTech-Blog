from factory.django import DjangoModelFactory
from category.models import Category
from permission.models import Permission
from django.core.exceptions import ObjectDoesNotExist


class GetOrCreateFactory(DjangoModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        name = kwargs.pop('name', None)
        description = kwargs.pop('description', None)
        try:
            return model_class.objects.get_or_create(
                name=name, defaults=kwargs)[0]
        except ObjectDoesNotExist:
            return model_class.objects.create(
                name=name, description=description, **kwargs)


class PermissionFactory(GetOrCreateFactory):
    class Meta:
        model = Permission

    name = "None"
    description = "You can not read or edit"


class CategoryFactory(GetOrCreateFactory):
    class Meta:
        model = Category

    name = "Author"
    description = "Who made this"
