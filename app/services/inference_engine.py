from typing import Any
from .evaluation_schema import Rule, ResultadoEvaluacion
from .clinical_knowledge import (
    calcular_imc,
    clasificar_imc,
    peso_ideal_devine,
    rango_saludable,
    somatotipo_por_grasa,
    somatotipo_por_imc,
    estimar_grasa_deurenberg,
    masa_grasa_kg,
    masa_magra_kg,
    agua_watson,
)
from .nutritional_knowledge import (
    tmb_mifflin_stjeor,
    factor_actividad,
    calorias_objetivo,
    distribuir_macros,
    LIMITES_CALORICOS,
)


class InferenceEngine:
    def __init__(self, rules: list[Rule]):
        self.rules = rules
        self.hechos: dict[str, Any] = {}
        self.certezas: dict[str, float] = {}
        self.fired_rules: set[str] = set()
        self.trazas: list[str] = []

    def agregar_hecho(self, atributo: str, valor: Any, cf: float = 1.0):
        self.hechos[atributo] = valor
        self.certezas[atributo] = cf

    def obtener_hecho(self, atributo: str) -> Any:
        return self.hechos.get(atributo)

    def _disparar_stage(self, modulo: str):
        stage_rules = [r for r in self.rules if r.modulo == modulo]
        while True:
            fired = False
            for rule in sorted(stage_rules, key=lambda r: r.prioridad, reverse=True):
                if rule.id in self.fired_rules:
                    continue
                if rule.evaluar(self.hechos):
                    for attr, val in rule.conclusiones:
                        if attr not in self.hechos:
                            self.hechos[attr] = val
                            self.certezas[attr] = rule.cf
                            self.trazas.append(
                                f"{rule.id}: {rule.description} -> {attr} = {val} "
                                f"(CF: {rule.cf})"
                            )
                    self.fired_rules.add(rule.id)
                    fired = True
                    break
            if not fired:
                break

    def disparar_reglas(self):
        orden = ["validacion", "antropometrico", "metabolico",
                 "adaptacion", "prescripcion", "riesgos"]
        for modulo in orden:
            self._disparar_stage(modulo)

    def _aplicar_funciones(self):
        """Ejecuta las funciones de cálculo reales según los hechos inferidos."""
        peso = self.hechos.get("peso", 0)
        estatura = self.hechos.get("estatura", 0)
        edad = self.hechos.get("edad", 0)
        sexo = self.hechos.get("sexo", "M")
        pc_grasa = self.hechos.get("pc_grasa")
        nivel = self.hechos.get("nivel_actividad", "sedentario")
        objetivo = self.hechos.get("objetivo", "mantenimiento")

        # --- Antropométrico ---
        imc = calcular_imc(peso, estatura)
        self.agregar_hecho("imc", imc, 1.0)

        clasificacion = clasificar_imc(imc)
        self.agregar_hecho("clasificacion_imc", clasificacion, 1.0)

        peso_ideal = peso_ideal_devine(estatura, sexo)
        self.agregar_hecho("peso_ideal", peso_ideal, 0.95)

        r_min, r_max = rango_saludable(estatura)
        self.agregar_hecho("rango_min", r_min, 0.90)
        self.agregar_hecho("rango_max", r_max, 0.90)

        # Estimar % grasa si no se proporcionó (Deurenberg)
        if pc_grasa is None:
            pc_grasa = estimar_grasa_deurenberg(imc, edad, sexo)
            self.agregar_hecho("pc_grasa_estimado", pc_grasa, 0.70)
            fuente_soma = self.hechos.get("somatotipo_fuente", "imc")
        else:
            self.agregar_hecho("pc_grasa_estimado", pc_grasa, 1.0)
            fuente_soma = "grasa"

        if fuente_soma == "grasa":
            somatipo, somatipo_desc = somatotipo_por_grasa(pc_grasa, sexo)
        else:
            somatipo, somatipo_desc = somatotipo_por_imc(imc)
        self.agregar_hecho("somatotipo", somatipo, 0.85 if fuente_soma == "grasa" else 0.70)
        self.agregar_hecho("somatotipo_desc", somatipo_desc, 0.85 if fuente_soma == "grasa" else 0.70)

        m_grasa = masa_grasa_kg(peso, pc_grasa)
        self.agregar_hecho("masa_grasa", m_grasa, 0.90)

        m_magra = masa_magra_kg(peso, m_grasa)
        self.agregar_hecho("masa_magra", m_magra, 0.90)

        agua = agua_watson(peso, estatura, edad, sexo)
        self.agregar_hecho("agua_corporal", agua, 0.90)

        # --- Metabólico ---
        tmb = int(round(tmb_mifflin_stjeor(peso, estatura, edad, sexo)))
        self.agregar_hecho("tmb", tmb, 0.95)

        factor, etiqueta_act = factor_actividad(nivel)
        self.agregar_hecho("factor_act", factor, 1.0)
        self.agregar_hecho("actividad_etiqueta", etiqueta_act, 1.0)

        tdee = int(round(tmb * factor))
        self.agregar_hecho("tdee", tdee, 0.90)

        # --- Adaptación por objetivo ---
        cal_objetivo, obj_etiqueta = calorias_objetivo(tdee, objetivo)
        limite = LIMITES_CALORICOS.get(sexo, 1200)
        if cal_objetivo < limite:
            cal_objetivo = limite
            self.agregar_hecho(
                "alerta",
                f"Las calorías calculadas estaban por debajo del límite seguro "
                f"({limite} kcal). Se ha ajustado automáticamente."
            )
        self.agregar_hecho("calorias_objetivo", cal_objetivo, 0.85)
        self.agregar_hecho("objetivo_etiqueta", obj_etiqueta, 0.85)

        # --- Prescripción de macros ---
        macros = distribuir_macros(cal_objetivo, objetivo, peso, sexo)
        for key, val in macros.items():
            self.agregar_hecho(key, val, 0.80)

        # --- Riesgos metabólicos / nutricionales ---
        riesgo_meta = ""
        riesgo_nutri = ""
        if "Obesidad" in clasificacion:
            riesgo_meta = "Alto"
        elif imc >= 25:
            riesgo_meta = "Moderado"
        else:
            riesgo_meta = "Bajo"

        if clasificacion == "Delgadez severa":
            riesgo_nutri = "Alto"
        elif clasificacion in ("Delgadez moderada", "Delgadez leve"):
            riesgo_nutri = "Moderado"
        else:
            riesgo_nutri = "Bajo"

        self.agregar_hecho("riesgo_metabolico", riesgo_meta, 0.85)
        self.agregar_hecho("riesgo_nutricional", riesgo_nutri, 0.85)

        # --- Nota clínica ---
        nota = self._generar_nota_clinica(
            obj_etiqueta, cal_objetivo, clasificacion, peso_ideal, riesgo_meta
        )
        self.agregar_hecho("nota_clinica", nota, 1.0)

    def _generar_nota_clinica(
        self, objetivo_etiqueta: str, calorias: int,
        clasificacion_imc: str, peso_ideal: float,
        riesgo_metabolico: str
    ) -> str:
        partes = []
        if objetivo_etiqueta == "Hipertrofia Muscular":
            partes.append(
                f"Plan nutricional diseñado para máxima síntesis proteica "
                f"con {calorias} kcal/día en superávit controlado."
            )
        elif objetivo_etiqueta == "Pérdida de Grasa":
            partes.append(
                f"Plan hipocalórico estructurado para pérdida de grasa "
                f"manteniendo masa muscular, basado en {calorias} kcal/día."
            )
        else:
            partes.append(
                f"Plan nutricional equilibrado para mantenimiento de "
                f"composición corporal con {calorias} kcal/día."
            )

        if "Obesidad" in clasificacion_imc or riesgo_metabolico == "Alto":
            partes.append(
                "Se recomienda supervisión profesional periódica debido "
                "al perfil metabólico identificado."
            )

        if peso_ideal > 0:
            peso_actual = self.hechos.get("peso", 0)
            diff = round(peso_actual - peso_ideal, 1)
            if abs(diff) > 5:
                partes.append(
                    f"Su peso actual difiere significativamente del peso "
                    f"ideal estimado ({peso_ideal} kg). "
                    f"{'Superávit' if diff > 0 else 'Déficit'} de {abs(diff)} kg."
                )

        partes.append(
            "Se recomienda seguir este plan por un mínimo de 4 semanas "
            "para observar cambios significativos. Ajuste las porciones "
            "según su respuesta individual."
        )

        return " ".join(partes)

    def construir_resultado(self) -> ResultadoEvaluacion:
        self._aplicar_funciones()

        alertas = [
            v for k, v in self.hechos.items()
            if k.startswith("alerta") and isinstance(v, str)
        ]

        recomendaciones = [
            v for k, v in self.hechos.items()
            if k.startswith("recomendacion") and isinstance(v, str)
        ]

        resultado = ResultadoEvaluacion(
            imc=self.hechos.get("imc", 0.0),
            clasificacion_imc=self.hechos.get("clasificacion_imc", ""),
            peso_ideal=self.hechos.get("peso_ideal", 0.0),
            rango_min=self.hechos.get("rango_min", 0.0),
            rango_max=self.hechos.get("rango_max", 0.0),
            somatotipo=self.hechos.get("somatotipo", ""),
            somatotipo_desc=self.hechos.get("somatotipo_desc", ""),
            masa_grasa=self.hechos.get("masa_grasa", 0.0),
            masa_magra=self.hechos.get("masa_magra", 0.0),
            agua_corporal=self.hechos.get("agua_corporal", 0.0),
            tmb=self.hechos.get("tmb", 0),
            factor_actividad=self.hechos.get("factor_act", 0.0),
            actividad_etiqueta=self.hechos.get("actividad_etiqueta", ""),
            calorias_objetivo=self.hechos.get("calorias_objetivo", 0),
            objetivo_etiqueta=self.hechos.get("objetivo_etiqueta", ""),
            proteina_g=self.hechos.get("proteina_g", 0.0),
            carbos_g=self.hechos.get("carbos_g", 0.0),
            grasas_g=self.hechos.get("grasas_g", 0.0),
            pct_proteina=self.hechos.get("pct_proteina", 0),
            pct_carbos=self.hechos.get("pct_carbos", 0),
            pct_grasas=self.hechos.get("pct_grasas", 0),
            cal_proteina=self.hechos.get("cal_proteina", 0),
            cal_carbos=self.hechos.get("cal_carbos", 0),
            cal_grasas=self.hechos.get("cal_grasas", 0),
            riesgo_metabolico=self.hechos.get("riesgo_metabolico", ""),
            riesgo_nutricional=self.hechos.get("riesgo_nutricional", ""),
            alertas=alertas,
            recomendaciones=recomendaciones,
            nota_clinica=self.hechos.get("nota_clinica", ""),
            explicaciones=list(self.trazas),
        )

        return resultado
