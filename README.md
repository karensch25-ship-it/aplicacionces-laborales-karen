# aplicaciones_laborales

En este repo yacen todas las aplicaciones laborales realizadas

## 🚀 Mejoras Recientes: Sistema de Personalización Inteligente + Scoring Automático

Este repositorio incluye un **motor de personalización avanzado** y un **sistema de scoring multi-dimensional** que genera hojas de vida verdaderamente adaptadas a cada vacante y evalúa objetivamente el match del candidato con los requerimientos del puesto.

### 📊 Mejoras Implementadas

#### Fase 1-3: Sistema de Personalización (COMPLETADO ✅)
- ✅ **Professional Summary Personalizado:** Se genera dinámicamente según los requisitos de cada vacante
- ✅ **Job Alignment Inteligente:** Mapea requisitos a logros reales con evidencia cuantificable
- ✅ **Sin Errores Gramaticales:** Corrección completa de problemas de redacción
- ✅ **Evidencia Concreta:** En lugar de "Demonstrated experience in...", muestra logros específicos con métricas
- ✅ **Nivel de Personalización:** Incrementado de 5% a 65%

#### Fase 4: Sistema de Scoring Automático (NUEVO ✅)
- ✅ **Análisis Multi-dimensional:** Evalúa el match en 5 dimensiones clave
  - Technical Skills Match (30% peso)
  - Experience Depth & Relevance (25% peso)
  - Domain Knowledge (20% peso)
  - Soft Skills & Cultural Fit (15% peso)
  - Achievement Quality (10% peso)
- ✅ **Reporte de Scoring Detallado:** Genera automáticamente un informe completo con:
  - Puntuación global y recomendación (EXCELLENT/STRONG/GOOD/MODERATE/WEAK FIT)
  - Desglose por dimensión con visualización de barras
  - Identificación de fortalezas y gaps
  - Estrategias de mitigación para gaps
  - Recomendaciones accionables priorizadas
  - Análisis detallado requisito por requisito
- ✅ **Transparencia Total:** Cada puntuación explica cómo se calculó y qué evidencia la respalda
- ✅ **Integración Automática:** Se ejecuta automáticamente en el flujo de GitHub Actions

#### Fase 5: Formato Profesional ATS-Friendly en PDF (NUEVO ✅)
- ✅ **Header Centrado y Profesional:** Nombre destacado, información de contacto centrada
- ✅ **Compatible con ATS:** Sin enlaces azules, fuentes estándar, formato limpio
- ✅ **Tipografía Mejorada:** LaTeX/XeTeX para apariencia profesional
- ✅ **Líneas Horizontales Rectas:** Separadores limpios y consistentes
- ✅ **Márgenes Optimizados:** 0.75 pulgadas, formato estándar
- ✅ **Enlaces en Negro:** Todos los enlaces en color negro para ATS
- ✅ **Documentación Completa:** Guías de uso y personalización incluidas

### 📁 Documentación Completa

- **[DIAGNOSTIC_REPORT.md](DIAGNOSTIC_REPORT.md):** Diagnóstico completo del sistema de generación de CVs, identificación de limitaciones y propuestas de mejora
- **[BEFORE_AFTER_COMPARISON.md](BEFORE_AFTER_COMPARISON.md):** Ejemplos comparativos mostrando el antes y después de las mejoras
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md):** Guía técnica de implementación, uso y mantenimiento del sistema
- **[PHASE4_SCORING_SYSTEM_DESIGN.md](PHASE4_SCORING_SYSTEM_DESIGN.md):** Diseño completo del sistema de scoring multi-dimensional (Fase 4)
- **[CV_PDF_FORMATTING.md](CV_PDF_FORMATTING.md):** Documentación técnica del formato profesional de PDF (Fase 5)
- **[GUIA_FORMATO_CV.md](GUIA_FORMATO_CV.md):** Guía de usuario sobre el formato profesional ATS-friendly en PDF

### 🎯 Ejemplo de Mejora

**ANTES:**
```markdown
- Demonstrated experience in build and maintain custom dashboards..
```

**DESPUÉS (CV Personalizado):**
```markdown
**Build and maintain custom dashboards to support business operations**

Architected consolidated dashboard integrating 8 data sources, cutting data preparation time by 70%
```

**NUEVO (Scoring Report):**
```markdown
## Overall Match Score: 75.5% - STRONG FIT 🟢

### Dimensional Analysis

1. Technical Skills Match: 85% 🟢 (Contribution: 25.5%)
   ✅ Matched: dashboard, sql, etl, automation
   
2. Experience Depth: 90% 🟢 (Contribution: 22.5%)
   5+ years with 6 quantifiable achievements
   
3. Domain Knowledge: 75% 🟢 (Contribution: 15.0%)
   
4. Soft Skills: 70% 🟢 (Contribution: 10.5%)
   
5. Achievement Quality: 75% 🟢 (Contribution: 7.5%)

### Key Strengths
✅ Dashboard Expertise: 8 data sources integrated, 70% time reduction
✅ Automation Track Record: 60-75% time savings demonstrated

### Actionable Recommendations
🔴 [High] Prepare 2-3 stories highlighting dashboard & automation experience
🟡 [Medium] Review Zapier basics (30 minutes)
```

### 🔧 Uso

El sistema funciona automáticamente:

1. Coloca un archivo YAML en `to_process/` con los datos de la vacante
2. GitHub Actions procesa automáticamente el archivo
3. Se genera una carpeta en `to_process_procesados/` con:
   - **CV personalizado** en Markdown y PDF
   - **Reporte de scoring** en Markdown y PDF
   - Descripción de la vacante
   - Lista de requerimientos

### 🛠️ Componentes Técnicos

**Personalización:**
- **Motor de Personalización:** `aplicaciones_laborales/scripts/cv_personalization_engine.py`
- **Script Principal:** `aplicaciones_laborales/scripts/procesar_aplicacion.py`
- **Template:** `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md`

**Scoring (Nuevo):**
- **Motor de Scoring:** `aplicaciones_laborales/scripts/scoring_engine.py`
- **Generador de Reportes:** `aplicaciones_laborales/scripts/scoring_report_generator.py`
- **Tests:** `aplicaciones_laborales/scripts/test_scoring_engine.py`
- **Workflow:** `.github/workflows/crear_aplicacion.yml`

### 📈 Roadmap Futuro

- **Fase 5:** Análisis semántico avanzado con embeddings (opcional)
- **Fase 6:** Feedback loop y calibración automática de pesos
- **Fase 7:** Dashboard de métricas y tracking de aplicaciones
- **Fase 8:** Integración con APIs externas para benchmarking

---

Para más detalles, consulta la documentación completa en los archivos mencionados arriba.
