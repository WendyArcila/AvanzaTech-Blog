from factory.django import DjangoModelFactory
from post_cat_permission.models import PostCategoryPermission
from test.factories.category_permission.factories import CategoryAuthenticatedFactory,CategoryAuthorFactory,CategoryPublicFactory,CategoryTeamFactory
from test.factories.category_permission.factories import PermissionEditFactory, PermissionNoneFactory, PermissionReadOnlyFactory
from factory import SubFactory

class CreateWithBlogPostFactory(DjangoModelFactory):
    @classmethod
    def create_with_blog_post(cls, blog_post, **kwargs):
        return cls.create(blog_post=blog_post, **kwargs)

class PostCategoryPermissionPublicReadFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryPublicFactory)
    permission = SubFactory(PermissionReadOnlyFactory)    
    
    
    
class PostCategoryPermissionAuthenticatedReadFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryAuthenticatedFactory)
    permission = SubFactory(PermissionEditFactory)    
    
    
    
class PostCategoryPermissionTeamReadFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryTeamFactory)
    permission = SubFactory(PermissionReadOnlyFactory)    
    

    
    

class PostCategoryPermissionAuthorReadFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryAuthorFactory)
    permission = SubFactory(PermissionReadOnlyFactory)    
    

    
    
class PostCategoryPermissionPublicEditFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryPublicFactory)
    permission = SubFactory(PermissionEditFactory)    

class PostCategoryPermissionAuthenticatedEditFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryAuthenticatedFactory)
    permission = SubFactory(PermissionEditFactory)    
    

    
class PostCategoryPermissionTeamEditFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryTeamFactory)
    permission = SubFactory(PermissionEditFactory)    


class PostCategoryPermissionAuthorEditFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryAuthorFactory)
    permission = SubFactory(PermissionEditFactory)    
    

                

class PostCategoryPermissionPublicNoneFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryPublicFactory)
    permission = SubFactory(PermissionNoneFactory)    

    
class PostCategoryPermissionAuthenticatedNoneFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryAuthenticatedFactory)
    permission = SubFactory(PermissionNoneFactory)    

    
    
class PostCategoryPermissionTeamNoneFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryTeamFactory)
    permission = SubFactory(PermissionNoneFactory)    

    
    

class PostCategoryPermissionAuthorNoneFactory(CreateWithBlogPostFactory):
    class Meta:
        model = PostCategoryPermission
        
    category = SubFactory(CategoryAuthorFactory)
    permission = SubFactory(PermissionNoneFactory)    
