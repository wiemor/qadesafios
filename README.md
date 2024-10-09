# Proyecto de Desafios para QA Automation Engineer

Finalidad: realizar la automaticación de los desafios del servicio RestFul Booker y la app de Booking.

## Arquitectura y Tecnologías

- **Metodología BDD**: Utilice Behave con la finalidad de:

  - Crear escenarios de prueba en un lenguaje natural (Gherkin).
  - Facilita tambien la colaboración entre equipos técnicos y no técnicos.
  - Mantener una trazabilidad clara entre los requisitos del negocio y las pruebas automatizadas.

- **Patrones de Diseño**: Use diversos patrones de diseño para optimizar la estructura y la eficiencia de las pruebas automatizadas. Con la finalidad de aumentar la legibilidad del código y la incorporación de nuevas caracteristicas.

## Herramientas:

- Lenguaje de Programación: Python 3 (requests, coverage, Appium-Python-Client, uiautomator2)
- Postman
- BDD: Behave
- Control de Versiones: Git
- Integración Continua: Jenkins
- Java JDK 11
- Android SDK
- Automatización: Appium

## Configuración y Ejecución

### 0. Establecer variables globales:
```
JAVA_HOME = C:\Program Files\Eclipse Adoptium\jdk-8.0.422.5-hotspot
ANDROID_HOME = C:\Users\[USERNAME]\AppData\Local\Android\Sdk
```
### 1. Configurar el entorno de pruebas:

```
# Clonar repo:

git clone https://github.com/wiemor/qaautomationengineer.git
cd qaautomationengineer
```

```
# Variables de Entorno:
# confirmar con java --version
# 
```

### 2. Desafio 01:

**Plan de Pruebas 01.docx** esta dento de a carpeta Desafio01. Asi como, tambien la carpeta **reports**

```
# Entorno virtual y dependencias:

cd desafio01
python -m venv env
.\env\Scripts\activate
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
pip install -r requirements.txt
```

```
# Ejecutar:

behave
```

### 3. Desafio 02:

**Plan de Pruebas 02.docx** esta dento de a carpeta Desafio02. Asi como, tambien la carpeta **reports**

```
# Entorno virtual y dependencias:

cd desafio02
python -m venv env
.\env\Scripts\activate
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
pip install -r requirements.txt
```

```
# ejecucion de appium
appium --base-path /wd/hub --relaxed-security
```

## Utilitarios
- El Desafio02/ui2.py permite recuperar los elementos de la pantalla
