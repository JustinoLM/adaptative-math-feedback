import json
from loguru import logger
from src.utils.llm_client import OllamaClient
from src.phase3_script_generation.templates import get_script_generation_prompt
from pydantic import BaseModel
from typing import List, Optional

class StepInstruction(BaseModel):
    paso_numero: int
    texto: str
    operacion: str
    visual_cue: str
    duracion_estimada: int

class ScriptSection(BaseModel):
    texto: str
    duracion_estimada: int
    visual_cue: Optional[str] = None
    analogia: Optional[str] = None

class ProblemaSimilar(BaseModel):
    incluir: bool
    problema: Optional[str] = None
    hint: Optional[str] = None

class EducationalScript(BaseModel):
    introduccion: ScriptSection
    identificacion_error: ScriptSection
    explicacion_concepto: ScriptSection
    solucion_paso_a_paso: List[StepInstruction]
    problema_similar: ProblemaSimilar
    cierre: ScriptSection
    
    @property
    def duracion_total(self) -> int:
        """Calcula duración total en segundos"""
        total = (
            self.introduccion.duracion_estimada +
            self.identificacion_error.duracion_estimada +
            self.explicacion_concepto.duracion_estimada +
            sum(step.duracion_estimada for step in self.solucion_paso_a_paso) +
            self.cierre.duracion_estimada
        )
        return total

class ScriptGenerator:
    def __init__(self):
        self.llm = OllamaClient()
    
    def generate(
        self,
        problem: str,
        correct_answer: str,
        student_answer: str,
        error_analysis: dict,
        strategy: dict,
        solution_steps: str = ""
    ) -> EducationalScript:
        """Genera guión educativo estructurado"""
        
        logger.info("Generando guión educativo...")
        
        prompt = get_script_generation_prompt(
            problem, correct_answer, student_answer,
            error_analysis, strategy, solution_steps
        )
        
        response = self.llm.generate(prompt, temperature=0.7, max_tokens=3000)
        
        logger.debug(f"Respuesta LLM (script): {response[:200]}...")
        
        try:
            # Limpiar respuesta
            response_clean = response.strip()
            if "```json" in response_clean:
                response_clean = response_clean.split("```json")[1].split("```")[0]
            elif "```" in response_clean:
                response_clean = response_clean.split("```")[1].split("```")[0]
            
            data = json.loads(response_clean)
            script = EducationalScript(**data)
            
            logger.info(f"Guión generado. Duración estimada: {script.duracion_total}s")
            return script
            
        except Exception as e:
            logger.error(f"Error parseando guión: {e}")
            logger.error(f"Respuesta: {response}")
            raise


if __name__ == "__main__":
    from src.phase1_error_analysis.classifier import ErrorClassifier
    from src.phase2_content_adaptation.strategy import ContentAdapter
    from src.phase2_content_adaptation.student_level import StudentProfile, ProgressLevel
    from pathlib import Path
    
    # Simular pipeline completo
    problem = "Juan tiene 24 manzanas y compra 18 más. ¿Cuántas tiene en total?"
    correct_answer = "42"
    student_answer = "432"
    
    # Fase 1: Clasificar error
    classifier = ErrorClassifier()
    error = classifier.classify(problem, correct_answer, student_answer)
    
    # Fase 2: Determinar estrategia
    student = StudentProfile(
        progress_level=ProgressLevel.LENTO,
        tiempo_esperado=45.0,
        tiempo_realizado=78.0,
        unidad="Unidad 2",
        leccion="Lección 2",
        nivel=1,
        clase=1
    )
    
    adapter = ContentAdapter()
    strategy = adapter.determine_strategy(error, student)
    
    # Fase 3: Generar guión
    generator = ScriptGenerator()
    script = generator.generate(
        problem=problem,
        correct_answer=correct_answer,
        student_answer=student_answer,
        error_analysis=error.model_dump(),  # Cambiado de .dict() a .model_dump()
        strategy=strategy.model_dump(),  # Cambiado de .dict() a .model_dump()
        solution_steps="Paso 1: Sumar 24 + 18\nPaso 2: 24 + 18 = 42"
    )
    
    print(f"\n=== GUIÓN GENERADO ===")
    print(f"Duración total: {script.duracion_total}s")
    print(f"\nIntroducción: {script.introduccion.texto}")
    print(f"\nError identificado: {script.identificacion_error.texto}")
    print(f"\nExplicación: {script.explicacion_concepto.texto}")
    print(f"\nPasos de solución: {len(script.solucion_paso_a_paso)}")
    for step in script.solucion_paso_a_paso:
        print(f"  {step.paso_numero}. {step.texto}")
    
    # GUARDAR JSON
    output_dir = Path("output/temp")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    script_file = output_dir / "test_script.json"
    with open(script_file, 'w', encoding='utf-8') as f:
        json.dump(script.model_dump(), f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Guión guardado en: {script_file}")