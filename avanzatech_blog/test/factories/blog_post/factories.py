import factory 
from faker import Faker
from category.models import Category
from permission.models import Permission
from factory.django import DjangoModelFactory
from blog_post.models import BlogPost

fake = Faker()

class BlogPostFactory(DjangoModelFactory):
    
    class Meta:
        model = BlogPost

    title = fake.name()
    content = fake.text(max_nb_chars=500)
    
    
    
    ''' 
    def build_blogpost_JSON(self): 
        return {
                "title": fake.text(),
                "content": fake.text(max_nb_chars = 500), 
                post_category_permission = factory.LazyAttribute(
                        lambda obj: [
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                        ]
    )
        
        

    class Meta: 
        model = BlogPost
        
    title = fake.text()
    content = fake.text(max_nb_chars = 500)
    post_category_permission = [['permission': factory.SubFactory(PermissionFactory),'category' : factory.SubFactory(CategoryFactory)], 
                                ['permission': factory.SubFactory(PermissionFactory),'category' : factory.SubFactory(CategoryFactory)],
                                ['permission': factory.SubFactory(PermissionFactory),'category' : factory.SubFactory(CategoryFactory)],                          ['permission': factory.SubFactory(PermissionFactory),'category' : factory.SubFactory(CategoryFactory)],
                                ]
'''   

class PermissionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Permission     
        
    name = fake.name()
    description = fake.text()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category
        
    name = fake.name()
    description = fake.text()
    