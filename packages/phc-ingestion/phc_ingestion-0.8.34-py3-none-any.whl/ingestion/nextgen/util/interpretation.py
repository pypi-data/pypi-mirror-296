from logging import Logger


def map_interpretation(status: str, log: Logger):
    """
    Map interpretation for structural and copy number variants
    """
    if status == "Pathogenic":
        return "Pathogenic"
    elif "VUS" in status:
        return "Uncertain significance"
    else:
        log.error(f"Failed to resolve interpretation: {status}")
        return ""


def map_vendsig(vendsig: str) -> str:
    """
    Map vendor significance for short variants
    """
    if vendsig in ["Pathogenic"]:
        return "VENDSIG=Pathogenic"
    elif vendsig in ["Likely Pathogenic", "LikelyPathogenic"]:
        return "VENDSIG=Likely pathogenic"
    elif vendsig in ["VUS"]:
        return "VENDSIG=Uncertain significance"
    else:
        raise RuntimeError(f"Unable to map vendor significance: {vendsig}")
