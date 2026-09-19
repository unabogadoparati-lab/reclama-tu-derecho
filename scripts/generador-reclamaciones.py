#!/usr/bin/env python3
"""
Generador de reclamaciones previas para consumidores
Especializado en reclamaciones contra grandes empresas por:
- Incumplimiento de plazo de entrega
- Productos defectuosos
- Incumplimiento de garantía
"""

import os
import sys
from datetime import datetime
from string import Template

class ReclamacionGenerator:
    def __init__(self):
        self.plantillas_dir = os.path.join(os.path.dirname(__file__), '..', 'plantillas')
        self.output_dir = os.path.join(os.path.dirname(__file__), '..', 'generadas')
        os.makedirs(self.output_dir, exist_ok=True)
    
    def cargar_plantilla(self, nombre_plantilla):
        """Carga una plantilla desde el directorio de plantillas"""
        ruta_plantilla = os.path.join(self.plantillas_dir, nombre_plantilla)
        try:
            with open(ruta_plantilla, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            print(f"Error: Plantilla {nombre_plantilla} no encontrada")
            return None
    
    def generar_reclamacion(self, datos):
        """
        Genera una reclamación previa basada en los datos proporcionados
        
        Args:
            datos (dict): Diccionario con los datos necesarios para la reclamación
                - tipo: 'amazon_retraso', 'generica', etc.
                - nombre_usuario, dni, email, numero_pedido, etc.
                - fecha_pedido, fecha_estimada, fecha_real (para retrasos)
                - importe, descripcion_problema, etc.
        """
        
        # Seleccionar plantilla según tipo
        tipo = datos.get('tipo', 'generica')
        if tipo == 'amazon_retraso':
            plantilla_content = self.cargar_plantilla('reclamacion_amazon_retraso_entrega.txt')
        else:
            plantilla_content = self.cargar_plantilla('plantilla_reclamacion_generica.txt')
        
        if not plantilla_content:
            return None
        
        # Preparar datos para sustitución
        datos_sustitucion = {
            'FECHA': datos.get('fecha', datetime.now().strftime('%d/%m/%Y')),
            'EMPRESA': datos.get('empresa', 'Amazon España'),
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
            'DOCUMENTOS_ADJUNTOS': datos.get('documentos_adjuntos', 'Copia del pedido y historial de seguimiento')
        }
        
        # Crear objeto Template y hacer sustitución
        try:
            plantilla = Template(plantilla_content)
            reclamacion_generada = plantilla.safe_substitute(datos_sustitucion)
            
            # Generar nombre de archivo de salida
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            nombre_archivo = f"reclamacion_{datos.get('empresa', 'empresa').lower().replace(' ', '_')}_{datos.get('tipo', 'reclamacion')}_{timestamp}.txt"
            ruta_salida = os.path.join(self.output_dir, nombre_archivo)
            
            # Guardar archivo
            with open(ruta_salida, 'w', encoding='utf-8') as f:
                f.write(reclamacion_generada)
            
            return ruta_salida
            
        except Exception as e:
            print(f"Error al generar la reclamación: {e}")
            return None

def ejemplo_uso():
    """Función de ejemplo para demostrar el uso del generador"""
    
    # Datos de ejemplo para una reclamación de Amazon por retraso de entrega
    datos_ejemplo = {
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
        'descripcion': 'Realicé el pedido ES123456789-0123456 el 15/11/2026 con fecha estimada de entrega el 20/11/2026. Sin embargo, la entrega se realizó efectivamente el 27/11/2026, lo que constituye un retraso de 7 días hábiles respecto a la fecha estimada proporcionada por Amazon.',
        'leyes': '- Artículo 20 de la Ley 7/1996, de Ordenación del Comercio Minorista: establece que el vendedor debe entregar en la fecha pactada o, en su defecto, en el plazo máximo de 30 días.\n- Artículo 123 del Real Decreto Legislativo 1/2007, de 16 de noviembre, por el que se aprueba el Texto Refundido de la Ley General para la Defensa de los Consumidores y Usuarios: reconoce el derecho a la resolución del contrato y reembolso en caso de incumplimiento esencial por parte del vendedor.\n- Directiva 2011/83/UE sobre los derechos de los consumidores: refuerza los derechos en materia de información clara y entrega oportuna.',
        'condiciones': 'Condiciones de Venta de Amazon.es, sección 5.Entrega: "Nos esforzamos por entregar en la fecha estimada..." y política de atención al cliente.',
        'peticiones': '1. El reembolso íntegro del importe abonado por el pedido ES123456789-0123456 (89,99 €).\n2. La compensación por los daños y perjuicios ocasionados por el retraso, conforme a su política interna o normativa aplicable.\n3. Que dicha resolución se comunique por escrito a mi correo juan.perez@email.com en un plazo máximo de 10 días hábiles.',
        'documentos_adjuntos': 'Copia del pedido ES123456789-0123456 (confirmación de compra)\nHistorial de seguimiento del envío que muestra fecha estimada vs. fecha real de entrega'
    }
    
    generator = ReclamacionGenerator()
    ruta_generada = generator.generar_reclamacion(datos_ejemplo)
    
    if ruta_generada:
        print(f"Reclamación generada exitosamente en: {ruta_generada}")
        print("\n--- PREVIA DE LA RECLAMACIÓN ---\n")
        with open(ruta_generada, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("Error al generar la reclamación")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--ejemplo":
        ejemplo_uso()
    else:
        print("Generador de Reclamaciones Previas para Consumidores")
        print("Uso: python generador_reclamaciones.py --ejemplo")
        print("     (para ver un ejemplo de funcionamiento)")