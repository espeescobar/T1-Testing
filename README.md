# Ingeniería de Prompts Iterativa para Pruebas Automatizadas de Código

Agente basado en Gemini Flash Lite 3.1 que genera pruebas unitarias con `pytest` y las refina hasta alcanzar la cobertura de líneas, la cobertura de ramas y el *mutation score* objetivo.

**Video explicativo:** https://youtu.be/7lZABCpb-WM

---

## 1. Estrategia Implementada

El sistema es un **agente iterativo** que crea y corrige pruebas unitarias con el siguiente flujo:

* **Prompt base con rol senior**: el modelo adopta el rol de *ingeniero QA senior* y recibe el código fuente junto con reglas estrictas de generación.
* **Ciclo iterativo de retroalimentación**:
  1. El agente genera un conjunto inicial de tests para la clase objetivo.
  2. Ejecuta los tests y evalúa en orden su validez (`pytest`), su **cobertura** (`coverage`) y su **mutation score** (`cosmic-ray`).
  3. Si los tests fallan, o la cobertura o la mutación son bajas, le devuelve al modelo el error o las métricas junto con las pruebas actuales, dentro del mismo hilo conversacional, para que corrija y ajuste casos borde.
  4. El ciclo se repite hasta que se cumplen los umbrales o se acaba el tiempo disponible.
* **Control de ejecución y métricas**: hay un tiempo de espera (*sleep*) cuando la API está saturada y un temporizador que corta el ciclo. Al final, el agente guarda los tests en `test_<clase>.py` y las métricas en `metrics.json`.

---

## 2. Principales Decisiones de Diseño del Agente

El agente se estructuró como un ciclo **generar → ejecutar → evaluar → retroalimentar**, en el que el modelo nunca trabaja a ciegas: cada nueva respuesta se construye sobre el resultado real de la anterior. Las decisiones clave surgieron de los problemas encontrados:

| Desafío | Causa | Decisión de diseño |
| --- | --- | --- |
| **Ciclo infinito sin corregir errores** | La conversación se reiniciaba en cada iteración y el modelo perdía el historial. | **Contexto conversacional persistente**: una sola conversación durante toda la ejecución, para que la IA entienda y corrija sus errores previos. |
| **Alucinación de rutas de importación** | La IA inventaba rutas que no existían y los tests fallaban antes de ejecutarse. | **Regla de importación exacta**: el agente extrae la ruta real del archivo y la inyecta en el prompt como regla estricta. |
| **Clases falsas al simular dependencias** | Al simular dependencias, la IA creaba clases que no existían, con problemas de memoria y referencias. | **Regla de *mocking***: el prompt exige `MagicMock` en lugar de clases ficticias hechas a mano. |

Además, la evaluación es **escalonada**: la mutación solo se mide cuando los tests ya pasan y la cobertura es suficiente, porque es la etapa más costosa en tiempo.

---

## 3. Limitaciones Encontradas

* **Variabilidad en el número de iteraciones**: depende del archivo y cambia entre corridas. Los archivos con lógica directa llegan al 100% de cobertura en un intento; los más extensos necesitan 3 o 4 iteraciones, y algunos hasta 10. Por ejemplo, `stock4/validate` tomó 3 iteraciones en una corrida y 1 en otra.
* **Redundancia de tests**: de 23 archivos, 187 tests y 352 aserciones, hay pruebas clonadas o muy parecidas entre proyectos (p. ej., tests de *kernels* repetidos en `svm` y `blackjack`).
* **Oscilación del mutation score**: aunque los tests sean válidos y cubran el código, el *mutation score* varía mucho entre archivos (95% en unos frente a 64% en otros).
