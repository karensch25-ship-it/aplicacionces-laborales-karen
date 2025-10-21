# Guía de Uso del Sistema Mejorado de Generación de CV PDF

## Cómo Usar el Sistema

### 1. Crear una Nueva Aplicación

Crea un archivo YAML en `to_process/` con el siguiente formato:

```yaml
cargo: "Nombre del Cargo"
empresa: "Nombre de la Empresa"
fecha: "YYYY-MM-DD"
descripcion: "Descripción del puesto..."

requerimientos:
- Primer requerimiento
- Segundo requerimiento
- Tercer requerimiento
```

### 2. Commit y Push

```bash
git add to_process/mi_aplicacion.yaml
git commit -m "Nueva aplicación: Cargo en Empresa"
git push
```

### 3. El Workflow Procesará Automáticamente

GitHub Actions detectará el nuevo YAML y ejecutará el procesamiento.

## Qué Esperar - Logs del Workflow

### Logs de Éxito ✅

```
============================================================
PROCESAMIENTO DE APLICACIÓN LABORAL
============================================================
Archivo YAML: to_process/nueva_aplicacion.yaml

📋 Detalles de la aplicación:
   Cargo: Billing Analyst
   Empresa: Tata Consultancy Services
   Fecha: 2025-10-21
   Carpeta destino: BillingAnalyst_TataConsultancyServices_2025-10-21
============================================================

✓ Carpeta de salida creada: to_process_procesados/BillingAnalyst_TataConsultancyServices_2025-10-21

📝 Generando descripcion.md...
   ✓ descripcion.md creado

📝 Generando requerimientos.md...
   ✓ requerimientos.md creado (7 requerimientos)

📝 Generando hoja_de_vida_adecuada.md...
   ✓ Plantilla Harvard encontrada: aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md
   🔄 Generando sección de alineación con el puesto...
   🔄 Generando resumen profesional personalizado...
   ✓ hoja_de_vida_adecuada.md creada y personalizada

============================================================
GENERACIÓN DE REPORTE DE SCORING
============================================================
✅ Reporte de Scoring generado exitosamente
   Puntuación Global: 65%
   Recomendación: RECOMENDADA
   Archivo: scoring_report.md
============================================================

============================================================
GENERACIÓN DE PDF DE HOJA DE VIDA
============================================================
Archivo fuente: to_process_procesados/.../hoja_de_vida_adecuada.md
Archivo destino: to_process_procesados/.../KAREN_SCHMALBACH_TataConsultancyServices.pdf
Nombre estándar: KAREN_SCHMALBACH_TataConsultancyServices.pdf
============================================================

ℹ️  No se encontró header LaTeX personalizado en aplicaciones_laborales/plantillas/cv_header.tex

🔄 Ejecutando pandoc para generar PDF...
   Comando: pandoc ... -o ... --pdf-engine=xelatex ...
✅ CV PDF generado exitosamente!
   Archivo: KAREN_SCHMALBACH_TataConsultancyServices.pdf
   Tamaño: 23,529 bytes
   Ruta completa: to_process_procesados/.../KAREN_SCHMALBACH_TataConsultancyServices.pdf

============================================================
GENERACIÓN DE PDF DE SCORING REPORT
============================================================
🔄 Generando PDF del reporte de scoring...
✅ Scoring Report PDF generado exitosamente
   Archivo: SCORING_REPORT.pdf
   Tamaño: 23,075 bytes
============================================================

📦 Moviendo archivo YAML procesado a la carpeta de salida...
   ✓ YAML movido a: to_process_procesados/.../nueva_aplicacion.yaml

============================================================
✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE
============================================================
Carpeta de salida: to_process_procesados/BillingAnalyst_TataConsultancyServices_2025-10-21

Archivos generados:
   ✓ descripcion.md
   ✓ requerimientos.md
   ✓ hoja_de_vida_adecuada.md
   ✓ KAREN_SCHMALBACH_TataConsultancyServices.pdf
   ✓ scoring_report.md
   ✓ SCORING_REPORT.pdf

Próximos pasos:
   - El workflow copiará estos archivos a: aplicaciones/2025-10-21/BillingAnalyst_TataConsultancyServices_2025-10-21/
   - El PDF principal es: KAREN_SCHMALBACH_TataConsultancyServices.pdf
============================================================
```

### Logs de Error - YAML Inválido ❌

```
============================================================
PROCESAMIENTO DE APLICACIÓN LABORAL
============================================================
Archivo YAML: to_process/aplicacion_mala.yaml

❌ ERROR: Formato YAML inválido en to_process/aplicacion_mala.yaml
   Detalle: while parsing a block mapping
  in "<unicode string>", line 1, column 1:
    cargo "Missing colon"
           ^
expected <block end>, but found '<scalar>'
```

### Logs de Error - Campos Faltantes ❌

```
============================================================
PROCESAMIENTO DE APLICACIÓN LABORAL
============================================================
Archivo YAML: to_process/aplicacion_incompleta.yaml

❌ ERROR: Campos requeridos faltantes en YAML: empresa, fecha
```

### Logs de Error - Fallo en Pandoc ❌

```
============================================================
GENERACIÓN DE PDF DE HOJA DE VIDA
============================================================
Archivo fuente: to_process_procesados/.../hoja_de_vida_adecuada.md
Archivo destino: to_process_procesados/.../KAREN_SCHMALBACH_Empresa.pdf
Nombre estándar: KAREN_SCHMALBACH_Empresa.pdf
============================================================

🔄 Ejecutando pandoc para generar PDF...
   Comando: pandoc ... -o ... --pdf-engine=xelatex ...

❌ ERROR CRÍTICO al convertir a PDF con pandoc
============================================================
Código de salida: 43
STDERR:
Error producing PDF.
! LaTeX Error: File `...` not found.
============================================================

🔍 DIAGNÓSTICO:
   1. Verificar que pandoc está instalado correctamente
   2. Verificar que xelatex está instalado (texlive-xetex)
   3. Revisar el contenido del archivo markdown por errores de sintaxis
   4. Verificar que las fuentes necesarias están disponibles

❌ El proceso se detiene aquí. No se puede continuar sin el PDF.
```

## Archivos Generados

Después de un procesamiento exitoso, encontrarás:

### En `to_process_procesados/{Cargo}_{Empresa}_{Fecha}/`

1. **KAREN_SCHMALBACH_{Empresa}.pdf** ⭐
   - CV principal en formato PDF
   - Nombre estandarizado para fácil identificación
   - Contenido 100% en español
   - Información de Karen Schmalbach

2. **SCORING_REPORT.pdf**
   - Reporte de análisis de coincidencia
   - Puntuación y recomendación
   - Análisis de habilidades

3. **hoja_de_vida_adecuada.md**
   - CV en formato markdown
   - Personalizado para el puesto
   - Sección de alineación con requerimientos

4. **scoring_report.md**
   - Reporte de scoring en markdown
   - Recomendaciones detalladas

5. **descripcion.md**
   - Descripción del puesto

6. **requerimientos.md**
   - Lista de requerimientos

7. **{nombre_original}.yaml**
   - YAML original movido aquí

### En `aplicaciones/{YYYY-MM-DD}/{Cargo}_{Empresa}_{Fecha}/`

Copia de todos los archivos anteriores, organizada por fecha de aplicación.

## Características del CV Generado

### Nombre del Archivo
- **Formato:** `KAREN_SCHMALBACH_{NombreEmpresa}.pdf`
- **Ejemplo:** `KAREN_SCHMALBACH_TataConsultancyServices.pdf`

### Contenido
- ✅ Nombre: KAREN SCHMALBACH (en el header)
- ✅ Idioma: 100% Español
- ✅ Secciones:
  - Perfil Profesional (personalizado por puesto)
  - Habilidades Clave
  - Experiencia Profesional
  - Formación Académica
  - Certificaciones
  - Idiomas
  - Desarrollo Profesional Continuo
  - **Cómo mi experiencia se alinea con este puesto** (personalizado)
  - Notas adicionales

### Personalización Automática

El sistema personaliza automáticamente:

1. **Perfil Profesional**
   - Se ajusta según los requerimientos del puesto
   - Destaca experiencia relevante

2. **Sección de Alineación**
   - Mapea cada requerimiento a experiencia de Karen
   - Explica cómo las competencias aplican al puesto

3. **Scoring**
   - Analiza coincidencia de palabras clave
   - Proporciona recomendación (Alta/Media/Baja)
   - Identifica habilidades coincidentes

## Solución de Problemas

### El PDF no se genera

**Síntoma:** El workflow falla en la generación del PDF

**Posibles causas:**
1. Pandoc o LaTeX no instalados en el entorno
2. Error de sintaxis en el markdown generado
3. Fuente LaTeX no disponible

**Solución:** Revisar logs del workflow en GitHub Actions

### El PDF tiene nombre incorrecto

**Antes (Incorrecto):** `ANTONIO_GUTIERREZ_RESUME_Empresa.pdf`
**Ahora (Correcto):** `KAREN_SCHMALBACH_Empresa.pdf`

Si ves el nombre incorrecto, es un bug que debe reportarse.

### El contenido está en inglés

**Síntoma:** Partes del CV aparecen en inglés

**Causa:** Template incorrecto o código de personalización con bug

**Solución:** Verificar que se usa el template correcto en `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md`

## Soporte

Para problemas o preguntas:

1. Revisar este documento
2. Revisar `CAMBIOS_PDF_GENERATION.md` para detalles técnicos
3. Revisar logs del workflow en GitHub Actions
4. Crear un issue en el repositorio con:
   - Logs completos del workflow
   - Archivo YAML usado
   - Comportamiento esperado vs. observado
