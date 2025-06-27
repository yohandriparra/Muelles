import traceback
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from Utilidades import iniciar_driver, iniciarDriver
from selenium.webdriver.common.by import By
from Utilidades import waitTo
from pathlib import Path
import pdfplumber
import time
import os

# Diccionario centralizado de URLs
URLS = {
    "Cartagena": "https://clientes.compas.com.co/COMPAS-Online/Situaci%C3%B3n-Portuaria-COMPAS/COMPAS-Cartagena",
    "Barranquilla": "https://clientes.compas.com.co/COMPAS-Online/Situaci%C3%B3n-Portuaria-COMPAS/COMPAS-Barranquilla",
    "Buenaventura": "https://clientes.compas.com.co/COMPAS-Online/Situaci%C3%B3n-Portuaria-COMPAS/COMPAS-Buenaventura",
    "Tolu": "https://clientes.compas.com.co/COMPAS-Online/Situaci%C3%B3n-Portuaria-COMPAS/COMPAS-Tol%C3%BA",
    "AguaDulce_compas": "https://clientes.compas.com.co/COMPAS-Online/Situaci%C3%B3n-Portuaria-COMPAS/BOSCOAL-Buenaventura",
    "Portuaria": "https://portaln4.sprbun.com/portal/#/situacion-portuaria/muelle",
    "AguaDulce_Industrial": "https://www.puertoaguadulce.com/programacion-de-buques/"
}

# FUNCION PARA EXTRAER LOS PUERTOS
def extraer_tabla(driver, selectores, campos, nombre_tabla):
    print(f"Iniciando extracción de la tabla: {nombre_tabla}")
    datos = []
    tabla = None

    for tipo, valor in selectores:
        print(f"Buscando tabla con selector: {tipo}, valor: {valor}")
        tabla = waitTo(driver, (tipo, valor), time=5)
        if tabla:
            print(f"Tabla localizada para {nombre_tabla}")
            break

    if not tabla:
        print(f"[WARN] No se encontró la tabla para {nombre_tabla}")
        return [{"mensaje": f"No se encontró la tabla de {nombre_tabla}"}]

    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", tabla)
    time.sleep(2)

    try:
        tbody = tabla.find_element(By.TAG_NAME, "tbody")
        filas = tbody.find_elements(By.TAG_NAME, "tr")
        filas_procesadas = 0

        for fila in filas:
            celdas = fila.find_elements(By.TAG_NAME, "td")
            if not celdas or not celdas[0].text.strip():
                continue
            if celdas[0].text.strip().lower() == "no records to display":
                print(f"No hay registros para mostrar en {nombre_tabla}")
                return [{"mensaje": "No hay registros para mostrar"}]
            registro = {campo: celdas[i].text.strip() if i < len(celdas) else "" for i, campo in enumerate(campos)}
            datos.append(registro)
            filas_procesadas += 1

        print(f"{filas_procesadas} filas procesadas en {nombre_tabla}")

        if filas_procesadas == 0:
            return [{"mensaje": "No hay registros para mostrar"}]

        return datos

    except Exception as e:
        print(f"[ERROR] Error al procesar la tabla de {nombre_tabla}: {str(e)}")
        return [{"mensaje": f"Error al procesar la tabla de {nombre_tabla}: {traceback.format_exc()}"}]

# Función para Cartagena
def Muelle_cartagena():
    print("[INFO] Iniciando extracción de datos para: Cartagena")
    url = URLS["Cartagena"]
    driver = iniciar_driver(True)
    resultado = {"anunciadas": [], "atracadas": [], "Zarpadas": []}

    try:
        driver.get(url)
        print(f"[INFO] Accediendo a URL: {url}")
        time.sleep(2)

        resultado["anunciadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAnunciadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAnunciadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAnunciadas')]"),
        ], ["Buque", "NroViaje", "Eta", "Destino", "Agente", "Linea"], "anunciadas")

        resultado["atracadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAtracadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAtracadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAtracadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "ETD", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea", "Muelle"], "atracadas")

        resultado["Zarpadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasZarpadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasZarpadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasZarpadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "FechaZarpadas", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea"], "zarpadas")
        print("[INFO] Extracción completada para Cartagena")
    except Exception as e:
        print(f"[ERROR] Fallo en Cartagena: {str(e)}")
        resultado = {traceback.format_exc()}
    finally:
        driver.quit()
        print("[INFO] Sesión cerrada para Cartagena")
    return resultado

# Función para Barranquilla
def Muelle_barranquilla():
    print("[INFO] Iniciando extracción de datos para: Barranquilla")
    url = URLS["Barranquilla"]
    driver = iniciar_driver(True)
    resultado = {"anunciadas": [], "atracadas": [], "Zarpadas": []}

    try:
        driver.get(url)
        print(f"[INFO] Accediendo a URL: {url}")
        time.sleep(2)

        resultado["anunciadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAnunciadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAnunciadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAnunciadas')]"),
        ], ["Buque", "NroViaje", "Eta", "Destino", "Agente", "Linea"], "anunciadas")

        resultado["atracadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAtracadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAtracadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAtracadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "ETD", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea", "Muelle"], "atracadas")

        resultado["Zarpadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasZarpadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasZarpadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasZarpadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "FechaZarpadas", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea"], "zarpadas")
        print("[INFO] Extracción completada para Barranquilla")
    except Exception as e:
        print(f"[ERROR] Fallo en Barranquilla: {str(e)}")
        resultado = {traceback.format_exc()}
    finally:
        driver.quit()
        print("[INFO] Sesión cerrada para Barranquilla")
    return resultado

# Función para Buenaventura
def Muelle_buenaventura():
    print("[INFO] Iniciando extracción de datos para: Buenaventura")
    url = URLS["Buenaventura"]
    driver = iniciar_driver(True)
    resultado = {"anunciadas": [], "atracadas": [], "Zarpadas": []}

    try:
        driver.get(url)
        print(f"[INFO] Accediendo a URL: {url}")
        time.sleep(2)

        resultado["anunciadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAnunciadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAnunciadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAnunciadas')]"),
        ], ["Buque", "NroViaje", "Eta", "Destino", "Agente", "Linea"], "anunciadas")

        resultado["atracadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAtracadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAtracadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAtracadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "ETD", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea", "Muelle"], "atracadas")

        resultado["Zarpadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasZarpadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasZarpadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasZarpadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "FechaZarpadas", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea"], "zarpadas")
        print("[INFO] Extracción completada para Buenaventura")
    except Exception as e:
        print(f"[ERROR] Fallo en Buenaventura: {str(e)}")
        resultado = {traceback.format_exc()}
    finally:
        driver.quit()
        print("[INFO] Sesión cerrada para Buenaventura")
    return resultado

# Función para Tolu
def Muelle_tolu():
    print("[INFO] Iniciando extracción de datos para: Tolu")
    url = URLS["Tolu"]
    driver = iniciar_driver(True)
    resultado = {"anunciadas": [], "atracadas": [], "Zarpadas": []}

    try:
        driver.get(url)
        print(f"[INFO] Accediendo a URL: {url}")
        time.sleep(2)

        resultado["anunciadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAnunciadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAnunciadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAnunciadas')]"),
        ], ["Buque", "NroViaje", "Eta", "Destino", "Agente", "Linea"], "anunciadas")

        resultado["atracadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAtracadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAtracadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAtracadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "ETD", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea", "Muelle"], "atracadas")

        resultado["Zarpadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasZarpadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasZarpadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasZarpadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "FechaZarpadas", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea"], "zarpadas")
        print("[INFO] Extracción completada para Tolu")
    except Exception as e:
        print(f"[ERROR] Fallo en Tolu: {str(e)}")
        resultado = {traceback.format_exc()}
    finally:
        driver.quit()
        print("[INFO] Sesión cerrada para Tolu")
    return resultado

# Función para AguaDulce
def Muelle_aguadulce():
    print("Iniciando extracción de datos para: AguaDulce_compas")
    url = URLS["AguaDulce_compas"]
    driver = iniciar_driver(True)
    resultado = {"anunciadas": [], "atracadas": [], "Zarpadas": []}

    try:
        driver.get(url)
        print(f"Accediendo a URL: {url}")
        time.sleep(2)

        resultado["anunciadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAnunciadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAnunciadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAnunciadas')]"),
        ], ["Buque", "NroViaje", "Eta", "Destino", "Agente", "Linea"], "anunciadas")

        resultado["atracadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasAtracadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasAtracadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasAtracadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "ETD", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea", "Muelle"], "atracadas")

        resultado["Zarpadas"] = extraer_tabla(driver, [
            (By.ID, 'dnn_ctr938_SituacionPortuaria_grillaEscalasZarpadas_ctl00'),
            (By.CSS_SELECTOR, 'table[id*="grillaEscalasZarpadas"]'),
            (By.XPATH, "//table[contains(@id, 'grillaEscalasZarpadas')]"),
        ], ["Buque", "NroViaje", "Fecha_Atraque", "FechaInicioOperacion", "FechaFinOperacion",
            "FechaZarpadas", "Destino", "RegCapitania", "RegAduanero", "Agente", "Linea"], "zarpadas")
        print("Extracción completada para AguaDulce_compas")

    except Exception as e:
        print(f"[ERROR] Fallo en AguaDulce_compas: {str(e)}")
        resultado = {traceback.format_exc()}
    finally:
        driver.quit()
        print("Sesión cerrada para AguaDulce_compas")
    return resultado

# FUNCION PARA EXTRAER LAS TABLAS DEL PDF
def pdf_tablas_a_json(ruta_pdf, salida_json='datos.json'):
    resultados = []
    
    with pdfplumber.open(ruta_pdf) as pdf:
        encabezadoAlmacenado: bool = False
        cabecera = []
        for pagina in pdf.pages:
            # Extraer tablas de la página actual
            tablas = pagina.extract_tables()
            if encabezadoAlmacenado == False:
                tabla = tablas[1]
                encabezados = [col.strip() if col else f"columna_{i}" 
                for i, col in enumerate(tabla[1], 1)]
                cabecera = encabezados
                encabezadoAlmacenado = True

            for tabla in tablas:
                if len(tabla) > 1:  # Asegurarse que tiene encabezados y datos
                    # Tomar la primera fila como encabezados
                    encabezados = [col.strip() if col else f"columna_{i}" 
                    for i, col in enumerate(tabla[1], 1)]
                    
                    # Procesar filas de datos
                    for fila in tabla[2:]:
                        if any(cell for cell in fila):  # Ignorar filas vacías
                            fila_dict = {}
                            for idx, (header, valor) in enumerate(zip(cabecera, fila)):
                                # Limpieza básica de datos
                                valor_limpio = (
                                    valor.strip().replace('\n', ' ') 
                                    if valor and str(valor).strip() 
                                    else None
                                )
                                fila_dict[header] = valor_limpio
                            
                            resultados.append(fila_dict)
    return resultados    
    
# FUNCION PARA SITUACION PORTUARIA
def Muelle_Portuaria():
    url = URLS["Portuaria"]
    driver = iniciar_driver(True)
    
    download_dir = os.path.join(os.getcwd(), "Descargas")
    Path(download_dir).mkdir(parents=True, exist_ok=True)

    params = {'behavior': 'allow', 'downloadPath': download_dir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    resultado = []

    try:
        driver.get(url)
        time.sleep(5)
        
        download = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH , '//*[@id="content"]/div[2]/div/div[2]/div[2]/div/div/ul/li[2]/a')))
        if download:            
            download.click()
            time.sleep(4)

            ruta_pdf = os.path.join(download_dir, "situacion-portuaria.pdf")
            resultado = pdf_tablas_a_json(ruta_pdf)

            # Eliminar el archivo después de procesarlo
            if os.path.exists(ruta_pdf):
                os.remove(ruta_pdf)

    except Exception as e:
        resultado = {traceback.format_exc()}
    finally:
        driver.quit()
        return resultado

# FUNCION PARA AGUADULCE_2
def Consulta_Aguadulce_2():
    url = URLS["AguaDulce_Industrial"]
    driver = iniciarDriver(True)
    resultados = {}

    try:
        driver.get(url)
        time.sleep(3)

        WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'vc_tta-container'))
        )

        pestanas = driver.find_elements(By.CLASS_NAME, 'vc_tta-tab')
        nombres_pestanas = [pestana.text.strip() for pestana in pestanas]

        def extraer_datos_pestana(indice_pestana):
            try:
                if len(pestanas) <= indice_pestana:
                    return None

                pestanas[indice_pestana].click()
                time.sleep(2)

                cuerpo_pestana = driver.find_element(By.CSS_SELECTOR, 'div.vc_tta-panel.vc_active div.vc_tta-panel-body')

                if 'table' not in cuerpo_pestana.get_attribute('innerHTML'):
                    return None

                tabla = cuerpo_pestana.find_element(By.TAG_NAME, 'table')
                filas = tabla.find_elements(By.TAG_NAME, 'tr')

                if not filas:
                    return None

                datos_pestana = []
                for fila in filas:
                    celdas = fila.find_elements(By.TAG_NAME, 'td')
                    if celdas:
                        datos_pestana.append([celda.text.strip() for celda in celdas])
                return datos_pestana

            except Exception as e:
                return None

        for i in range(min(4, len(nombres_pestanas))):
            datos = extraer_datos_pestana(i)
            if datos and len(datos) > 1:
                nombre = nombres_pestanas[i] if i < len(nombres_pestanas) else f"Pestaña {i+1}"
                encabezados = datos[0]
                datos_procesados = [dict(zip(encabezados, fila)) for fila in datos[1:]]
                resultados[nombre] = datos_procesados

    except Exception as e:
        resultados = {"error": str(e)}

    finally:
        driver.quit()
        return resultados