import pytest
import json
from faker import Faker
from test.factories.blog_post.factories import BlogPostReadAuthorFactory,BlogPostReadAuthenticatedFactory,BlogPostReadPublicFactory,BlogPostEditFactory, BlogPostNoneFactory, BlogPostReadFactory, BlogPostReadTeamFactory
from test.factories.post_category_permission.factories import PermissionEditFactory,PermissionNoneFactory, PermissionReadOnlyFactory
from test.factories.post_category_permission.factories import CategoryAuthenticatedFactory, CategoryAuthorFactory, CategoryPublicFactory, CategoryTeamFactory
from user.models import CustomUser
from post_cat_permission.models import PostCategoryPermission
from rest_framework.test import APIClient

fake = Faker()


#Test para la creación de un post con toda la información correcta 
@pytest.mark.django_db
def test_creation_post(authenticated_client):
    
    json_data = {
            "title": fake.name(),
            "content": fake.text( max_nb_chars=500),
            "post_category_permission": [
                            {"permission": PermissionReadOnlyFactory.create().id, "category": CategoryPublicFactory.create().id},
                            {"permission": PermissionNoneFactory.create().id, "category": CategoryAuthenticatedFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryTeamFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryAuthorFactory.create().id},
                        ]
            
        }
    # Definir la URL a la que quieres hacer la solicitud POST
    url = '/blogpost/'
    
    # Hacer la solicitud POST con el JSON
    response = authenticated_client.post(url, json.dumps(json_data), content_type='application/json')
    
    # Ahora puedes verificar la respuesta
    assert response.status_code == 201 
    
    
#creación de un test con menos información de la que necesita 
@pytest.mark.django_db
def  test_creation_post_with_insufficient_data(authenticated_client):
    
    json_data_without_title = {
            "content": fake.text( max_nb_chars=500),
            "post_category_permission": [
                            {"permission": PermissionReadOnlyFactory.create().id, "category": CategoryPublicFactory.create().id},
                            {"permission": PermissionNoneFactory.create().id, "category": CategoryAuthenticatedFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryTeamFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryAuthorFactory.create().id},
                        ]
            
        }
    
    json_data_without_content= {
            "title": fake.name(),
            "post_category_permission": [
                            {"permission": PermissionReadOnlyFactory.create().id, "category": CategoryPublicFactory.create().id},
                            {"permission": PermissionNoneFactory.create().id, "category": CategoryAuthenticatedFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryTeamFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryAuthorFactory.create().id},
                        ]
            
        }
    
    json_data_without_post_category_permission = {
            "title": fake.name(),
            "content": fake.text( max_nb_chars=500)
        }
    
    json_data_without_info_in_post_category_permission = {
            "title": fake.name(),
            "content": fake.text( max_nb_chars=500),
            "post_category_permission": []
        }
    
    json_data_with_less_info_in_post_category_permission = {
            "title": fake.name(),
            "content": fake.text( max_nb_chars=500),
            "post_category_permission": [
                            {"permission": PermissionReadOnlyFactory.create().id, "category": CategoryPublicFactory.create().id},
                            {"permission": PermissionNoneFactory.create().id, "category": CategoryAuthenticatedFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryTeamFactory.create().id},
                        ]
            
        }
    
    json_data_with_more_info_in_post_category_permission = {
            "title": fake.name(),
            "content": fake.text( max_nb_chars=500),
            "post_category_permission": [
                            {"permission": PermissionReadOnlyFactory.create().id, "category": CategoryPublicFactory.create().id},
                            {"permission": PermissionNoneFactory.create().id, "category": CategoryAuthenticatedFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryTeamFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryAuthorFactory.create().id},
                            {"permission": PermissionEditFactory.create().id, "category": CategoryAuthorFactory.create().id},
                        ]
            
        }
    
    
    # Definir la URL a la que quieres hacer la solicitud POST
    url = '/blogpost/'
    
    # Hacer la solicitud POST con sin el atributo title
    response = authenticated_client.post(url, json.dumps(json_data_without_title), content_type='application/json')
    assert response.status_code == 400 
    assert "This field is required." in response.data['title']
    
    # Hacer la solicitud POST con sin el atributo content
    response = authenticated_client.post(url, json.dumps(json_data_without_content), content_type='application/json')
    assert response.status_code == 400 
    assert "This field is required." in response.data['content']
    
    # Hacer la solicitud POST con sin el atributo post_category_permission 
    response = authenticated_client.post(url, json.dumps( json_data_without_post_category_permission), content_type='application/json')
    assert response.status_code == 400 
    assert "This field is required." in response.data['post_category_permission']
    
    # Hacer la solicitud POST con sin datos en el atributo post_category_permission 
    response = authenticated_client.post(url, json.dumps(json_data_without_info_in_post_category_permission), content_type='application/json')
    assert response.status_code == 400 
    assert "Permission are necessary to create a post." in response.data['non_field_errors']
    
    # Hacer la solicitud POST con menos datos en el atributo post_category_permission 
    response = authenticated_client.post(url, json.dumps(json_data_with_less_info_in_post_category_permission), content_type='application/json')
    assert response.status_code == 400 
    assert "The post needs exactly four permissions." in response.data['non_field_errors']
    
    # Hacer la solicitud POST con más datos en el atributo post_category_permission 
    response = authenticated_client.post(url, json.dumps(json_data_with_more_info_in_post_category_permission), content_type='application/json')
    assert response.status_code == 400 
    assert "The post needs exactly four permissions." in response.data['non_field_errors']


#Test para asegurar el funcionamiento de la factory de blog_post al almacenar post_category_permission
@pytest.mark.django_db
def test_blog_post_factory_creates_post_category_permissions(user_creation_one):

    # Crear un BlogPost utilizando la BlogPostFactory
    blog_post = BlogPostReadFactory.create(author=user_creation_one)
    # Verificar que existen exactamente 4 instancias de PostCategoryPermission asociadas con el BlogPost
    assert PostCategoryPermission.objects.filter(blog_post=blog_post).count() == 4
    
    # Opcional: Puedes verificar que cada PostCategoryPermission está correctamente relacionada con el BlogPost
    for post_category_permission in PostCategoryPermission.objects.filter(blog_post=blog_post):
        assert post_category_permission.blog_post == blog_post



@pytest.mark.django_db
def test_blogpost_list_public_permissions_view(user_creation_one):
    blog_posts = [
            BlogPostReadPublicFactory.create(author=user_creation_one),
            BlogPostReadPublicFactory.create(author=user_creation_one),
            BlogPostReadTeamFactory.create(author=user_creation_one),
            BlogPostReadAuthenticatedFactory.create(author=user_creation_one),
            BlogPostReadAuthorFactory.create(author=user_creation_one)
        ]
        
    client = APIClient()
    
    # Realizar la solicitud GET a la vista de lista de posts de blog
    url = '/blogpost/' 
    response = client.get(url)
    
    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que la cantidad de posts devueltos es igual a la cantidad de posts creados
    assert len(response.data) == 2

    
@pytest.mark.django_db
def test_blogpost_list_authenticated_permissions_view(user_creation_three,user_creation_one,user_creation_two, authenticated_client):
    user_creation_three.team = user_creation_one.team
    
    blog_posts = [
            BlogPostReadAuthenticatedFactory.create(author=user_creation_two),
            BlogPostReadAuthenticatedFactory.create(author=user_creation_two),
            BlogPostReadAuthenticatedFactory.create(author=user_creation_one), #author 
            BlogPostReadAuthenticatedFactory.create(author=user_creation_three), #team
            BlogPostReadPublicFactory.create(author=user_creation_two),
        ]
        
    client = APIClient()
    client.force_authenticate(user= user_creation_one)
    print("team:", user_creation_three.team == user_creation_one.team )

    
    # Realizar la solicitud GET a la vista de lista de posts de blog
    url = '/blogpost/' 
    response = client.get(url)
    
    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que la cantidad de posts devueltos es igual a la cantidad de posts creadAuthenticatedos
    assert len(response.data) == 2


@pytest.mark.django_db
def test_blogpost_list_team_permissions_view(user_creation_one,user_creation_two,user_creation_three, authenticated_client):
    user_creation_three.team = user_creation_one.team
    #print(user_creation_three.team == user_creation_one.team)
    blog_posts = [
            BlogPostReadTeamFactory.create(author=user_creation_three),
            BlogPostReadTeamFactory.create(author=user_creation_three),
            BlogPostReadTeamFactory.create(author=user_creation_two), # != team
            BlogPostReadTeamFactory.create(author=user_creation_one), # author
            BlogPostReadPublicFactory.create(author=user_creation_two),
            BlogPostReadAuthenticatedFactory.create(author=user_creation_three)
        ]
            
    client = authenticated_client

    
    # Realizar la solicitud GET a la vista de lista de posts de blog
    url = '/blogpost/' 
    response = client.get(url)
    
    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que la cantidad de posts devueltos es igual a la cantidad de posts creados
    assert len(response.data) == 1

@pytest.mark.django_db
def test_blogpost_list_author_permissions_view(user_creation_one,user_creation_two,user_creation_three, authenticated_client):
    user_creation_three.team = user_creation_one.team
    #print(user_creation_three.team == user_creation_one.team)
    blog_posts = [
            BlogPostReadAuthorFactory.create(author=user_creation_one),
            BlogPostReadAuthorFactory.create(author=user_creation_one),
            BlogPostReadAuthorFactory.create(author=user_creation_two), # != team
            BlogPostReadAuthorFactory.create(author=user_creation_three), # author
            BlogPostReadPublicFactory.create(author=user_creation_two),
            BlogPostReadAuthenticatedFactory.create(author=user_creation_three)
        ]
            
    client = authenticated_client

    
    # Realizar la solicitud GET a la vista de lista de posts de blog
    url = '/blogpost/' 
    response = client.get(url)
    
    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200

    # Verificar que la cantidad de posts devueltos es igual a la cantidad de posts creados
    assert len(response.data) == 2
