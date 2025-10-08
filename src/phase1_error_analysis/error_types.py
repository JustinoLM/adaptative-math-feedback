from enum import Enum
from pydantic import BaseModel
from typing import Optional

class ErrorType(str, Enum):
    CONCEPTUAL = "conceptual"  # No entiende qué operación usar
    PROCEDIMENTAL = "procedimental"  # Procedimiento incorrecto
    OPERACIONAL = "operacional"  # Error en el cálculo
    ATENCIONAL = "atencional"  # Error de distracción/copia
    NINGUNO = "ninguno"  # Respuesta correcta

class ErrorAnalysis(BaseModel):
    error_type: ErrorType
    description: str
    gap_level: int  # 1-5: qué tan lejos está de la solución
    misconception: Optional[str] = None  # Qué concepto malinterpretó
    correct_step_missed: Optional[str] = None