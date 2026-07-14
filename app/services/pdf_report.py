from datetime import datetime
from fpdf import FPDF


class NutricionReport(FPDF):
    """Reporte clinico estilo sistema experto MYCIN."""

    COLOR_PRINCIPAL = (0, 114, 255)
    COLOR_VERDE = (0, 200, 83)
    COLOR_NARANJA = (255, 109, 0)
    COLOR_ROJO = (239, 68, 68)
    COLOR_PURPURA = (155, 81, 224)
    COLOR_BG = (6, 9, 19)
    COLOR_TEXTO = (30, 30, 30)
    COLOR_GRIS = (120, 120, 120)
    COLOR_CLARO = (240, 243, 250)
    COLOR_BLANCO = (255, 255, 255)

    def __init__(self):
        super().__init__()
        self.set_auto_page_break(auto=True, margin=25)

    def header(self):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_GRIS)
        self.cell(0, 6, "NutriExpert - Sistema Experto de Asesoria Nutricional", align="L")
        self.cell(0, 6, f"Pagina {self.page_no()}/{{nb}}", align="R", new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(*self.COLOR_PRINCIPAL)
        self.set_line_width(0.4)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(4)

    def footer(self):
        self.set_y(-20)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(*self.COLOR_GRIS)
        self.multi_cell(0, 4,
            "NOTA: Este reporte es generado por un Sistema Experto de Asesoria Nutricional. "
            "No sustituye el diagnostico medico profesional. Factor de Certeza (CF) "
            "indica el nivel de confianza de cada inferencia (0.0 - 1.0).",
            align="C")

    def seccion_titulo(self, numero, titulo):
        self.ln(3)
        self.set_fill_color(*self.COLOR_PRINCIPAL)
        self.set_text_color(*self.COLOR_BLANCO)
        self.set_font("Helvetica", "B", 11)
        self.cell(0, 8, f"  {numero}. {titulo.upper()}", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def subseccion(self, titulo):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_PRINCIPAL)
        self.cell(0, 6, titulo, new_x="LMARGIN", new_y="NEXT")
        self.ln(1)

    def campo(self, etiqueta, valor, color=None):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_GRIS)
        self.cell(65, 5, etiqueta + ":")
        if color:
            self.set_text_color(*color)
        else:
            self.set_text_color(*self.COLOR_TEXTO)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, str(valor), new_x="LMARGIN", new_y="NEXT")

    def campo_doble(self, etiq1, val1, etiq2, val2, color1=None, color2=None):
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_GRIS)
        self.cell(35, 5, etiq1 + ":")
        if color1:
            self.set_text_color(*color1)
        else:
            self.set_text_color(*self.COLOR_TEXTO)
        self.set_font("Helvetica", "", 9)
        self.cell(55, 5, str(val1))

        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_GRIS)
        self.cell(35, 5, etiq2 + ":")
        if color2:
            self.set_text_color(*color2)
        else:
            self.set_text_color(*self.COLOR_TEXTO)
        self.set_font("Helvetica", "", 9)
        self.cell(0, 5, str(val2), new_x="LMARGIN", new_y="NEXT")

    def riesgo_badge(self, nivel):
        colores = {
            "Bajo": self.COLOR_VERDE,
            "Moderado": self.COLOR_NARANJA,
            "Alto": self.COLOR_ROJO,
        }
        c = colores.get(nivel, self.COLOR_GRIS)
        self.set_font("Helvetica", "B", 10)
        self.set_text_color(*c)
        self.cell(0, 6, f"[ {nivel.upper()} ]", new_x="LMARGIN", new_y="NEXT")

    def alerta_item(self, texto):
        self.set_fill_color(255, 243, 224)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_NARANJA)
        x = self.get_x()
        self.cell(5, 5, "!")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.COLOR_TEXTO)
        self.multi_cell(0, 5, texto, fill=True)
        self.ln(1)

    def recomendacion_item(self, idx, texto):
        self.set_fill_color(232, 245, 233)
        self.set_font("Helvetica", "B", 9)
        self.set_text_color(*self.COLOR_VERDE)
        self.cell(8, 5, f"{idx}.")
        self.set_font("Helvetica", "", 8)
        self.set_text_color(*self.COLOR_TEXTO)
        self.multi_cell(0, 5, texto, fill=True)
        self.ln(1)

    def nota_clinica_block(self, texto):
        self.set_fill_color(232, 240, 254)
        self.set_draw_color(*self.COLOR_PRINCIPAL)
        x = self.get_x()
        y = self.get_y()
        self.set_font("Helvetica", "I", 9)
        self.set_text_color(*self.COLOR_TEXTO)
        self.multi_cell(180, 5, texto, border=0, fill=True)
        self.ln(2)

    def traza_item(self, traza_texto):
        self.set_font("Helvetica", "", 7)
        self.set_text_color(80, 80, 80)
        self.set_fill_color(248, 248, 248)
        self.multi_cell(0, 4, traza_texto, fill=True)
        self.ln(0.5)

    def linea_separadora(self):
        self.set_draw_color(200, 200, 200)
        self.set_line_width(0.2)
        self.line(10, self.get_y(), 200, self.get_y())
        self.ln(2)


def _color_riesgo(nivel):
    colores = {
        "Bajo": (0, 200, 83),
        "Moderado": (255, 109, 0),
        "Alto": (239, 68, 68),
    }
    return colores.get(nivel, (120, 120, 120))


def generar_reporte_pdf(evaluacion, paciente) -> bytes:
    pdf = NutricionReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    r = evaluacion.resultados_dict

    # =========================================================
    # PORTADA / ENCABEZADO
    # =========================================================
    pdf.set_font("Helvetica", "B", 20)
    pdf.set_text_color(*NutricionReport.COLOR_PRINCIPAL)
    pdf.cell(0, 12, "NUTRIEXPERT", align="C", new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 10)
    pdf.set_text_color(*NutricionReport.COLOR_GRIS)
    pdf.cell(0, 6, "Sistema Experto de Asesoria Nutricional", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 5, "Reporte de Evaluacion Clinica", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    pdf.set_draw_color(*NutricionReport.COLOR_PRINCIPAL)
    pdf.set_line_width(0.8)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(6)

    # =========================================================
    # 1. DATOS DEL PACIENTE
    # =========================================================
    pdf.seccion_titulo("1", "Datos del Paciente")

    sexo_str = {"M": "Masculino", "F": "Femenino"}.get(paciente.sexo, "Otro")
    pdf.campo("Nombre completo", paciente.nombre)
    pdf.campo("Correo electronico", paciente.correo)
    pdf.campo_doble("Edad", f"{paciente.edad} anios", "Sexo", sexo_str)
    pdf.campo("Fecha de evaluacion", evaluacion.fecha_registro.strftime("%d/%m/%Y %H:%M"))
    pdf.ln(2)

    pdf.subseccion("Parametros de Entrada")
    pdf.campo_doble("Estatura", f"{evaluacion.estatura} cm", "Peso", f"{evaluacion.peso} kg")
    pg = evaluacion.porcentaje_grasa
    pdf.campo("Grasa corporal", f"{pg}%" if pg else "No proporcionado (estimado por Deurenberg)")
    pdf.campo("Nivel de actividad", r.get("actividad_etiqueta", evaluacion.nivel_actividad))
    pdf.campo("Objetivo nutricional", r.get("objetivo_etiqueta", evaluacion.objetivo_principal))
    pdf.ln(2)

    # =========================================================
    # 2. PERFIL ANTROPOMETRICO
    # =========================================================
    pdf.seccion_titulo("2", "Perfil Antropometrico")

    imc = r.get("imc", 0)
    clasif = r.get("clasificacion_imc", "N/A")
    pdf.campo_doble("IMC", f"{imc}", "Clasificacion OMS", clasif)
    pdf.campo_doble("Peso ideal (Devine)", f"{r.get('peso_ideal', 0)} kg",
                     "Rango saludable", f"{r.get('rango_min', 0)} - {r.get('rango_max', 0)} kg")

    peso_diff = round(evaluacion.peso - r.get("peso_ideal", evaluacion.peso), 1)
    signo = "+" if peso_diff > 0 else ""
    pdf.campo("Diferencia vs peso ideal", f"{signo}{peso_diff} kg")
    pdf.ln(1)

    pdf.subseccion("Composicion Corporal")
    pdf.campo("Somatotipo", r.get("somatotipo", "N/A"))
    pdf.campo("  Descripcion", r.get("somatotipo_desc", ""))
    pdf.campo_doble("Masa grasa", f"{r.get('masa_grasa', 0)} kg",
                     "Masa magra", f"{r.get('masa_magra', 0)} kg")
    pdf.campo("Agua corporal total", f"{r.get('agua_corporal', 0)} L")
    pdf.ln(2)

    # =========================================================
    # 3. PERFIL METABOLICO
    # =========================================================
    pdf.seccion_titulo("3", "Perfil Metabolico")

    tmb = r.get("tmb", 0)
    factor = r.get("factor_actividad", 0)
    tdee = int(round(tmb * factor)) if tmb and factor else 0
    pdf.campo_doble("TMB (Mifflin-St Jeor)", f"{tmb} kcal/dia",
                     "Factor de actividad", f"{factor} ({r.get('actividad_etiqueta', '')})")
    pdf.campo_doble("TDEE (gasto total)", f"{tdee} kcal/dia",
                     "Calorias objetivo", f"{r.get('calorias_objetivo', 0)} kcal/dia")
    pdf.campo("Ajuste por objetivo", r.get("objetivo_etiqueta", ""))
    pdf.ln(2)

    # =========================================================
    # 4. DISTRIBUCION DE MACRONUTRIENTES
    # =========================================================
    pdf.seccion_titulo("4", "Distribucion de Macronutrientes")

    pdf.subseccion("Prescripcion Diaria")
    pdf.campo_doble("Proteina", f"{r.get('proteina_g', 0)} g",
                     "Calorias", f"{r.get('cal_proteina', 0)} kcal")
    pdf.campo_doble("Carbohidratos", f"{r.get('carbos_g', 0)} g",
                     "Calorias", f"{r.get('cal_carbos', 0)} kcal")
    pdf.campo_doble("Grasas", f"{r.get('grasas_g', 0)} g",
                     "Calorias", f"{r.get('cal_grasas', 0)} kcal")
    pdf.ln(1)

    pdf.subseccion("Distribucion Porcentual")
    pdf.campo_doble("Proteina", f"{r.get('pct_proteina', 0)}%",
                     "Carbohidratos", f"{r.get('pct_carbos', 0)}%")
    pdf.campo("Grasas", f"{r.get('pct_grasas', 0)}%")
    pdf.ln(2)

    # =========================================================
    # 5. EVALUACION DE RIESGOS
    # =========================================================
    pdf.seccion_titulo("5", "Evaluacion de Riesgos")

    riesgo_meta = r.get("riesgo_metabolico", "Bajo")
    riesgo_nutri = r.get("riesgo_nutricional", "Bajo")

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NutricionReport.COLOR_GRIS)
    pdf.cell(65, 5, "Riesgo metabolico:")
    pdf.riesgo_badge(riesgo_meta)
    pdf.ln(1)

    pdf.set_font("Helvetica", "B", 9)
    pdf.set_text_color(*NutricionReport.COLOR_GRIS)
    pdf.cell(65, 5, "Riesgo nutricional:")
    pdf.riesgo_badge(riesgo_nutri)
    pdf.ln(4)

    # =========================================================
    # 6. ALERTAS CLINICAS
    # =========================================================
    alertas = r.get("alertas", [])
    if alertas:
        pdf.seccion_titulo("6", "Alertas Clinicas (Motor de Inferencia)")
        for i, alerta in enumerate(alertas, 1):
            pdf.alerta_item(f"{i}. {alerta}")
        pdf.ln(1)
    else:
        pdf.seccion_titulo("6", "Alertas Clinicas (Motor de Inferencia)")
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*NutricionReport.COLOR_VERDE)
        pdf.cell(0, 5, "No se identificaron alertas clinicas para este perfil.",
                 new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)

    # =========================================================
    # 7. RECOMENDACIONES PERSONALIZADAS
    # =========================================================
    recomendaciones = r.get("recomendaciones", [])
    pdf.seccion_titulo("7", "Recomendaciones Personalizadas")
    if recomendaciones:
        for i, rec in enumerate(recomendaciones, 1):
            pdf.recomendacion_item(i, rec)
    else:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*NutricionReport.COLOR_GRIS)
        pdf.cell(0, 5, "Siga las indicaciones generales del plan nutricional.",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # =========================================================
    # 8. NOTA CLINICA DEL SISTEMA EXPERTO
    # =========================================================
    nota = r.get("nota_clinica", "")
    pdf.seccion_titulo("8", "Nota Clinica del Sistema Experto")
    if nota:
        pdf.nota_clinica_block(nota)
    else:
        pdf.set_font("Helvetica", "I", 9)
        pdf.set_text_color(*NutricionReport.COLOR_GRIS)
        pdf.cell(0, 5, "No se genero nota clinica adicional.",
                 new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)

    # =========================================================
    # 9. TRAZA DE INFERENCIA (MYCIN)
    # =========================================================
    explicaciones = r.get("explicaciones", [])
    pdf.seccion_titulo("9", "Trazabilidad de Inferencia (MYCIN)")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*NutricionReport.COLOR_GRIS)
    pdf.multi_cell(0, 4,
        "Cada regla muestra: ID | Descripcion | Conclusion | Factor de Certeza (CF). "
        "El CF indica la confianza del sistema en esa inferencia (1.0 = maxima certeza).")
    pdf.ln(2)

    if explicaciones:
        for traza in explicaciones:
            pdf.traza_item(traza)
    else:
        pdf.set_font("Helvetica", "I", 8)
        pdf.set_text_color(*NutricionReport.COLOR_GRIS)
        pdf.cell(0, 5, "No hay trazas de inferencia disponibles.",
                 new_x="LMARGIN", new_y="NEXT")

    # =========================================================
    # PIE DE PAGINA FINAL
    # =========================================================
    pdf.ln(6)
    pdf.set_draw_color(*NutricionReport.COLOR_PRINCIPAL)
    pdf.set_line_width(0.5)
    pdf.line(10, pdf.get_y(), 200, pdf.get_y())
    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_text_color(*NutricionReport.COLOR_PRINCIPAL)
    pdf.cell(0, 5, "Generado por NutriExpert - IA Experta Nutricional",
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(*NutricionReport.COLOR_GRIS)
    pdf.cell(0, 4, datetime.now().strftime("Fecha de generacion: %d/%m/%Y %H:%M"),
             align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 4,
             "Este documento es confidencial. Uso exclusivo del profesional de nutricion.",
             align="C", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())
