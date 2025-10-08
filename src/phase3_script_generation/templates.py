def get_script_generation_prompt(
    problem: str,
    correct_answer: str,
    student_answer: str,
    error_analysis: dict,
    strategy: dict,
    solution_steps: str = ""
) -> str:
    
    depth_instructions = {
        "minima": "Breve corrección en 1-2 pasos.",
        "basica": "Corrección + 1 ejemplo simple.",
        "intermedia": "Corrección + explicación del concepto + ejemplo.",
        "profunda": "Corrección detallada + explicación conceptual + analogía + múltiples ejemplos paso a paso."
    }
    
    encouragement = {
        "bajo": "Tono neutral y directo.",
        "medio": "Tono amigable con motivación ligera.",
        "alto": "Tono muy motivador y alentador. El estudiante necesita confianza."
    }
    
    return f"""Eres un tutor de matemáticas para niños de 5to grado. Genera un guión educativo estructurado.

PROBLEMA: {problem}
RESPUESTA CORRECTA: {correct_answer}
RESPUESTA DEL ESTUDIANTE: {student_answer}

ANÁLISIS DEL ERROR:
- Tipo: {error_analysis['error_type']}
- Descripción: {error_analysis['description']}
- Concepto erróneo: {error_analysis.get('misconception', 'N/A')}

ESTRATEGIA PEDAGÓGICA:
- Profundidad: {strategy['depth']} - {depth_instructions[strategy['depth']]}
- Enfoque conceptual: {strategy['focus_on_concept']}
- Incluir problema similar: {strategy['include_similar_problem']}
- Nivel de ánimo: {encouragement[strategy['encouragement_level']]}

{f"SOLUCIÓN CORRECTA: {solution_steps}" if solution_steps else ""}

Genera un guión en JSON con esta estructura exacta:

{{
    "introduccion": {{
        "texto": "Saludo motivador (2-3 oraciones)",
        "duracion_estimada": 5
    }},
    "identificacion_error": {{
        "texto": "Qué hizo el estudiante y dónde está el error",
        "visual_cue": "Descripción de qué mostrar en pantalla",
        "duracion_estimada": 8
    }},
    "explicacion_concepto": {{
        "texto": "Explicación del concepto correcto (adaptar según profundidad)",
        "analogia": "Analogía del mundo real si es profunda, o null",
        "visual_cue": "Qué animación mostrar",
        "duracion_estimada": 15
    }},
    "solucion_paso_a_paso": [
        {{
            "paso_numero": 1,
            "texto": "Explicación del paso",
            "operacion": "Operación matemática a mostrar",
            "visual_cue": "Cómo animar este paso",
            "duracion_estimada": 5
        }}
    ],
    "problema_similar": {{
        "incluir": {str(strategy['include_similar_problem']).lower()},
        "problema": "Problema similar para practicar (o null)",
        "hint": "Pista inicial (o null)"
    }},
    "cierre": {{
        "texto": "Mensaje motivador de cierre",
        "duracion_estimada": 5
    }}
}}

IMPORTANTE: 
- Lenguaje simple para niños de 10-11 años
- Evita tecnicismos innecesarios
- Usa figuras para poder demostrar de forma visual si es posible
- {encouragement[strategy['encouragement_level']]}
- Solo JSON, sin texto adicional"""