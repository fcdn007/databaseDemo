from .models import User


class EmailBackend(object):
    def authenticate(self, request, **credentials):
        email = credentials.get('email', credentials.get('username'))
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(index=user_id)
        except User.DoesNotExist:
            return None


class NicknameBackend(object):
    def authenticate(self, request, **credentials):
        nick_name = credentials.get('nick_name', credentials.get('username'))
        try:
            user = User.objects.get(nick_name=nick_name)
        except User.DoesNotExist:
            pass
        else:
            if user.check_password(credentials["password"]):
                return user

    def get_user(self, user_id):
        try:
            return User.objects.get(index=user_id)
        except User.DoesNotExist:
            return None
