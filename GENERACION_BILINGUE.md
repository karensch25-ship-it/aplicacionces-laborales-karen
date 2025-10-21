# 🌍 Generación Automática de Hoja de Vida Bilingüe

## Descripción

El sistema de aplicaciones laborales ahora genera **automáticamente dos versiones completas** de la hoja de vida en cada ejecución del pipeline:

- 🇪🇸 **Versión en Español**: Optimizada para aplicaciones en mercado hispanohablante
- 🇬🇧 **Versión en Inglés**: Optimizada para aplicaciones en mercado internacional

## Ventajas

### ✅ Generación Automática
- No requiere configuración adicional
- No requiere intervención manual
- Ambas versiones se generan en cada aplicación

### ✅ Profesionalismo Garantizado
- Traducciones profesionales y revisadas
- Consistencia en estructura y formato
- Nombres estandarizados y diferenciados

### ✅ Personalización Inteligente
- Ambas versiones se personalizan según los requerimientos del puesto
- Secciones de alineación adaptadas en cada idioma
- Resumen profesional personalizado en ambos idiomas

### ✅ Alcance Global
- Lista para aplicar a empresas nacionales
- Lista para aplicar a empresas internacionales
- Un solo proceso genera ambas versiones

## Archivos Generados

### En Cada Aplicación

El sistema genera los siguientes archivos en la carpeta de cada aplicación:

```
aplicaciones/YYYY-MM-DD/{Cargo}_{Empresa}_{Fecha}/
├── KAREN_SCHMALBACH_{Empresa}_es.pdf    ⭐ CV en español
├── KAREN_SCHMALBACH_{Empresa}_en.pdf    ⭐ CV en inglés
├── hoja_de_vida_adecuada.md             📄 Markdown español
├── hoja_de_vida_adecuada_en.md          📄 Markdown inglés
├── SCORING_REPORT.pdf
├── scoring_report.md
├── descripcion.md
├── requerimientos.md
└── {archivo_original}.yaml
```

## Nomenclatura de Archivos

### Versión Español
- **Formato**: `KAREN_SCHMALBACH_{NombreEmpresa}_es.pdf`
- **Ejemplos**:
  - `KAREN_SCHMALBACH_TataConsultancyServices_es.pdf`
  - `KAREN_SCHMALBACH_Microsoft_es.pdf`
  - `KAREN_SCHMALBACH_Google_es.pdf`

### Versión Inglés
- **Formato**: `KAREN_SCHMALBACH_{NombreEmpresa}_en.pdf`
- **Ejemplos**:
  - `KAREN_SCHMALBACH_TataConsultancyServices_en.pdf`
  - `KAREN_SCHMALBACH_Microsoft_en.pdf`
  - `KAREN_SCHMALBACH_Google_en.pdf`

## Contenido de las Versiones

### Secciones Incluidas (Ambos Idiomas)

Ambas versiones incluyen todas las secciones completamente traducidas:

#### 1. Perfil Profesional
- **Español**: "Perfil Profesional"
- **Inglés**: "Professional Summary"
- Personalizado según los requerimientos del puesto

#### 2. Habilidades Clave
- **Español**: "Habilidades Clave"
- **Inglés**: "Key Skills"
- Incluye todas las competencias técnicas y blandas

#### 3. Experiencia Profesional
- **Español**: "Experiencia Profesional"
- **Inglés**: "Professional Experience"
- Historial completo de trabajo traducido

#### 4. Formación Académica
- **Español**: "Formación Académica"
- **Inglés**: "Education"
- Títulos y certificaciones

#### 5. Certificaciones
- **Español**: "Certificaciones"
- **Inglés**: "Certifications"

#### 6. Idiomas
- **Español**: "Idiomas"
- **Inglés**: "Languages"

#### 7. Desarrollo Profesional Continuo
- **Español**: "Desarrollo Profesional Continuo"
- **Inglés**: "Continuous Professional Development"

#### 8. Alineación con el Puesto
- **Español**: "Cómo mi experiencia se alinea con este puesto"
- **Inglés**: "How My Experience Aligns with This Position"
- **✨ Personalización inteligente**: Esta sección mapea cada requerimiento del puesto con la experiencia relevante de Karen, en el idioma correspondiente

#### 9. Notas Adicionales
- **Español**: "Notas adicionales"
- **Inglés**: "Additional Notes"

## Personalización Inteligente por Idioma

### Motor de Personalización

El sistema incluye un motor de personalización que adapta el contenido según:

1. **Requerimientos del Puesto**: Analiza las palabras clave en los requerimientos
2. **Experiencia Relevante**: Mapea cada requerimiento con la experiencia de Karen
3. **Idioma de Salida**: Genera la explicación en español o inglés según corresponda

### Ejemplo de Personalización

Para un requerimiento: "Experiencia en conciliaciones bancarias"

**Versión Español:**
```
- **Experiencia en conciliaciones bancarias**: Experiencia sólida en conciliaciones 
  bancarias nacionales e internacionales en UPS y Accenture, gestionando procesos 
  EFT y aplicaciones de pagos.
```

**Versión Inglés:**
```
- **Experiencia en conciliaciones bancarias**: Strong experience in national and 
  international bank reconciliations at UPS and Accenture, managing EFT processes 
  and payment applications.
```

## Cómo Usar las Versiones

### Para Aplicaciones en Español
1. Descarga `KAREN_SCHMALBACH_{Empresa}_es.pdf`
2. Úsalo directamente en tu aplicación
3. El contenido está 100% en español profesional

### Para Aplicaciones en Inglés
1. Descarga `KAREN_SCHMALBACH_{Empresa}_en.pdf`
2. Úsalo directamente en tu aplicación
3. El contenido está 100% en inglés profesional

### Para Aplicaciones Bilingües
1. Incluye ambas versiones en tu aplicación
2. O elige la versión más apropiada según el idioma principal de la empresa

## Logs del Workflow

El workflow muestra claramente la generación de ambas versiones:

```
============================================================
GENERACIÓN DE HOJAS DE VIDA (ESPAÑOL E INGLÉS)
============================================================

📝 Generando hoja de vida en ESPAÑOL...
   ✓ Template found: aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md
   🔄 Generating job alignment section (es)...
   🔄 Generating personalized professional summary (es)...
   ✓ CV created and personalized (es)

📝 Generando hoja de vida en INGLÉS...
   ✓ Template found: aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template_en.md
   🔄 Generating job alignment section (en)...
   🔄 Generating personalized professional summary (en)...
   ✓ CV created and personalized (en)

============================================================

============================================================
GENERACIÓN DE PDFS DE HOJAS DE VIDA (ESPAÑOL E INGLÉS)
============================================================

📄 Generando PDF en ESPAÑOL...
   Archivo fuente: hoja_de_vida_adecuada.md
   Archivo destino: KAREN_SCHMALBACH_TataConsultancyServices_es.pdf
   ✅ PDF español generado exitosamente!
   Tamaño: 23,529 bytes

📄 Generando PDF en INGLÉS...
   Archivo fuente: hoja_de_vida_adecuada_en.md
   Archivo destino: KAREN_SCHMALBACH_TataConsultancyServices_en.pdf
   ✅ PDF inglés generado exitosamente!
   Tamaño: 23,142 bytes
```

## Arquitectura Técnica

### Plantillas

El sistema utiliza dos plantillas profesionales:

1. **Plantilla Español**: `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md`
   - Formato Harvard Business School
   - Headers y secciones en español
   - Contenido profesional en español

2. **Plantilla Inglés**: `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template_en.md`
   - Formato Harvard Business School
   - Headers y secciones en inglés
   - Contenido profesional en inglés

### Motor de Personalización

**Archivo**: `aplicaciones_laborales/scripts/cv_personalization_engine.py`

Funciones principales:

```python
# Genera sección de alineación en el idioma especificado
generar_job_alignment_inteligente(requerimientos, language='es')

# Genera resumen profesional personalizado en el idioma especificado
generar_professional_summary_personalizado(cargo, requerimientos, language='es')
```

Soporta:
- `language='es'` para español
- `language='en'` para inglés

### Script de Procesamiento

**Archivo**: `aplicaciones_laborales/scripts/procesar_aplicacion.py`

El script ahora:
1. ✅ Genera `hoja_de_vida_adecuada.md` (español)
2. ✅ Genera `hoja_de_vida_adecuada_en.md` (inglés)
3. ✅ Convierte ambos a PDF con Pandoc
4. ✅ Nombres diferenciados: `_es.pdf` y `_en.pdf`

## Garantía de Calidad

### Traducciones Profesionales
- ✅ Todas las traducciones fueron revisadas manualmente
- ✅ Terminología profesional apropiada en ambos idiomas
- ✅ Estructura y formato consistentes

### Validación Automática
- ✅ Tests unitarios para ambos idiomas
- ✅ Validación de contenido en español
- ✅ Validación de contenido en inglés
- ✅ Verificación de nombres de archivos

### Pruebas Realizadas
```bash
# Test del motor de personalización
python test_bilingual_cv.py

# Test de generación completa
python procesar_aplicacion.py test_application.yaml
```

## Solución de Problemas

### No se genera la versión en inglés

**Síntoma**: Solo aparece `_es.pdf`, no `_en.pdf`

**Posibles causas**:
1. La plantilla en inglés no existe
2. Error durante la conversión a PDF

**Solución**:
1. Verificar que existe: `aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template_en.md`
2. Revisar los logs del workflow para mensajes de error
3. El sistema siempre generará al menos la versión en español

### Contenido en idioma incorrecto

**Síntoma**: La versión inglés tiene contenido en español o viceversa

**Causa**: Error en la plantilla o en el motor de personalización

**Solución**:
1. Verificar que se usan las plantillas correctas
2. Revisar el output del motor de personalización en los logs
3. Reportar el issue con ejemplos específicos

### Tamaño diferente de PDFs

**Síntoma**: Los PDFs tienen tamaños muy diferentes

**Explicación**: Es normal que tengan tamaños ligeramente diferentes debido a:
- Longitud diferente de palabras en español vs inglés
- Diferente cantidad de caracteres
- Pero deberían ser similares (±10%)

**Acción**: Si la diferencia es > 20%, revisar que ambos tengan todo el contenido

## Próximos Pasos

### Posibles Mejoras Futuras
- [ ] Soporte para más idiomas (portugués, francés)
- [ ] Personalización de idioma por empresa
- [ ] Generación condicional (solo español o solo inglés)
- [ ] Detección automática del idioma de los requerimientos

### Mantenimiento
- Actualizar traducciones cuando se agregue nuevo contenido
- Mantener ambas plantillas sincronizadas en estructura
- Revisar periódicamente la calidad de las traducciones

## Soporte

Para problemas o preguntas sobre la generación bilingüe:

1. Revisar esta documentación
2. Revisar `GUIA_USO_SISTEMA.md`
3. Revisar logs del workflow en GitHub Actions
4. Crear un issue con:
   - Descripción del problema
   - Logs relevantes
   - Ejemplos de archivos generados
   - Comportamiento esperado vs. observado

## Resumen

✅ **Generación automática**: Ambas versiones se generan sin intervención manual

✅ **Profesional**: Traducciones de calidad y formato consistente

✅ **Personalizado**: Adaptado a cada puesto en ambos idiomas

✅ **Sin esfuerzo**: Un solo proceso, dos versiones completas

✅ **Alcance global**: Lista para mercado nacional e internacional
