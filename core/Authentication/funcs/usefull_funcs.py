# SECTION - Бизнес логика для классов предствления из микросервиса account


from ..models import User, ROLES, Role
from rest_framework.response import Response
from django.http import HttpRequest
from rest_framework import status, request

def _role_is_exist(roles):
    try:
        roles_count = len(roles)
        counter = 0

        for role in roles:
            for my_role in ROLES:
                if role in my_role:
                    counter += 1
                    break

        if (counter == roles_count): return True
        
        else: return False

    except:
        return False
    
def add_role(user, validate_data):

    check_role = _role_is_exist(validate_data['roles'])

    response = {}

    try:
        if check_role:
            roles = list(Role.objects.filter(role__in=validate_data['roles']))
            user.roles.set(roles)

        else:
            response[f"{user}"] = "Роли не были добавлены. Убедитесь в корректности введенных ролей"

    except:
        response["server"] = "Ошибка при назначении ролей"

    return response

def add_users(request, user = User):
    try:
        
        if isinstance(request.data, dict):
            response = add_one_user(user, request.data)

        elif isinstance(request.data, list):
            response = add_many_users(request.data)

        else:
            return Response({'server': 'Ошибка в синтаксисе json'})
                
        return Response(response)
    

    except:
        return Response(data={
            "server": 'Неверные данные'
        }, status=status.HTTP_400_BAD_REQUEST)


def add_many_users(data):
    response = {}

    for user_data in data:
        user = User
        response.update(add_one_user(user, user_data))

    return response


def add_one_user(user, validated_data):
    try:
        response = {}

        user = user.objects.create(
             lastName=validated_data['lastName'],
             firstName=validated_data['firstName'],
             username=validated_data['username']
             )

        user.set_password(validated_data['password'])

        user.save()
    
        response[f"{user}"] = "Пользователь успешно добавлен"

        try:
            if validated_data['roles']:
                response_from_roles = add_role(user, validated_data)

                if response_from_roles:
                    response["messages"] = response_from_roles

        except:
            pass
        
        return response

    except:
        return {f"{user.username}": "не был добавлен"}
        

def delete(request, id):
    try:
        user = User.objects.get(pk=id)
        username = user.username
        user.delete()

        return Response({f"{username}": "Успешно удален"})
    
    except:
        return Response({"server": "Пользователь не найден"})


def filter_users(request, user_role):
    if user_role in ROLES:
        try:
            role = Role.objects.filter(role=user_role)
            filter_users = User.objects.filter(roles__in=role)
            user = filter_users[0]

            return Response({
                "nameFilter": user.get_full_name,
                "from": user.pk,
                "count": len(filter_users)
                }, status=status.HTTP_200_OK)

        except:
            print('Ошибка при фильтрации')


def get_info(user):

    role_list = []
    
    try:
        for role in user.roles.all():
            role_list.append(role.role)

    except:
        pass

    return Response({
        "lastName": str(user.lastName),
        "firstName": str(user.firstName),
        "username": str(user.username),
        "roles": role_list
        })

def _role_is_exist(roles: list[str]) -> bool:
    try:
        roles_count = len(roles)
        counter = 0

        for role in roles:
            for my_role in ROLES:
                if role in my_role:
                    counter += 1
                    break

        if (counter == roles_count): return True
        
        else: return False

    except:
        return False
    
def update_user(request, id=False):
    if id:
        user = User.objects.get(pk=id)

        response = update(user, request.data)

        return Response(response)


    else:
        user = request.user

        response = update(user, request.data)

        return Response(response)
    

def update(user, data):
    try:
        response = {}

        user.lastName=data['lastName']
        user.firstName=data['firstName']
        user.username=data['username']

        user.set_password(data['password'])

        user.save()

        response[f"{user.username}"] = "Успешно обновлен"

        try:
            if data['roles']:
                response_from_roles = add_role(user, data)

                if response_from_roles:
                    response["messages"] = response_from_roles

        except:
            pass

        return response
    
    except:
        return {f"{user.username}": "Пользователь не был обновлен."}