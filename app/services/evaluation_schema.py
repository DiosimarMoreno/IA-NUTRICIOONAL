from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass
class Hecho:
    atributo: str
    valor: Any
    cf: float = 1.0
    regla_origen: str | None = None


@dataclass
class Rule:
    id: str
    description: str
    condiciones: list[tuple[str, str, Any]]
    conclusiones: list[tuple[str, Any]]
    prioridad: int = 10
    cf: float = 1.0
    modulo: str = ""
    evidencia: str = ""

    def evaluar(self, hechos: dict[str, Any]) -> bool:
        if not self.condiciones:
            return True
        for attr, op, val in self.condiciones:
            hecho_val = hechos.get(attr)
            if op == "existe":
                if hecho_val is None:
                    return False
            elif op == "no_existe":
                if hecho_val is not None:
                    return False
            elif hecho_val is None:
                return False
            elif op == "==" and hecho_val != val:
                return False
            elif op == "!=" and hecho_val == val:
                return False
            elif op == ">=" and not (hecho_val >= val):
                return False
            elif op == "<=" and not (hecho_val <= val):
                return False
            elif op == ">" and not (hecho_val > val):
                return False
            elif op == "<" and not (hecho_val < val):
                return False
            elif op == "contains" and val not in str(hecho_val):
                return False
        return True


@dataclass
class ResultadoEvaluacion:
    imc: float = 0.0
    clasificacion_imc: str = ""
    peso_ideal: float = 0.0
    rango_min: float = 0.0
    rango_max: float = 0.0
    somatotipo: str = ""
    somatotipo_desc: str = ""
    masa_grasa: float = 0.0
    masa_magra: float = 0.0
    agua_corporal: float = 0.0
    tmb: int = 0
    factor_actividad: float = 0.0
    actividad_etiqueta: str = ""
    calorias_objetivo: int = 0
    objetivo_etiqueta: str = ""
    proteina_g: float = 0.0
    carbos_g: float = 0.0
    grasas_g: float = 0.0
    pct_proteina: int = 0
    pct_carbos: int = 0
    pct_grasas: int = 0
    cal_proteina: int = 0
    cal_carbos: int = 0
    cal_grasas: int = 0
    riesgo_metabolico: str = ""
    riesgo_nutricional: str = ""
    alertas: list[str] = field(default_factory=list)
    recomendaciones: list[str] = field(default_factory=list)
    nota_clinica: str = ""
    explicaciones: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
