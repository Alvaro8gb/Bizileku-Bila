# Bizileku Bila: En busca de un lugar para vivir en Euskadi.
   [![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]()

<div>
    <img src="static/logo.svg" alt="Project Logo" style="height: 200px; vertical-align: middle;" />

</div>




``Bizileku Bila`` surge como una herramienta que facilita la búsqueda del municipio ideal en Euskadi a través de las fuentes de datos abiertos del País Vasco: [APIs](https://opendata.euskadi.eus/apis/-/apis-open-data)



## Características

1. **Encuentra tu municipio ideal**: Permite encontrar dado un conjunto de indicadores de interes, el municipio que mejor se ajuste a sus preferencias.
   
2. **Explora los municipios**: Accede a todos los indicadores de un municipio, junto con su localización y datos adicionales de Wikidata.

## Instalación

1. Clona el repositorio o descarga el código fuente.
2. Instala las dependencias de Python necesarias:

```bash
pip install -r requirements.txt
```

## Ejecutar la Aplicación

Para ejecutar la aplicación de Streamlit, navega al directorio del proyecto y ejecuta el siguiente comando:

```bash
streamlit run app.py
```

Esto iniciará el servidor de Streamlit y abrirá la aplicación en tu navegador predeterminado.

## Estructura de la Aplicación

### Módulos de funcionalidad (Frontend):
   Estos archivos y carpetas están relacionados con la interfaz de usuario o la presentación de datos:
   - **visualization**: Contiene scripts o módulos para la visualización de datos (gráficos, diagramas, etc.).
   - **static**: Archivos estáticos como CSS, JavaScript e imágenes que son parte de la interfaz gráfica o front-end de la aplicación.

### Módulos de funcionalidad (Backend):
   Estos archivos manejan la lógica de negocio, acceso a datos y las operaciones de backend:
   - **apiManager.py**: Gestiona interacciones con APIs externas.
   - **app.py**: Archivo principal que ejecuta la aplicación backend.
   - **globals.py**: Configuraciones globales utilizadas en el backend.
   - **linkedData.py**: Gestión de datos enlazados (linked data) utilizando tecnologías como RDF y SPARQL.
   - **models.py**: Define los modelos de datos y objetos de negocio del backend.
   - **resourceManager.py**: Administra recursos del sistema (datos, APIs, archivos).
   - **score.py**: Lógica de cálculo de indicadores.
   - **sparql**: Consultas SPARQL para interactuar con bases de datos RDF.
   - **wikiData.py**: Gestión de la interacción con Wikidata para obtener y procesar información.

### 3. **Metaarchivos de instalación y configuración**:
   Estos archivos son usados para la instalación, configuración y documentación del proyecto:
   - **LICENSE**: Especifica los términos de licencia del proyecto.
   - **Makefile**: Automatiza tareas como la instalación de dependencias y ejecución de pruebas.
   - **README.md**: Proporciona información sobre el proyecto, cómo instalarlo y cómo usarlo.
   - **requirements.txt**: Lista de dependencias de Python necesarias para el proyecto.
   - **pruebas**: Carpeta que contiene pruebas unitarias o de integración para asegurar el correcto funcionamiento.

## Datos

En el desarrollo de este proyecto se han utilizado los siguientes conjuntos de datos abiertos:

- **Portal de Datos Abiertos de Euskadi**:
  - [**SPARQL Endpoint**](https://api.euskadi.eus/sparql): Permite realizar consultas a datos almacenados en formato RDF mediante el lenguaje SPARQL.
  - [**Udalmap API**](https://opendata.euskadi.eus/api-udalmap/?api=udalmap): Sistema de Información Municipal que ofrece detalles sobre la realidad de los municipios de la C.A. de Euskadi.

- [**Wikidata**](https://www.wikidata.org/): Base de conocimientos libre y abierta que se nutre de datos de diversos proyectos de Wikimedia, portales de datos abiertos, y bases de datos como DBpedia y OpenStreetMap, así como de contribuciones de usuarios y organizaciones internacionales. 

## Licencia

Este proyecto está bajo la licencia [GNU](LICENSE).

## Reporte 

Para más información sobre el proyecto leer [reporte](report.pdf).
## Créditos

- **Fuente de Datos**: [Datos Abiertos de Euskadi](https://opendata.euskadi.eus)
- **Librerías Usadas**: [Streamlit](https://streamlit.io/), [Pandas](https://pandas.pydata.org/), PyDeck, PIL (Pillow)

