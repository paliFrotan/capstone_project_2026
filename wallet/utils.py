from decimal import Decimal, InvalidOperation

def parse_amount(value):
    try:
        if value is not None and isinstance(value, str):
            value = value.strip()

            # Case 1: whole number (e.g., "34")
            if value.isdigit():
                return int(value) * 100

            # Case 2: decimal number (e.g., "34.56")
            if value.count('.') == 1 and value.replace('.', '').isdigit():
                pounds, pence = value.split('.')

                if len(pence) == 1:
                    pence += '0'
                elif len(pence) > 2:
                    pence = pence[:2]

                return int(pounds) * 100 + int(pence)

        # Fallback: Decimal
        dec = Decimal(value)
        return int(dec * 100)

    except (InvalidOperation, TypeError, ValueError):
        return None
