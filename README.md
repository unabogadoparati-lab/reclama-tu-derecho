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
