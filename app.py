import streamlit as st
import requests
import statistics

def tasar_producto_usado(query):
    url = f"https://api.mercadolibre.com/sites/MLA/search?q={query}&condition=used&limit=50"
    
    try:
        respuesta = requests.get(url)
        respuesta.raise_for_status()
        datos = respuesta.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"Error de conexión con el mercado: {e}"}

    resultados = datos.get("results", [])
    
    if not resultados:
        return {"error": "No se encontraron publicaciones de este producto usado."}

    precios = [item["price"] for item in resultados if item.get("price")]
    if not precios:
        return {"error": "No se pudieron extraer los precios."}
        
    precios.sort()
    corte = int(len(precios) * 0.15) 
    precios_limpios = precios[corte:-corte] if corte > 0 else precios

    return {
        "producto": query,
        "muestra": len(precios_limpios),
        "minimo": min(precios_limpios),
        "maximo": max(precios_limpios),
        "promedio": statistics.mean(precios_limpios),
        "sugerido": statistics.median(precios_limpios)
    }

# Configuración de la página
st.set_page_config(page_title="Tasador Inteligente", page_icon="🔍", layout="centered")

st.title("🔍 Tasador Inteligente de Mercado")
st.markdown("Descubrí a qué precio vender o comprar un artículo usado en Argentina basándote en publicaciones reales.")

# Entrada del usuario
producto = st.text_input("¿Qué producto querés tasar?", placeholder="Ej. iPhone 13 128gb")

if st.button("Calcular Precio Real", type="primary"):
    if producto:
        with st.spinner("Analizando el mercado en tiempo real..."):
            resultado = tasar_producto_usado(producto)
            
            # Manejo de errores limpio dentro de Streamlit
            if "error" in resultado:
                st.error(resultado["error"])
            else:
                st.success(f"Análisis basado en **{resultado['muestra']}** publicaciones verificadas.")
                
                # Diseño de tarjetas (métricas)
                st.header(f"Valor sugerido: ${resultado['sugerido']:,.0f}")
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric(label="Mínimo de mercado", value=f"${resultado['minimo']:,.0f}")
                with col2:
                    st.metric(label="Promedio", value=f"${resultado['promedio']:,.0f}")
                with col3:
                    st.metric(label="Máximo de mercado", value=f"${resultado['maximo']:,.0f}")
                    
                st.info("💡 **Dato:** El valor sugerido utiliza la mediana estadística para ignorar accesorios baratos camuflados o precios irreales.")
    else:
        st.warning("Por favor, escribí el nombre de un producto para comenzar.")
