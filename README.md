# Smart-Gate: Control de Acceso Biométrico

**Smart-Gate** es un sistema de control de acceso basado en reconocimiento facial e inteligencia artificial, desarrollado como proyecto para la Licenciatura en Inteligencia Artificial en el **Instituto Profesional de Líderes (IPL)**.

## 🚀 Características
- **Reconocimiento Facial en Tiempo Real:** Utiliza algoritmos LBPH (Local Binary Patterns Histograms) para una detección robusta.
- **Persistencia de Datos:** Integración completa con SQLite para el registro de accesos y gestión de usuarios.
- **Protocolo de Seguridad:** Captura automática de imágenes ante intentos de acceso no autorizados.
- **Gestión de Usuarios:** Interfaz de consola para registrar, actualizar y eliminar usuarios.

## 🛠️ Tecnologías Utilizadas
- **Python 3.x**
- **OpenCV:** Para el procesamiento de imágenes y reconocimiento facial.
- **SQLite3:** Para la base de datos relacional.
- **LBPH & Haar Cascades:** Algoritmos de visión artificial.

## 📂 Estructura del Proyecto
```text
Proyecto Iv IPL/
├── data/               # Imágenes capturadas e intrusos
├── database/           # Base de datos SQLite y esquemas SQL
├── docs/               # Documentación y reportes
├── models/             # Modelos entrenados (archivos .yml)
├── src/                # Código fuente del sistema
│   ├── capture_faces.py
│   ├── db_manager.py
│   ├── main.py
│   ├── recognize_faces.py
│   └── train_model.py
├── .gitignore
├── README.md
└── requirements.txt
```

## ⚙️ Instalación y Uso

### 1. Requisitos Previos
Asegúrate de tener Python instalado y una cámara web funcional.

### 2. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 3. Ejecutar el Sistema
El punto de entrada principal es `src/main.py`.
```bash
python src/main.py
```
> **Nota:** Las credenciales por defecto para el prototipo son:
> - **Usuario:** `admin`
> - **Contraseña:** `ipl2026`

## 📝 Documentación
Para más detalles técnicos, consulta el archivo `docs/REPORT_DRAFT.md`.

## 🎓 Créditos
Desarrollado para el **Proyecto Mensual - Inteligencia Artificial** (IPL).
