from flask import Flask, request, jsonify, send_file
from scripts.generador_reclamaciones import ReclamacionGenerator
import tempfile
import os

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "message": "API de Generador de Reclamaciones - Reclama tu Derecho",
        "endpoints": {
            "/generar": "POST - Genera una reclamación previa",
            "/ejemplo": "GET - Devuelve un ejemplo de reclamación"
        }
    })

@app.route('/ejemplo', methods=['GET'])
def ejemplo():
    generator = ReclamacionGenerator()
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
    ruta = generator.generar_reclamacion(datos_ejemplo)
    if ruta:
        with open(ruta, 'r', encoding='utf-8') as f:
            contenido = f.read()
        # Clean up temp file
        try:
            os.remove(ruta)
        except:
            pass
        return jsonify({
            "success": True,
            "reclamacion": contenido
        })
    else:
        return jsonify({"success": False, "error": "No se pudo generar la reclamación"}), 500

@app.route('/generar', methods=['POST'])
def generar():
    if not request.is_json:
        return jsonify({"success": False, "error": "Se espera JSON"}), 400
    
    datos = request.get_json()
    generator = ReclamacionGenerator()
    ruta = generator.generar_reclamacion(datos)
    
    if ruta:
        # Determine if user wants download or just content
        if request.args.get('descargar') == 'true':
            return send_file(ruta, as_attachment=True, download_name='reclamacion.txt')
        else:
            with open(ruta, 'r', encoding='utf-8') as f:
                contenido = f.read()
            # Clean up
            try:
                os.remove(ruta)
            except:
                pass
            return jsonify({
                "success": True,
                "reclamacion": contenido
            })
    else:
        return jsonify({"success": False, "error": "No se pudo generar la reclamación con los datos proporcionados"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
