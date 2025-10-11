# CV PDF Formatting - Technical Documentation

## Overview

This document describes the enhancements made to the CV generation system to produce professional, ATS-friendly PDF documents with centered headers, clean formatting, and proper typography.

## Changes Made

### 1. LaTeX Header Template (`aplicaciones_laborales/plantillas/cv_header.tex`)

Created a professional LaTeX header template that defines:
- **Page geometry**: Letter size with 0.75-inch margins
- **Font**: Latin Modern Roman (standard, ATS-friendly)
- **Hyphenation**: Disabled for better ATS parsing
- **Links**: Black color, no borders (ATS-compatible)
- **Section formatting**: Clean, professional styling
- **Spacing**: Optimized for readability

### 2. Updated Markdown Template

Modified `hoja_de_vida_harvard_template.md` to use:
- **Pure LaTeX header block** for centered name and contact information
- **Horizontal rule**: Clean LaTeX `\rule` command instead of Markdown `---`
- **Proper spacing**: Vertical space commands for professional appearance

#### Header Format
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

### 3. Enhanced Pandoc Conversion

Updated `procesar_aplicacion.py` with professional PDF generation parameters:

```python
pandoc_args = [
    "pandoc",
    dest_adaptada_cv,
    "-o", pdf_path,
    "--pdf-engine=xelatex",        # Modern LaTeX engine
    "-V", "geometry:margin=0.75in",  # Professional margins
    "-V", "fontsize=11pt",           # Standard font size
    "-V", "colorlinks=true",         # Enable link coloring
    "-V", "linkcolor=black",         # Black links (ATS-friendly)
    "-V", "urlcolor=black",          # Black URLs (ATS-friendly)
    "-V", "toccolor=black",          # Black TOC links
]
```

### 4. Scoring Report PDF Enhancement

Added emoji-to-text replacement for scoring reports to ensure PDF compatibility:
- Converts emojis (🟢, 🟡, 🔴) to text markers ([EXCELLENT], [GOOD], [NEEDS IMPROVEMENT])
- Handles progress bar characters (█, ░)
- Maintains readability while ensuring LaTeX compatibility

## ATS Compatibility Features

✅ **No blue hyperlinks**: All links rendered in black  
✅ **No underlines on links**: Clean appearance  
✅ **Standard fonts**: Latin Modern Roman for maximum compatibility  
✅ **No hyphenation**: Words not split across lines  
✅ **Clean formatting**: No decorative elements that confuse ATS parsers  
✅ **Proper spacing**: Consistent vertical and horizontal spacing  
✅ **Centered header**: Professional appearance matching classic CV formats  

## Visual Improvements

### Before
- Left-aligned header
- Blue hyperlinks
- Wavy/inconsistent horizontal lines
- Generic Markdown appearance

### After
- **Centered header** with name prominently displayed
- **Black text throughout** (including links)
- **Straight horizontal line** separator
- **Professional typography** with proper spacing
- **Clean, minimalist appearance** matching traditional LaTeX CVs

## Dependencies

The system requires:
- `pandoc` (version 2.0+)
- `texlive-xetex` (XeLaTeX engine)
- `texlive-fonts-recommended` (font packages)
- `texlive-latex-extra` (additional LaTeX packages)

These are automatically installed by the GitHub Actions workflow.

## Testing

To test the CV generation locally:

```bash
# Create a test YAML file
cat > test.yaml << EOF
cargo: "Data Analyst"
empresa: "TestCompany"
fecha: "2025-10-11"
descripcion: "Test position"
requerimientos:
  - SQL experience
  - Power BI skills
EOF

# Generate CV
python aplicaciones_laborales/scripts/procesar_aplicacion.py test.yaml

# Check output
ls -l to_process_procesados/DataAnalyst_TestCompany_2025-10-11/
```

## Maintenance

When updating the CV template:
1. Keep LaTeX blocks intact in the header section
2. Use `\vspace{Npt}` for vertical spacing instead of blank lines
3. Avoid Markdown `---` separators; use LaTeX spacing instead
4. Test PDF generation after any template changes

## Future Enhancements

Potential improvements:
- [ ] Add custom font options (while maintaining ATS compatibility)
- [ ] Implement theme variations (color schemes for non-ATS versions)
- [ ] Add PDF metadata (author, title, keywords)
- [ ] Optimize for specific ATS systems (Greenhouse, Lever, etc.)
- [ ] Add validation checks for ATS compatibility

## References

- [Pandoc LaTeX Template Documentation](https://pandoc.org/MANUAL.html#templates)
- [ATS-Friendly Resume Best Practices](https://www.jobscan.co/blog/ats-resume/)
- [XeLaTeX Font Documentation](https://www.overleaf.com/learn/latex/XeLaTeX)
