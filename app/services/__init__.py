from .evaluation_schema import ResultadoEvaluacion
from .knowledge_base import get_all_rules
from .inference_engine import InferenceEngine


def ejecutar_analisis(datos: dict) -> dict:
    engine = InferenceEngine(rules=get_all_rules())

    for clave, valor in datos.items():
        engine.agregar_hecho(clave, valor, 1.0)

    engine.disparar_reglas()

    if "error" in engine.hechos:
        return {"error": engine.hechos["error"]}

    resultado = engine.construir_resultado()
    return resultado.to_dict()
