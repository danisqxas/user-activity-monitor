# 👁️‍🗨️ User Activity Monitor

![Logo](https://raw.githubusercontent.com/danisqxas/user-activity-monitor/main/.assets/logo-monitor-dark.png)

> ⚡ Herramienta visual de auditoría y trazabilidad para entornos Discord. Diseñada con precisión quirúrgica para brindar control absoluto sobre la actividad de usuarios en tiempo real.

Un proyecto pensado para administradores exigentes, desarrolladores que aman entender todo lo que ocurre en sus servidores, y equipos de seguridad que valoran el **detalle invisible al ojo humano**.

---

## ✨ ¿Qué hace?

🔹 Monitorea eventos clave: mensajes (envío, edición, borrado), canales de voz (join/leave/mute), creación de threads, cambios de nick, reacciones, actualizaciones de roles y más.  
🔹 Interfaz gráfica en pestañas: historial completo, filtro de eventos, panel de configuración interactiva.  
🔹 Soporte avanzado para excluir servidores, eventos y usuarios según criterios definidos.  
🔹 Persistencia total mediante archivo JSON sincronizado en tiempo real.

> Todo el seguimiento ocurre desde una interfaz intuitiva, sin necesidad de terminal ni comandos manuales.

---

## 🎯 Objetivo

Centralizar el registro de actividad del usuario en un entorno Discord para brindar trazabilidad a moderadores, analistas o bots de control. El foco es la **usabilidad, modularidad y experiencia visual limpia**.

---

## 📺 Vista general

```plaintext
📊 [History Tab]   ➤ Tabla con todos los eventos del usuario con acciones como: jump, eliminar, copiar ID
🎛 [Filter Tab]    ➤ Selector múltiple de eventos y servidores ignorados (persistentes)
🛠  [Config Tab]    ➤ Edición directa del JSON con validación instantánea
```

Todo se actualiza en tiempo real, y los cambios se reflejan sin reiniciar el bot.

---

## 🧰 Requisitos técnicos

- Python 3.9+
- Bot con permisos y `discord.py`
- SO Windows o Linux

---

## 🚀 Instalación

```bash
git clone https://github.com/danisqxas/user-activity-monitor.git
cd user-activity-monitor
python User_Activity_V1.1.py
```

> Requiere que tu bot esté en ejecución con los eventos habilitados.

---

## 📁 Estructura del proyecto

```
user-activity-monitor/
├── User_Activity_V1.1.py   # Script principal con GUI
├── userActivity.json       # Config y estados guardados dinámicamente
├── LICENSE                 # MIT License
├── README.md               # Este archivo
├── .gitignore              # Exclusiones comunes
└── .assets/                # Logos, capturas y recursos visuales (opcional)
```

---

## 🧠 Funcionalidades avanzadas

- 🔍 Filtro por servidor, tipo de evento, usuario o canal
- 🔗 Enlace directo a mensajes en Discord (compatibles con `discord://` en desktop)
- 🧩 Menús contextuales para copiar, eliminar, acceder a acciones rápidas
- 🎨 Diseño intuitivo: interfaz GUI limpia y funcional
- 🔒 No almacena contraseñas, ni datos sensibles; solo actividad observable del servidor
- 💾 Auto-guardado de cada acción realizada

---

## 📸 Capturas

> *Capturas de pantalla con temas oscuros y claros próximamente.*

También se puede generar una demo animada del flujo de uso si es solicitado.

---

## 💬 ¿Por qué este proyecto?

Porque el monitoreo no debería depender de logs manuales o bots limitados.

Porque las herramientas de auditoría visual deben ser tan claras como los eventos que muestran.

Porque la trazabilidad **no es opcional**, es una capa fundamental de cualquier ecosistema Discord bien administrado.

---

## 👨‍💻 Autor

**Daniel Sebastián Rocha Jaureguy**  
GitHub: [@danisqxas](https://github.com/danisqxas)  
Estudiante de Ingeniería en Ciberseguridad. Apasionado por el código robusto, los entornos oscuros y los gatos que maúllan mientras se loguea un evento.

> “No se trata de ver todo. Se trata de ver lo que importa.”

---

## 📝 Licencia

Distribuido bajo la Licencia MIT. Uso libre para fines personales, educativos o comerciales.

---

<p align="center">
  <b>🚨 Este no es un proyecto improvisado.</b><br>
  <i>Es una herramienta forjada desde la obsesión por el detalle, la estética funcional y el código que respira claridad.</i><br>
  <br>
  🧩 <b>Si tu equipo necesita monitoreo real, esto no es una opción. Es una necesidad.</b>
</p>
