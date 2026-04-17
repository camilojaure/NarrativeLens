# Instrucciones para el tutor (Claude)

Este archivo contiene criterios y contexto acumulado para la tesis de Camilo. Pegarlo al inicio de cualquier sesión de revisión de escritura.

---

## Contexto de la tesis

- **Tema:** Identificar qué dimensiones creativas están asociadas con mayor CTR en campañas de paid social (TikTok), para orientar a creative strategists en la optimización de su creative diversity score.
- **Plataforma:** TikTok Top Ads
- **Metodología:** OLS + Random Forest + SHAP. Si ambos modelos convergen en el mismo ranking de dimensiones, eso constituye evidencia robusta (Breiman, 2001).
- **Framework epistemológico:** Puramente predictivo/descriptivo. No hay pretensión causal.
- **Estado:** La tesis tiene escritura avanzada pero recibió dos pre-dictámenes pidiendo mejorar el marco conceptual y validar supuestos del análisis.

---

## Dataset

- **Archivo:** `tiktok_topads_clean.csv` en `/Users/camilojaureguiberry/Documents/devs/NarrativeLens/data/datasets/`
- **Observaciones:** 578 ads
- **Variable dependiente:** CTR (continua, muy sesgada a la derecha → se usa log(CTR))
- **Dimensiones creativas:** `creative_theme` (9 cat.), `creative_concept` (20 cat.), `talent_type` (7 cat.)
- **Controles:** `duration`, `objective_value`, `campaign_objective`
- **Nulos:** `talent_type` null = ausencia real de talento en el ad (se rellena con "No Talent"). `creative_concept` null = "Not Applicable"

---

## Arquitectura metodológica

### Justificación (Breiman, 2001 — "Statistical Modeling: The Two Cultures")
- **OLS** = data model: asume forma funcional lineal, da coeficientes interpretables y comunicables a creative strategists.
- **Random Forest** = algorithmic model: no asume forma funcional, captura interacciones y no linealidades.
- **SHAP** (Lundberg & Lee, 2017): calcula contribución marginal de cada variable por observación individual. Más honesto que impurity-based feature importance, especialmente para variables categóricas con muchas categorías.
- La convergencia entre OLS y RF (vía SHAP) constituye evidencia robusta independiente de los supuestos de cada modelo.

### Rol de cada modelo
- RF + SHAP → identifica qué dimensiones tienen mayor capacidad predictiva (sin supuestos de forma)
- OLS → provee coeficientes interpretables para comunicar magnitud del efecto a practitioners
- Si una dimensión es relevante en ambos modelos → usar coeficiente OLS para comunicar el efecto
- Si divergen → la divergencia indica posible no linealidad; apoyarse en SHAP

### Resultados del análisis (verificados, abril 2026)
- **OLS R² out-of-sample (5-fold CV):** 0.496 ± 0.07
- **RF R² out-of-sample (5-fold CV):** 0.519 ± 0.14
- Los modelos convergen fuera de muestra (RF sobreajusta fuertemente in-sample: 0.90)
- **Ranking SHAP de dimensiones creativas:** 1) creative_theme, 2) talent_type, 3) creative_concept
- **Durbin-Watson ≈ 0.76** → posible autocorrelación (clustering intra-marca). Mencionar como limitación.

### Hallazgo metodológico clave (sesión abril 2026)
La comparación OLS vs SHAP **debe hacerse a nivel de categoría individual** (n=34), no a nivel de dimensión agregada (n=3). Comparar con n=3 es estadísticamente inútil y llevó a conclusiones erróneas de "no convergencia".

**El problema de métrica**: OLS |coeficiente| y SHAP mean |value| miden cosas distintas:
- OLS |coef| = tamaño del efecto puro de la categoría (desviación respecto a la gran media)
- SHAP mean |value| = contribución promedio en el dataset = efecto × prevalencia

Una categoría con n=3 observaciones puede tener un OLS enorme pero SHAP ≈ 0 (afecta a 3 de 578 ads). La comparación directa sin ponderar da ρ = −0.03 (p = 0.87), sugiriendo "divergencia". Pero al ponderar OLS |coef| × prevalencia (n_cat/578), la correlación sube a **Spearman ρ = 0.74, p < 0.0001** → convergencia fuerte.

**Implicación para la tesis:** el argumento de convergencia sí se sostiene, pero requiere la métrica correcta. Comunicar que SHAP ya incorpora la prevalencia intrínsecamente (promedia sobre todas las observaciones), por lo que para hacerla comparable con OLS hay que ponderar el coeficiente por la frecuencia de la categoría.

### Ranking de categorías creativas (convergencia OLS ponderado × SHAP)

**Top Tier — ambos modelos coinciden (SHAP top 10 + OLS significativo):**

| Dir. | Categoría | Dimensión | n | CTR medio | OLS coef | Sig. | SHAP rank |
|------|-----------|-----------|---|-----------|----------|------|-----------|
| − | Humor & Entertainment | creative_theme | 32 | 0.015 | −0.505 | *** | #1 |
| − | No Talent | talent_type | 227 | 0.029 | −0.144 | ** | #2 |
| + | Day-in-the-life story | creative_concept | 36 | 0.048 | +0.435 | *** | #3 |
| − | Customers | talent_type | 120 | 0.025 | −0.139 | ** | #4 |
| − | Product demo | creative_concept | 252 | 0.040 | −0.193 | * | #5 |
| + | Product-Centric | creative_theme | 220 | 0.045 | +0.258 | ** | #8 |

**Tier 2 — alto SHAP, OLS no significativo (posible no-linealidad):**

| Dir. | Categoría | Dimensión | n | SHAP rank |
|------|-----------|-----------|---|-----------|
| + | Lifestyle & Aspirational | creative_theme | 49 | #6 |
| − | Not Applicable (sin concepto) | creative_concept | 100 | #7 |
| + | Promotional & Offer-Based | creative_theme | 128 | #9 |
| + | Combination of actors & customers | talent_type | 25 | #10 |

**Tier 3 — OLS significativo pero SHAP bajo (efecto intenso, muy pocos casos):**
- Event-driven (n=3, CTR=0.347): OLS +1.35***, SHAP #14
- Aspirational creator collaboration (n=2): OLS +0.651***, SHAP #20
- Testimonial & Social Proof (n=37): OLS +0.338***, SHAP #19
- FAQ (n=14): OLS −0.416***, SHAP #23
- Meme-based content (n=6): OLS −0.603***, SHAP #26

**Insight narrativo**: "Humor & Entertainment" siendo el predictor con mayor SHAP (negativo) es contraintuitivo para TikTok y potencialmente el hallazgo más interesante para discutir. Los ads sin talento (No Talent, n=227) también están asociados negativamente. Del lado positivo, "Day-in-the-life story" y "Product-Centric" son los conceptos más robustos.

### Variables creativas adicionales en el dataset (no incluidas en el modelo actual)
El dataset tiene 21 columnas; las siguientes podrían considerarse variables creativas:
- `format_production_style` (6 cat.): 92% Native Video → poca variabilidad, probablemente agregar poco
- `is_ugc` (bool): UGC (n=470, CTR=0.038) vs no-UGC (n=108, CTR=0.017) — diferencia notable
- `demographic_representation` (12 cat.): algunas con n=1 o n=3, habría que colapsar categorías
- `audience_focus` (5 cat.): más estrategia que creatividad per se
- `industry_parent` / `industry_child`: exógenas, no se "deciden" creativamente

---

## Archivos del proyecto

- **Notebook principal:** `/Users/camilojaureguiberry/Documents/devs/NarrativeLens/src/modeling/regression_analysis_thesis_v2.ipynb`
- **Entorno Python:** venv en `/Users/camilojaureguiberry/Documents/devs/NarrativeLens/NarrativeLens/` — usar `/usr/local/bin/python3` como intérprete en VS Code (el symlink interno está roto)

---

## Criterios de revisión de escritura

### 1. Lenguaje causal vs. asociativo
La tesis no tiene pretensión causal. Evitar frases como:
- ❌ "la dimensión X **impacta** el CTR"
- ❌ "la dimensión X **produce** mayor performance"
- ❌ "la dimensión X **causa** / **genera** / **lleva a**..."

Usar en cambio:
- ✅ "la dimensión X **está asociada con** mayor CTR"
- ✅ "la dimensión X **es un predictor relevante** de CTR"
- ✅ "cuando X está presente, históricamente la performance fue mejor"

### 2. Supuestos a mencionar como limitaciones
- Supuesto i.i.d. (Breiman, 2001): puede verse afectado por clustering intra-marca (varias campañas del mismo anunciante comparten características no observadas)
- Durbin-Watson bajo: reportar como posible autocorrelación en los residuos
- **Normalidad de residuos:** Shapiro-Wilk la rechaza, pero no invalida el análisis. Dos razones: (1) con n=578 el TCL garantiza distribución muestral normal de los coeficientes → inferencia válida con HC1 (Fox, 2016, Cap. 5); (2) el patrón en "V" del Scale-Location y las dos bandas en Residuos vs. Fitted son un *floor effect* de CTR mínimo = 0.01 → log(CTR) = −4.6, no heterocedasticidad clásica.

**Texto listo para sección de Limitaciones:**
> "El test de Shapiro-Wilk rechaza la normalidad de los residuos (p < 0.05). Sin embargo, este resultado no invalida el análisis por dos razones. Primero, con n = 578, el Teorema Central del Límite asegura que la distribución muestral de los coeficientes es aproximadamente normal, por lo que la inferencia basada en errores estándar robustos HC1 (White, 1980) es asintóticamente válida (Fox, 2016, Cap. 5). Segundo, el patrón estructural observado en los gráficos de diagnóstico es consistente con la naturaleza discreta del CTR en el dataset: el valor mínimo reportado es 0.01, lo que genera una masa de probabilidad concentrada en log(CTR) = −4.6 (efecto piso), produciendo artificialmente las bandas visibles en los residuos. Se reporta como limitación junto con la baja continuidad de la variable dependiente."

---

## Nota sobre objective_value_Conversions (variable de control dominante)

`objective_value` es la variable con mayor SHAP en todo el modelo — muy por encima de las dimensiones creativas. La categoría **Conversions** tiene coeficiente OLS = −1.16*** y SHAP negativo muy fuerte:

- **Lectura del beeswarm SHAP:** puntos rojos (Conversions = 1) a la izquierda → menor CTR predicho. Puntos azules (Conversions = 0) a la derecha → mayor CTR predicho.
- **Por qué tiene sentido:** las campañas optimizadas por Conversions instruyen al algoritmo de TikTok a mostrar el ad a usuarios con alta probabilidad de *convertir*, no de *hacer click*. El algoritmo trabaja con audiencias más pequeñas y selectivas → CTR naturalmente más bajo. Las campañas de App Installs o Product Sales buscan clicks → CTR más alto.
- **Implicación metodológica:** esto justifica incluirla como control, no como variable de interés. Sin controlarla, se mezclarían dos poblaciones de ads con CTRs estructuralmente distintos y los coeficientes creativos absorberían ese ruido. La pregunta de la tesis queda correctamente formulada como: *"dado el mismo tipo de campaña, ¿qué dimensiones creativas están asociadas con mayor CTR?"*
- **Importante para la defensa:** `objective_value` no es una decisión creativa — es una configuración de TikTok Business Center. Su dominancia en el modelo es una validación de que el modelo captura señal real, no un problema.

---

## Robustness Check — Colapso de categorías con n < 10

**Criterio:** categorías con menos de 10 observaciones → colapsadas en "Other" (Fox, 2016, Cap. 5; James et al., 2021, Cap. 3).

**Impacto:**
- `creative_concept`: 20 → 7 categorías individuales + "Other" (n=57)
- `creative_theme`: sin cambios (todas n ≥ 10)
- `talent_type`: 1 categoría colapsada (n=2)

**Resultados:**
- OLS R² CV: 0.496 → 0.505 (leve mejora, coeficientes más estables)
- Convergencia Spearman: ρ = 0.74 → 0.57 (sigue significativa, p=0.006)
- Top Tier es prácticamente idéntico — hallazgos principales son robustos
- Única excepción: "Product demo" pierde significancia OLS al colapsar

---

*Última actualización: 17 de abril 2026 — supuestos OLS, objective_value, robustness check*
