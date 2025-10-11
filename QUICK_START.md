# 🚀 Quick Start: Sistema de Personalización de CVs

Esta guía te ayudará a comenzar a usar el sistema de generación automática de hojas de vida personalizadas en menos de 5 minutos.

---

## 📋 Paso 1: Crear Archivo YAML con los Datos de la Vacante

Crea un archivo en la carpeta `to_process/` con el siguiente formato:

**Nombre del archivo:** `nueva_aplicacion_[nombre].yaml`

**Contenido:**

```yaml
cargo: "Data Analyst"
empresa: "TechCorp Inc"
fecha: "2025-10-15"
descripcion: |
  We are looking for a talented Data Analyst to join our team...
  (Pega aquí la descripción completa de la vacante)

requerimientos:
  - Build and maintain dashboards for business intelligence
  - Strong SQL skills for data analysis and reporting
  - Experience with ETL processes and data automation
  - Collaborate with stakeholders to understand data needs
  - Knowledge of Power BI, Tableau, or similar tools
```

### 💡 Tips para Mejores Resultados

1. **Copia los requisitos exactamente como aparecen en la oferta**
   - El sistema detecta keywords automáticamente
   - Más detalle = mejor matching

2. **Incluye tanto requisitos obligatorios como deseables**
   - Marca los opcionales con "Bonus:" si quieres
   - Ejemplo: `- Bonus: Experience with machine learning`

3. **No te preocupes por el formato**
   - El sistema maneja strings simples o estructuras complejas
   - Soporta requisitos en formato de lista o diccionarios

---

## ⚙️ Paso 2: El Sistema Procesa Automáticamente

Una vez que hagas push del archivo YAML:

1. **GitHub Actions se activa automáticamente**
2. **Procesa el archivo** con el motor de personalización
3. **Genera los siguientes archivos** en `to_process_procesados/[Cargo_Empresa_Fecha]/`:
   - `descripcion.md` - Descripción de la vacante
   - `requerimientos.md` - Lista de requisitos
   - `hoja_de_vida_adecuada.md` - CV personalizado en Markdown
   - `ANTONIO_GUTIERREZ_RESUME_[Empresa].pdf` - CV en PDF

### ⏱️ Tiempo de Procesamiento

- **Típicamente:** 2-3 minutos
- **Puedes verificar el progreso** en la pestaña "Actions" de GitHub

---

## 📊 Paso 3: Revisar el CV Generado

### ✅ Qué Esperar en el CV Personalizado

**Professional Summary Personalizado:**
```markdown
## Professional Summary

Data Analyst with 5+ years of experience specializing in business intelligence 
and dashboard development and data automation and ETL processes. Proven track 
record in delivering data-driven solutions...
```

**Job Alignment con Evidencia Concreta:**
```markdown
## How My Experience Aligns with This Role

**Build and maintain dashboards for business intelligence**

Architected consolidated dashboard integrating 8 data sources, cutting data 
preparation time by 70%

**Strong SQL skills for data analysis and reporting**

Built 20+ SQL stored procedures, improving query performance by 40% and 
reducing error rates by 75%
```

### 🎯 Indicadores de Buena Personalización

- ✅ Summary menciona competencias clave de la oferta
- ✅ Cada requisito tiene evidencia con métricas específicas
- ✅ No hay errores gramaticales
- ✅ Logros son relevantes y cuantificables

---

## 🔍 Paso 4: Evaluar el Match Score (Opcional)

Para conocer el porcentaje de compatibilidad con la vacante, ejecuta:

```bash
python aplicaciones_laborales/scripts/cv_personalization_engine.py
```

Esto mostrará:
```
Match Percentage: 75.0%
Strong Matches: 4
Moderate Matches: 2
Weak Matches: 1
Recommendation: Strong fit
```

### 📈 Interpretación del Score

- **≥70%:** Strong fit - ¡Aplica con confianza!
- **50-69%:** Good fit - Buena oportunidad
- **<50%:** Moderate fit - Evalúa si aplicar

---

## 🛠️ Troubleshooting Rápido

### Problema: "No se generó el CV"

**Solución:**
1. Verifica que el archivo YAML esté en `to_process/`
2. Revisa el formato del YAML (usa un validador online)
3. Comprueba GitHub Actions para ver errores

### Problema: "Requisitos sin evidencia concreta"

**Solución:**
- Algunos requisitos muy específicos pueden no tener match directo
- El sistema usa un fallback genérico pero profesional
- Para mejorar: actualiza `achievement_mapping` en `cv_personalization_engine.py`

### Problema: "Professional Summary no parece personalizado"

**Solución:**
- Verifica que los requisitos incluyan keywords técnicos
- Ejemplo: En lugar de "Experiencia en datos", usa "Experience with SQL, Power BI, and ETL processes"

---

## 📚 Ejemplo Completo

### Input: nueva_aplicacion_ejemplo.yaml

```yaml
cargo: "Senior BI Analyst"
empresa: "DataCorp Solutions"
fecha: "2025-10-15"
descripcion: |
  DataCorp Solutions is seeking a Senior BI Analyst to lead our analytics team.
  You will be responsible for developing dashboards, automating reports, and
  providing data-driven insights to executive leadership.

requerimientos:
  - 5+ years experience in business intelligence and data analysis
  - Expert-level SQL for complex queries and stored procedures
  - Proficiency with Power BI or Tableau for dashboard development
  - Experience with ETL processes and data pipeline automation
  - Strong stakeholder management and communication skills
  - Knowledge of Python or R for advanced analytics
  - Bonus: Experience with cloud data platforms (AWS, Azure, GCP)
```

### Output Generado

**Carpeta:** `to_process_procesados/SeniorBIAnalyst_DataCorpSolutions_2025-10-15/`

**Professional Summary (Personalizado):**
```markdown
Data Analyst with 5+ years of experience specializing in business intelligence 
and dashboard development and data automation and ETL processes. Proven track 
record in delivering data-driven solutions that reduce operational costs, 
improve decision-making accuracy, and drive business outcomes...
```

**Job Alignment (Con Evidencia):**
```markdown
**5+ years experience in business intelligence and data analysis**

Implemented sales and inventory dashboards for Latin America, reducing 
decision-making time by 40%

**Expert-level SQL for complex queries and stored procedures**

Built 20+ SQL stored procedures, improving query performance by 40% and 
reducing error rates by 75%

**Proficiency with Power BI or Tableau for dashboard development**

Implemented sales and inventory dashboards for Latin America, reducing 
decision-making time by 40%

**Experience with ETL processes and data pipeline automation**

Automated ETL processes, reducing daily processing time from 4 hours to 30 minutes
```

---

## 🎓 Mejores Prácticas

### ✅ DO: Hacer

1. **Copiar requisitos tal cual de la oferta**
   - Incluye detalles técnicos específicos
   - Ejemplo: "Experience with SQL (joins, CTEs, window functions)"

2. **Incluir tanto requisitos hard skills como soft skills**
   - Hard: "SQL, Power BI, Python"
   - Soft: "Stakeholder management, collaboration"

3. **Revisar el CV generado antes de enviarlo**
   - Verifica que los matches sean relevantes
   - Ajusta manualmente si es necesario

### ❌ DON'T: Evitar

1. **No uses requisitos demasiado genéricos**
   - ❌ "Experiencia con datos"
   - ✅ "Experience with SQL databases and data warehousing"

2. **No omitas requisitos importantes**
   - Incluye todos, incluso si no tienes match perfecto
   - El sistema manejará los gaps apropiadamente

3. **No edites directamente el template**
   - Usa el YAML para todos los cambios
   - El template debe permanecer genérico

---

## 🔄 Workflow Completo

```
1. Crear YAML → 2. Push a GitHub → 3. Actions procesa → 4. CV generado → 5. Descargar PDF
    (2 min)          (instantáneo)        (2-3 min)         (automático)      (listo!)
```

**Tiempo total:** ~5 minutos desde que creas el YAML hasta tener el PDF listo

---

## 📞 Soporte y Documentación

- **Problema técnico?** Revisa `IMPLEMENTATION_GUIDE.md`
- **Quieres ver ejemplos?** Consulta `BEFORE_AFTER_COMPARISON.md`
- **Entender el diagnóstico?** Lee `DIAGNOSTIC_REPORT.md`
- **Mejorar el sistema?** Actualiza `cv_personalization_engine.py`

---

## 🎯 Próximos Pasos

Una vez que domines el uso básico:

1. **Personaliza el motor** agregando tus propios logros
2. **Experimenta con diferentes vacantes** para ver el nivel de matching
3. **Compara CVs** generados para diferentes roles
4. **Mantén actualizado** el `achievement_mapping` con nuevas experiencias

---

**¡Listo para comenzar! 🚀**

Crea tu primer YAML y observa cómo el sistema genera un CV profesional y personalizado en minutos.
