# Sistema de Retroalimentación Adaptativa - Matemáticas 5to Grado

Sistema que analiza errores matemáticos, clasifica tipos de error y genera videos explicativos personalizados.

## 🏗️ Arquitectura

```
┌─────────────┐
│   Input     │ Problema + Respuesta del estudiante (texto)
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────┐
│  1. Análisis de Error               │
│  - Llama 3.1 8B / Mistral 7B        │
│  - Clasificación: Conceptual,       │
│    Procedimental, Operacional,      │
│    Atencional                       │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  2. Adaptación de Contenido         │
│  - Nivel del estudiante             │
│  - Profundidad de explicación       │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  3. Generación de Guión             │
│  - LLM con prompts pedagógicos      │
│  - Script estructurado              │
└──────┬──────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────┐
│  4. Producción Visual               │
│  - MANIM Community Edition          │
│  - Video MP4 animado                │
└─────────────────────────────────────┘
```

## 📁 Estructura del Repositorio

```
adaptive-math-feedback/
├── data/
│   ├── problems/              # Dataset de problemas
│   ├── error_examples/        # Ejemplos de errores generados
│   └── student_profiles/      # Perfiles de prueba
│
├── src/
│   ├── phase1_error_analysis/
│   │   ├── __init__.py
│   │   ├── classifier.py      # Clasificación de errores
│   │   ├── prompts.py         # Prompts para LLM
│   │   └── error_types.py     # Definiciones de tipos de error
│   │
│   ├── phase2_content_adaptation/
│   │   ├── __init__.py
│   │   ├── student_level.py   # Evaluación de nivel
│   │   └── strategy.py        # Estrategia pedagógica
│   │
│   ├── phase3_script_generation/
│   │   ├── __init__.py
│   │   ├── script_builder.py  # Generación de guión
│   │   └── templates.py       # Templates educativos
│   │
│   ├── phase4_video_production/
│   │   ├── __init__.py
│   │   ├── manim_renderer.py  # Rendering con MANIM
│   │   └── scenes.py          # Escenas matemáticas
│   │
│   └── utils/
│       ├── llm_client.py      # Cliente LLM (local)
│       └── cache.py           # Sistema de caché
│
├── models/
│   └── download_models.py     # Script para descargar modelos
│
├── tests/
│   ├── test_phase1.py
│   ├── test_phase2.py
│   ├── test_phase3.py
│   └── test_phase4.py
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   └── 02_error_generation.ipynb
│
├── output/
│   ├── videos/                # Videos generados
│   └── logs/                  # Logs del sistema
│
├── docker/
│   ├── Dockerfile.llm         # Container para LLM
│   └── Dockerfile.manim       # Container para MANIM
│
├── requirements.txt
├── requirements-dev.txt
├── .env.example
├── .gitignore
└── README.md
```

## 🚀 Instalación Local

### Prerrequisitos
- Python 3.10+
- Docker (opcional, para LLM en contenedor)
- 16GB RAM mínimo
- GPU recomendada (para LLM)

### Setup

```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/adaptive-math-feedback.git
cd adaptive-math-feedback

# Crear entorno virtual
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configurar variables de entorno
cp .env.example .env
# Editar .env con tus configuraciones

# Descargar modelo LLM
python models/download_models.py
```

## 🧪 Modo de Desarrollo

### Fase 1 - Análisis de Error (En desarrollo)
```bash
python -m src.phase1_error_analysis.classifier \
  --problem "Juan tiene 24 manzanas y compra 18 más. ¿Cuántas tiene en total?" \
  --student_answer "48" \
  --correct_answer "42"
```

## 📊 Dataset

Coloca tu dataset en `data/problems/`. Formato esperado:

```json
{
  "problem_id": "P001",
  "grade": 5,
  "topic": "addition",
  "difficulty": "medium",
  "problem_text": "Juan tiene 24 manzanas...",
  "correct_answer": "42",
  "solution_steps": [...]
}
```

## 🔧 Tecnologías

- **LLM**: Llama 3.1 8B (local via Ollama/llama.cpp)
- **Video**: MANIM Community Edition
- **Framework**: Python 3.10+
- **Testing**: pytest
- **Containerización**: Docker

## 📝 Próximos Pasos

1. ✅ Setup del repositorio
2. ✅ Implementar Fase 1: Análisis de Error
3. ✅ Implementar Fase 2: Adaptación de Contenido
4. 🔄 Implementar Fase 3: Generación de Guión
5. ⏳ Implementar Fase 4: Producción Visual


## 📄 Licencia

MIT License
