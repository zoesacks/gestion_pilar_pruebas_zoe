# ------------------------------------------------------------------------------------------
# Calculadora de Tasas por Servicios Generales - Ministerio de Pilar
# Desarrollador Kevin Turkienich
# Septiembre 2023
# Kevin_turkienich@outlook.com
# ------------------------------------------------------------------------------------------

# Modelado de bases de datos para altas, bajas y modificaciones de datos maestros.

# ------------------------------------------------------------------------------------------
# Modulos importados
from django.db import models

caracteristicas = [
    ("ABIERTO","ABIERTO"),
    ("COUNTRY","COUNTRY"),
]
meses = [
    ("01","ENERO"),
    ("02","FEBRERO"),
    ("03","MARZO"),
    ("04","ABRIL"),
    ("05","MAYO"),
    ("06","JUNIO"),
    ("07","JULIO"),
    ("08","AGOSTO"),
    ("09","SEPTIEMBRE"),
    ("10","OCTUBRE"),
    ("11","NOVIEMBRE"),
    ("12","DICIEMBRE"),
]
# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# Tabla de alicuotas destino
class destinoFondo(models.Model):
    DESCRIPCION = models.CharField(max_length=255,blank=False,null=False)
    MODULO = models.DecimalField(max_digits=10,decimal_places=2,default=0, null=False, blank=False)

    def __str__(self):
        NAME = str(self.DESCRIPCION) + " - (Modulos:" + str(self.MODULO) + ")"
        return NAME
    
    class Meta:
        verbose_name = 'destino de fondo educativo'
        verbose_name_plural ='Config. Destinos fondo edu.' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------
# Tabla de alicuotas destino
class destino(models.Model):
    NUM_ORDENANZA = models.IntegerField(blank=False,null=False)
    ID_SISTEMA = models.IntegerField(blank=False,null=False)
    DESCRIPCION = models.CharField(max_length=255,blank=False,null=False)
    COEFICIENTE = models.DecimalField(max_digits=10,decimal_places=2,default=1, null=False, blank=False)
    MINIMO = models.DecimalField(max_digits=10,decimal_places=2,default=0, null=False, blank=False)
    EXCLUYE_FONDO = models.BooleanField(verbose_name="Excluye sub-tasa por Fondo Educativo",default=False)
    DESTINO_FONDO = models.ForeignKey(destinoFondo,models.CASCADE, null=True, blank=True)

    def __str__(self):
        NAME = str(self.DESCRIPCION) + " - (Coef:" + str(self.COEFICIENTE) + ")"
        return NAME
    
    class Meta:
        verbose_name = 'Destino'
        verbose_name_plural ='Tabla de destinos' 

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------

# --------------- Alicuotas y modulos ---------------
class configuracion(models.Model):
    EJERCICIO = models.IntegerField(blank=False,null=False,default=2023)
    MES = models.CharField(max_length=255,choices=meses,default=1,  null=False, blank=False)
    ALICUOTA = models.DecimalField(max_digits=15,decimal_places=4, null=True, blank=True)
    MODULO = models.DecimalField(max_digits=15,decimal_places=4, null=True, blank=True)
    BOMBERO = models.DecimalField(max_digits=15,decimal_places=2, null=False, blank=False)
    CORREO = models.DecimalField(max_digits=15,decimal_places=2, null=False, blank=False)
    ALICUOTA_PROYECTADA = models.DecimalField(max_digits=15,decimal_places=4, null=True, blank=True) 

    def __str__(self):
        NAME = str(self.MES) + "/" + str(self.EJERCICIO) + " ALIC: " + str(self.ALICUOTA) + " MOD: " + str(self.MODULO)
        return NAME
    
    class Meta:
        verbose_name = 'periodo'
        verbose_name_plural ='Conf. por periodo' 

# --------------- Partidas inmobiliarias ---------------
class partida(models.Model):
    PARTIDA = models.IntegerField(unique=True,blank=False,null=False)
    EJERCICIO = models.IntegerField(blank=False,null=False,default=2023)
    MES = models.CharField(max_length=255,choices=meses,default=1, null=False, blank=False)
    TITULAR = models.CharField(max_length=255, null=False, blank=False)
    CARACTERISTICA = models.CharField(max_length=255,choices=caracteristicas,default=1, null=False, blank=False) 
    BARRIO = models.CharField(max_length=255, null=True, blank=True)
    DESTINO = models.ForeignKey(destino,models.CASCADE, null=True, blank=True)
    VALUACION_FISCAL = models.DecimalField(max_digits=20,decimal_places=2,blank=True,null=True)

    EMISION_ANTERIOR = models.DecimalField(max_digits=20,default=0,decimal_places=2,blank=True,null=True)

    DESC_CONTRIBUYENTE = models.DecimalField(verbose_name="Desc. Buen Contr.)",max_digits=20,decimal_places=2,blank=False,null=False,default=0)
    DESC_DEBITO_AUT = models.DecimalField(verbose_name="Desc. Deb. Aut.", max_digits=20,decimal_places=2,blank=False,null=False,default=0)
    DESC_EDENOR = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=False,default=0)
    DESC_PARTIDA = models.DecimalField(max_digits=20,decimal_places=2,blank=False,null=False,default=0)
    CORREO = models.BooleanField(default=True,verbose_name="APLICA CORREO")


    def __str__(self):
        NAME = str(self.PARTIDA)
        return NAME
    
    class Meta:
        verbose_name = 'tasa'
        verbose_name_plural ='Base de tasas' 
    
    # --------------- FUNCIONES ---------------
    
    def tsg_neta(self):

        config = configuracion.objects.filter(EJERCICIO=self.EJERCICIO,MES=self.MES).first()
        destinos = destino.objects.filter(DESCRIPCION=self.DESTINO.DESCRIPCION).first()

        # Variables:
        x = float(self.VALUACION_FISCAL)       # Valor fiscal uniforme     > Se obtiene del mismo registro
        c = float(destinos.COEFICIENTE)        # Coeficiente destino       > Se obtiene cruzando el destino vs tabla de destinos (traer coeficiente)
        a = float(config.ALICUOTA)             # Alicuota                  > Se obtiene de configuracion configuracion.ALICUOTA
        m = float(config.MODULO)               # Módulo                    > Se obtiene de configuracion configuracion.MODULO
        b = float(config.BOMBERO)       # Bomberos                         > Se obtiene de configuracion configuracion.BOMBERO
        p = float(config.CORREO)       # Correo                            > Se obtiene de configuracion configuracion.CORREO
        h = float(self.DESTINO.MINIMO)       # Minimo                      > Se obtiene de la configuracioneS DESTINO > MINIMO
        f = 0                               # fondo educativo               
        tope = 5.86       # Tope                                           > Limite de aumento respecto a la cuota anterior (Valor en %)

        #tsg = float((VALUACION_FISCAL * ALICUOTA * COEFICIENTE * MODULO)/12)
        tsg = float((x * a * c * m)/12) # tsg_bruta

        # Aplicacion de minimo.
        if h > 0: #si el minimo es mayor a 0
            if tsg < h:  #si la tsg_bruta es menor que el minimo
                tsg = h  # el minimo de la tsg_bruta se aplica.

        # calculo de sub-tasas

        # Si no deberia aplicar correo se puede excluir desde la siguiente linea
        if self.CORREO == False:#                                          > Verificar si la casilla de correo esta acriva:
            p = 0

        # calculo de fondo educativo
        if self.DESTINO.EXCLUYE_FONDO:        #                > Se obtiene del caclulo de la funcion
            f = 0 
        else:
            if self.CARACTERISTICA == "ABIERTO":
                f = 14
            else:
                f = 34  

        # calculo para Justicia

        if tsg < 1456:
            calculo = tsg / 2
        elif tsg < 6370:
            calculo = round((((tsg-1456) * 0.45) + 728),2)
        elif tsg < 14560:
            calculo = round((((tsg-6370)) * 0.35 + 2939.3),2)       
        elif tsg < 25480:
            calculo = round((((tsg-14560)) * 0.3 + 5805.8),2)
        else:
            calculo = round(((tsg-25480.01)) * 0.25 + 9081.8,2)

        j = calculo        # Justicia

      # tsg_bruto = round(tsg_bruta + (((BOMBERO + CORREO + fondo educativo) * modulo) + justicia))
        tsg_bruto = round(tsg + (((b + p + f) * m) + j)) # calculo TSG bruto
        

        # si existe descuento por buen contribuyente, se toma el valor en %
        dc = round(self.DESC_CONTRIBUYENTE,2)   # Descuento contribuyente  

        dd = round(self.DESC_DEBITO_AUT,2)      # Descuento Debito autom.

        de = self.DESC_EDENOR     # Descuento Edenor 

        dp = self.DESC_PARTIDA      # Descuento Partida Global

        tsg_neto = round( tsg_bruto - (de + dd + dp + dc),2) # CALCULO TSG NETA
        
        # en caso que la tsg_neta de negatibo setear en $0
        if tsg_neto < 0:
            tsg_neto = 0

        return tsg_neto

    def total_tsg(self):

        config = configuracion.objects.filter(EJERCICIO=self.EJERCICIO,MES=self.MES).first()
        destinos = destino.objects.filter(DESCRIPCION=self.DESTINO.DESCRIPCION).first()

        # Variables:
        x = float(self.VALUACION_FISCAL)       # Valor fiscal uniforme     > Se obtiene del mismo registro
        c = float(destinos.COEFICIENTE)        # Coeficiente destino       > Se obtiene cruzando el destino vs tabla de destinos (traer coeficiente)
        a = float(config.ALICUOTA)             # Alicuota                  > Se obtiene de configuracion configuracion.ALICUOTA
        m = float(config.MODULO)               # Módulo                    > Se obtiene de configuracion configuracion.MODULO
        b = float(config.BOMBERO)       # Bomberos                         > Se obtiene de configuracion configuracion.BOMBERO
        p = float(config.CORREO)       # Correo                            > Se obtiene de configuracion configuracion.CORREO
        h = float(self.DESTINO.MINIMO)       # Minimo                      > Se obtiene de la configuracioneS DESTINO > MINIMO
        f = 0                               # fondo educativo               
        tope = 5.86       # Tope                                           > Limite de aumento respecto a la cuota anterior (Valor en %)

        #tsg = float((VALUACION_FISCAL * ALICUOTA * COEFICIENTE * MODULO)/12)
        tsg = float((x * a * c * m)/12) # tsg_bruta

        # Aplicacion de minimo.
        if h > 0: #si el minimo es mayor a 0
            if tsg < h:  #si la tsg_bruta es menor que el minimo
                tsg = h  # el minimo de la tsg_bruta se aplica.

        # calculo de sub-tasas

        # Si no deberia aplicar correo se puede excluir desde la siguiente linea
        if self.CORREO == False:#                                          > Verificar si la casilla de correo esta acriva:
            p = 0

        # calculo de fondo educativo
        if self.DESTINO.EXCLUYE_FONDO:        #                > Se obtiene del caclulo de la funcion
            f = 0 
        else:
            if self.CARACTERISTICA == "ABIERTO":
                f = 14
            else:
                f = 34  

        # calculo para Justicia

        if tsg < 1456:
            calculo = tsg / 2
        elif tsg < 6370:
            calculo = round((((tsg-1456) * 0.45) + 728),2)
        elif tsg < 14560:
            calculo = round((((tsg-6370)) * 0.35 + 2939.3),2)       
        elif tsg < 25480:
            calculo = round((((tsg-14560)) * 0.3 + 5805.8),2)
        else:
            calculo = round(((tsg-25480.01)) * 0.25 + 9081.8,2)

        j = calculo        # Justicia

      # tsg_bruto = round(tsg_bruta + (((BOMBERO + CORREO + fondo educativo) * modulo) + justicia))
        tsg_bruto = round(tsg + (((b + p + f) * m) + j)) # calculo TSG bruto
        

        # si existe descuento por buen contribuyente, se toma el valor en %
        dc = round(self.DESC_CONTRIBUYENTE,2)   # Descuento contribuyente  

        dd = round(self.DESC_DEBITO_AUT,2)      # Descuento Debito autom.

        de = self.DESC_EDENOR     # Descuento Edenor 

        dp = self.DESC_PARTIDA      # Descuento Partida Global

        tsg_neto = round( tsg_bruto - (de + dd + dp + dc),2) # CALCULO TSG NETA
        
        # Aplicacion de tope

        if self.EMISION_ANTERIOR > 0 and self.EMISION_ANTERIOR < tsg_neto:    # Descuento Por Tope
            excedente = float(tsg_neto - self.EMISION_ANTERIOR) / float(self.EMISION_ANTERIOR) * 100
            if excedente > tope:
                tsg_neto = float(self.EMISION_ANTERIOR) + float(float(self.EMISION_ANTERIOR) * float(5.86) / 100)
            elif excedente > 0:
                tsg_neto = float(self.EMISION_ANTERIOR) + float(float(self.EMISION_ANTERIOR) * float(excedente) / 100)

        # en caso que la tsg_neta de negatibo setear en $0
        if tsg_neto < 0:
            tsg_neto = 0

        return tsg_neto

    def tsg(self):

        config = configuracion.objects.first()
        destinos = destino.objects.filter(DESCRIPCION=self.DESTINO.DESCRIPCION).first()

        # Variables:
        x = float(self.VALUACION_FISCAL)       # Valor fiscal uniforme     > Se obtiene del mismo registro
        c = float(destinos.COEFICIENTE)        # Coeficiente destino       > Se obtiene cruzando el destino vs tabla de destinos (traer coeficiente)
        a = float(config.ALICUOTA)             # Alicuota                  > Se obtiene de configuracion configuracion.ALICUOTA
        m = float(config.MODULO)               # Módulo                    > Se obtiene de configuracion configuracion.MODULO
        b = float(config.BOMBERO)       # Bomberos                         > Se obtiene de configuracion configuracion.BOMBERO
        p = float(config.CORREO)       # Correo                            > Se obtiene de configuracion configuracion.CORREO
        h = float(self.DESTINO.MINIMO)       # Minimo                      > Se obtiene de la configuracioneS DESTINO > MINIMO
        f = 0                               # fondo educativo               
        tope = 5.86       # Tope                                           > Limite de aumento respecto a la cuota anterior (Valor en %)

        #tsg = float((VALUACION_FISCAL * ALICUOTA * COEFICIENTE * MODULO)/12)
        tsg = float((x * a * c * m)/12) # tsg_bruta

        # Aplicacion de minimo.
        if h > 0: #si el minimo es mayor a 0
            if tsg < h:  #si la tsg_bruta es menor que el minimo
                tsg = h  # el minimo de la tsg_bruta se aplica.

        return tsg

    def tsg_bruta(self):

        config = configuracion.objects.first()
        destinos = destino.objects.filter(DESCRIPCION=self.DESTINO.DESCRIPCION).first()

        # Variables:
        x = float(self.VALUACION_FISCAL)       # Valor fiscal uniforme     > Se obtiene del mismo registro
        c = float(destinos.COEFICIENTE)        # Coeficiente destino       > Se obtiene cruzando el destino vs tabla de destinos (traer coeficiente)
        a = float(config.ALICUOTA)             # Alicuota                  > Se obtiene de configuracion configuracion.ALICUOTA
        m = float(config.MODULO)               # Módulo                    > Se obtiene de configuracion configuracion.MODULO
        b = float(config.BOMBERO)       # Bomberos                         > Se obtiene de configuracion configuracion.BOMBERO
        p = float(config.CORREO)       # Correo                            > Se obtiene de configuracion configuracion.CORREO
        h = float(self.DESTINO.MINIMO)       # Minimo                      > Se obtiene de la configuracioneS DESTINO > MINIMO
        f = 0                               # fondo educativo               
        tope = 5.86       # Tope                                           > Limite de aumento respecto a la cuota anterior (Valor en %)

        #tsg = float((VALUACION_FISCAL * ALICUOTA * COEFICIENTE * MODULO)/12)
        tsg = float((x * a * c * m)/12) # tsg_bruta

        # Aplicacion de minimo.
        if h > 0: #si el minimo es mayor a 0
            if tsg < h:  #si la tsg_bruta es menor que el minimo
                tsg = h  # el minimo de la tsg_bruta se aplica.

        # calculo de sub-tasas

        # Si no deberia aplicar correo se puede excluir desde la siguiente linea
        if self.CORREO == False:#                                          > Verificar si la casilla de correo esta acriva:
            p = 0

        # calculo de fondo educativo
        if self.DESTINO.EXCLUYE_FONDO:        #                > Se obtiene del caclulo de la funcion
            f = 0 
        else:
            if self.CARACTERISTICA == "ABIERTO":
                f = 14
            else:
                f = 34  

        # calculo para Justicia
        if tsg < 1456:
            calculo = tsg / 2
        elif tsg < 6370:
            calculo = round((((tsg-1456) * 0.45) + 728),2)
        elif tsg < 14560:
            calculo = round((((tsg-6370)) * 0.35 + 2939.3),2)       
        elif tsg < 25480:
            calculo = round((((tsg-14560)) * 0.3 + 5805.8),2)
        else:
            calculo = round(((tsg-25480.01)) * 0.25 + 9081.8,2)

        j = calculo        # Justicia

      # tsg_bruto = round(tsg_bruta + (((BOMBERO + CORREO + fondo educativo) * modulo) + justicia))
        tsg_bruto = round(tsg + (((b + p + f) * m) + j)) # calculo TSG bruto

        return tsg_bruto

    def tsg_justicia(self):

        config = configuracion.objects.first()
        destinos = destino.objects.filter(DESCRIPCION=self.DESTINO.DESCRIPCION).first()

        # Variables:
        x = float(self.VALUACION_FISCAL)       # Valor fiscal uniforme     > Se obtiene del mismo registro
        c = float(destinos.COEFICIENTE)        # Coeficiente destino       > Se obtiene cruzando el destino vs tabla de destinos (traer coeficiente)
        a = float(config.ALICUOTA)             # Alicuota                  > Se obtiene de configuracion configuracion.ALICUOTA
        m = float(config.MODULO)               # Módulo                    > Se obtiene de configuracion configuracion.MODULO
        h = float(self.DESTINO.MINIMO)       # Minimo                      > Se obtiene de la configuracioneS DESTINO > MINIMO

        #tsg = float((VALUACION_FISCAL * ALICUOTA * COEFICIENTE * MODULO)/12)
        tsg = float((x * a * c * m)/12) # tsg_bruta

        # Aplicacion de minimo.
        if h > 0: #si el minimo es mayor a 0
            if tsg < h:  #si la tsg_bruta es menor que el minimo
                tsg = h  # el minimo de la tsg_bruta se aplica.

        if tsg < 1456:
            calculo = tsg / 2
        elif tsg < 6370:
            calculo = round((((tsg-1456) * 0.45) + 728),2)
        elif tsg < 14560:
            calculo = round((((tsg-6370)) * 0.35 + 2939.3),2)       
        elif tsg < 25480:
            calculo = round((((tsg-14560)) * 0.3 + 5805.8),2)
        else:
            calculo = round(((tsg-25480.01)) * 0.25 + 9081.8,2)

        j = calculo        # Justicia

        return j

    def tsg_bombero(self):

        config = configuracion.objects.first()
        
        # Variables:
        p = float(config.BOMBERO)  
        m = float(config.MODULO)

        # Si no deberia aplicar correo se puede excluir desde la siguiente linea
        if self.CORREO == False:#                                          > Verificar si la casilla de correo esta acriva:
            p = 0

        tsg_bruto = round(p*m,2) # calculo TSG bruto

        return tsg_bruto
  
    def tsg_correo(self):


        config = configuracion.objects.first()
        
        # Variables:
        p = float(config.CORREO)  
        m = float(config.MODULO)

        tsg_bruto = round(p*m,2) # calculo TSG bruto

        return tsg_bruto

    def total_tsg_proyectada(self):

        config = configuracion.objects.first()
        destinos = destino.objects.filter(DESCRIPCION=self.DESTINO.DESCRIPCION).first()

        # Variables:
        x = float(self.VALUACION_FISCAL)       # Valor fiscal uniforme     > Se obtiene del mismo registro
        c = float(destinos.COEFICIENTE)        # Coeficiente destino       > Se obtiene cruzando el destino vs tabla de destinos (traer coeficiente)
        a = float(config.ALICUOTA_PROYECTADA)             # Alicuota                  > Se obtiene de configuracion configuracion.ALICUOTA_PROYECTADA
        m = float(config.MODULO)               # Módulo                    > Se obtiene de configuracion configuracion.MODULO
        b = float(config.BOMBERO)       # Bomberos                         > Se obtiene de configuracion configuracion.BOMBERO
        p = float(config.CORREO)       # Correo                            > Se obtiene de configuracion configuracion.CORREO
        h = float(self.DESTINO.MINIMO)       # Minimo                      > Se obtiene de la configuracioneS DESTINO > MINIMO
        f = 0                               # fondo educativo               
        tope = 5.86       # Tope                                           > Limite de aumento respecto a la cuota anterior (Valor en %)

        #tsg = float((VALUACION_FISCAL * ALICUOTA * COEFICIENTE * MODULO)/12)
        tsg = float((x * a * c * m)/12) # tsg_bruta

        # Aplicacion de minimo.
        if h > 0: #si el minimo es mayor a 0
            if tsg < h:  #si la tsg_bruta es menor que el minimo
                tsg = h  # el minimo de la tsg_bruta se aplica.

        # calculo de sub-tasas

        # Si no deberia aplicar correo se puede excluir desde la siguiente linea
        if self.CORREO == False:#                                          > Verificar si la casilla de correo esta acriva:
            p = 0

        # calculo de fondo educativo
        if self.DESTINO.EXCLUYE_FONDO:        #                > Se obtiene del caclulo de la funcion
            f = 0 
        else:
            if self.CARACTERISTICA == "ABIERTO":
                f = 14
            else:
                f = 34  

        # calculo para Justicia

        if tsg < 1456:
            calculo = tsg / 2
        elif tsg < 6370:
            calculo = round((((tsg-1456) * 0.45) + 728),2)
        elif tsg < 14560:
            calculo = round((((tsg-6370)) * 0.35 + 2939.3),2)       
        elif tsg < 25480:
            calculo = round((((tsg-14560)) * 0.3 + 5805.8),2)
        else:
            calculo = round(((tsg-25480.01)) * 0.25 + 9081.8,2)

        j = calculo        # Justicia

      # tsg_bruto = round(tsg_bruta + (((BOMBERO + CORREO + fondo educativo) * modulo) + justicia))
        tsg_bruto = round(tsg + (((b + p + f) * m) + j)) # calculo TSG bruto
        

        # si existe descuento por buen contribuyente, se toma el valor en %
        dc = round(self.DESC_CONTRIBUYENTE,2)   # Descuento contribuyente  

        dd = round(self.DESC_DEBITO_AUT,2)      # Descuento Debito autom.

        de = self.DESC_EDENOR     # Descuento Edenor 

        dp = self.DESC_PARTIDA      # Descuento Partida Global

        tsg_neto = round( tsg_bruto- (de + dd + dp + dc),2) # CALCULO TSG NETA
        
        # Aplicacion de tope

        # en caso que la tsg_neta de negatibo setear en $0
        if tsg_neto < 0:
            tsg_neto = 0

        return tsg_neto

    def tsg_fondo_educativo(self):

        config = configuracion.objects.first()
        destino = destinoFondo.objects.filter(DESCRIPCION=self.DESTINO.DESTINO_FONDO.DESCRIPCION).first()

        m = float(config.MODULO)

        # calculo de fondo educativo
        if self.DESTINO.EXCLUYE_FONDO:     
            f = 0 
        else:
            f = float(destino.MODULO)

        fondo = f * m

        return fondo

    # --------------- FIN FUNCIONES ---------------

# ------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------