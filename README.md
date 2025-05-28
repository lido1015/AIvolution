# AIvolution
 

## Descripción General
Un sistema de simulación que estudia la interacción entre evolución genética y cultural en un ecosistema artificial. Combina:
- **Simulación basada en agentes** con dinámicas depredador-presa
- **Sistemas expertos difusos** para toma de decisiones
- **Metaheurísticas poblacionales** para optimización paramétrica
- **Modelos de lenguaje** (LLMs) para herencia cultural

**Objetivo central**: Comparar los resultados de la selección natural biológica vs. optimización metaheurística, para evaluar cómo los algoritmos evolutivos capturan procesos biológicos reales.

---

## Componentes de Simulación

### 1. Arquitectura BDI de Agentes
Los organismos (depredadores y presas) implementan un modelo **Creencias-Deseos-Intenciones**:
- **Creencias**: Percepción del entorno (nivel de energía, proximidad a amenazas, recursos disponibles)
- **Deseos**: Objetivos primarios (supervivencia, reproducción, alimentación)
- **Intenciones**: Acciones concretas determinadas por el sistema experto difuso

**Mecánica clave**:
- Los agentes actualizan sus creencias mediante sensores virtuales
- El sistema difuso traduce deseos en intenciones usando reglas lingüísticas
- Las acciones modifican el entorno y desencadenan nuevas percepciones

### 2. Entorno Dinámico
- **Generación procedural** de recursos usando distribuciones aleatorias (Poisson para eventos raros, Normal para recursos básicos)
- **Zonas de influencia** con efectos diferenciados (áreas fértiles, territorios peligrosos)
- **Clima estocástico** que afecta las reglas de supervivencia

### 3. Dos Modos de Simulación

1. **Optimización endógena (Selección Natural)**

    **Mecanismo:** Proceso emergente basado en variación genética aleatoria y presión ambiental

    **Dinámica:**

    - Mutaciones graduales en atributos físicos/comportamentales

    - Supervivencia diferencial de organismos

    - Acumulación adaptativa multi-generacional

    **Analogía biológica:** Evolución darwiniana clásica

2. **Optimización exógena (Metaheurísticas)**

    **Mecanismo:** Búsqueda algorítmica dirigida en espacio de parámetros

    **Dinámica:**
    - Atributos fijos en cada simulación

    - Evaluación sistemática de configuraciones

    - Recombinación guiada de soluciones

    - Convergencia hacia óptimos globales

    **Analogía técnica:** Ingeniería inversa de la evolución

---

## Componentes de Inteligencia Artificial

### 1. Sistema Experto Difuso
**Funcionamiento**:
1. **Fuzzificación**: Conversión de entradas numéricas (ej: 75% energía) a términos lingüísticos ("Alta")
2. **Base de Reglas**: reglas del tipo *"SI (energía ES Baja Y riesgo ES Alto) ENTONCES (prioridad=Huir)"*
3. **Defuzzificación**: Traducción de conclusiones difusas a acciones concretas



### 2. Metaheurísticas Poblacionales
**Implementación**:
- **Algoritmos Genéticos**: Optimizan parámetros de agentes (velocidad, tasa reproducción)
- **Enjambre de Partículas (PSO)**: Busca configuraciones óptimas del ecosistema

**Flujo de trabajo**:
1. Ejecutar simulación con parámetros iniciales
2. Calcular métricas de desempeño (supervivencia, crecimiento poblacional)
3. Generar nueva población de parámetros usando operadores evolutivos
4. Repetir hasta convergencia

### 3. Herencia Cultural con LLMs
**Proceso**:
1. Los agentes registran experiencias clave (ej: "escape exitoso de depredador")
2. Un LLM sintetiza "memes culturales" a partir de estas experiencias
3. Los memes se propagan mediante interacciones sociales entre agentes
4. Los memes modifican las reglas de decisión (ej: preferencia por estrategias aprendidas)

**Mecánica**:
- Base de conocimiento memética compartida
- Sistema de reputación para validar memes
- Decaimiento natural de memes no exitosos

---


## Metodología de Validación
1. **Evolución por selección natural**:
   - Ejecutar 1000 generaciones
   - Registrar distribución de rasgos emergentes
2. **Evolución por metaheurísticas poblacionales**:
   - Optimizar parámetros con metaheurísticas diferentes
   - Comparar soluciones obtenidas
3. **Análisis cruzado**:
   - Medir divergencia entre rasgos naturales vs. óptimos algorítmicos
   - Evaluar impacto de los memes en la velocidad de adaptación

**Métricas clave**:
- Tasa de convergencia
- Resiliencia del ecosistema
- Diversidad genética/cultural
