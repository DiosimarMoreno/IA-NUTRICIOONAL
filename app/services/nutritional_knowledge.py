FACTORES_ACTIVIDAD: dict[str, tuple[float, str]] = {
    "sedentario": (1.2, "Sedentario"),
    "ligera": (1.375, "Actividad ligera"),
    "moderado": (1.55, "Moderadamente activo"),
    "muy_activo": (1.725, "Muy activo"),
    "extremo": (1.9, "Extremadamente activo"),
}

OBJETIVOS: dict[str, tuple[str, float, float, float]] = {
    "hipertrofia": ("Hipertrofia Muscular", 1.15, 2.0, 0.50),
    "mantenimiento": ("Mantenimiento", 1.0, 1.8, 0.50),
    "perdida": ("Pérdida de Grasa", 0.80, 2.2, 0.35),
}

LIMITES_CALORICOS = {"M": 1200, "F": 1000}
CALORIAS_POR_GRAMO = {"proteina": 4, "carbos": 4, "grasas": 9}


def tmb_mifflin_stjeor(peso: float, estatura_cm: float, edad: int, sexo: str) -> float:
    if sexo == "M":
        return 10 * peso + 6.25 * estatura_cm - 5 * edad + 5
    elif sexo == "F":
        return 10 * peso + 6.25 * estatura_cm - 5 * edad - 161
    else:
        m = 10 * peso + 6.25 * estatura_cm - 5 * edad + 5
        f = 10 * peso + 6.25 * estatura_cm - 5 * edad - 161
        return (m + f) / 2


def factor_actividad(nivel: str) -> tuple[float, str]:
    return FACTORES_ACTIVIDAD.get(nivel, (1.2, "Sedentario"))


def calorias_objetivo(tdee: float, objetivo: str) -> tuple[int, str]:
    config = OBJETIVOS.get(objetivo, OBJETIVOS["mantenimiento"])
    etiqueta = config[0]
    multiplo = config[1]
    return (int(round(tdee * multiplo)), etiqueta)


def distribuir_macros(
    cal_objetivo: int, objetivo: str, peso: float, sexo: str = "M"
) -> dict:
    config = OBJETIVOS.get(objetivo, OBJETIVOS["mantenimiento"])
    etiqueta = config[0]
    prot_g_kg = config[2]
    pct_carbos = config[3]

    proteina_g = round(prot_g_kg * peso, 1)
    cal_proteina = int(proteina_g * CALORIAS_POR_GRAMO["proteina"])
    pct_proteina = round(cal_proteina / cal_objetivo * 100) if cal_objetivo > 0 else 0

    carbos_g = round((cal_objetivo * pct_carbos) / CALORIAS_POR_GRAMO["carbos"], 1)
    cal_carbos = int(carbos_g * CALORIAS_POR_GRAMO["carbos"])
    pct_carbos_real = round(cal_carbos / cal_objetivo * 100) if cal_objetivo > 0 else 0

    pct_grasas = max(0, 100 - pct_proteina - pct_carbos_real)
    grasas_g = round((cal_objetivo * (pct_grasas / 100)) / CALORIAS_POR_GRAMO["grasas"], 1)
    cal_grasas = int(grasas_g * CALORIAS_POR_GRAMO["grasas"])

    return {
        "objetivo_etiqueta": etiqueta,
        "proteina_g": proteina_g,
        "carbos_g": carbos_g,
        "grasas_g": grasas_g,
        "pct_proteina": pct_proteina,
        "pct_carbos": pct_carbos_real,
        "pct_grasas": pct_grasas,
        "cal_proteina": cal_proteina,
        "cal_carbos": cal_carbos,
        "cal_grasas": cal_grasas,
    }
