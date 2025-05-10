# User Activity Monitor (Advanced Script)

> 🎯 Monitorea, analiza y exporta la actividad de usuarios con una interfaz potente, extensible y profesional.

---

## 📌 Descripción

**User Activity Monitor** es una solución de seguimiento avanzada diseñada para monitorear y analizar eventos generados por usuarios en entornos digitales, especialmente en Discord. Implementa una arquitectura modular basada en Python, integrando GUI con `customtkinter` y soporte para bots usando `discord.py`.

Este monitor no solo registra datos, sino que ofrece herramientas para analizar comportamientos, exportar registros e interactuar desde una interfaz gráfica moderna.

---

## 📂 Estructura del Proyecto

```
user-activity-monitor/
├── src/
│   ├── user_activity_tracker.py   # Script principal con GUI y lógica de tracking
│   └── __init__.py                # Inicializador del módulo (opcional)
│
├── .github/
│   └── workflows/
│       └── pylint.yml             # CI para linting automático
│
├── requirements.txt              # Dependencias necesarias
├── LICENSE                       # Licencia MIT
└── README.md                     # Este archivo
```

---

## 🛠️ Tecnologías y Dependencias

* `Python >= 3.10`
* `customtkinter` → interfaz moderna y adaptable
* `discord.py` → integración con bots
* `pyperclip` → copiado de logs
* Librerías estándar: `asyncio`, `csv`, `uuid`, `datetime`, `logging`

### Instalación

```bash
pip install -r requirements.txt
```

O bien manualmente:

```bash
pip install customtkinter discord.py pyperclip
```

---

## 🚀 Funcionalidades Destacadas

### 🔍 Seguimiento Inteligente

* Registro en tiempo real de mensajes, reacciones y cambios de voz
* Sistema de caché TTL configurable
* Filtros activos por servidor o evento

### 📊 Módulo de Análisis

* Eventos más frecuentes por usuario
* Servidor más activo
* Gráficos diarios y por hora

### 💾 Exportación Precisa

* Exportación de registros a CSV
* Compatibilidad con hojas de cálculo y visualizadores externos

### 🖥️ GUI Moderna

* Interfaz limpia usando `customtkinter`
* Botones, selectores, métricas y tablas interactivas
* Temas claros y oscuros compatibles

### 🤖 Modo Bot Discord

* Integración con `discord.ext.commands`
* Comandos personalizados (`!purge_events`, etc.)

---

## 🧪 Modo de Uso

### ▶️ Ejecutar Interfaz Gráfica

```bash
python src/user_activity_tracker.py
```

### ⚙️ Usar como bot de Discord

1. Crea una aplicación en el [portal de Discord](https://discord.com/developers/applications)
2. Activa los intents requeridos (presencia, contenido de mensaje)
3. Inserta tu token en el script correspondiente

---

## 🗺️ Roadmap

* [x] Seguimiento de eventos con caché TTL
* [x] Análisis gráfico por usuario y servidor
* [x] Exportación automatizada
* [x] GUI profesional interactiva
* [ ] Base de datos persistente (SQLite/PostgreSQL)
* [ ] Panel web con FastAPI
* [ ] Integración con dashboards externos (Grafana, Metabase)

---

## 🧑‍💻 Autor

**Aerthex** – [@danisqxas](https://github.com/danisqxas)
🔐 Ciberseguridad ofensiva & automatización
🧩 Arquitectura de scripts con estilo y propósito

---

## 📄 Licencia

Distribuido bajo la licencia **MIT**. Puedes modificar, distribuir o integrarlo en tus proyectos siempre que se mantenga la atribución.

---

## 🌌 Última palabra

> "Un sistema bien trazado es el primer paso hacia la visibilidad total." – Aerthex Labs
