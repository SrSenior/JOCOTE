# JOCOTE – Transpilador en Python

## 📌 Descripción

**JOCOTE** es un lenguaje de programación diseñado como parte de un proyecto académico, junto con un transpilador implementado en Python.

El sistema toma código escrito en JOCOTE y lo transforma en código Python ejecutable, pasando por múltiples etapas del proceso de compilación.

El lenguaje está inspirado conceptualmente en la resiliencia y crecimiento del fruto jocote, reflejando estructuras dinámicas y evolución del código.

---

## 🧠 Arquitectura del compilador

El transpilador está compuesto por cuatro etapas principales:

* **Explorador (Lexer)** → análisis léxico del código fuente
* **Analizador (Parser)** → construcción del árbol de sintaxis abstracta (AST)
* **Verificador (Semantic Analyzer)** → validación semántica y manejo de símbolos
* **Generador de código** → transformación del AST a código Python

Además, el sistema implementa manejo de errores mediante **modo pánico**, permitiendo continuar el análisis incluso ante errores para detectar múltiples fallos en una sola ejecución.

---

## ⚙️ Tecnologías

* Python
* Diseño de compiladores
* Estructuras de datos (árboles, tablas de símbolos)

---

## 🧩 Estructura del proyecto

```bash
.
├── jocote.py
├── explorador/
├── analizador/
├── verificador/
├── generador/
└── utils/
```

Cada módulo representa una etapa del proceso de compilación.

---

## 🚀 Cómo ejecutar

Ejecuta el transpilador con:

```bash
python3 jocote.py --solo-jocotiar input/carreraCaracoles.tcj
```

Esto generará un archivo en la carpeta `output`, el cual puede ejecutarse como un programa Python estándar.

---

## 💡 Aprendizajes

* Implementación de un pipeline completo de compilador
* Diseño de lenguajes de programación
* Construcción y recorrido de AST
* Manejo de errores en compiladores (modo pánico)
* Separación de fases en procesamiento de código

---

## 👥 Equipo

Proyecto desarrollado en colaboración con:

* Luis Fernando Benavides
* Kristhel Cordero
* Juan Diego Jiménez
* Alex Naranjo Masis
* José Pablo Vega Solano

---

## 📌 Notas

* Proyecto académico enfocado en el diseño e implementación de un lenguaje de programación
* Incluye ejemplos funcionales dentro del repositorio
