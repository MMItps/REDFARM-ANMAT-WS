import json


filter_cuit = lambda value : value if value.get('fecha_baja', None) else None

def search_list_cuit(list_cuit, datos):
    bajas = []
    for cuit in list_cuit:
        result_cuit = datos.get(cuit, None)
        if result_cuit:
            bajas.append(filter_cuit(result_cuit))
    
    return list(filter(None,bajas))

list_cuits = ["30717231186", "30644029162", "30714905658", "30716962225", "27266740056"]

with open("result.json", "r", encoding="utf-8") as f:
    datos = json.load(f)

    p = search_list_cuit(list_cuits, datos)

    print(len(p))