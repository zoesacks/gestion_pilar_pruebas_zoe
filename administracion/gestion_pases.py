from django.contrib.auth.decorators import user_passes_test

def is_base_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_general').exists()

def is_contaduria_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria').exists()

def is_ingresos_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_ingresos').exists()

def is_tesoreria_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_tesoreria').exists()

# Decoradores para cada grupo de aplicaciones
contaduria_required = user_passes_test(is_contaduria_user, login_url='/sin_acceso/')
ingresos_required = user_passes_test(is_ingresos_user, login_url='/sin_acceso/')
tesoreria_required = user_passes_test(is_tesoreria_user, login_url='/sin_acceso/')
general_required = user_passes_test(is_base_user, login_url='/sin_acceso/')