from enum import Enum
from pydantic import BaseModel

class ProgressLevel(str, Enum):
    MUY_LENTO = "muy_lento"
    LENTO = "lento"
    INTERMEDIO = "intermedio"
    RAPIDO = "rapido"
    MUY_RAPIDO = "muy_rapido"

class StudentProfile(BaseModel):
    progress_level: ProgressLevel
    tiempo_esperado: float  # segundos
    tiempo_realizado: float  # segundos
    unidad: str
    leccion: str
    nivel: int
    clase: int
    
    @property
    def ratio_tiempo(self) -> float:
        """Ratio tiempo_realizado / tiempo_esperado"""
        if self.tiempo_esperado == 0:
            return 1.0
        return self.tiempo_realizado / self.tiempo_esperado
    
    @property
    def necesita_explicacion_profunda(self) -> bool:
        """Determina si necesita explicación detallada"""
        # Si es lento o muy lento, o tardó mucho más
        return (
            self.progress_level in [ProgressLevel.MUY_LENTO, ProgressLevel.LENTO] or
            self.ratio_tiempo > 1.5
        )