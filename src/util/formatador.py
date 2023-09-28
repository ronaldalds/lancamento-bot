import re
from datetime import datetime, timedelta

def formatar_data(data) -> str:
    try:
        return data.strftime("%d%m%Y")
    except:
        if (type(data) == float) or (type(data) == int):
            data = datetime(1899, 12, 30) + timedelta(days=int(data))
            return data.strftime("%d%m%Y")
        else:
            # regex data
            df = re.compile("([0-9]{2,4})[-]?[/]?([0-9]{2})[-]?[/]?([0-9]{2,4})")
            data = df.findall(data)[0]
            if len(data[2]) == 2:
                return f"{data[2]}{data[1]}{data[0]}"
            
            return f"{data[0]}{data[1]}{data[2]}"

def formatar_valor(multa) -> str:
    if multa >= 0:
        return f"{float(multa):.2f}".replace(".", ",")
    else:
        return "0"
