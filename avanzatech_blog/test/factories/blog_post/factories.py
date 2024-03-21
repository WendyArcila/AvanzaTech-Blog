    
import factory
from factory.django import DjangoModelFactory
from blog_post.models import BlogPost
from test.factories.post_category_permission.factories import PostCategoryPermissionTeamReadFactory,PostCategoryPermissionPublicReadFactory,PostCategoryPermissionAuthenticatedReadFactory,PostCategoryPermissionAuthorReadFactory
from test.factories.post_category_permission.factories import PostCategoryPermissionPublicNoneFactory, PostCategoryPermissionAuthenticatedNoneFactory,PostCategoryPermissionTeamNoneFactory,PostCategoryPermissionAuthorNoneFactory
from test.factories.post_category_permission.factories import PostCategoryPermissionPublicEditFactory,PostCategoryPermissionAuthenticatedEditFactory,PostCategoryPermissionAuthorEditFactory,PostCategoryPermissionTeamEditFactory



class BlogPostFactoryBasic(DjangoModelFactory):
    class Meta:
        model = BlogPost
        skip_postgeneration_save = True
        
    title = factory.Faker('name')
    content = factory.Faker('text', max_nb_chars=500)
    #author = SubFactory(UserFactory)
    
    @factory.post_generation
    def set_author(self, create, extracted, **kwargs):
        if extracted:
            # Si se pasa un autor, lo asignamos al BlogPost
            self.author = extracted
            self.save()

class BlogPostReadFactory(BlogPostFactoryBasic):
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicReadFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedReadFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamReadFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorReadFactory.create_with_blog_post(self)
            
            
class BlogPostReadPublicFactory(BlogPostFactoryBasic):
    
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicReadFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorNoneFactory.create_with_blog_post(self)
        

class BlogPostReadAuthenticatedFactory(BlogPostFactoryBasic):
      
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedReadFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorNoneFactory.create_with_blog_post(self)

class BlogPostReadTeamFactory(BlogPostFactoryBasic):
        
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamReadFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorNoneFactory.create_with_blog_post(self)

class BlogPostReadAuthorFactory(BlogPostFactoryBasic):
    
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorReadFactory.create_with_blog_post(self)


class BlogPostEditFactory(BlogPostFactoryBasic):
    
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicEditFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedEditFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamEditFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorEditFactory.create_with_blog_post(self)
        
class BlogPostNoneFactory(BlogPostFactoryBasic):
    
    @factory.post_generation
    def post_category_permission(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        
        PostCategoryPermissionPublicNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthenticatedNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionTeamNoneFactory.create_with_blog_post(self)
        PostCategoryPermissionAuthorNoneFactory.create_with_blog_post(self)
        
        

