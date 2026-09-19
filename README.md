# Reclama tu derecho 💖

Automatización de reclamaciones por retrasos en entregas (España, Amazon)
Hecho con ❤️ y un toque kawaii para hacer justicia más accesible.

## Características

- 📄 Plantillas legales automatizadas para reclamaciones contra Amazon por retrasos en entrega
- 🐍 Generador de reclamaciones en Python usando string.Template
- 📋 Fácil de usar y extender para otros tipos de reclamaciones
- 🇪🇸 Basado en la legislación española y comunitaria aplicable

## Estructura del proyecto

```
reclama-tu-derecho/
├── scripts/
│   └── generador-reclamaciones.py     # Script principal para generar reclamaciones
├── plantillas/
│   └── reclamacion_amazon_retraso_entrega.txt  # Plantilla para retrasos en Amazon
└── documentacion/
    └── (próximamente: guías legales y ejemplos)
```

## Cómo usar

1. Asegúrate de tener Python 3 instalado
2. Navega al directorio del proyecto
3. Ejecuta el generador con un ejemplo:

```bash
python scripts/generador-reclamaciones.py --ejemplo
```

Esto generará una reclamación de ejemplo en la consola y guardará una copia en el directorio de salida (se crea automáticamente).

## Personalizar

Para usar el generador con tus propios datos, modifica el diccionario `datos_ejemplo` en el script o crea tu propia función que pase un diccionario con los campos requeridos:

- `tipo`: 'amazon_retraso' (por ahora)
- `empresa`: Nombre de la empresa (ej: 'Amazon España')
- `numero_pedido`: Tu número de pedido
- `nombre_usuario`: Tu nombre completo
- `dni`: Tu DNI
- `email`: Tu correo electrónico
- `fecha_pedido`: DD/MM/AAAA
- `fecha_estimada`: DD/MM/AAAA (fecha prometida de entrega)
- `fecha_real`: DD/MM/AAAA (fecha real de entrega)
- `numero_dias`: Número de días de retraso (calculado automáticamente si no lo proporcionas)
- `importe`: Importe del pedido (con separador decimal de coma, ej: '89,99')
- `descripcion`: Descripción detallada del problema
- `leyes`: Leyes y artículos aplicables (separados por \n si son múltiples)
- `condiciones`: Referencia a las condiciones de venta de la empresa
- `peticiones`: Qué exactamente pides (reembolso, compensación, etc.)
- `documentos_adjuntos`: Lista de documentos que estás adjuntando

## Próximos pasos

- [ ] Añadir soporte para otros tipos de reclamaciones (productos defectuosos, garantía, etc.)
- [ ] Crear interfaz web sencilla para usuarios no técnicos
- [ ] Añadir validación de datos de entrada
- [ ] Generar versiones en PDF de las reclamaciones
- [ ] Integrar con servicios de notificación (email, Telegram)

## Licencia

Este proyecto es de código abierto y está pensado para ayudar a consumidores a hacer valer sus derechos. Si lo encuentras útil, ¡compártelo con quien pueda necesitarlo!

---

Hecho con cariño por el equipo de Derecho Accesible 🌸


## API REST

Esta versión incluye una API REST basada en Flask para generar reclamaciones mediante peticiones HTTP.

### Endpoints

- `GET /` - Información básica de la API
- `GET /ejemplo` - Devuelve una reclamación de ejemplo
- `POST /generar` - Genera una reclamación a partir de JSON

#### Ejemplo de uso con curl:

```bash
# Ejemplo
curl -X GET https://tu-servicio.onrender.com/ejemplo

# Generar una reclamación (reemplaza con tus datos)
curl -X POST https://tu-servicio.onrender.com/generar \
  -H "Content-Type: application/json" \
  -d '{
    "tipo": "amazon_retraso",
    "empresa": "Amazon España",
    "numero_pedido": "TU-PEDIDO",
    "nombre_usuario": "Tu Nombre",
    "dni": "TU-DNI",
    "email": "tu@email.com",
    "fecha_pedido": "01/01/2026",
    "fecha_estimada": "05/01/2026",
    "fecha_real": "12/01/2026",
    "numero_dias": "7",
    "importe": "50,00",
    "descripcion": "Descripción del problema...",
    "leyes": "Ley aplicable...",
    "condiciones": "Condiciones de la empresa...",
    "peticiones": "Qué pides...",
    "documentos_adjuntos": "Lista de documentos..."
  }'
```

La respuesta será JSON con el campo `reclamacion` conteniendo el texto generado.
