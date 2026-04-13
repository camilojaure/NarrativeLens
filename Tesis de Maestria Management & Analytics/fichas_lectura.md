# Fichas de Lectura — Tesis ITBA
## Creative Diversity y Ad Performance en TikTok

Instrucciones de uso:
- Antes de abrir cada paper, leé la columna "Qué necesito"
- Leé en este orden: Abstract → Intro → Conclusión → Sección específica indicada
- Completá solo los tres campos de la ficha: idea, frase, decisión
- El campo "Borrador para la tesis" es opcional pero muy recomendado

---

## GRUPO A — Metodología estadística (OLS y sus supuestos)
*Prioridad alta: responden directamente al dictamen de Sauer*

> **Nota sobre libros disponibles:** Revisando tu biblioteca personal, ya tenés en el estante
> los dos textos más importantes para esta tesis: **Fox (2016)** y **James et al. (ISLP)**.
> Ambos ya están cargados en `references.bib`. Fox reemplaza completamente a Wooldridge
> para los supuestos del OLS. Hastie et al. (ESL) es gratuito en PDF oficial.
> No necesitás comprar nada.

---

### 1. Fox (2016) — Applied Regression Analysis and Generalized Linear Models
**Dónde conseguirlo:** ✅ Ya lo tenés en tu biblioteca personal
**Sección a leer:** Cap. 5 (supuestos del OLS) y Cap. 12 (heterocedasticidad y errores robustos)
**Tiempo estimado:** 30 minutos (dos capítulos)

**Qué necesito de este libro:**
Poder listar los supuestos formales del OLS (linealidad, media cero del error,
homocedasticidad, no multicolinealidad, normalidad) y explicar cuál de ellos
el CTR podría violar y por qué. Fox cubre exactamente lo mismo que Wooldridge
para este propósito y tiene la ventaja de que también incluye GLMs.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.1):**

---

### 2. Papke & Wooldridge (1996) — Econometric Methods for Fractional Response Variables
**PDF gratuito:** https://www.nber.org/system/files/working_papers/t0147/t0147.pdf
**Sección a leer:** Abstract + Introduction (páginas 1-4 son suficientes)
**Tiempo estimado:** 15 minutos

**Qué necesito de este paper:**
La intuición de por qué usar OLS con una variable dependiente acotada en (0,1)
es problemático, y el nombre de la solución que proponen (fractional logit).
NO necesito la demostración matemática.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.1):**

---

### 3. Ferrari & Cribari-Neto (2004) — Beta Regression for Modelling Rates and Proportions
**PDF gratuito:** https://www.ime.usp.br/~sferrari/beta.pdf
**Sección a leer:** Abstract + Introduction (páginas 1-3)
**Tiempo estimado:** 10 minutos

**Qué necesito de este paper:**
Que existe una alternativa a OLS diseñada específicamente para variables
continuas en (0,1): la regresión beta. Su ventaja principal: las predicciones
siempre caen dentro del rango válido.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.1):**

---

### 4. White (1980) — A Heteroskedasticity-Consistent Covariance Matrix Estimator
**Dónde conseguirlo:** https://www.econometricsociety.org/publications/econometrica/1980/05/01/...
**Sección a leer:** Solo el Abstract y la Introduction (2 páginas)
**Tiempo estimado:** 10 minutos

**Qué necesito de este paper:**
El nombre y la intuición del estimador de White (errores estándar robustos).
Es el paper que justifica reportar HC standard errors cuando sospechás
heterocedasticidad. Solo necesito poder decir "se reportan errores estándar
robustos siguiendo a White (1980)".

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.1):**

---

## GRUPO B — Random Forest: fundamentos e interpretabilidad
*Prioridad alta: profundidad teórica que pide el dictamen*

---

### 5. Breiman (2001b) — Statistical Modeling: The Two Cultures
**PDF gratuito:** https://projecteuclid.org/journals/statistical-science/volume-16/issue-3/Statistical-Modeling--The-Two-Cultures-with-comments-and-a/10.1214/ss/1009213726.full
**Sección a leer:** COMPLETO — son 20 páginas, vale la pena
**Tiempo estimado:** 45 minutos

**Qué necesito de este paper:**
El concepto de las "dos culturas" (modelado de datos vs. algorítmica) y por qué
combinarlas es valioso. Es el fundamento filosófico de tu decisión metodológica
de usar OLS + RF. Ya lo usás implícitamente en la página 31 de tu tesis.
Leerlo completo te va a dar vocabulario propio para articularlo mejor.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.3):**

---

### 6. Varian (2014) — Big Data: New Tricks for Econometrics
**PDF gratuito:** https://people.ischool.berkeley.edu/~hal/Papers/2013/ml.pdf
**Sección a leer:** Completo — son 25 páginas, muy accesible y sin fórmulas densas
**Tiempo estimado:** 30 minutos

**Qué necesito de este paper:**
Hal Varian (economista jefe de Google) argumenta que las técnicas de ML
(árboles de decisión, random forests, etc.) complementan a la econometría
clásica. ML es mejor para predicción y para descubrir relaciones no lineales;
la econometría clásica (OLS) es mejor para estimación causal e inferencia.
Esto es exactamente el argumento de tu Sección 2.6.3: por qué usás ambos.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.3):**

---

### 7. Mullainathan & Spiess (2017) — Machine Learning: An Applied Econometric Approach
**Acceso:** https://www.aeaweb.org/articles?id=10.1257/jep.31.2.87 (acceso institucional ITBA vía JSTOR)
**Sección a leer:** Abstract + Introduction + sección "What is Machine Learning?" (primeras 8 páginas)
**Tiempo estimado:** 20 minutos

**Qué necesito de este paper:**
La distinción clave entre predicción (ŷ) y estimación (β̂). ML optimiza
predicción; econometría optimiza estimación de parámetros. Son complementarios,
no competidores. Este es el argumento teórico más fuerte para justificar ante
los jurados por qué tu tesis usa OLS (para estimar coeficientes) + RF
(para validar el ranking de importancia).

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.3):**

---

### 8. Strobl et al. (2007) — Bias in Random Forest Variable Importance Measures
**PDF gratuito (open access):** https://pmc.ncbi.nlm.nih.gov/articles/PMC1796903/
**Sección a leer:** Abstract + Introduction + sección "Results: Illustration of the bias"
**Tiempo estimado:** 20 minutos

**Qué necesito de este paper:**
Que la importancia por Gini (MDI, la que usa scikit-learn por defecto) tiene
sesgo sistemático hacia variables con más categorías o mayor varianza.
Esto es directamente relevante para tu análisis porque creative_concept
tiene ~20 categorías y talent_type tiene ~7. Necesito poder decir esto
explícitamente y justificar el uso de permutation importance.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.2):**

---

### 9. Strobl et al. (2008) — Conditional Variable Importance for Random Forests
**PDF gratuito (open access):** https://pmc.ncbi.nlm.nih.gov/articles/PMC2491635/
**Sección a leer:** Abstract + Introduction (páginas 1-3)
**Tiempo estimado:** 15 minutos

**Qué necesito de este paper:**
Que la permutation importance también tiene problemas cuando las variables
están correlacionadas entre sí. En tu caso, creative_theme y creative_concept
probablemente correlen (un anuncio humorístico tiene cierto tipo de concepto
creativo). Esto va como caveat/limitación reconocida.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.2):**

---

### 8. Lundberg & Lee (2017) — A Unified Approach to Interpreting Model Predictions (SHAP)
**arXiv gratuito:** https://arxiv.org/abs/1705.07874
**Sección a leer:** Abstract + Introduction + sección "SHAP Values" (primeras 6 páginas)
**Tiempo estimado:** 20 minutos

**Qué necesito de este paper:**
La intuición de SHAP: asigna a cada variable una contribución promedio
a la predicción, basada en teoría de juegos (Shapley values). Es el método
de interpretabilidad más robusto actualmente. Puedo mencionarlo como
alternativa superior a Gini, tanto para trabajo futuro como para validar
los resultados del RF.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.2):**

---

## GRUPO C — Publicidad digital y TikTok
*Prioridad media: fortalecen el marco empírico de las secciones 2.1 a 2.3*

---

### 9. James, Witten, Hastie & Tibshirani — An Introduction to Statistical Learning (ISLP)
**Dónde conseguirlo:** ✅ Ya lo tenés en tu biblioteca personal
**Sección a leer:** Cap. 8 (Tree-Based Methods), especialmente 8.2 (Bagging, Random Forests, Boosting)
**Tiempo estimado:** 25 minutos
**Nota:** Este libro ya está citado como `james2021`. Leer este capítulo te va a dar vocabulario
preciso para describir el algoritmo de Random Forest en la Sección 2.6.2 con tus propias palabras.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.2):**

---

### 10. Breiman (2001) — Random Forests [YA LO TENÉS CITADO]
**PDF gratuito:** https://www.stat.berkeley.edu/~breiman/randomforest2001.pdf
**Sección a leer:** Abstract + Introduction + sección "Random Forests"
**Tiempo estimado:** 20 minutos
**Nota:** Ya lo citás. Leerlo te va a dar más confianza para hablar del algoritmo
con tus propias palabras en la defensa oral.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.6.2):**

---

### 11. TikTok — Marketing Science (DOI: 10.1287/mksc.2021.0107)
**Link:** https://pubsonline.informs.org/doi/10.1287/mksc.2021.0107
**Sección a leer:** Abstract + Introduction + hallazgos principales
**Tiempo estimado:** 20 minutos
**Tarea previa:** Verificar autores y año exactos → completar entrada en references.bib

**Qué necesito de este paper:**
Un hallazgo empírico concreto sobre atributos de video en TikTok y su
relación con performance. Un número, un resultado, algo citable que diga
"en TikTok, X se asocia con Y". Eso fortalece la Sección 2.1.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.1):**

---

### 12. TikTok — Journal of Business Research 2024
**Link:** https://www.sciencedirect.com/science/article/abs/pii/S0148296324003783
**Sección a leer:** Abstract + Introduction + tabla de resultados principales
**Tiempo estimado:** 20 minutos
**Tarea previa:** Verificar autores → completar entrada en references.bib

**Qué necesito de este paper:**
Mismo objetivo que el paper anterior: un hallazgo empírico concreto
sobre características del contenido de TikTok y comportamiento del usuario.

**Mi ficha:**
- **Idea central que me llevo:**
- **Frase/dato que puedo citar textualmente:**
- **Decisión que tomo para mi tesis:**
- **Borrador para la tesis (Sección 2.1):**

---

## Orden de lectura recomendado

Si tenés ~5 horas en total:

| Orden | Fuente | Tiempo | Urgencia | Dónde conseguirlo |
|-------|--------|--------|----------|-------------------|
| 1 | Breiman (2001b) Two Cultures | 45 min | Alta — fundamento filosófico | PDF gratis (link en ficha) |
| 2 | Varian (2014) Big Data: New Tricks | 30 min | Alta — reemplaza Chen (2023) | PDF gratis (link en ficha) |
| 3 | Mullainathan & Spiess (2017) | 20 min | Alta — reemplaza AlAli (2020) | JSTOR (acceso ITBA) |
| 4 | Strobl et al. (2007) | 20 min | Alta — afecta tus resultados | PDF gratis (link en ficha) |
| 5 | Papke & Wooldridge (1996) | 15 min | Alta — dictamen Sauer | PDF gratis (link en ficha) |
| 6 | Ferrari & Cribari-Neto (2004) | 10 min | Alta — dictamen Sauer | PDF gratis (link en ficha) |
| 7 | White (1980) | 10 min | Alta — 2 páginas nomás | PDF gratis (link en ficha) |
| 8 | Fox (2016) caps 5 y 12 | 30 min | Alta — reemplaza Wooldridge | ✅ Ya lo tenés en el estante |
| 9 | James et al. (ISLP) cap. 8 | 25 min | Media — vocabulario RF | ✅ Ya lo tenés en el estante |
| 10 | Strobl et al. (2008) | 15 min | Media | PDF gratis (link en ficha) |
| 11 | Lundberg & Lee (2017) SHAP | 20 min | Media | PDF gratis (link en ficha) |
| 12 | TikTok Marketing Science | 20 min | Media | Link en ficha |
| 13 | TikTok JBR 2024 | 20 min | Media | Link en ficha |
| 14 | Breiman (2001) RF | 20 min | Baja — para la defensa oral | PDF gratis (link en ficha) |

> **Nota:** Chen (2023) y AlAli (2020) fueron eliminados de la bibliografía. Eran hallucinations.
> Reemplazados por Varian (2014) y Mullainathan & Spiess (2017), ambos del Journal of Economic
> Perspectives — mucho más peso académico para los jurados.

---

## Cómo exportar desde Zotero a references.bib

1. Seleccioná todos los papers de la carpeta "Tesis ITBA"
2. Click derecho → Exportar colección
3. Formato: BibTeX
4. Guardá como `references.bib`
5. Reemplazá el archivo en la carpeta `tesis_overleaf` de tu computadora
6. Subí el nuevo `references.bib` a Overleaf (arrastrá al panel izquierdo)
