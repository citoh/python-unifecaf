def format_brl_price(value: float):
    if value is None:
        return ""
    formatted = f"{value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")