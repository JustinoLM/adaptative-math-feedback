def get_error_classification_prompt(problem: str, correct_answer: str, student_answer: str, solution_steps: str = "") -> str:
    return f"""Eres un experto en educación matemática de 5to grado. Analiza el error del estudiante.

PROBLEMA:
{problem}

RESPUESTA CORRECTA: {correct_answer}

RESPUESTA DEL ESTUDIANTE: {student_answer}

{f"PASOS DE SOLUCIÓN CORRECTA: {solution_steps}" if solution_steps else ""}

Clasifica el error en UNA de estas categorías:

1. CONCEPTUAL: No entendió qué operación usar (ej: sumó cuando debía multiplicar)
2. PROCEDIMENTAL: Eligió bien la operación pero la ejecutó mal (ej: multiplicó de derecha a izquierda)
3. OPERACIONAL: Hizo bien el procedimiento pero se equivocó en un cálculo (ej: 7+8=16)
4. ATENCIONAL: Error de distracción, copió mal un número
5. NINGUNO: La respuesta es correcta

Responde en este formato JSON exacto:
{{
    "error_type": "conceptual|procedimental|operacional|atencional|ninguno",
    "description": "Descripción breve del error",
    "gap_level": 1-5,
    "misconception": "Qué concepto malinterpretó (o null)",
    "correct_step_missed": "Qué paso correcto no hizo (o null)"
}}

IMPORTANTE: Solo JSON, sin texto adicional."""