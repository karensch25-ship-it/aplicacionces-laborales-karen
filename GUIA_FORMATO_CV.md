# Guía de Formato Profesional del CV en PDF

## 🎯 Nuevas Características

El sistema de generación de CVs ahora produce documentos PDF con formato profesional, minimalista y compatible con sistemas ATS (Applicant Tracking Systems).

## ✨ Mejoras Implementadas

### 1. **Header Centrado y Profesional**
- Nombre en tamaño grande y destacado
- Información de contacto centrada
- Línea horizontal recta y limpia

### 2. **Formato ATS-Friendly**
- ✅ Sin enlaces azules (todo en negro)
- ✅ Sin subrayados en enlaces
- ✅ Fuentes estándar (Latin Modern Roman)
- ✅ Sin guiones de separación de palabras
- ✅ Formato limpio y sin elementos decorativos

### 3. **Tipografía Profesional**
- Tamaño de fuente: 11pt
- Márgenes: 0.75 pulgadas
- Espaciado optimizado para lectura
- Líneas rectas y consistentes

## 📊 Comparación Visual

### Antes
```
{Nombre Completo}                    ← Alineado a la izquierda
Email: correo@ejemplo.com            ← Link azul
LinkedIn: perfil                     ← Link azul
~~~~~~~~~~~~~~~~~~~~~~               ← Línea ondulada
```

### Después
```
        Antonio Gutierrez Amaranto   ← Centrado, grande, bold
           
     Medellín, Antioquia, Colombia   ← Centrado
        Tel: +57 304-650-3897        ← Centrado
      Email: antoineg84@hotmail.com  ← Negro, sin subrayado
    LinkedIn: antoniogutierrez-datos ← Negro, sin subrayado
           
    ─────────────────────────────    ← Línea recta y limpia
```

## 🔧 Cómo Funciona

### Tecnologías Utilizadas

1. **Markdown con LaTeX**: El template combina Markdown estándar con bloques LaTeX para control preciso del formato
2. **Pandoc con XeLaTeX**: Motor de conversión que soporta tipografía avanzada
3. **Parámetros optimizados**: Configuración específica para ATS y apariencia profesional

### Archivo de Template

El template actualizado (`hoja_de_vida_harvard_template.md`) incluye:

```latex
\begin{center}
{\LARGE\bfseries Antonio Gutierrez Amaranto}

\vspace{8pt}

Medellín, Antioquia, Colombia\\
Tel: +57 304-650-3897\\
Email: antoineg84@hotmail.com\\
LinkedIn: antoniogutierrez-datos

\vspace{6pt}
\noindent\rule{\textwidth}{0.4pt}
\end{center}
```

### Proceso de Generación

```
YAML → Python Script → Markdown con LaTeX → Pandoc/XeLaTeX → PDF Profesional
```

## 🚀 Uso

No hay cambios en el uso del sistema. El formato mejorado se aplica automáticamente:

1. Crea un archivo YAML en `to_process/`
2. El sistema procesa automáticamente
3. Genera PDF con el nuevo formato profesional

## 📋 Checklist de Calidad ATS

Todos los PDFs generados cumplen con:

- [x] Texto extraíble (no imágenes)
- [x] Fuentes estándar
- [x] Sin tablas complejas
- [x] Sin columnas múltiples
- [x] Sin encabezados/pies de página complejos
- [x] Links en negro (no azul)
- [x] Sin elementos gráficos decorativos
- [x] Formato consistente
- [x] Sin compresión de texto
- [x] Márgenes adecuados

## 🎨 Detalles Técnicos

### Parámetros de Pandoc
```bash
pandoc documento.md -o salida.pdf \
  --pdf-engine=xelatex \
  -V geometry:margin=0.75in \
  -V fontsize=11pt \
  -V colorlinks=true \
  -V linkcolor=black \
  -V urlcolor=black \
  -V toccolor=black
```

### LaTeX Header Template
El archivo `cv_header.tex` define:
- Geometría de página
- Configuración de fuentes
- Estilos de sección
- Espaciado
- Formato de enlaces

## 🔍 Validación

Para verificar que el PDF cumple con estándares ATS:

1. **Extracción de texto**: 
   ```bash
   pdftotext CV.pdf output.txt
   ```
   El texto debe ser legible y mantener el formato.

2. **Inspección visual**: El PDF debe verse limpio, profesional y sin elementos decorativos.

3. **Herramientas ATS**: Puedes usar [Jobscan](https://www.jobscan.co/) o herramientas similares para verificar compatibilidad.

## 📝 Personalización

Si necesitas personalizar el formato:

1. **Modificar el header**: Edita `aplicaciones_laborales/plantillas/cv_header.tex`
2. **Ajustar márgenes**: Cambia el parámetro `geometry:margin` en `procesar_aplicacion.py`
3. **Cambiar fuente**: Actualiza `\setmainfont` en el header template

## ⚠️ Notas Importantes

- **No editar manualmente los PDFs generados**: Siempre regenera desde el YAML
- **Mantener LaTeX blocks en el template**: No eliminar los bloques `\begin{center}...` del template
- **Probar después de cambios**: Siempre genera un CV de prueba después de modificar templates

## 🆘 Solución de Problemas

### PDF no se genera
**Causa**: Falta pandoc o XeLaTeX  
**Solución**: El workflow de GitHub Actions instala automáticamente. Para testing local:
```bash
sudo apt-get install pandoc texlive-xetex texlive-fonts-recommended
```

### El formato no se ve bien
**Causa**: Template modificado incorrectamente  
**Solución**: Verifica que los bloques LaTeX estén intactos en el template

### Texto no centrado
**Causa**: Bloques `\begin{center}...\end{center}` dañados  
**Solución**: Restaura el template desde el repositorio

## 📚 Referencias

- [Pandoc User's Guide](https://pandoc.org/MANUAL.html)
- [LaTeX/XeTeX Font Guide](https://www.overleaf.com/learn/latex/Font_typefaces)
- [ATS Resume Guide](https://www.jobscan.co/blog/ats-resume/)
- Documentación técnica completa: `CV_PDF_FORMATTING.md`

## 🎯 Resultados

Los CVs generados ahora:
- Se ven tan profesionales como plantillas LaTeX tradicionales
- Son 100% compatibles con sistemas ATS
- Mantienen toda la personalización inteligente del sistema
- Requieren cero configuración adicional del usuario

---

**¿Preguntas o sugerencias?** Abre un issue en el repositorio.
