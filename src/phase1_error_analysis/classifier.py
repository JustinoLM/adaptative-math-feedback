import json
from loguru import logger
from src.utils.llm_client import OllamaClient
from src.phase1_error_analysis.prompts import get_error_classification_prompt
from src.phase1_error_analysis.error_types import ErrorAnalysis, ErrorType

class ErrorClassifier:
    def __init__(self):
        self.llm = OllamaClient()
        
    def classify(self, problem: str, correct_answer: str, student_answer: str, solution_steps: str = "") -> ErrorAnalysis:
        """Clasifica el error del estudiante"""
        
        logger.info(f"Analizando respuesta: '{student_answer}' vs '{correct_answer}'")
        
        # Generar prompt
        prompt = get_error_classification_prompt(problem, correct_answer, student_answer, solution_steps)
        
        # Llamar LLM
        response = self.llm.generate(prompt, temperature=0.3)
        
        logger.debug(f"Respuesta LLM: {response}")
        
        # Parsear respuesta
        try:
            # Limpiar respuesta (a veces el LLM añade texto extra)
            response_clean = response.strip()
            if "```json" in response_clean:
                response_clean = response_clean.split("```json")[1].split("```")[0]
            elif "```" in response_clean:
                response_clean = response_clean.split("```")[1].split("```")[0]
            
            data = json.loads(response_clean)
            return ErrorAnalysis(**data)
            
        except Exception as e:
            logger.error(f"Error parseando respuesta: {e}")
            logger.error(f"Respuesta original: {response}")
            
            # Fallback
            return ErrorAnalysis(
                error_type=ErrorType.OPERACIONAL,
                description="No se pudo clasificar automáticamente",
                gap_level=3,
                misconception=None,
                correct_step_missed=None
            )

if __name__ == "__main__":
    # Prueba rápida
    classifier = ErrorClassifier()
    
    result = classifier.classify(
        problem="Juan tiene 24 manzanas y compra 18 más. ¿Cuántas manzanas tiene en total?",
        correct_answer="42",
        student_answer="48",
        solution_steps="24 + 18 = 42"
    )
    
    print(f"\nTipo de error: {result.error_type}")
    print(f"Descripción: {result.description}")
    print(f"Nivel de brecha: {result.gap_level}")
    print(f"Concepto erróneo: {result.misconception}")