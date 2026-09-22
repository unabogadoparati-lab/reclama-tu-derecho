#!/usr/bin/env python3
"""
Generador de documentos para consumidores y divulgación legal.

Tipos soportados (campo 'tipo'):
- 'amazon_retraso'     -> Reclamación previa por incumplimiento de plazo de entrega
- 'articulo_ai_legal'  -> Artículo divulgativo sobre IA y derecho (SEO / blog)
- 'generica'           -> Reclamación genérica

Las plantillas usan marcadores del estilo [NOMBRE_DEL_CAMPO], que se
sustituyen con el diccionario de datos recibido. Si un marcador no tiene
dato asociado, se deja tal cual en la salida (útil como borrador).
"""

import os
import re
import sys
from datetime import datetime

# Marcadores del tipo [NOMBRE], sin anidamiento de corchetes.
PATRON_MARCADOR = re.compile(r'\[([^\[\]]+)\]')

# Mapa tipo -> fichero de plantilla
PLANTILLAS = {
    'amazon_retraso': 'reclamacion_amazon_retraso_entrega.txt',
    'articulo_ai_legal': 'articulo_ai_legal.txt',
    'generica': 'plantilla_reclamacion_generica.txt',
}

# Prefijo del nombre de fichero de salida por tipo
PREFIJOS = {
    'articulo_ai_legal': 'articulo',
    'amazon_retraso': 'reclamacion',
    'generica': 'reclamacion',
}


class ReclamacionGenerator:
    """Genera documentos a partir de plantillas con marcadores [CAMPO]."""

    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        self.plantillas_dir = os.path.join(base, '..', 'plantillas')
        self.output_dir = os.path.join(base, '..', 'generadas')
        os.makedirs(self.output_dir, exist_ok=True)

    def cargar_plantilla(self, nombre_plantilla):
        """Carga una plantilla desde el directorio de plantillas."""
        ruta_plantilla = os.path.join(self.plantillas_dir, nombre_plantilla)
        try:
            with open(ruta_plantilla, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Plantilla {nombre_plantilla} no encontrada")
            return None

    @staticmethod
    def sustituir(texto, valores):
        """Reemplaza los marcadores [CAMPO] por su valor.

        Los marcadores sin valor (o con valor vacío) se conservan intactos.
        """
        def _reemplazo(match):
            clave = match.group(1).strip()
            valor = valores.get(clave)
            if valor is None or str(valor).strip() == '':
                return match.group(0)
            return str(valor)

        return PATRON_MARCADOR.sub(_reemplazo, texto)

    def construir_valores(self, datos):
        """Normaliza el diccionario de datos a los marcadores de plantilla."""
        hoy = datetime.now().strftime('%d/%m/%Y')
        return {
            # --- comunes ---
            'FECHA': datos.get('fecha', hoy),
            'LOGO O NOMBRE DE TU SERVICIO': datos.get('marca', ''),

            # --- reclamaciones ---
            'EMPRESA': datos.get('empresa', ''),
            'NUMERO_DE_PEDIDO': datos.get('numero_pedido', ''),
            'NOMBRE_USUARIO': datos.get('nombre_usuario', ''),
            'DNI': datos.get('dni', ''),
            'EMAIL': datos.get('email', ''),
            'FECHA_PEDIDO': datos.get('fecha_pedido', ''),
            'FECHA_ESTIMADA': datos.get('fecha_estimada', ''),
            'FECHA_REAL': datos.get('fecha_real', ''),
            'NUMERO_DIAS': datos.get('numero_dias', ''),
            'IMPORTE': datos.get('importe', ''),
            'DESCRIPCION_DETALLADA_DEL_INCUMPLIMIENTO': datos.get('descripcion', ''),
            'LEYES_Y_ARTICULOS_APLICABLES': datos.get('leyes', ''),
            'CONDICIONES_DE_VENTA_EMPRESA_SECCION_RELEVANTE': datos.get('condiciones', ''),
            'PETICIONES_CONCRETAS': datos.get('peticiones', ''),
            'DOCUMENTOS_ADJUNTOS': datos.get('documentos_adjuntos', ''),
            'FIRMA': datos.get('firma', datos.get('nombre_usuario', '')),

            # --- artículos divulgativos ---
            'TITULO_ARTICULO': datos.get('titulo', ''),
            'INTRODUCCION': datos.get('introduccion', ''),
            'DESARROLLO': datos.get('desarrollo', ''),
            'CONCLUSION': datos.get('conclusion', ''),
            'LLAMADA_ACCION': datos.get('llamada_accion', ''),
            'PALABRAS_CLAVE': datos.get('palabras_clave', ''),
        }

    # Nombre histórico: se mantiene por compatibilidad con app.py
    def generar_reclamacion(self, datos):
        """Genera un documento (reclamación o artículo) y devuelve su ruta."""
        tipo = datos.get('tipo', 'generica')
        nombre_plantilla = PLANTILLAS.get(tipo, PLANTILLAS['generica'])
        plantilla_content = self.cargar_plantilla(nombre_plantilla)

        if not plantilla_content:
            return None

        valores = self.construir_valores(datos)
        documento = self.sustituir(plantilla_content, valores)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        prefijo = PREFIJOS.get(tipo, 'documento')
        if tipo == 'articulo_ai_legal':
            nombre_archivo = f"{prefijo}_{timestamp}.txt"
        else:
            empresa = str(datos.get('empresa', 'empresa')).lower().replace(' ', '_')
            nombre_archivo = f"{prefijo}_{empresa}_{tipo}_{timestamp}.txt"

        ruta_salida = os.path.join(self.output_dir, nombre_archivo)

        try:
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(documento)
            return ruta_salida
        except Exception as e:
            print(f"Error al guardar el documento: {e}")
            return None


def _datos_ejemplo_reclamacion():
    return {
        'tipo': 'amazon_retraso',
        'empresa': 'Amazon España',
        'numero_pedido': 'ES123456789-0123456',
        'nombre_usuario': 'Juan Pérez López',
        'dni': '12345678Z',
        'email': 'juan.perez@email.com',
        'fecha_pedido': '15/11/2026',
        'fecha_estimada': '20/11/2026',
        'fecha_real': '27/11/2026',
        'numero_dias': '7',
        'importe': '89,99',
        'descripcion': (
            'Realicé el pedido ES123456789-0123456 el 15/11/2026 con fecha estimada '
            'de entrega el 20/11/2026. Sin embargo, la entrega se realizó efectivamente '
            'el 27/11/2026, lo que constituye un retraso de 7 días hábiles respecto a la '
            'fecha estimada proporcionada por Amazon.'
        ),
        'leyes': (
            '- Artículo 20 de la Ley 7/1996, de Ordenación del Comercio Minorista.\n'
            '- Artículo 123 del Real Decreto Legislativo 1/2007 (Texto Refundido de la '
            'Ley General para la Defensa de los Consumidores y Usuarios).\n'
            '- Directiva 2011/83/UE sobre los derechos de los consumidores.'
        ),
        'condiciones': (
            'Condiciones de Venta de Amazon.es, sección 5 (Entrega) y política de '
            'atención al cliente.'
        ),
        'peticiones': (
            '1. El reembolso íntegro del importe abonado por el pedido '
            'ES123456789-0123456 (89,99 €).\n'
            '2. La compensación por los daños y perjuicios ocasionados por el retraso.\n'
            '3. Que dicha resolución se comunique por escrito a mi correo '
            'juan.perez@email.com en un plazo máximo de 10 días hábiles.'
        ),
        'documentos_adjuntos': (
            'Copia del pedido ES123456789-0123456 (confirmación de compra)\n'
            'Historial de seguimiento del envío (fecha estimada vs. fecha real)'
        ),
    }


def _datos_ejemplo_articulo():
    return {
        'tipo': 'articulo_ai_legal',
        'marca': 'Abogado Gatell',
        'titulo': (
            '¿Puede una IA negarte el reembolso por un retraso en Amazon? '
            'Lo que dice la nueva Directiva de IA de la UE'
        ),
        'introduccion': (
            'Imagina este escenario: esperas tu paquete de Amazon, pero llega con una '
            'semana de retraso. Solicitas el reembolso y recibes una respuesta automática '
            'denegada por un "sistema de IA que detecta fraude". ¿Es legal?\n\n'
            'Con la entrada en vigor progresiva de la Directiva (UE) 2024/1689 sobre '
            'Inteligencia Artificial (la "IA Act"), esta pregunta deja de ser teórica '
            'para millones de consumidores españoles.'
        ),
        'desarrollo': (
            '## ¿Qué dice la normativa?\n'
            'La regulación europea clasifica los sistemas de IA por nivel de riesgo. Los '
            'que deciden sobre reembolsos, préstamos o seguros se consideran de alto '
            'riesgo (Art. 6 y Anexo III), con obligaciones de transparencia (Art. 52), '
            'derecho a explicación (Art. 14) e intervención humana (Art. 22 RGPD).\n\n'
            '## Qué puedes hacer\n'
            '1. Solicita explícitamente revisión humana.\n'
            '2. Pide la lógica de la decisión.\n'
            '3. Documenta todo (capturas, referencias, fechas).\n'
            '4. Escala al DPO de la empresa, a la AEPD o a los tribunales.'
        ),
        'conclusion': (
            'La normativa no prohíbe usar IA en atención al cliente: exige límites y '
            'supervisión humana. La tecnología debe servir a las personas, no al revés.'
        ),
        'llamada_accion': (
            '¿Te ha ocurrido algo similar? Cuéntalo en comentarios para ayudar a otros '
            'consumidores a conocer sus derechos.'
        ),
        'palabras_clave': (
            'inteligencia artificial, derechos del consumidor, IA Act, Directiva UE '
            '2024/1689, reembolso Amazon, decisiones automatizadas, RGPD, IA legal España'
        ),
    }


def ejemplo_uso(tipo='amazon_retraso'):
    """Genera un documento de ejemplo y lo muestra por consola."""
    datos = _datos_ejemplo_articulo() if tipo == 'articulo_ai_legal' else _datos_ejemplo_reclamacion()
    generator = ReclamacionGenerator()
    ruta_generada = generator.generar_reclamacion(datos)

    if ruta_generada:
        print(f"Documento generado exitosamente en: {ruta_generada}")
        print("\n--- PREVIA DEL DOCUMENTO ---\n")
        with open(ruta_generada, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("Error al generar el documento")


if __name__ == "__main__":
    args = sys.argv[1:]
    if '--articulo' in args or '--articulo-ejemplo' in args:
        ejemplo_uso('articulo_ai_legal')
    elif '--ejemplo' in args:
        ejemplo_uso('amazon_retraso')
    else:
        print("Generador de documentos legales para consumidores")
        print("Uso:")
        print("  python generador-reclamaciones.py --ejemplo      # ejemplo de reclamación")
        print("  python generador-reclamaciones.py --articulo     # ejemplo de artículo IA legal")