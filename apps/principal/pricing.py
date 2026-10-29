from decimal import Decimal


PRECIO_PAQUETE = {
    "xs": Decimal("3000"),
    "s": Decimal("3900"),
    "m": Decimal("4800"),
    "l": Decimal("5700"),
    "xl": Decimal("6800"),
}

RECARGO_REGION = {
    "1": Decimal("2450"),
    "2": Decimal("2000"),
    "3": Decimal("1600"),
    "4": Decimal("1250"),
    "5": Decimal("950"),
    "6": Decimal("700"),
    "7": Decimal("500"),
    "8": Decimal("700"),
    "9": Decimal("950"),
    "10": Decimal("1250"),
    "11": Decimal("1600"),
    "12": Decimal("2000"),
    "13": Decimal("2500"),
    "14": Decimal("3000"),
    "15": Decimal("3550"),
    "16": Decimal("4150"),
}

RECARGO_EXPRESS = Decimal("500")


def calcular_costo_envio(tipo_paquete, region, tipo_envio):
    try:
        total = PRECIO_PAQUETE[tipo_paquete] + RECARGO_REGION[region]
    except KeyError as error:
        raise ValueError("El tamaño de paquete o la región no es válida.") from error

    if tipo_envio == "express":
        total += RECARGO_EXPRESS
    elif tipo_envio != "normal":
        raise ValueError("El tipo de envío no es válido.")

    return total
