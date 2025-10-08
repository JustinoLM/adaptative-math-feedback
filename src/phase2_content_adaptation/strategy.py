from enum import Enum
from pydantic import BaseModel
from src.phase1_error_analysis.error_types import ErrorType, ErrorAnalysis
from src.phase2_content_adaptation.student_level import StudentProfile, ProgressLevel

class ExplanationDepth(str, Enum):
    MINIMA = "minima"  # Solo corrección
    BASICA = "basica"  # Corrección + 1 ejemplo
    INTERMEDIA = "intermedia"  # Corrección + concepto + ejemplo
    PROFUNDA = "profunda"  # Corrección + concepto + múltiples ejemplos + analogía

class PedagogicalStrategy(BaseModel):
    depth: ExplanationDepth
    focus_on_concept: bool  # Enfocarse en concepto vs procedimiento
    use_visual_aids: bool  # Usar más animaciones visuales
    include_similar_problem: bool  # Incluir problema similar
    encouragement_level: str  # "bajo", "medio", "alto"
    
class ContentAdapter:
    def __init__(self):
        pass
    
    def determine_strategy(
        self, 
        error_analysis: ErrorAnalysis, 
        student_profile: StudentProfile
    ) -> PedagogicalStrategy:
        """Determina estrategia pedagógica basada en error y perfil"""
        
        # Determinar profundidad
        depth = self._calculate_depth(error_analysis, student_profile)
        
        # Error conceptual siempre requiere enfoque en concepto
        focus_on_concept = error_analysis.error_type == ErrorType.CONCEPTUAL
        
        # Estudiantes lentos o errores conceptuales necesitan más visuales
        use_visual_aids = (
            student_profile.necesita_explicacion_profunda or
            error_analysis.error_type in [ErrorType.CONCEPTUAL, ErrorType.PROCEDIMENTAL]
        )
        
        # Incluir problema similar si gap_level >= 3
        include_similar_problem = error_analysis.gap_level >= 3
        
        # Más ánimo para estudiantes lentos
        if student_profile.progress_level in [ProgressLevel.MUY_LENTO, ProgressLevel.LENTO]:
            encouragement_level = "alto"
        elif student_profile.progress_level == ProgressLevel.INTERMEDIO:
            encouragement_level = "medio"
        else:
            encouragement_level = "bajo"
        
        return PedagogicalStrategy(
            depth=depth,
            focus_on_concept=focus_on_concept,
            use_visual_aids=use_visual_aids,
            include_similar_problem=include_similar_problem,
            encouragement_level=encouragement_level
        )
    
    def _calculate_depth(
        self, 
        error_analysis: ErrorAnalysis, 
        student_profile: StudentProfile
    ) -> ExplanationDepth:
        """Calcula profundidad de explicación"""
        
        # Error atencional simple -> mínima
        if (error_analysis.error_type == ErrorType.ATENCIONAL and 
            error_analysis.gap_level <= 2):
            return ExplanationDepth.MINIMA
        
        # Error operacional simple + estudiante rápido -> básica
        if (error_analysis.error_type == ErrorType.OPERACIONAL and 
            error_analysis.gap_level <= 2 and
            student_profile.progress_level in [ProgressLevel.RAPIDO, ProgressLevel.MUY_RAPIDO]):
            return ExplanationDepth.BASICA
        
        # Error conceptual siempre profunda
        if error_analysis.error_type == ErrorType.CONCEPTUAL:
            return ExplanationDepth.PROFUNDA
        
        # Estudiante lento o gap alto -> profunda
        if (student_profile.necesita_explicacion_profunda or 
            error_analysis.gap_level >= 4):
            return ExplanationDepth.PROFUNDA
        
        # Por defecto, intermedia
        return ExplanationDepth.INTERMEDIA


if __name__ == "__main__":
    from src.phase1_error_analysis.error_types import ErrorAnalysis, ErrorType
    
    # Ejemplo de prueba
    error = ErrorAnalysis(
        error_type=ErrorType.CONCEPTUAL,
        description="Usó multiplicación en vez de suma",
        gap_level=4,
        misconception="Confunde suma con multiplicación",
        correct_step_missed="Debió sumar"
    )
    
    student = StudentProfile(
        progress_level=ProgressLevel.LENTO,
        tiempo_esperado=60.0,
        tiempo_realizado=95.0,
        unidad="Unidad 2",
        leccion="Lección 2",
        nivel=2,
        clase=1
    )
    
    adapter = ContentAdapter()
    strategy = adapter.determine_strategy(error, student)
    
    print(f"Profundidad: {strategy.depth}")
    print(f"Enfoque conceptual: {strategy.focus_on_concept}")
    print(f"Ayudas visuales: {strategy.use_visual_aids}")
    print(f"Problema similar: {strategy.include_similar_problem}")
    print(f"Nivel de ánimo: {strategy.encouragement_level}")