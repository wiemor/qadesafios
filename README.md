# Proyecto de Desafios para QA Automation Engineer

Finalidad: realizar la automaticación de los desafios del servicio RestFul Booker y la app de Booking.

## Arquitectura y Tecnologías

- **POO**: Seguí los principios de la Programación Orientada a Objetos  lo que permite una estructura modular, reutilizable y fácil de mantener.

- **Patrones de Diseño**: Use diversos patrones de diseño para optimizar la estructura y la eficiencia de las pruebas automatizadas. Con la finalidad de aumentar la legibilidad del código y la incorporación de nuevas caracteristicas.

- **Metodología BDD**: Utilice Behave con la finalidad de:

  - Crear escenarios de prueba en un lenguaje natural (Gherkin).
  - Facilita tambien la colaboración entre equipos técnicos y no técnicos.
  - Mantener una trazabilidad clara entre los requisitos del negocio y las pruebas automatizadas.

## Herramientas:

- Lenguaje de Programación: Python 3 (requests, pytest, pytest-check)
- Postman
- BDD: Behave
- Control de Versiones: Git
- Integración Continua: Jenkins
- Java JDK 11
- Android SDK
- Automatización: Appium

## Configuración y Ejecución

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

La estrategia de pruebas se encuentra dentro del directorio desafio01 con del nombre de **Plan de Pruebas 01.docx** 

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

La estrategia de pruebas se encuentra dentro del directorio desafio02 con del nombre de **Plan de Pruebas 02.docx** 

```
# Entorno virtual y dependencias:

cd desafio02
python -m venv env
.\env\Scripts\activate
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
pip install -r requirements.txt
```