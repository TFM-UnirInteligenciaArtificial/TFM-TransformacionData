# 📂 ETL: Extracción y Transformación de Logs (XML a CSV)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![ETL](https://img.shields.io/badge/Pipeline-ETL-orange?style=for-the-badge)
![Data](https://img.shields.io/badge/Data-Preprocessing-green?style=for-the-badge)

> **Propósito:** Este repositorio contiene las herramientas de **Ingeniería de Datos** necesarias para procesar logs brutos de Windows (_Event Viewer XML_) y convertirlos en datasets estructurados (CSV) listos para el entrenamiento de modelos de Machine Learning.

---

## 🚀 Tecnologías Utilizadas

El proyecto utiliza un enfoque nativo y eficiente para el manejo de grandes volúmenes de datos sin dependencias pesadas.

| Tecnología             |                                       Icono                                        | Función Principal                                                 |
| :--------------------- | :--------------------------------------------------------------------------------: | :---------------------------------------------------------------- |
| **Python 3**           | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Core del scripting y lógica de transformación.                    |
| **XML (ElementTree)**  |               ![XML](https://img.shields.io/badge/-XML_Parsing-grey)               | Parsing por streaming (`iterparse`) para bajo consumo de memoria. |
| **CSV (Standard Lib)** |                  ![CSV](https://img.shields.io/badge/-CSV-green)                   | Generación de datasets estructurados para BigQuery/Pandas.        |

---

## ⚙️ Funcionalidades del Script

El script principal, `scripts/evtx_xml_to_csv.py`, es un motor de transformación diseñado para preparar los datos que alimentarán modelos como **Random Forest** y **K-Means**.

- ✅ **Parsing por Streaming:** Procesa archivos XML de gigabytes línea por línea sin saturar la memoria RAM.
- ✅ **Modo Dual:** Funciona tanto para archivos individuales como para directorios completos (procesamiento por lotes).
- ✅ **Estandarización:** Normaliza timestamps y campos clave (`ProviderName`, `EventID`, `Level`, `Message`) para su ingesta en Vertex AI.

---

## 📖 Guía de Uso

---

## 📋 0. Extracción de Datos (Pre-requisito)

Antes de ejecutar el script de conversión, necesitas exportar los logs desde el servidor Windows. Puedes hacerlo de dos formas:

### 🔹 Opción A: Manual (Interfaz Gráfica)

Ideal para extracciones puntuales o si no tienes permisos de administrador en consola.

1. Presiona `Win + R`, escribe **`eventvwr.msc`** y pulsa Enter.
2. Navega a **Registros de Windows** (Windows Logs) > **Aplicación** (o Seguridad/Sistema).
3. En el panel derecho, haz clic en **"Guardar todos los eventos como..."** (_Save All Events As..._).
4. **¡Importante!** En el desplegable "Tipo", selecciona **XML (\*.xml)** (por defecto viene .evtx).
5. Guarda el archivo en la carpeta `Data/` de este repositorio.

### 🔹 Opción B: Línea de Comandos (CMD / PowerShell)

Ideal para automatización o servidores Core. Usa la herramienta nativa `wevtutil`.

```batch
:: Sintaxis básica: wevtutil qe <NombreLog> /f:xml > <RutaSalida>

:: 1. Exportar Logs de Aplicación
wevtutil qe Application /f:xml > "Data/Application_Logs.xml"

:: 2. Exportar Logs de Seguridad
wevtutil qe Security /f:xml > "Data/Security_Logs.xml"

:: 3. Exportar Logs de Sistema
wevtutil qe System /f:xml > "Data/System_Logs.xml"
```

### 1. Procesar un archivo individual

Ideal para pruebas rápidas o actualizaciones incrementales de un servidor específico.

```bash
python scripts/evtx_xml_to_csv.py -i "Data/Aplicacion_09112025.xml" -o "evtx_csv_output/Aplicacion.csv"
```
