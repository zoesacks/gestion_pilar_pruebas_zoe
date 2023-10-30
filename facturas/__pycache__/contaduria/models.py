# ------------------------------------------------------------------------------------------
# Sistema de administracion - Ministerio de Desarrollo - Pilar
# Desarrollador Kevin Turkienich
# Julio 2023
# Kevin_turkienich@outlook.com
# ------------------------------------------------------------------------------------------

# Modelado de bases de datos para altas, bajas y modificaciones de datos maestros.

# ------------------------------------------------------------------------------------------
# Modulos importados
import datetime
from django.db import models
from django.forms import ValidationError
from administracion.models import fondo,proveedor,concepto,Equivalencia,recurso,codigoFinanciero
from django.utils import timezone
from datetime import datetime

TIPO_PRESTAMO = [ 
    ("SOLICITUD","SOLICITUD"),
    ("DEVOLUCION","DEVOLUCION")
]
MESES_CUSTOM = [ 
    ("1","ENERO"),
    ("2","FEBRERO"),
    ("3","MARZO"),
    ("4","ABRIL"),
    ("5","MAYO"),
    ("6","JUNIO"),
    ("7","JULIO"),
    ("8","AGOSTO"),
    ("9","SEPTIEMBRE"),
    ("10","OCTUBRE"),
    ("11","NOVIEMBRE"),
    ("12","DICIEMBRE")
]
EJERCICIO = [ 
    ("2020","2020"),
    ("2021","2021"),
    ("2022","2022"),
    ("2023","2023"),
    ("2024","2024"),
    ("2025","2025")
]

# ------------------------------------------------------------------------------------------
# DASHBOARD GASTOS
class asientosGastos(models.Model):
    
    Ejercicio = models.CharField(max_length=255,null=True, blank=True) 
    
    Codigo = models.ForeignKey(codigoFinanciero,on_delete=models.CASCADE,blank=True,null=True)

    Jurisdiccion = models.CharField(max_length=255,null=True, blank=True) 
    JurisdiccionDescripcion = models.CharField(max_length=255,null=True, blank=True) 

    EstructuraProgramatica = models.CharField(max_length=255,null=True, blank=True) 
    EstructuraProgramaticaDescripcion = models.CharField(max_length=255,null=True, blank=True) 

    FuenteFinanciamiento = models.CharField(max_length=255,null=True, blank=True) 
    FuenteFinanciamientoDescripcion = models.CharField(max_length=255,null=True, blank=True) 

    ObjetodelGasto = models.CharField(max_length=255,null=False, blank=False) 
    ObjetodelGastoDescripcion = models.CharField(max_length=255,null=False, blank=False) 

    Fecha = models.DateField(null=False, blank=False) 

    ComprobanteTipo = models.CharField(max_length=255,null=False, blank=False) 
    ComprobanteEjercicio = models.CharField(max_length=255,null=False, blank=False) 
    ComprobanteNumero = models.CharField(max_length=255,null=False, blank=False) 

    AplicacionTipo = models.CharField(max_length=255,null=False, blank=False) 
    AplicacionEjercicio = models.CharField(max_length=255,null=False, blank=False) 
    AplicacionNumero = models.CharField(max_length=255,null=False, blank=False) 

    Oficina = models.CharField(max_length=255,null=True, blank=True) 
    OficinaDescripcion = models.CharField(max_length=255,null=True, blank=True) 

    Obra = models.CharField(max_length=255,null=True, blank=True) 
    ObraDescripcion = models.CharField(max_length=255,null=True, blank=True) 

    Patrimonio = models.CharField(max_length=255,null=True, blank=True) 
    PatrimonioDescripcion = models.CharField(max_length=255,null=True, blank=True) 

    ProveedorTipo = models.CharField(max_length=255,null=True, blank=True) 
    ProveedorNumero = models.CharField(max_length=255,null=True, blank=True) 
    RazonSocial = models.CharField(max_length=255,null=True, blank=True) 

    Presupuesto = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    Preventivo = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    Compromiso = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    Devengado = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    MandadoaPagar = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    Pagado = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)

    class Meta:
        verbose_name = 'Asiento de gasto'
        verbose_name_plural ='Asientos de gastos' 
    
    def __str__(self):
        if self.pk:
            return f"Pagado #{self.pk} FF: {self.FuenteFinanciamiento} Comp: {self.ComprobanteTipo}"
        else:
            return ""

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# DASHBOARD GASTOS
class asientosIngresos(models.Model):

    Ejercicio = models.CharField(max_length=255,null=True, blank=True) 

    Clasificacion = models.ForeignKey(Equivalencia,on_delete=models.CASCADE,null=True, blank=True)

    Recurso_Agrupamiento = models.CharField(max_length=255,null=True, blank=True) 
    Recurso_Descripcion = models.CharField(max_length=255,null=True, blank=True) 

    OrigProc_Agrupamiento = models.CharField(max_length=255,null=True, blank=True) 
    OrigProc_Descripcion = models.CharField(max_length=255,null=True, blank=True) 

    Fecha = models.DateField(null=False, blank=False) 

    Devengado = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    Percibido = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)

    class Meta:
        verbose_name = 'Asiento de ingreso'
        verbose_name_plural ='Asientos de ingresos' 
    
    def __str__(self):
        if self.pk:
            return f"{self.Clasificacion} | {self.Fecha} | {self.Recurso_Descripcion} | ${self.Percibido} |"
        else:
            return ""
    
    def save(self, *args, **kwargs):

        self.Ejercicio = str(self.Fecha.year)

        super(asientosIngresos, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PRESTAMOS
class prestamo(models.Model):
    FECHA = models.DateField(null=False, blank=False) 
    GASTO = models.ForeignKey(asientosGastos,on_delete=models.PROTECT,null=False, blank=False)
    FONDO = models.ForeignKey(fondo,on_delete=models.PROTECT,null=True, blank=True)
    IMPORTE  = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    PENDIENTE = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    ORDEN_DE_PAGO = models.CharField(max_length=120, null=True, blank=True)
    REGISTRO_PAGADO = models.CharField(max_length=120, null=True, blank=True)
    PROVEEDOR = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Prestamo'
        verbose_name_plural ='Prestamos' 
    
    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.PENDIENTE)
        formatted_fecha = self.FECHA.strftime('%d/%m/%Y')
        NAME = "📅 " + formatted_fecha + " | 🧾" + str(self.GASTO) + " | 👤" + str(self.GASTO.RazonSocial) + " | 💲" + formatted_importe
        return NAME

    def clean(self):

        super().clean()

    def save(self, *args, **kwargs):
        if self.GASTO.AplicacionTipo != 0 and self.GASTO.AplicacionTipo != "":
            self.REGISTRO_PAGADO = f'{self.GASTO.AplicacionTipo} - {self.GASTO.AplicacionEjercicio} -{self.GASTO.AplicacionNumero}'
            self.PROVEEDOR =  f'{self.GASTO.ProveedorTipo} - {self.GASTO.ProveedorNumero} - {self.GASTO.RazonSocial}'

        super(prestamo, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION DE PRESTAMOS
class devolucionPrestamo(models.Model):
    ESTADO =models.BooleanField(default=0)
    FECHA = models.DateField(null=False, blank=False,default=timezone.now) 
    PRESTAMO = models.ForeignKey(prestamo,on_delete=models.PROTECT,null=False, blank=False,limit_choices_to={'PENDIENTE__lt': 0})
    IMPORTE  = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    FONDO = models.CharField(max_length=120, null=True, blank=True)
    ORDEN_DE_PAGO = models.CharField(max_length=120, null=True, blank=True)
    REGISTRO_PAGADO = models.CharField(max_length=120, null=True, blank=True)
    PROVEEDOR = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.IMPORTE)
        NAME = str(self.FECHA) + " - " + str(self.PRESTAMO) + " - " + str(self.PROVEEDOR) + " - $" + formatted_importe
        return NAME


    def clean(self):

        if self.PRESTAMO.PENDIENTE == 0 or self.ESTADO == 1:
            raise ValidationError(f"El prestamo ya está cancelado.")
        if self.PRESTAMO.PENDIENTE > self.IMPORTE:
            raise ValidationError(f"Está generando una devolucion por un importe superior al adeudado por el fondo. El máximo permitido es de {self.PRESTAMO.PENDIENTE}")
        if self.IMPORTE <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
        super().clean()

    def save(self, *args, **kwargs):


        self.FONDO = self.PRESTAMO.FONDO
        self.ORDEN_DE_PAGO =  self.PRESTAMO.ORDEN_DE_PAGO
        self.REGISTRO_PAGADO =  self.PRESTAMO.REGISTRO_PAGADO
        self.PROVEEDOR =  self.PRESTAMO.PROVEEDOR
        
        if self.PRESTAMO.PENDIENTE == -1 * self.IMPORTE:
            self.ESTADO = True
        # Actualizar el campo PENDIENTE del préstamo correspondiente
        
        self.PRESTAMO.PENDIENTE += self.IMPORTE
        self.PRESTAMO.save()

        super(devolucionPrestamo, self).save(*args, **kwargs)
        
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION DE PRESTAMOS

class proyeccionGastos(models.Model):
    CODIGO = models.CharField(max_length=120, null=True, blank=True)
    CONCEPTO = models.ForeignKey(concepto,on_delete=models.PROTECT, null=True, blank=True)
    PROVEEDOR = models.ForeignKey(proveedor,on_delete=models.PROTECT, null=True, blank=True)
    MES = models.CharField(max_length=255,null=False, blank=False,choices=MESES_CUSTOM) 
    EJERCICIO = models.CharField(max_length=255,null=False, blank=False,choices=EJERCICIO)
    PERIODO = models.DateField(null=True, blank=True) 
    IMPORTE = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    MODIFICADO_POR  = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    FECHA_MODIFICACION = models.CharField(max_length=120, null=True, blank=True)

        
    class Meta:
        verbose_name = 'Proyeccion de gasto'
        verbose_name_plural ='Proyecciones de gastos' 


    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.IMPORTE)

        if self.CODIGO:
            NAME = str(self.CODIGO) + " - " + str(self.MES) + " - " + str(self.PROVEEDOR) + " - $" + formatted_importe
        else:
            NAME = "NO SELECCIONADO - " + str(self.MES) + " - " + str(self.PROVEEDOR) + " - $" + formatted_importe

        return NAME
    
    def clean(self):

        if self.IMPORTE <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
 
        super().clean()

    def save(self, *args, **kwargs):

        mes_int = int(self.MES)
        ejercicio_int = int(self.EJERCICIO)
        self.PERIODO = datetime(ejercicio_int, mes_int, 1)

        super(proyeccionGastos, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE DEVOLUCION DE PRESTAMOS
class proyeccionIngresos(models.Model):
    RECURSO = models.ForeignKey(recurso,on_delete=models.PROTECT, null=True, blank=True)
    CLASIFICACION = models.ForeignKey(Equivalencia,on_delete=models.CASCADE,null=True, blank=True)
    MES = models.CharField(max_length=255,null=False, blank=False,choices=MESES_CUSTOM) 
    EJERCICIO = models.CharField(max_length=255,null=False, blank=False,choices=EJERCICIO)
    PERIODO = models.DateField(null=True, blank=True) 
    IMPORTE = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    MODIFICADO_POR  = models.DecimalField(max_digits=30,decimal_places=2,blank=True,null=True)
    FECHA_MODIFICACION = models.CharField(max_length=120, null=True, blank=True)

    class Meta:
        verbose_name = 'Proyeccion de ingreso'
        verbose_name_plural ='Proyecciones de ingresos' 

    def __str__(self):
        formatted_importe = '{:,.2f}'.format(self.IMPORTE)
        NAME = str(self.RECURSO) + " - " + str(self.MES) + "/" + str(self.EJERCICIO) + " - $" + formatted_importe
        return NAME
    
    def clean(self):

        if self.IMPORTE <= 0:
             raise ValidationError("Ingrese un importe mayor a $ 0.-")
 
        super().clean()

    def save(self, *args, **kwargs):

        mes_int = int(self.MES)
        ejercicio_int = int(self.EJERCICIO)
        self.PERIODO = datetime(ejercicio_int, mes_int, 1)

        super(proyeccionIngresos, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# CLASE PRESTAMOS
class regularizacion(models.Model):
    FECHA = models.DateField(null=False, blank=False) 
    GASTO = models.ForeignKey(asientosGastos,on_delete=models.PROTECT,null=False, blank=False)
    FONDO = models.ForeignKey(fondo,on_delete=models.PROTECT,null=True, blank=True)
    IMPORTE  = models.DecimalField(max_digits=30,decimal_places=2,blank=False,null=False)
    REGISTRO_PAGADO = models.CharField(max_length=120, null=True, blank=True)
    PROVEEDOR = models.CharField(max_length=120, null=True, blank=True)
    
    class Meta:
        verbose_name = 'Regularizacion'
        verbose_name_plural ='Regularizaciones' 
    
    def __str__(self):
        formatted_fecha = self.FECHA.strftime('%d/%m/%Y')
        NAME = "📅 " + formatted_fecha + " | 🧾" + str(self.GASTO) + " | 👤" + str(self.GASTO.RazonSocial)
        return NAME

    def clean(self):

        super().clean()

    def save(self, *args, **kwargs):

        super(regularizacion, self).save(*args, **kwargs)

# ------------------------------------------------------------------------------------------