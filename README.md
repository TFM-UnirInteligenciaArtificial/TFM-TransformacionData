# 📂 ETL: Extracción y Transformación de Logs (XML a CSV)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![ETL](https://img.shields.io/badge/Pipeline-ETL-orange?style=for-the-badge)
![Data](https://img.shields.io/badge/Data-Preprocessing-green?style=for-the-badge)

> **Propósito:** Este repositorio contiene las herramientas de **Ingeniería de Datos** necesarias para procesar logs brutos de Windows (*Event Viewer XML*) y convertirlos en datasets estructurados (CSV) listos para el entrenamiento de modelos de Machine Learning.

---

## 🚀 Tecnologías Utilizadas

El proyecto utiliza un enfoque nativo y eficiente para el manejo de grandes volúmenes de datos sin dependencias pesadas.

| Tecnología | Icono | Función Principal |
| :--- | :---: | :--- |
| **Python 3** | ![Python](https://img.shields.io/badge/-Python-3776AB?logo=python&logoColor=white) | Core del scripting y lógica de transformación. |
| **XML (ElementTree)** | ![XML](https://img.shields.io/badge/-XML_Parsing-grey) | Parsing por streaming (`iterparse`) para bajo consumo de memoria. |
| **CSV (Standard Lib)** | ![CSV](https://img.shields.io/badge/-CSV-green) | Generación de datasets estructurados para BigQuery/Pandas. |

---

## ⚙️ Funcionalidades del Script

El script principal, `scripts/evtx_xml_to_csv.py`, es un motor de transformación diseñado para preparar los datos que alimentarán modelos como **Random Forest** y **K-Means**.

* ✅ **Parsing por Streaming:** Procesa archivos XML de gigabytes línea por línea sin saturar la memoria RAM.
* ✅ **Modo Dual:** Funciona tanto para archivos individuales como para directorios completos (procesamiento por lotes).
* ✅ **Estandarización:** Normaliza timestamps y campos clave (`ProviderName`, `EventID`, `Level`, `Message`) para su ingesta en Vertex AI.

---

## 📖 Guía de Uso

### 1. Procesar un archivo individual
Ideal para pruebas rápidas o actualizaciones incrementales de un servidor específico.

```bash
python scripts/evtx_xml_to_csv.py -i "Data/Aplicacion_09112025.xml" -o "evtx_csv_output/Aplicacion.csv"