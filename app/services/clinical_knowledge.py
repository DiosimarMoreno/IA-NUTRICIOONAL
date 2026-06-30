IMC_CLASIFICACIONES = [
    (0, 16.0, "Delgadez severa"),
    (16.0, 17.0, "Delgadez moderada"),
    (17.0, 18.5, "Delgadez leve"),
    (18.5, 25.0, "Normal"),
    (25.0, 30.0, "Sobrepeso"),
    (30.0, 35.0, "Obesidad tipo I"),
    (35.0, 40.0, "Obesidad tipo II"),
    (40.0, float("inf"), "Obesidad tipo III"),
]

SOMATOTIPO_POR_GRASA_M = [
    (0, 10, "Ectomorfo", "Complexión delgada, metabolismo acelerado, dificultad para ganar peso"),
    (10, 18, "Mesomorfo", "Complexión atlética, buena respuesta muscular, facilidad para definir"),
    (18, 100, "Endomorfo", "Tendencia a acumular grasa, metabolismo lento, facilidad para ganar masa"),
]

SOMATOTIPO_POR_GRASA_F = [
    (0, 18, "Ectomorfo", "Complexión delgada, metabolismo acelerado, dificultad para ganar peso"),
    (18, 28, "Mesomorfo", "Complexión atlética, buena respuesta muscular, facilidad para definir"),
    (28, 100, "Endomorfo", "Tendencia a acumular grasa, metabolismo lento, facilidad para ganar masa"),
]

SOMATOTIPO_POR_IMC = [
    (0, 18.5, "Ectomorfo", "Complexión delgada estimada por IMC bajo"),
    (18.5, 25.0, "Mesomorfo", "Complexión proporcionada estimada por IMC normal"),
    (25.0, float("inf"), "Endomorfo", "Complexión con tendencia a acumular grasa estimada por IMC elevado"),
]


def calcular_imc(peso: float, estatura_cm: float) -> float:
    if estatura_cm <= 0:
        return 0.0
    estatura_m = estatura_cm / 100
    return round(peso / (estatura_m ** 2), 2)


def clasificar_imc(imc: float) -> str:
    for inferior, superior, categoria in IMC_CLASIFICACIONES:
        if inferior <= imc < superior:
            return categoria
    return "No clasificado"


def peso_ideal_devine(estatura_cm: float, sexo: str) -> float:
    if sexo == "M":
        return round(50 + 0.91 * (estatura_cm - 152.4), 2)
    elif sexo == "F":
        return round(45.5 + 0.91 * (estatura_cm - 152.4), 2)
    else:
        masculino = 50 + 0.91 * (estatura_cm - 152.4)
        femenino = 45.5 + 0.91 * (estatura_cm - 152.4)
        return round((masculino + femenino) / 2, 2)


def rango_saludable(estatura_cm: float) -> tuple[float, float]:
    if estatura_cm <= 0:
        return (0.0, 0.0)
    estatura_m = estatura_cm / 100
    minimo = round(18.5 * (estatura_m ** 2), 1)
    maximo = round(24.99 * (estatura_m ** 2), 1)
    return (minimo, maximo)


def somatotipo_por_grasa(pc_grasa: float, sexo: str) -> tuple[str, str]:
    tabla = SOMATOTIPO_POR_GRASA_M if sexo == "M" else SOMATOTIPO_POR_GRASA_F
    for inferior, superior, nombre, desc in tabla:
        if inferior <= pc_grasa < superior:
            return (nombre, desc)
    return ("No determinado", "No se pudo determinar el somatotipo")


def somatotipo_por_imc(imc: float) -> tuple[str, str]:
    for inferior, superior, nombre, desc in SOMATOTIPO_POR_IMC:
        if inferior <= imc < superior:
            return (nombre, desc)
    return ("No determinado", "No se pudo determinar el somatotipo")


def estimar_grasa_deurenberg(imc: float, edad: int, sexo: str) -> float:
    if sexo == "M":
        return round(1.20 * imc + 0.23 * edad - 10.8 * 1 - 5.4, 1)
    elif sexo == "F":
        return round(1.20 * imc + 0.23 * edad - 10.8 * 0 - 5.4, 1)
    else:
        m = 1.20 * imc + 0.23 * edad - 10.8 * 1 - 5.4
        f = 1.20 * imc + 0.23 * edad - 10.8 * 0 - 5.4
        return round((m + f) / 2, 1)


def masa_grasa_kg(peso: float, pc_grasa: float) -> float:
    return round(peso * pc_grasa / 100, 2)


def masa_magra_kg(peso: float, masa_grasa_kg: float) -> float:
    return round(peso - masa_grasa_kg, 2)


def agua_watson(peso: float, estatura_cm: float, edad: int, sexo: str) -> float:
    if sexo == "M":
        return round(2.447 - 0.09156 * edad + 0.1074 * estatura_cm + 0.3362 * peso, 1)
    elif sexo == "F":
        return round(-2.097 + 0.1069 * estatura_cm + 0.2466 * peso, 1)
    else:
        m = 2.447 - 0.09156 * edad + 0.1074 * estatura_cm + 0.3362 * peso
        f = -2.097 + 0.1069 * estatura_cm + 0.2466 * peso
        return round((m + f) / 2, 1)
