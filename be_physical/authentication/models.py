from rest_framework.authtoken.models import Token

# Create your models here.


class BearerToken(Token):
    keyword = "Bearer"
