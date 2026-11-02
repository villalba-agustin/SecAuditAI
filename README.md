# SecAuditAI &mdash; Auditoría y Cumplimiento ISO/IEC 27001:2022 con IA Local

![Python](https://img.shields.io/badge/Python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688.svg)
![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg?logo=docker&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-orange.svg)
![Tests](https://img.shields.io/badge/Tests-48%20Passed-brightgreen.svg)
![License](https://img.shields.io/badge/License-Proprietary%20%2F%20Academic-lightgrey.svg)

**SecAuditAI** es una aplicación web integral, modular y soberana diseñada para evaluar, documentar y gestionar el cumplimiento del estándar internacional **ISO/IEC 27001:2022** (incluyendo la **Enmienda 1:2024** sobre cambio climático) asistida por inteligencia artificial local ejecutada mediante **Ollama**.

---

## 📑 Tabla de Contenidos

1. [🚀 Inicio Rápido con Docker (Recomendado)](#-inicio-rápido-con-docker-recomendado)
2. [🔐 Credenciales por Defecto](#-credenciales-por-defecto)
3. [🚀 Características Principales](#-características-principales)
4. [📂 Estructura del Proyecto](#-estructura-del-proyecto)
5. [⚙️ Configuración y Variables de Entorno](#️-configuración-y-variables-de-entorno)
6. [🛠️ Instalación Manual (Desarrollo)](#️-instalación-manual-desarrollo)
7. [🧪 Ejecución de Pruebas Automatizadas](#-ejecución-de-pruebas-automatizadas)
8. [📊 Declaración de Aplicabilidad (SoA)](#-guía-de-la-declaración-de-aplicabilidad-soa-y-exportación)
9. [🛡️ Seguridad y AppSec](#️-seguridad-y-appsec)
10. [🧠 Skill Declarativa del Agente](#-skill-declarativa-del-agente)
11. [⚠️ Limitaciones y Próximos Pasos](#️-limitaciones-y-próximos-pasos)

---

## 🐳 Inicio Rápido con Docker (Recomendado)

> **Requisito único**: tener instalado [Docker Desktop](https://www.docker.com/products/docker-desktop/) o `docker` + `docker compose` en el sistema.

### 3 pasos para tener todo corriendo

```bash
# 1. Clonar el repositorio
git clone <URL_DEL_REPOSITORIO> SecAuditAI
cd SecAuditAI

# 2. Levantar todos los servicios (app + Ollama + descarga del modelo)
docker compose up -d

# 3. Abrir el navegador
# 👉 http://localhost:8080
```

¡Listo! Docker Compose levanta automáticamente:

| Servicio | Descripción |
|---|---|
| `app` | Aplicación SecAuditAI (FastAPI + SQLite) en el puerto **8080** |
| `ollama` | Servidor de IA local Ollama en el puerto **11434** |
| `ollama-pull` | Descarga el modelo `qwen3.5:4b` automáticamente (solo la primera vez) |

> [!NOTE]
> La primera vez que ejecutes `docker compose up -d`, Docker descarga las imágenes base y el modelo de IA (`qwen3.5:4b`, ~2.5 GB). Puede tardar **3 a 10 minutos** dependiendo de tu conexión. Las ejecuciones siguientes son instantáneas.

### Comandos útiles de Docker

```bash
# Ver el estado de los contenedores
docker compose ps

# Ver los logs en tiempo real
docker compose logs -f

# Ver solo los logs de la app
docker compose logs -f app

# Detener los servicios (conserva los datos)
docker compose down

# Detener y eliminar todos los datos (base de datos + uploads + modelo)
docker compose down -v
```

### Activar soporte GPU NVIDIA (opcional)

Si tenés una GPU NVIDIA con `nvidia-container-toolkit` instalado, descomenta el bloque `deploy` en [`docker-compose.yml`](docker-compose.yml):

```yaml
# En el servicio "ollama" dentro de docker-compose.yml:
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          count: all
          capabilities: [gpu]
```

---

## 🔐 Credenciales por Defecto

Una vez que la aplicación esté corriendo, ingresá en **`http://localhost:8080`** con:

| Campo | Valor |
|---|---|
| **Usuario** | `admin` |
| **Contraseña** | `SecAudit2025!` |

> [!WARNING]
> Cambiá la contraseña antes de desplegar en un entorno accesible desde internet. Editá las variables `DEFAULT_ADMIN_USER` y `DEFAULT_ADMIN_PASSWORD` en [`docker-compose.yml`](docker-compose.yml) o en el archivo [`.env`](.env).

---

## 🚀 Características Principales

- **Tablero Dinámico (Dashboard)**: Métricas reales de SQLite, porcentaje de cumplimiento con fórmula explícita, distribución por temas del Anexo A y registro de auditoría (`AuditLog`).
- **Cláusulas Normativas (4 a 10)**: 30 subcláusulas obligatorias incluyendo cambio climático (Enmienda 1:2024 en cláusulas 4.1 y 4.2).
- **Catálogo Completo del Anexo A (93 Controles)**:
  - **A.5**: 37 Controles Organizacionales
  - **A.6**: 8 Controles de Personas
  - **A.7**: 14 Controles Físicos
  - **A.8**: 34 Controles Tecnológicos
- **Declaración de Aplicabilidad (SoA)**: Exportable a **Excel (.xlsx)** con estilos y a **CSV**.
- **Gestión Segura de Evidencias**: PDF, DOCX, TXT, Markdown. Hash SHA-256, magic bytes y protección anti path traversal.
- **Agente IA Local Soberano**: Skill declarativa en Markdown + YAML, protección contra prompt injection, respuesta en JSON validado con Pydantic.
- **Supervisión Humana**: Separación estricta entre propuestas de IA y decisiones aprobadas por el auditor.
- **Interfaz 100% en Español y Autónoma**: CSS nativo sin CDNs, operable en entornos air-gapped.

---

## 📂 Estructura del Proyecto

```text
SecAuditAI/
├── Dockerfile                          # Imagen multi-stage de la aplicación
├── docker-compose.yml                  # Orquestación: app + Ollama + descarga de modelo
├── .dockerignore                       # Archivos excluidos del contexto Docker
├── .agents/
│   └── skills/
│       └── iso27001-evidence-review/
│           └── SKILL.md               # Skill declarativa con frontmatter YAML
├── agents/
│   └── secauditai.agent.md            # Especificación del agente
├── app/
│   ├── main.py                        # Punto de entrada FastAPI
│   ├── core/
│   │   ├── config.py                  # Variables de entorno con pydantic-settings
│   │   └── security.py               # AppSec: sanitización, hash y prompt defense
│   ├── db/
│   │   ├── session.py                 # Sesión SQLite y engine SQLAlchemy 2.0
│   │   ├── init_db.py                 # Inicialización idempotente
│   │   └── seed_data.py              # 30 cláusulas + 93 controles Anexo A
│   ├── models/                        # Entidades ORM
│   ├── schemas/                       # Modelos Pydantic v2
│   ├── services/                      # Lógica de negocio
│   ├── routers/                       # Endpoints HTTP
│   ├── templates/                     # Vistas Jinja2
│   └── static/                        # CSS y JS nativos
├── data/
│   ├── uploads/                       # Evidencias cargadas (volumen Docker)
│   └── samples/                       # Evidencias ficticias de prueba
├── docs/
│   ├── ARCHITECTURE.md
│   ├── SECURITY.md
│   └── DEMO_SCRIPT.md
├── tests/
│   ├── conftest.py
│   ├── unit/
│   ├── integration/
│   └── security/
├── .env.example                       # Plantilla de variables de entorno
├── requirements.txt
├── pytest.ini
└── ruff.toml
```

---

## ⚙️ Configuración y Variables de Entorno

Todas las variables se pueden sobreescribir en la sección `environment` de [`docker-compose.yml`](docker-compose.yml) o creando un archivo `.env`:

| Variable | Valor por Defecto | Descripción |
| :--- | :--- | :--- |
| `APP_ENV` | `production` | Entorno de ejecución |
| `DEBUG` | `False` | Modo depuración |
| `DATABASE_URL` | `sqlite:////app/data/db/secauditai.db` | Cadena de conexión SQLAlchemy |
| `UPLOAD_DIR` | `/app/data/uploads` | Directorio de evidencias |
| `MAX_UPLOAD_SIZE_MB` | `15` | Tamaño máximo por evidencia (MB) |
| `OLLAMA_BASE_URL` | `http://ollama:11434` | URL del servicio Ollama |
| `OLLAMA_MODEL` | `qwen3.5:4b` | Modelo LLM para análisis |
| `OLLAMA_TIMEOUT_SECONDS` | `180` | Timeout de inferencia |
| `DEFAULT_ADMIN_USER` | `admin` | Usuario administrador |
| `DEFAULT_ADMIN_PASSWORD` | `SecAudit2025!` | Contraseña por defecto |

> [!NOTE]
> **Modo Simulado Automático**: Si Ollama no está disponible o el modelo no está descargado, el sistema activa automáticamente su motor de contingencia determinista. Podés evaluar evidencias, exportar la SoA y ejecutar los tests sin que Ollama esté corriendo.

---

## 🛠️ Instalación Manual (Desarrollo)

Si preferís ejecutar la aplicación sin Docker para desarrollar o depurar:

### Requisitos
- Python 3.11 o 3.12
- Ollama instalado localmente desde [ollama.ai](https://ollama.ai) (opcional)

### Pasos

```bash
# 1. Crear entorno virtual
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2. Instalar dependencias
pip install --upgrade pip
pip install -r requirements.txt

# 3. Configurar variables de entorno
cp .env.example .env

# 4. Descargar modelo (opcional)
ollama pull qwen3.5:4b

# 5. Iniciar el servidor
python -m uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

Luego abrí **`http://127.0.0.1:8080`** e ingresá con `admin` / `SecAudit2025!`.

---

## 🧪 Ejecución de Pruebas Automatizadas

La suite incluye 48 pruebas bajo el patrón **AAA (Arrange, Act, Assert)**:

```bash
# Todas las pruebas
.venv/bin/pytest -v

# Por categoría
.venv/bin/pytest tests/unit/ -v        # Unitarias
.venv/bin/pytest tests/integration/ -v # Integración
.venv/bin/pytest tests/security/ -v    # Seguridad

# Linter
.venv/bin/ruff check app tests
```

---

## 📊 Guía de la Declaración de Aplicabilidad (SoA) y Exportación

1. Ingresá a la sección **SoA** (`/soa`) en el menú superior.
2. Por cada control podés definir: aplicabilidad, justificación (obligatoria si está excluido), estado de implementación y resumen operativo.
3. **Exportar a Excel**: botón **"Exportar a Excel (XLSX)"** — hoja formateada con `openpyxl`.
4. **Exportar a CSV**: botón **"Exportar CSV"** — UTF-8 con BOM, compatible con cualquier hoja de cálculo.

---

## 🛡️ Seguridad y AppSec

- **Prevención de Path Traversal**: `sanitize_filename()` + UUID aleatorio + `is_path_safe()`.
- **Validación Multi-Capa de Archivos**: tamaño, whitelist de extensiones y magic bytes.
- **Defensa ante Prompt Injection**: documentos aislados entre delimitadores `<<<DOCUMENT_CONTENT>>>`.
- **Privacidad Soberana**: procesamiento 100% local, sin envío de datos al exterior.
- **Trazabilidad Inmutable**: `Assessment` + `AuditLog` registran toda acción.
- **Supresión de Trazas de Error**: las excepciones no revelan rutas ni stack traces al usuario.

Para más detalles: [docs/SECURITY.md](docs/SECURITY.md).

---

## 🧠 Skill Declarativa del Agente

La lógica del agente auditor reside en:  
📁 [`.agents/skills/iso27001-evidence-review/SKILL.md`](.agents/skills/iso27001-evidence-review/SKILL.md)

- Frontmatter YAML válido con `name` y `description`.
- Procedimiento paso a paso para confrontar documentos contra cláusulas 4–10 y Anexo A.
- Esquema JSON estricto de respuesta validado con Pydantic.
- La aplicación carga este archivo dinámicamente para construir el prompt enviado a Ollama.

Especificación del agente: [`agents/secauditai.agent.md`](agents/secauditai.agent.md).


---

## ⚠️ Limitaciones y Próximos Pasos

- **Alcance MVP**: Diseñado para uso local y académico. No exponer a internet sin MFA, RBAC y proxy TLS.
- **PDFs Escaneados**: `pypdf` procesa texto digital. PDFs basados en imágenes requieren OCR previo (ej. Tesseract).
- **Escala Interna**: La escala de madurez 0–5 es un mecanismo diagnóstico propio de SecAuditAI, no una clasificación formal de la norma.
- **No Certificación**: Las evaluaciones de la IA no sustituyen la labor de un organismo certificador acreditado.
