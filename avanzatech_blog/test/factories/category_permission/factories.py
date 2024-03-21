from factory.django import DjangoModelFactory
from category.models import Category
from permission.models import Permission
from django.core.exceptions import ObjectDoesNotExist


class GetOrCreateFactory(DjangoModelFactory):
    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        # Intenta obtener el objeto, si no existe, lo crea
        name = kwargs.pop('name', None)
        description = kwargs.pop('description', None)
        # Intenta obtener el objeto, si no existe, lo crea
        try:
            return model_class.objects.get_or_create(name=name, defaults=kwargs)[0]
        except ObjectDoesNotExist:
            # Si no se encuentra, crea el objeto
            return model_class.objects.create(name=name, description=description, **kwargs)

class PermissionEditFactory(GetOrCreateFactory):
    class Meta:
        model = Permission

    name = "Edit"
    description =  "You can read and edit"
    

class PermissionNoneFactory(GetOrCreateFactory):
    class Meta:
        model = Permission
    
    name = "None"
    description =  "You can not read or edit"
    



class PermissionReadOnlyFactory(GetOrCreateFactory):
    class Meta:
        model = Permission
    
    name = "ReadOnly"
    description =  "You can only read"
    



class CategoryAuthorFactory(GetOrCreateFactory):
    class Meta:
        model = Category
    
    name = "Author"
    description = "Who made this"
    
    

class CategoryTeamFactory(GetOrCreateFactory):
    class Meta:
        model = Category
    
    name = "Team"
    description = "Belongs to the  author's team"
    


class CategoryAuthenticatedFactory(GetOrCreateFactory):
    class Meta:
        model = Category
    
    name = "Authenticated"
    description = "Login user"
    
    
    
class CategoryPublicFactory(GetOrCreateFactory):
    class Meta:
        model = Category
    
    name = "Public"
    description = "No authenticated user"
    
