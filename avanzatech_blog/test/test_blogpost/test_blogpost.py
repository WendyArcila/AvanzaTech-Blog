import pytest
import json
from test.factories.blog_post.factories import BlogPostFactory
from test.factories.blog_post.factories import PermissionFactory
from test.factories.blog_post.factories import CategoryFactory


@pytest.mark.django_db
def test_creation_post(authenticated_client):
    # Crear una instancia de BlogPost con la fábrica
    blog_post = BlogPostFactory.build()
    # Obtener el JSON que necesitas
    json_data = {
            "title": blog_post.title,
            "content": blog_post.content,
            "post_category_permission": [
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                            {"permission": PermissionFactory.create().id, "category": CategoryFactory.create().id},
                        ]
            
        }
    print(json_data)
    # Definir la URL a la que quieres hacer la solicitud POST
    url = '/blogpost/'
    
    # Hacer la solicitud POST con el JSON
    response = authenticated_client.post(url, json.dumps(json_data), content_type='application/json')
    
    # Ahora puedes verificar la respuesta
    assert response.status_code == 201 # Asegúrate de que la solicitud POST fue exitosa