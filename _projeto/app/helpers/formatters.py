from datetime import datetime

def format_brl_price(value: float):
    if value is None:
        return ""
    formatted = f"{value:,.2f}"
    return formatted.replace(",", "X").replace(".", ",").replace("X", ".")

def format_brl_date(value: datetime):
    if not value:
        return ""
    return value.strftime("%d/%m/%Y %H:%M")