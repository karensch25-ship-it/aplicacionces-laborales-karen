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

**NOTA:** El workflow CI/CD ha sido mejorado para garantizar que SIEMPRE detecta y procesa archivos YAML modificados o nuevos. Ver `MEJORAS_WORKFLOW_DETECCION_YAML.md` para detalles completos de las mejoras.

#### Características de Detección Robusta:
- ✅ Detecta nuevos archivos YAML
- ✅ Detecta modificaciones en archivos existentes
- ✅ Detecta archivos renombrados
- ✅ Funciona en primer commit de rama
- ✅ Funciona con force pushes
- ✅ Fallback automático si la detección falla
- ✅ Logs detallados de todo el proceso

## Qué Esperar - Logs del Workflow

### Logs de Detección de Archivos 🔍

El workflow ahora muestra información detallada sobre la detección de archivos:

```
============================================================
DETECCIÓN DE ARCHIVOS YAML MODIFICADOS
============================================================
📋 Información del contexto de GitHub Actions:
   Event: push
   Before SHA: abc123def456...
   Current SHA: def456abc789...
   Ref: refs/heads/main

📋 Estado actual del repositorio:
def456a Latest commit message
abc123d Previous commit message

📋 Archivos YAML existentes en to_process/:
-rw-r--r-- 1 runner runner 1234 Oct 21 10:00 nueva_aplicacion.yaml

🔍 Detectando cambios usando git diff...
   Comando: git diff --name-only abc123def456 def456abc789
   ✓ Git diff ejecutado exitosamente

============================================================
✅ Archivos YAML detectados para procesar: 1
============================================================
to_process/nueva_aplicacion.yaml
============================================================

🔄 Iniciando procesamiento de archivos...

-----------------------------------------------------------
📄 Procesando: to_process/nueva_aplicacion.yaml
   ✓ Archivo existe en el workspace
```

Después de esto, verás los logs de procesamiento de cada archivo individual.

### Logs de Resumen del Procesamiento 📊

Al final del procesamiento de archivos:

```
============================================================
📊 RESUMEN DEL PROCESAMIENTO
============================================================
   Total archivos detectados: 1
   Procesados exitosamente: 1
   Fallidos: 0

   Carpetas generadas:
      - BillingAnalyst_TataConsultancyServices_2025-10-21
============================================================
```

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

1. **KAREN_SCHMALBACH_{Empresa}_es.pdf** ⭐
   - CV en formato PDF en ESPAÑOL
   - Nombre estandarizado para fácil identificación
   - Contenido 100% en español profesional
   - Listo para aplicaciones en mercado hispanohablante

2. **KAREN_SCHMALBACH_{Empresa}_en.pdf** ⭐
   - CV en formato PDF en INGLÉS
   - Nombre estandarizado para fácil identificación
   - Contenido 100% en inglés profesional
   - Listo para aplicaciones en mercado internacional

3. **SCORING_REPORT.pdf**
   - Reporte de análisis de coincidencia
   - Puntuación y recomendación
   - Análisis de habilidades

4. **hoja_de_vida_adecuada.md**
   - CV en formato markdown en español
   - Personalizado para el puesto
   - Sección de alineación con requerimientos

5. **hoja_de_vida_adecuada_en.md**
   - CV en formato markdown en inglés
   - Personalizado para el puesto
   - Sección de alineación con requerimientos en inglés

6. **scoring_report.md**
   - Reporte de scoring en markdown
   - Recomendaciones detalladas

7. **descripcion.md**
   - Descripción del puesto

8. **requerimientos.md**
   - Lista de requerimientos

9. **{nombre_original}.yaml**
   - YAML original movido aquí

### En `aplicaciones/{YYYY-MM-DD}/{Cargo}_{Empresa}_{Fecha}/`

Copia de todos los archivos anteriores, organizada por fecha de aplicación.

## 🌍 Generación Bilingüe Automática

El sistema genera **automáticamente dos versiones completas** de tu hoja de vida:

### Versión en Español
- ✅ Archivo: `KAREN_SCHMALBACH_{Empresa}_es.pdf`
- ✅ Contenido 100% profesional en español
- ✅ Optimizada para aplicaciones en mercado hispanohablante
- ✅ Incluye todas las secciones traducidas y personalizadas

### Versión en Inglés
- ✅ Archivo: `KAREN_SCHMALBACH_{Empresa}_en.pdf`
- ✅ Contenido 100% profesional en inglés
- ✅ Optimizada para aplicaciones en mercado internacional
- ✅ Traducción profesional de toda la información
- ✅ Incluye todas las secciones traducidas y personalizadas

### Ventajas de la Generación Bilingüe
- 🎯 **Sin esfuerzo adicional**: Ambas versiones se generan automáticamente en cada aplicación
- 🌐 **Alcance global**: Lista para aplicar a empresas nacionales e internacionales
- 📋 **Consistencia**: Ambas versiones mantienen la misma estructura profesional
- ✨ **Personalización inteligente**: El sistema adapta el contenido según los requerimientos en ambos idiomas

## Características del CV Generado

### Nombre de los Archivos
- **Formato Español:** `KAREN_SCHMALBACH_{NombreEmpresa}_es.pdf`
- **Formato Inglés:** `KAREN_SCHMALBACH_{NombreEmpresa}_en.pdf`
- **Ejemplos:** 
  - `KAREN_SCHMALBACH_TataConsultancyServices_es.pdf`
  - `KAREN_SCHMALBACH_TataConsultancyServices_en.pdf`

### Contenido
- ✅ Nombre: KAREN SCHMALBACH (en el header)
- ✅ **Generación Bilingüe Automática**: Se generan dos versiones completas
  - **Español**: `KAREN_SCHMALBACH_{Empresa}_es.pdf`
  - **Inglés**: `KAREN_SCHMALBACH_{Empresa}_en.pdf`
- ✅ Secciones (en ambos idiomas):
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

### El workflow no detecta mi archivo YAML

**Síntoma:** Hiciste push de un archivo YAML pero el workflow no lo procesa.

**Soluciones:**

1. **Verifica que el archivo está en la carpeta correcta:**
   ```bash
   # Debe estar en: to_process/mi_aplicacion.yaml
   # NO en: aplicaciones/, aplicaciones_laborales/, etc.
   ```

2. **Verifica la extensión del archivo:**
   ```bash
   # Correcto: .yaml
   # Incorrecto: .yml, .YAML, .txt
   ```

3. **Revisa los logs del workflow:**
   - Ve a GitHub Actions en tu repositorio
   - Busca el último workflow run
   - Revisa la sección "DETECCIÓN DE ARCHIVOS YAML MODIFICADOS"
   - Verifica que tu archivo aparece listado

4. **Situaciones especiales (el workflow tiene fallback automático):**
   - Primer commit de rama: El workflow procesará TODOS los YAML
   - Force push: El workflow procesará TODOS los YAML
   - Si git diff falla: El workflow procesará TODOS los YAML

5. **Forzar procesamiento si es necesario:**
   ```bash
   # Opción 1: Modificar contenido (agregar comentario)
   echo "# Updated $(date)" >> to_process/mi_aplicacion.yaml
   git add to_process/mi_aplicacion.yaml
   git commit -m "Force reprocess"
   git push
   
   # Opción 2: Renombrar el archivo
   git mv to_process/app.yaml to_process/app_v2.yaml
   git commit -m "Rename to force reprocess"
   git push
   ```

### El workflow dice "No hay archivos YAML para procesar"

**Síntoma:** El workflow ejecuta pero dice que no hay archivos para procesar.

**Explicación:** Esto es NORMAL si:
- No modificaste ningún archivo YAML en `to_process/`
- Solo modificaste archivos en otras carpetas
- Ya procesaste estos archivos en un commit anterior

**Para verificar:**
```bash
# Ver qué archivos cambiaron en el último commit
git diff --name-only HEAD~1 HEAD

# Ver solo archivos YAML en to_process/
git diff --name-only HEAD~1 HEAD | grep 'to_process/.*\.yaml'
```

### El PDF no se genera

**Síntoma:** El workflow falla en la generación del PDF

**Posibles causas:**
1. Pandoc o LaTeX no instalados en el entorno
2. Error de sintaxis en el markdown generado
3. Fuente LaTeX no disponible

**Solución:** Revisar logs del workflow en GitHub Actions

### El PDF tiene nombre incorrecto

**Antes (Incorrecto):** `ANTONIO_GUTIERREZ_RESUME_Empresa.pdf`
**Ahora (Correcto - Español):** `KAREN_SCHMALBACH_Empresa_es.pdf`
**Ahora (Correcto - Inglés):** `KAREN_SCHMALBACH_Empresa_en.pdf`

Si ves el nombre incorrecto, es un bug que debe reportarse.

### No se genera la versión en inglés

**Síntoma:** Solo se genera el PDF en español

**Posibles causas:**
1. La plantilla en inglés no existe en `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template_en.md`
2. Error durante la generación del CV en inglés

**Solución:** 
- Revisar los logs del workflow para ver mensajes de error
- Verificar que ambas plantillas existen en la carpeta `aplicaciones_laborales/plantillas/`
- La versión en español se generará siempre, la versión en inglés es adicional

### El contenido tiene idiomas mezclados

**Síntoma:** Partes del CV aparecen en español y otras en inglés

**Causa:** Template incorrecto o error en el motor de personalización

**Solución:** Verificar que se usan los templates correctos:
- Español: `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md`
- Inglés: `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template_en.md`

## Soporte

Para problemas o preguntas:

1. Revisar este documento
2. Revisar `CAMBIOS_PDF_GENERATION.md` para detalles técnicos
3. Revisar logs del workflow en GitHub Actions
4. Crear un issue en el repositorio con:
   - Logs completos del workflow
   - Archivo YAML usado
   - Comportamiento esperado vs. observado
