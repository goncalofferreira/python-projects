from rest_framework.throttling import UserRateThrottle, AnonRateThrottle
from rest_framework.views import APIView

# Geral para utilizadores autenticados
class UserBurstThrottle(UserRateThrottle):
    scope = 'burst'

class UserSustainedThrottle(UserRateThrottle):
    scope = 'sustained'

# Geral para utilizadores anónimos
class AnonBurstThrottle(AnonRateThrottle):
    scope = 'anon_burst'

class AnonSustainedThrottle(AnonRateThrottle):
    scope = 'anon_sustained'

# Específicos para ações
class CreateBookThrottle(UserRateThrottle):
    scope = 'create_book'

class UpdateBookThrottle(UserRateThrottle):
    scope = 'update_book'

class DeleteBookThrottle(UserRateThrottle):
    scope = 'delete_book'

class CreateCategoryThrottle(UserRateThrottle):
    scope = 'create_category'

class CustomUserThrottle(UserRateThrottle):   
    scope = 'user'
    