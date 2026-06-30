from .evaluation_schema import Rule


def get_all_rules() -> list[Rule]:
    return [
        # ============================================================
        # MÓDULO 1: VALIDACIÓN (R001-R003)
        # ============================================================
        Rule(
            id="R001",
            description="Validar que estatura sea positiva",
            condiciones=[("estatura", "<=", 0)],
            conclusiones=[("error", "La estatura debe ser un valor positivo en centímetros")],
            prioridad=100, cf=1.0, modulo="validacion",
            evidencia="Validación de entrada"
        ),
        Rule(
            id="R002",
            description="Validar que peso sea positivo",
            condiciones=[("peso", "<=", 0)],
            conclusiones=[("error", "El peso debe ser un valor positivo en kilogramos")],
            prioridad=100, cf=1.0, modulo="validacion",
            evidencia="Validación de entrada"
        ),
        Rule(
            id="R003",
            description="Normalizar sexo no binario al promedio de fórmulas",
            condiciones=[("sexo", "!=", "M"), ("sexo", "!=", "F")],
            conclusiones=[("sexo_normalizado", "promedio")],
            prioridad=90, cf=0.8, modulo="validacion",
            evidencia="Consenso: cuando el sexo no está especificado, se promedian fórmulas masculinas y femeninas"
        ),

        # ============================================================
        # MÓDULO 2: ANTROPOMÉTRICO (R004-R015)
        # ============================================================
        Rule(
            id="R004",
            description="Calcular IMC mediante fórmula de Quetelet",
            condiciones=[],
            conclusiones=[("imc_calculado", True)],
            prioridad=80, cf=1.0, modulo="antropometrico",
            evidencia="Quetelet, 1832. El IMC se calcula como peso(kg) / estatura(m)²"
        ),
        Rule(
            id="R005",
            description="Clasificar IMC como Delgadez severa (OMS)",
            condiciones=[("imc", ">=", 0), ("imc", "<", 16.0)],
            conclusiones=[("clasificacion_imc", "Delgadez severa")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R006",
            description="Clasificar IMC como Delgadez moderada (OMS)",
            condiciones=[("imc", ">=", 16.0), ("imc", "<", 17.0)],
            conclusiones=[("clasificacion_imc", "Delgadez moderada")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R007",
            description="Clasificar IMC como Delgadez leve (OMS)",
            condiciones=[("imc", ">=", 17.0), ("imc", "<", 18.5)],
            conclusiones=[("clasificacion_imc", "Delgadez leve")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R008",
            description="Clasificar IMC como Normal (OMS)",
            condiciones=[("imc", ">=", 18.5), ("imc", "<", 25.0)],
            conclusiones=[("clasificacion_imc", "Normal")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R009",
            description="Clasificar IMC como Sobrepeso (OMS)",
            condiciones=[("imc", ">=", 25.0), ("imc", "<", 30.0)],
            conclusiones=[("clasificacion_imc", "Sobrepeso")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R010",
            description="Clasificar IMC como Obesidad tipo I (OMS)",
            condiciones=[("imc", ">=", 30.0), ("imc", "<", 35.0)],
            conclusiones=[("clasificacion_imc", "Obesidad tipo I")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R011",
            description="Clasificar IMC como Obesidad tipo II (OMS)",
            condiciones=[("imc", ">=", 35.0), ("imc", "<", 40.0)],
            conclusiones=[("clasificacion_imc", "Obesidad tipo II")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R012",
            description="Clasificar IMC como Obesidad tipo III (OMS)",
            condiciones=[("imc", ">=", 40.0)],
            conclusiones=[("clasificacion_imc", "Obesidad tipo III")],
            prioridad=70, cf=1.0, modulo="antropometrico",
            evidencia="OMS, 2000. Obesity: Preventing and managing the global epidemic."
        ),
        Rule(
            id="R013",
            description="Calcular peso ideal mediante fórmula de Devine (masculino)",
            condiciones=[("sexo", "==", "M")],
            conclusiones=[("peso_ideal_formula", "devine_m")],
            prioridad=60, cf=0.95, modulo="antropometrico",
            evidencia="Devine, 1974. Gentamicin therapy. Drug Intelligence & Clinical Pharmacy."
        ),
        Rule(
            id="R013b",
            description="Calcular peso ideal mediante fórmula de Devine (femenino)",
            condiciones=[("sexo", "==", "F")],
            conclusiones=[("peso_ideal_formula", "devine_f")],
            prioridad=60, cf=0.95, modulo="antropometrico",
            evidencia="Devine, 1974. Gentamicin therapy. Drug Intelligence & Clinical Pharmacy."
        ),
        Rule(
            id="R013c",
            description="Calcular peso ideal promedio (sexo no binario)",
            condiciones=[("sexo_normalizado", "==", "promedio")],
            conclusiones=[("peso_ideal_formula", "devine_promedio")],
            prioridad=60, cf=0.85, modulo="antropometrico",
            evidencia="Devine, 1974. Promedio de fórmulas masculina y femenina."
        ),
        Rule(
            id="R014",
            description="Estimar somatotipo usando porcentaje de grasa corporal",
            condiciones=[("pc_grasa", "!=", None)],
            conclusiones=[("somatotipo_fuente", "grasa")],
            prioridad=55, cf=0.85, modulo="antropometrico",
            evidencia="Clasificación de somatotipo basada en porcentaje de grasa por sexo (Heath-Carter, 1967)"
        ),
        Rule(
            id="R014b",
            description="Estimar somatotipo usando IMC como aproximación",
            condiciones=[("pc_grasa", "==", None)],
            conclusiones=[("somatotipo_fuente", "imc")],
            prioridad=50, cf=0.70, modulo="antropometrico",
            evidencia="Aproximación de somatotipo mediante IMC cuando no hay datos de composición corporal"
        ),
        Rule(
            id="R015",
            description="Calcular agua corporal total mediante fórmula de Watson",
            condiciones=[],
            conclusiones=[("agua_calculada", True)],
            prioridad=40, cf=0.90, modulo="antropometrico",
            evidencia="Watson et al., 1980. Total body water volumes for adults. Journal of Clinical Nutrition."
        ),

        # ============================================================
        # MÓDULO 3: METABÓLICO (R016-R020b)
        # ============================================================
        Rule(
            id="R016",
            description="Calcular TMB mediante Mifflin-St Jeor (masculino)",
            condiciones=[("sexo", "==", "M")],
            conclusiones=[("tmb_formula", "mifflin_m")],
            prioridad=80, cf=0.95, modulo="metabolico",
            evidencia="Mifflin et al., 1990. A new predictive equation for resting energy expenditure. AJCN."
        ),
        Rule(
            id="R016b",
            description="Calcular TMB mediante Mifflin-St Jeor (femenino)",
            condiciones=[("sexo", "==", "F")],
            conclusiones=[("tmb_formula", "mifflin_f")],
            prioridad=80, cf=0.95, modulo="metabolico",
            evidencia="Mifflin et al., 1990. A new predictive equation for resting energy expenditure. AJCN."
        ),
        Rule(
            id="R016c",
            description="Calcular TMB promedio (sexo no binario)",
            condiciones=[("sexo_normalizado", "==", "promedio")],
            conclusiones=[("tmb_formula", "mifflin_promedio")],
            prioridad=80, cf=0.85, modulo="metabolico",
            evidencia="Mifflin-St Jeor promediado para sexo no especificado."
        ),
        Rule(
            id="R017",
            description="Aplicar factor de actividad: sedentario",
            condiciones=[("nivel_actividad", "==", "sedentario")],
            conclusiones=[("factor_act", 1.2), ("actividad_etiqueta", "Sedentario")],
            prioridad=75, cf=1.0, modulo="metabolico",
            evidencia="FAO/WHO/UNU, 2005. Human energy requirements. Factor PAL 1.2."
        ),
        Rule(
            id="R018",
            description="Aplicar factor de actividad: ligera",
            condiciones=[("nivel_actividad", "==", "ligera")],
            conclusiones=[("factor_act", 1.375), ("actividad_etiqueta", "Actividad ligera")],
            prioridad=75, cf=1.0, modulo="metabolico",
            evidencia="FAO/WHO/UNU, 2005. Human energy requirements. Factor PAL 1.375."
        ),
        Rule(
            id="R019",
            description="Aplicar factor de actividad: moderado",
            condiciones=[("nivel_actividad", "==", "moderado")],
            conclusiones=[("factor_act", 1.55), ("actividad_etiqueta", "Moderadamente activo")],
            prioridad=75, cf=1.0, modulo="metabolico",
            evidencia="FAO/WHO/UNU, 2005. Human energy requirements. Factor PAL 1.55."
        ),
        Rule(
            id="R020",
            description="Aplicar factor de actividad: muy activo",
            condiciones=[("nivel_actividad", "==", "muy_activo")],
            conclusiones=[("factor_act", 1.725), ("actividad_etiqueta", "Muy activo")],
            prioridad=75, cf=1.0, modulo="metabolico",
            evidencia="FAO/WHO/UNU, 2005. Human energy requirements. Factor PAL 1.725."
        ),
        Rule(
            id="R020b",
            description="Aplicar factor de actividad: extremo",
            condiciones=[("nivel_actividad", "==", "extremo")],
            conclusiones=[("factor_act", 1.9), ("actividad_etiqueta", "Extremadamente activo")],
            prioridad=75, cf=1.0, modulo="metabolico",
            evidencia="FAO/WHO/UNU, 2005. Human energy requirements. Factor PAL 1.9."
        ),

        # ============================================================
        # MÓDULO 4: ADAPTACIÓN POR OBJETIVO (R021-R025)
        # ============================================================
        Rule(
            id="R021",
            description="Ajustar calorías para hipertrofia muscular (superávit 15%)",
            condiciones=[("objetivo", "==", "hipertrofia")],
            conclusiones=[("objetivo_etiqueta", "Hipertrofia Muscular")],
            prioridad=70, cf=0.85, modulo="adaptacion",
            evidencia="Slater & Phillips, 2011. Protein requirements for muscle hypertrophy. Sports Medicine."
        ),
        Rule(
            id="R022",
            description="Mantener calorías base para mantenimiento",
            condiciones=[("objetivo", "==", "mantenimiento")],
            conclusiones=[("objetivo_etiqueta", "Mantenimiento")],
            prioridad=70, cf=0.90, modulo="adaptacion",
            evidencia="Consenso: mantenimiento calórico igual al gasto energético total."
        ),
        Rule(
            id="R023",
            description="Ajustar calorías para pérdida de grasa (déficit 20%)",
            condiciones=[("objetivo", "==", "perdida")],
            conclusiones=[("objetivo_etiqueta", "Pérdida de Grasa")],
            prioridad=70, cf=0.85, modulo="adaptacion",
            evidencia="Donnelly et al., 2014. Appropriate physical activity intervention strategies for weight loss. Medicine & Science in Sports."
        ),
        Rule(
            id="R024",
            description="Aplicar límite de seguridad calórica mínimo (masculino)",
            condiciones=[("sexo", "==", "M")],
            conclusiones=[("limite_calorico_min", 1200)],
            prioridad=95, cf=0.95, modulo="adaptacion",
            evidencia="ACSM, 2009. Minimum calorie thresholds: 1200 kcal/día para hombres."
        ),
        Rule(
            id="R024b",
            description="Aplicar límite de seguridad calórica mínimo (femenino)",
            condiciones=[("sexo", "==", "F")],
            conclusiones=[("limite_calorico_min", 1000)],
            prioridad=95, cf=0.95, modulo="adaptacion",
            evidencia="ACSM, 2009. Minimum calorie thresholds: 1000 kcal/día para mujeres."
        ),
        Rule(
            id="R025",
            description="Clasificar déficit calórico por debajo del límite seguro",
            condiciones=[("calorias_objetivo", "existe", None)],
            conclusiones=[("verificar_seguridad", True)],
            prioridad=90, cf=1.0, modulo="adaptacion",
            evidencia="Verificación de seguridad nutricional."
        ),

        # ============================================================
        # MÓDULO 5: PRESCRIPCIÓN DE MACRONUTRIENTES (R026-R032)
        # ============================================================
        Rule(
            id="R026",
            description="Distribuir macros para hipertrofia: alta proteína, carbos moderados",
            condiciones=[("objetivo", "==", "hipertrofia")],
            conclusiones=[("macro_perfil", "hipertrofia")],
            prioridad=60, cf=0.80, modulo="prescripcion",
            evidencia="Jäger et al., 2017. International Society of Sports Nutrition position stand: protein and exercise. JISSN."
        ),
        Rule(
            id="R027",
            description="Distribuir macros para mantenimiento: perfil equilibrado",
            condiciones=[("objetivo", "==", "mantenimiento")],
            conclusiones=[("macro_perfil", "mantenimiento")],
            prioridad=60, cf=0.80, modulo="prescripcion",
            evidencia="WHO, 2015. Guideline: Carbohydrate intake for adults and children. Macronutrient balance."
        ),
        Rule(
            id="R028",
            description="Distribuir macros para pérdida de grasa: alta proteína, carbos reducidos",
            condiciones=[("objetivo", "==", "perdida")],
            conclusiones=[("macro_perfil", "perdida")],
            prioridad=60, cf=0.85, modulo="prescripcion",
            evidencia="Phillips & Van Loon, 2011. Dietary protein for athletes: from requirements to optimum adaptation. J Sports Sciences."
        ),
        Rule(
            id="R029",
            description="Calcular calorías aportadas por proteínas (4 kcal/g)",
            condiciones=[],
            conclusiones=[("calc_cal_proteina", True)],
            prioridad=40, cf=1.0, modulo="prescripcion",
            evidencia="Atwater general factor: 4 kcal/g para proteínas."
        ),
        Rule(
            id="R030",
            description="Calcular gramos y calorías de carbohidratos (4 kcal/g)",
            condiciones=[],
            conclusiones=[("calc_cal_carbos", True)],
            prioridad=40, cf=1.0, modulo="prescripcion",
            evidencia="Atwater general factor: 4 kcal/g para carbohidratos."
        ),
        Rule(
            id="R031",
            description="Calcular gramos y calorías de grasas (9 kcal/g)",
            condiciones=[],
            conclusiones=[("calc_cal_grasas", True)],
            prioridad=40, cf=1.0, modulo="prescripcion",
            evidencia="Atwater general factor: 9 kcal/g para grasas."
        ),
        Rule(
            id="R032",
            description="Ajustar porcentaje de grasas como remanente energético",
            condiciones=[],
            conclusiones=[("ajuste_grasas", True)],
            prioridad=35, cf=1.0, modulo="prescripcion",
            evidencia="Distribución energética: grasas cubren el resto calórico no asignado a proteínas y carbohidratos."
        ),

        # ============================================================
        # MÓDULO 6: RIESGOS Y NOTAS CLÍNICAS (R033-R040)
        # ============================================================
        Rule(
            id="R033",
            description="Identificar riesgo metabólico alto por obesidad",
            condiciones=[("clasificacion_imc", "contains", "Obesidad")],
            conclusiones=[("riesgo_metabolico", "Alto")],
            prioridad=50, cf=0.85, modulo="riesgos",
            evidencia="OMS, 2021. Obesity and overweight. Fact sheet. Riesgo elevado de enfermedades cardiovasculares y metabólicas."
        ),
        Rule(
            id="R034",
            description="Identificar riesgo nutricional alto por delgadez severa",
            condiciones=[("clasificacion_imc", "==", "Delgadez severa")],
            conclusiones=[("riesgo_nutricional", "Alto")],
            prioridad=50, cf=0.85, modulo="riesgos",
            evidencia="OMS, 2021. Malnutrition fact sheet. Riesgo elevado de deficiencias nutricionales."
        ),
        Rule(
            id="R035",
            description="Alerta por porcentaje de grasa demasiado bajo en hombres",
            condiciones=[("sexo", "==", "M"), ("pc_grasa_estimado", "<", 8)],
            conclusiones=[("alerta", "Porcentaje de grasa corporal muy bajo (<8%). Riesgo de desequilibrio hormonal y pérdida de masa muscular.")],
            prioridad=45, cf=0.90, modulo="riesgos",
            evidencia="ACSM, 2014. Essential body fat for men: 3-5%. Niveles inferiores a 8% requieren supervisión médica."
        ),
        Rule(
            id="R036",
            description="Alerta por porcentaje de grasa demasiado bajo en mujeres",
            condiciones=[("sexo", "==", "F"), ("pc_grasa_estimado", "<", 15)],
            conclusiones=[("alerta", "Porcentaje de grasa corporal muy bajo (<15%). Riesgo de alteraciones menstruales y densidad ósea.")],
            prioridad=45, cf=0.90, modulo="riesgos",
            evidencia="ACSM, 2014. Essential body fat for women: 8-12%. Niveles inferiores a 15% requieren supervisión médica."
        ),
        Rule(
            id="R037a",
            description="Recomendar consulta profesional por obesidad",
            condiciones=[("imc", ">", 30)],
            conclusiones=[("recomendacion_alta", "Se recomienda consultar con un profesional de la salud antes de iniciar cualquier plan nutricional debido a IMC elevado.")],
            prioridad=40, cf=0.80, modulo="riesgos",
            evidencia="Consenso: IMC superior a 30 requiere evaluación profesional."
        ),
        Rule(
            id="R037b",
            description="Recomendar consulta profesional por delgadez severa",
            condiciones=[("imc", "<", 16)],
            conclusiones=[("recomendacion_baja", "Se recomienda consultar con un profesional de la salud antes de iniciar cualquier plan nutricional debido a IMC muy bajo.")],
            prioridad=40, cf=0.80, modulo="riesgos",
            evidencia="Consenso: IMC inferior a 16 requiere evaluación profesional."
        ),
        Rule(
            id="R038",
            description="Generar nota clínica personalizada",
            condiciones=[],
            conclusiones=[("nota_generada", True)],
            prioridad=10, cf=1.0, modulo="riesgos",
            evidencia="Nota clínica generada dinámicamente según perfil del paciente."
        ),
    ]
