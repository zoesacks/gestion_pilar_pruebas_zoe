from django.contrib.auth.decorators import user_passes_test

def is_base_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_general').exists()

def is_contaduria_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria').exists()

def is_ingresos_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_ingresos').exists()

def is_tesoreria_user(user):
    return user.is_authenticated and user.groups.filter(name='acceso_tesoreria').exists()


# gestion de accesos a aplicaciones

# CONTADURIA
def acceso_solicitudes_de_pedido(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria_solicitudes_de_pedido').exists()
def acceso_facturas(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria_facturas').exists()
def acceso_ingresos(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria_ingresos').exists()
def acceso_gastos(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria_gastos').exists()
def acceso_prestamos(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria_prestamos').exists()
def acceso_redeterminaciones(user):
    return user.is_authenticated and user.groups.filter(name='acceso_contaduria_redeterminaciones').exists()

#INGRESOS
def acceso_calculadora_tasas(user):
    return user.is_authenticated and user.groups.filter(name='acceso_ingresos_calculadora_tasas').exists()
def acceso_servicios_generales(user):
    return user.is_authenticated and user.groups.filter(name='acceso_ingresos_servicios_generales').exists()



# Decoradores para cada grupo de aplicaciones
contaduria_required = user_passes_test(is_contaduria_user, login_url='/sin_acceso/')
ingresos_required = user_passes_test(is_ingresos_user, login_url='/sin_acceso/')
tesoreria_required = user_passes_test(is_tesoreria_user, login_url='/sin_acceso/')
general_required = user_passes_test(is_base_user, login_url='/sin_acceso/')

# Decoradores para cada aplicacion - CONTADURIA
solicitudes_pedido_required = user_passes_test(acceso_solicitudes_de_pedido, login_url='/sin_acceso/')
facturas_required = user_passes_test(acceso_facturas, login_url='/sin_acceso/')
ingresos_required = user_passes_test(acceso_ingresos, login_url='/sin_acceso/')
gastos_required = user_passes_test(acceso_gastos, login_url='/sin_acceso/')
prestamos_required = user_passes_test(acceso_prestamos, login_url='/sin_acceso/')
redeterminaciones_required = user_passes_test(acceso_redeterminaciones, login_url='/sin_acceso/')

# Decoradores para cada aplicacion - INGRESOS
calculadora_tasas_required = user_passes_test(acceso_calculadora_tasas, login_url='/sin_acceso/')
servicios_generales_required = user_passes_test(acceso_servicios_generales, login_url='/sin_acceso/')