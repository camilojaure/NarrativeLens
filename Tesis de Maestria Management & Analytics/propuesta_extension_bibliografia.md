# Propuesta de Extensión Bibliográfica
## Tesis: Creative Diversity y Ad Performance en TikTok

---

## 1. Diagnóstico de la Bibliografía Actual

### Fuentes académicas existentes (papers/libros)
| Fuente | Tema |
|--------|------|
| Guido et al. (2018) | Creatividad y atención en publicidad |
| Sudhir, Lee & Roy (2022) | Campañas de conversión vs. clicks, diseño experimental |
| Cunningham (2021) | Inferencia causal en economía |
| Breiman (2001) | Random Forests (paper original) |
| Fox (2016) | Applied Regression Analysis & GLM |
| James, Witten, Hastie & Tibshirani (2021) | ISLP -- Intro to Statistical Learning |
| Chen (2023) | Regresión logística vs RF para CTR en Taobao |
| AlAli et al. (2020) | Regresión lineal + RF en publicidad móvil |
| Lang (2000) | No especificado en detalle |
| Medidata (2023) | Modelos tree-based en planificación de medios |

### Fuentes de industria / web (no académicas)
| Fuente | Tipo |
|--------|------|
| Kantar (2023) | Caso KFC, calidad creativa |
| Meta (2022, 2023, 2024a, 2024b) | Blog posts de Meta for Business |
| Singular (2025) | Blog de industria -- fatiga creativa |
| Ad-Lib.io (2022) | Blog de industria -- fatiga creativa |
| Ready Set (2024) | Framework CDS (fuente primaria) |
| Estée Lauder | Caso de rotación creativa (fuente no identificada) |
| TikTok for Business | Blog corporativo |

### Diagnóstico
La bibliografía tiene una **proporción alta de fuentes de industria** (blogs, whitepapers, casos) vs. papers académicos peer-reviewed. Esto es comprensible dado que el tema es emergente, pero los dictámenes piden fortalecer el sustento teórico. Las áreas más débiles son:

1. **OLS con variable dependiente acotada**: no se citan los trabajos fundacionales sobre por qué OLS puede ser problemático con proporciones (0,1), ni las alternativas clásicas.
2. **Random Forest -- interpretabilidad**: solo se cita a Breiman (2001). Falta profundidad sobre variable importance, sesgos de Gini, y SHAP.
3. **Marco teórico de modelos estadísticos**: Hastie et al. (2009) "Elements of Statistical Learning" no está citado (solo el ISLP de James et al.).
4. **Publicidad digital en TikTok**: existen papers académicos recientes en journals como Marketing Science y Journal of Business Research que no se aprovechan.

---

## 2. Papers Propuestos por Área Temática

### A. OLS con variable dependiente acotada (0,1) -- Responde al dictamen de Sauer

Estos papers son esenciales para discutir en el Marco Teórico por qué usás OLS con CTR (acotado 0-1) y qué alternativas existen. Sauer pidió explícitamente que se discutan los supuestos del OLS.

**A1. Papke, L. E. & Wooldridge, J. M. (1996)**
*Econometric methods for fractional response variables with an application to 401(k) plan participation rates.*
Journal of Applied Econometrics, 11(6), 619--632.
- **Relevancia**: Paper fundacional sobre modelos de respuesta fraccional. Propone el fractional logit como alternativa a OLS cuando la variable dependiente está acotada en (0,1). Directamente aplicable al CTR.
- **Uso en la tesis**: Citar en el Marco Teórico para justificar la discusión de alternativas al OLS. Podría mencionarse como robustness check.

**A2. Ferrari, S. L. P. & Cribari-Neto, F. (2004)**
*Beta Regression for Modelling Rates and Proportions.*
Journal of Applied Statistics, 31(7), 799--815.
- **Relevancia**: Introduce la regresión beta, diseñada específicamente para variables continuas en (0,1). Los parámetros son interpretables en términos de la media y la dispersión.
- **Uso en la tesis**: Alternativa metodológica al OLS que garantiza predicciones dentro de (0,1). Discutir como posible extensión futura o robustness check.

**A3. White, H. (1980)**
*A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity.*
Econometrica, 48(4), 817--838.
- **Relevancia**: El paper más citado en economía desde 1970. Propone errores estándar robustos cuando hay heterocedasticidad, un supuesto que probablemente se viola con datos de CTR (varianza no constante).
- **Uso en la tesis**: Si usás OLS, deberías reportar errores estándar robustos (HC). Este paper justifica esa práctica.

**A4. Wooldridge, J. M. (2012)**
*Introductory Econometrics: A Modern Approach.* 5th ed. South-Western.
- **Relevancia**: Textbook estándar de econometría. Cubre supuestos de OLS (linealidad, homocedasticidad, normalidad de errores, no multicolinealidad) con rigor pero accesible.
- **Uso en la tesis**: Referencia canónica para la discusión de supuestos del OLS que pide Sauer.

### B. Random Forest: fundamentos, variable importance e interpretabilidad

**B1. Hastie, T., Tibshirani, R. & Friedman, J. (2009)**
*The Elements of Statistical Learning: Data Mining, Inference, and Prediction.* 2nd ed. Springer.
- **Relevancia**: El textbook de referencia en machine learning estadístico. Cubre Random Forest en profundidad (Cap. 15), incluyendo bagging, OOB error, y variable importance.
- **Uso en la tesis**: Complementa a James et al. (2021) con más profundidad teórica. Citar para la fundamentación del RF.

**B2. Strobl, C., Boulesteix, A. L., Zeileis, A. & Hothorn, T. (2007)**
*Bias in random forest variable importance measures: Illustrations, sources and a solution.*
BMC Bioinformatics, 8(1), 25.
- **Relevancia**: Demuestra que la importancia por Gini (Mean Decrease Impurity) tiene sesgo hacia variables con más categorías o mayor escala. Tus variables CDS son categóricas con distinto número de niveles, por lo que este sesgo podría afectar los resultados.
- **Uso en la tesis**: Crucial para la discusión de variable importance en el RF. Justifica usar permutation importance en lugar de (o además de) Gini importance.

**B3. Strobl, C., Boulesteix, A. L., Kneib, T., Augustin, T. & Zeileis, A. (2008)**
*Conditional variable importance for random forests.*
BMC Bioinformatics, 9, 307.
- **Relevancia**: Extiende el trabajo de 2007 mostrando que la permutation importance también tiene sesgo con variables correlacionadas. Propone conditional importance como solución.
- **Uso en la tesis**: Dado que tus variables CDS pueden estar correlacionadas (ej: creative_theme y creative_concept), este paper es relevante para interpretar correctamente la importancia relativa.

**B4. Lundberg, S. M. & Lee, S. I. (2017)**
*A Unified Approach to Interpreting Model Predictions.*
Advances in Neural Information Processing Systems (NeurIPS), 30, 4766--4777.
- **Relevancia**: Introduce SHAP (SHapley Additive exPlanations), el framework de interpretabilidad más usado actualmente para modelos de ML. Unifica 6 métodos previos.
- **Uso en la tesis**: Si usás o querés discutir feature importance de forma más robusta que la importancia por defecto de scikit-learn, SHAP es el estándar. Incluso como trabajo futuro.

### C. Machine Learning aplicado a publicidad digital / CTR

**C1. Engagement Patterns in TikTok: An Analysis of Short Video Ads (2024)**
ACM Digital Library, Proc. 2024.
- **Relevancia**: Analiza patrones de abandono (churn) en anuncios de video corto en TikTok usando regresión logística. Encuentra que la mayoría de usuarios abandona en el primer cuarto del video.
- **Uso en la tesis**: Paper académico sobre TikTok ads con metodología cuantitativa similar. Fortalece el marco de la plataforma.

**C2. The impact of content characteristics of Short-Form video ads on consumer purchase Behavior: Evidence from TikTok (2024)**
Journal of Business Research (ScienceDirect).
- **Relevancia**: Analiza 2,578 anuncios de TikTok y encuentra que trustworthiness, expertise y attractiveness impactan positivamente la compra. Relación U-shaped para autenticidad.
- **Uso en la tesis**: Directamente comparable -- también analiza atributos de contenido creativo en TikTok con dataset grande.

**C3. Engagement That Sells: Influencer Video Advertising on TikTok (2023)**
Marketing Science (INFORMS).
- **Relevancia**: Publicado en Marketing Science (top journal). Desarrolla un "product engagement score" usando deep CNNs para predecir ventas a partir de features visuales de videos de TikTok.
- **Uso en la tesis**: Paper de alto impacto en un journal top que estudia la relación entre atributos de video y performance en TikTok. Valida el enfoque general de tu tesis.

**C4. Influence of audiovisual features of short video advertising on consumer engagement behaviors: Evidence from TikTok (2025)**
Journal of Business Research (ScienceDirect).
- **Relevancia**: Identifica cuatro features audiovisuales (expresión coloquial, cadencia, colorfulness, prominencia visual) que correlacionan con engagement en TikTok.
- **Uso en la tesis**: Complementa tu enfoque basado en dimensiones CDS con evidencia de features específicas de video.

### D. Diversidad creativa en advertising (fuentes académicas)

**D1. Diversity Representations in Advertising: Enhancing Variety Perceptions and Brand Outcomes (2024)**
Journal of Consumer Research, 52(1), 179+.
- **Relevancia**: Demuestra que modelos diversos en publicidad crean percepción de mayor variedad de producto, lo que mejora la impresión de marca, percepción de creatividad y willingness to pay.
- **Uso en la tesis**: Aunque trata diversidad de representación (no diversidad creativa en el sentido CDS), es un paper en un journal top que conecta diversidad visual con métricas de performance.

**D2. Diversity and inclusion in advertising research (2022)**
International Journal of Advertising.
- **Relevancia**: Review comprehensivo del estado de la investigación sobre diversidad en publicidad.
- **Uso en la tesis**: Útil para contextualizar el concepto de diversidad creativa dentro de la literatura más amplia de advertising.

### E. Textbooks y referencias metodológicas complementarias

**E1. Breiman, L. (2001b)**
*Statistical Modeling: The Two Cultures.*
Statistical Science, 16(3), 199--231.
- **Relevancia**: Ya lo citás implícitamente cuando hablás de "las dos culturas de la estadística" en la pág. 31. Deberías citar este paper explícitamente, no solo el de Random Forests.
- **Uso en la tesis**: Fundamenta directamente tu decisión de combinar OLS (cultura de modelado de datos) con RF (cultura algorítmica).

---

## 3. Resumen de Prioridades

### Imprescindibles (responden directamente a los dictámenes)
1. **Papke & Wooldridge (1996)** -- alternativa al OLS para variables acotadas
2. **Ferrari & Cribari-Neto (2004)** -- regresión beta
3. **White (1980)** -- errores estándar robustos
4. **Wooldridge (2012)** o equivalente -- supuestos de OLS
5. **Strobl et al. (2007)** -- sesgo en variable importance de RF
6. **Lundberg & Lee (2017)** -- SHAP values
7. **Breiman (2001b)** -- "Two Cultures" (ya lo citás implícitamente)

### Muy recomendados (fortalecen el Marco Teórico significativamente)
8. **Hastie, Tibshirani & Friedman (2009)** -- ESL textbook
9. **Strobl et al. (2008)** -- conditional variable importance
10. **Paper de Marketing Science sobre TikTok** (C3)
11. **Paper de J. Business Research sobre TikTok** (C2)

### Deseables (profundidad adicional)
12. Engagement Patterns in TikTok (C1)
13. Audiovisual features en TikTok (C4)
14. Journal of Consumer Research sobre diversidad (D1)

---

## 4. Impacto en la Estructura del Marco Teórico

### Subsección nueva sugerida: "Modelos estadísticos para variables de respuesta acotadas"
Ubicación: después de la sección de métricas CTR/CPA, antes del enfoque analítico.
Contenido: discusión de por qué OLS tiene limitaciones con CTR (predicciones fuera de 0-1, heterocedasticidad inherente), presentación de alternativas (fractional logit, beta regression), y justificación de por qué se elige OLS igualmente (transparencia, ranking de features como objetivo principal, no predicción puntual).

### Subsección ampliada: "Random Forest como complemento no paramétrico"
Contenido actual: breve mención de Breiman (2001) y la lógica de complementar OLS.
Ampliación propuesta: agregar discusión de variable importance (Gini vs. permutation vs. SHAP), sesgos conocidos (Strobl et al.), y por qué la importancia por permutación es preferible en este contexto.

### Subsección ampliada: "Evidencia académica en TikTok"
Contenido actual: se apoya fuertemente en fuentes de industria (Meta, TikTok for Business).
Ampliación propuesta: incorporar los papers de Marketing Science y Journal of Business Research sobre TikTok para darle peso académico a la discusión de la plataforma.
