from django.http import HttpResponse
from reportlab.lib.pagesizes import legal
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from django.contrib import admin, messages
import os
import locale
from .models import configuracion

@admin.action(description="Descargar reporte")
def generar_reporte(modeladmin, request, queryset):

    #Validacion para que seleccione solo 1 queryset
    if len(queryset) != 1:
        messages.error(request, "Solo se puede emitir 1 tasa a la vez")
        return

    #Capturo la ruta actual para la ruta del logo
    current_directory = os.getcwd()

    logo_path = os.path.join(current_directory, 'static/assets/logo_fondo_b.png')

    # Obtener el primer pedido seleccionado
    tasa = queryset[0]

    config = configuracion.objects.filter(EJERCICIO=tasa.EJERCICIO,MES=tasa.MES).first()

    nombre_empresa = "Tasa por servicios generales"
    direccion_empresa = "Calculo generado por Gestion Pilar"


    # Establecer el idioma en español
    locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

    #Crear el objeto
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="TSG_{tasa.PARTIDA}.pdf"'

    # Crear el lienzo PDF
    p = canvas.Canvas(response, pagesize=legal)

    # Agregar contenido al lienzo
    y = 950  # Posición vertical inicial
    x = 50
        # Verificar si el archivo de imagen del logo existe
    if logo_path:
        # Tamaño y posición del logo
        logo_width = 180  # Ancho del logo
        logo_height = 130 # Alto del logo
        logo_x = 410  # Posición horizontal del logo
        logo_y = 865  # Posición vertical del logo

        # Agregar el logo al lienzo PDF
        logo_image = ImageReader(logo_path)
        p.drawImage(logo_image, logo_x, logo_y, width=logo_width, height=logo_height)

    # Titulo del reporte
    p.setFont("Helvetica-Bold", 18)
    p.drawString(x, y, nombre_empresa)
    y -= 20

    p.setFont("Helvetica", 12)  # Fuente normal
    p.drawString(x, y, direccion_empresa)
    y -= 50

    # Detalle de la cuota
    p.setFont("Helvetica-Bold", 13)
    p.drawString(x, y, f"Partida inmobiliaria : {tasa.PARTIDA}")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Ejercicio: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = f'{tasa.EJERCICIO}'
    p.drawString(120, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Cuota: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = f'{tasa.MES}'
    p.drawString(120, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Modulo: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = f'{config.MODULO}'
    p.drawString(120, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Alicuota: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = f'{config.ALICUOTA}'
    p.drawString(120, y, codigo_str)
    y -= 15

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Minimo: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = f'{tasa.DESTINO.MINIMO}'
    p.drawString(120, y, codigo_str)
    y -= 40

    # Calculo tsg neta
    p.setFont("Helvetica-Bold", 13)
    p.drawString(x, y, "Calculo de TSG Neta:")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Val. Fiscal Unif.: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.VALUACION_FISCAL))
    p.drawString(140, y, codigo_str)
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Destino:")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(tasa.DESTINO.DESCRIPCION)
    p.drawString(140, y, codigo_str)
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Destino Fiscal:")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str(f'{str(tasa.DESTINO.DESTINO_FONDO.DESCRIPCION)[:50]} |  Coef: {tasa.DESTINO.DESTINO_FONDO.MODULO}')
    p.drawString(140, y, codigo_str)
    y -= 40


    p.setFont("Helvetica", 10)
    p.drawString(x, y, "Calculo TSG Base : (Val_Fiscal * Alicuota * Coeficiente * Modulo) / 12")
    y -= 20
    p.drawString(x, y, f"Calculo TSG Base : ({tasa.VALUACION_FISCAL} * {config.ALICUOTA} * {tasa.DESTINO.DESTINO_FONDO.MODULO} * {config.MODULO}) / 12")
    y -= 30
    p.setFont("Helvetica-Bold", 13)

    calculo = round(( tasa.VALUACION_FISCAL * config.ALICUOTA * tasa.DESTINO.DESTINO_FONDO.MODULO * config.MODULO ) / 12,0)
    if calculo < tasa.DESTINO.MINIMO:
        p.setFont("Helvetica-Bold", 10)
        codigo_str = str("TSG Neta $ {:,.2f}".format(calculo))
        p.drawString(x, y, codigo_str)
        y -= 20

        p.setFont("Helvetica-Bold", 10)
        p.drawString(x, y, f"Aplica el minimo de TSG")
        y -= 20

    p.drawString(x, y, "TSG Base : ")
    p.setFont("Helvetica", 14)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.tsg()))
    p.drawString(120, y, codigo_str)
    y -= 40

    # Calculo tsg bruta
    p.setFont("Helvetica-Bold", 13)
    p.drawString(x, y, "Calculo de TSG Bruta:")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Exclusion correo: ")
    p.setFont("Helvetica", 10)  # Fuente normal

    if tasa.CORREO:
        codigo_str = str("NO")

        p.drawString(140, y, codigo_str)
        y -= 20

        p.setFont("Helvetica-Bold", 10)
        p.drawString(x, y, "Tasa Correo:")
        p.setFont("Helvetica", 10)  # Fuente normal
        codigo_str = str("$ {:,.2f}".format(tasa.tsg_correo()))
        p.drawString(140, y, codigo_str)
        y -= 20

    else:
        codigo_str = str("SI")
        p.drawString(140, y, codigo_str)
        y -= 20


    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Tasa Bomberos: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.tsg_bombero()))
    p.drawString(140, y, codigo_str)
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Tasa Justicia: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.tsg_justicia()))
    p.drawString(140, y, codigo_str)
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Tasa F. Educativo: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.tsg_fondo_educativo()))
    p.drawString(140, y, codigo_str)
    y -= 40


    p.setFont("Helvetica", 10)
    p.drawString(x, y, "Calculo TSG Bruta : TSG Base + Tasa Correo + Tasa Bombero + Tasa Justicia + Tasa F. Educativo")
    y -= 20
    p.drawString(x, y, f"Calculo TSG Bruta : {round(tasa.tsg(),2)} + {round(tasa.tsg_correo(),2)} + {round(tasa.tsg_bombero(),2)} + {round(tasa.tsg_justicia(),2)} + {round(tasa.tsg_fondo_educativo(),2)}")

    y -= 30
    p.setFont("Helvetica-Bold", 13)
    p.drawString(x, y, "TSG Bruta : ")
    p.setFont("Helvetica", 14)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.tsg_bruta()))
    p.drawString(130, y, codigo_str)
    y -= 40


    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "Descuentos: ")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Buen contribuyente: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.DESC_CONTRIBUYENTE))
    p.drawString(160, y, codigo_str)
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Debito automatico: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.DESC_DEBITO_AUT))
    p.drawString(160, y, codigo_str)
    y -= 20


    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Edenor: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.DESC_EDENOR))
    p.drawString(160, y, codigo_str)
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Partida Global: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.DESC_PARTIDA))
    p.drawString(160, y, codigo_str)
    y -= 40


    p.setFont("Helvetica", 10)
    p.drawString(x, y, "Emision TSG Neta : TSG Bruta - (Desc. Buen Contr. + Desc. Debito Aut. + Desc. Edenor + Desc. Partida Global)")
    y -= 20
    p.drawString(x, y, f"Calculo TSG Neta : {round(tasa.DESC_CONTRIBUYENTE,2)} + {round(tasa.DESC_DEBITO_AUT,2)} + {round(tasa.DESC_EDENOR,2)} + {round(tasa.DESC_PARTIDA,2)} + {round(tasa.tsg_fondo_educativo(),2)}")

    y -= 30
    p.setFont("Helvetica-Bold", 13)
    p.drawString(x, y, "TSG Neta : ")
    p.setFont("Helvetica", 14)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.tsg_neta()))
    p.drawString(130, y, codigo_str)
    y -= 40


    p.setFont("Helvetica-Bold", 12)
    p.drawString(x, y, "Aplicacion de TOPE: ")
    y -= 20

    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Emision Anterior: ")
    p.setFont("Helvetica", 10)  # Fuente normal
    codigo_str = str("$ {:,.2f}".format(tasa.EMISION_ANTERIOR))
    p.drawString(160, y, codigo_str)
    y -= 20


    p.setFont("Helvetica-Bold", 10)
    p.drawString(x, y, "Limite Exc.:")
    p.setFont("Helvetica", 10)  # Fuente normal
    emision_ant = float(tasa.EMISION_ANTERIOR)
    calculo = emision_ant * float(5.86) / 100

    codigo_str = "$ {:,.2f}".format(calculo)
    p.drawString(160, y, str(codigo_str))

    p.setFont("Helvetica", 10)  # Fuente normal
    calculo = float(tasa.EMISION_ANTERIOR) * float(5.86) / 100
    codigo_str = "$ {:,.2f}".format(calculo)
    p.drawString(160, y, str(codigo_str))
    y -= 20
    

    calculo = float(tasa.tsg_neta()) - float(tasa.EMISION_ANTERIOR)
    codigo_str = "{:,.2f}".format(calculo)
    if calculo > 0:
        p.setFont("Helvetica-Bold", 10)
        p.drawString(x, y, "Excedente por TOPE:")
        
        
        p.setFillColorRGB(1, 0, 0)  # Color en RGB (rojo puro)

        # Dibujar el texto en rojo con un signo negativo
        p.drawString(160, y, f'$ -{codigo_str}')

        # Restaurar el color de relleno a negro (o el color deseado)
        p.setFillColorRGB(0, 0, 0)

        y -= 40

    p.setFont("Helvetica-Bold", 15)
    p.drawString(x, y, "TSG a Emitir : ")
    p.setFont("Helvetica", 14)  # Fuente norma

    codigo_str = str("$ {:,.2f}".format(tasa.total_tsg()))
    p.drawString(150, y, codigo_str)
    # Restaurar el color de relleno a negro (o el color deseado)

    
  
    y -= 40


    y -= 20


    p.save()

    return response


