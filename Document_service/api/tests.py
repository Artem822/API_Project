import pytest
from api.models import  User, Role
import requests as rq



@pytest.fixture
def authenticate(request):

    admin = User.objects.create_user(username='test_admin', password='admin')
    role = Role.objects.create(role='Admin')
    admin.roles.add(role)
    admin.save()

    link = 'http://127.0.0.1:8001/api/Authentication/SignIn/'

    tokens = rq.post(link, json={'username': admin.username, 'password': admin.password}).json()
    print(f"\nToken: {tokens}")

    def token_delete():
        admin.delete()
        role.delete()
    request.addfinalizer(token_delete)
   


@pytest.mark.django_db
def test_get(authenticate):
    link = 'http://127.0.0.1:8003/api/Timetable/Hospital/1/'
    response = rq.get(link)
    print(response.json())