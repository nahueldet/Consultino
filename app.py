import requests
import statistics

def tasar_producto_usado(query):
    # API pública de MercadoLibre para Argentina (MLA), filtrando por "usado"
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={query}&condition=used&limit=50"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except requests.exceptions.RequestException as e:
        return f"Error en la conexión: {e}"

    resultados = datos.get("results", [])
    
    if not resultados:
        return "No se encontraron publicaciones para este producto."

    # Extraer todos los precios
    precios = [item["price"] for item in resultados]
    
    # Ordenar precios para eliminar valores atípicos (descartamos el 15% inferior y superior)
    precios.sort()
    corte = int(len(precios) * 0.15) 
    precios_limpios = precios[corte:-corte] if corte > 0 else precios

    # Cálculos estadísticos
    precio_min = min(precios_limpios)
    precio_max = max(precios_limpios)
    precio_promedio = statistics.mean(precios_limpios)
    precio_mediana = statistics.median(precios_limpios) # La mediana es el valor más realista

    return {
        "producto": query,
        "muestra_analizada": len(precios_limpios),
        "precio_minimo": round(precio_min, 2),
        "precio_maximo": round(precio_max, 2),
        "precio_promedio": round(precio_promedio, 2),
        "precio_sugerido": round(precio_mediana, 2) 
    }

# Prueba del script
busqueda = "iPhone 13 128gb"
resultado = tasar_producto_usado(busqueda)

print(f"--- Tasación de {resultado['producto']} (Usado) ---")
print(f"Muestra analizada: {resultado['muestra_analizada']} publicaciones")
print(f"Precio Mínimo: ${resultado['precio_minimo']:,.2f}")
print(f"Precio Máximo: ${resultado['precio_maximo']:,.2f}")
print(f"Precio Promedio: ${resultado['precio_promedio']:,.2f}")
print(f"Valor Sugerido de Venta: ${resultado['precio_sugerido']:,.2f}")
