# aplicaciones_laborales

En este repo yacen todas las aplicaciones laborales realizadas

## 🚀 Mejoras Recientes: Sistema de Personalización Inteligente

Este repositorio ahora incluye un **motor de personalización avanzado** que genera hojas de vida verdaderamente adaptadas a cada vacante, eliminando la simple copia de requisitos y conectando la experiencia del candidato con las necesidades específicas del puesto.

### 📊 Mejoras Implementadas (Fase 1)

- ✅ **Professional Summary Personalizado:** Se genera dinámicamente según los requisitos de cada vacante
- ✅ **Job Alignment Inteligente:** Mapea requisitos a logros reales con evidencia cuantificable
- ✅ **Sin Errores Gramaticales:** Corrección completa de problemas de redacción
- ✅ **Evidencia Concreta:** En lugar de "Demonstrated experience in...", muestra logros específicos con métricas
- ✅ **Nivel de Personalización:** Incrementado de 5% a 65%

### 📁 Documentación Completa

- **[DIAGNOSTIC_REPORT.md](DIAGNOSTIC_REPORT.md):** Diagnóstico completo del sistema de generación de CVs, identificación de limitaciones y propuestas de mejora
- **[BEFORE_AFTER_COMPARISON.md](BEFORE_AFTER_COMPARISON.md):** Ejemplos comparativos mostrando el antes y después de las mejoras
- **[IMPLEMENTATION_GUIDE.md](IMPLEMENTATION_GUIDE.md):** Guía técnica de implementación, uso y mantenimiento del sistema

### 🎯 Ejemplo de Mejora

**ANTES:**
```markdown
- Demonstrated experience in build and maintain custom dashboards..
```

**DESPUÉS:**
```markdown
**Build and maintain custom dashboards to support business operations**

Architected consolidated dashboard integrating 8 data sources, cutting data preparation time by 70%
```

### 🔧 Uso

El sistema funciona automáticamente:

1. Coloca un archivo YAML en `to_process/` con los datos de la vacante
2. GitHub Actions procesa automáticamente el archivo
3. Se genera una carpeta en `to_process_procesados/` con:
   - CV personalizado en Markdown y PDF
   - Descripción de la vacante
   - Lista de requerimientos

### 🛠️ Componentes Técnicos

- **Motor de Personalización:** `aplicaciones_laborales/scripts/cv_personalization_engine.py`
- **Script Principal:** `aplicaciones_laborales/scripts/procesar_aplicacion.py`
- **Template:** `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md`
- **Workflow:** `.github/workflows/crear_aplicacion.yml`

### 📈 Roadmap Futuro

- **Fase 2:** Priorización inteligente de experiencias por relevancia
- **Fase 3:** Integración con IA (GPT-4) para personalización avanzada
- **Fase 4:** Sistema de scoring automático y optimización para ATS

---

Para más detalles, consulta la documentación completa en los archivos mencionados arriba.
