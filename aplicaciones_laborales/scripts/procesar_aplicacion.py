import os
import sys
import shutil
import yaml
import subprocess

# Import the enhanced personalization engine and scoring system
from cv_personalization_engine import CVPersonalizationEngine
from scoring_engine import AdvancedScoringEngine
from scoring_report_generator import ScoringReportGenerator

def sanitize_filename(s):
    return "".join(c for c in s if c.isalnum() or c in (' ', '_', '-')).replace(" ", "")

def generar_job_alignment(requerimientos):
    """
    Generate intelligent job alignment using the personalization engine
    """
    engine = CVPersonalizationEngine()
    return engine.generar_job_alignment_inteligente(requerimientos)

def generar_professional_summary(cargo, requerimientos):
    """
    Generate personalized professional summary
    """
    engine = CVPersonalizationEngine()
    return engine.generar_professional_summary_personalizado(cargo, requerimientos)

def main(yaml_path):
    print("\n" + "="*60)
    print("PROCESAMIENTO DE APLICACIÓN LABORAL")
    print("="*60)
    print(f"Archivo YAML: {yaml_path}")
    
    # Load and validate YAML
    try:
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
    except FileNotFoundError:
        print(f"❌ ERROR: Archivo YAML no encontrado: {yaml_path}")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"❌ ERROR: Formato YAML inválido en {yaml_path}")
        print(f"   Detalle: {e}")
        sys.exit(1)
    
    # Validate required fields
    required_fields = ['cargo', 'empresa', 'fecha']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        print(f"❌ ERROR: Campos requeridos faltantes en YAML: {', '.join(missing_fields)}")
        sys.exit(1)

    cargo = sanitize_filename(data['cargo'])
    empresa = sanitize_filename(data['empresa'])
    fecha = data['fecha']
    folder_name = f"{cargo}_{empresa}_{fecha}"
    
    print(f"\n📋 Detalles de la aplicación:")
    print(f"   Cargo: {data['cargo']}")
    print(f"   Empresa: {data['empresa']}")
    print(f"   Fecha: {fecha}")
    print(f"   Carpeta destino: {folder_name}")
    print("="*60 + "\n")

    # Output directory in to_process_procesados
    output_dir = os.path.join("to_process_procesados", folder_name)
    os.makedirs(output_dir, exist_ok=True)
    print(f"✓ Carpeta de salida creada: {output_dir}\n")

    # descripcion.md
    print("📝 Generando descripcion.md...")
    with open(os.path.join(output_dir, "descripcion.md"), "w", encoding="utf-8") as f:
        f.write(f"# Descripción del Puesto\n\n**Cargo:** {data['cargo']}\n**Empresa:** {data['empresa']}\n**Fecha de aplicación:** {fecha}\n\n## Descripción\n\n{data['descripcion']}\n")
    print("   ✓ descripcion.md creado\n")

    # requerimientos.md
    print("📝 Generando requerimientos.md...")
    with open(os.path.join(output_dir, "requerimientos.md"), "w", encoding="utf-8") as f:
        f.write(f"# Requerimientos del Puesto\n\n")
        for req in data.get('requerimientos', []):
            f.write(f"- {req}\n")
    print(f"   ✓ requerimientos.md creado ({len(data.get('requerimientos', []))} requerimientos)\n")

    # hoja_de_vida_adecuada.md (Harvard template con job_alignment_section)
    print("📝 Generando hoja_de_vida_adecuada.md...")
    harvard_cv_path = "aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md"
    dest_adaptada_cv = os.path.join(output_dir, "hoja_de_vida_adecuada.md")
    if os.path.exists(harvard_cv_path):
        print(f"   ✓ Plantilla Harvard encontrada: {harvard_cv_path}")
        with open(harvard_cv_path, "r", encoding="utf-8") as src, open(dest_adaptada_cv, "w", encoding="utf-8") as dst:
            content = src.read()
            content = content.replace("{Cargo}", data['cargo']).replace("{Empresa}", data['empresa'])
            
            # Generate intelligent job alignment
            print("   🔄 Generando sección de alineación con el puesto...")
            job_alignment_section = generar_job_alignment(data.get('requerimientos', []))
            content = content.replace("{job_alignment_section}", job_alignment_section)
            
            # Generate personalized professional summary
            print("   🔄 Generando resumen profesional personalizado...")
            personalized_summary = generar_professional_summary(data['cargo'], data.get('requerimientos', []))
            # Replace the static summary with personalized one
            # Match either English or Spanish header and replace with Spanish section
            import re
            summary_pattern = r'##\s*(Professional Summary|Perfil Profesional)\n\n.*?(?=(\n##|$))'
            replacement_summary = f"## Perfil Profesional\n\n{personalized_summary}"
            content = re.sub(summary_pattern, replacement_summary, content, flags=re.DOTALL)

            # Forzar nombre estandarizado en la plantilla
            content = content.replace("{Nombre Completo}", "KAREN SCHMALBACH")
            dst.write(content)
        print("   ✓ hoja_de_vida_adecuada.md creada y personalizada\n")
    else:
        print(f"   ⚠️  Plantilla Harvard NO encontrada en {harvard_cv_path}")
        print("   📝 Creando hoja de vida básica...")
        with open(dest_adaptada_cv, "w", encoding="utf-8") as f:
            f.write(f"# Hoja de Vida Adaptada para {data['cargo']} en {data['empresa']}\n")
        print("   ✓ hoja_de_vida_adecuada.md creada (versión básica)\n")

    # Generate scoring report
    print("\n" + "="*60)
    print("GENERACIÓN DE REPORTE DE SCORING")
    print("="*60)
    scoring_engine = AdvancedScoringEngine()
    scoring_result = scoring_engine.calculate_comprehensive_score(
        requirements=data.get('requerimientos', []),
        job_description=data.get('descripcion', ''),
        job_title=data['cargo']
    )
    
    # Generate scoring report markdown
    report_generator = ScoringReportGenerator()
    scoring_report = report_generator.generate_report(
        scoring_result,
        data['cargo'],
        data['empresa'],
        fecha
    )
    
    # Save scoring report
    scoring_report_path = os.path.join(output_dir, "scoring_report.md")
    with open(scoring_report_path, "w", encoding="utf-8") as f:
        f.write(scoring_report)
    
    print(f"✅ Reporte de Scoring generado exitosamente")
    print(f"   Puntuación Global: {scoring_result['global_score']}%")
    print(f"   Recomendación: {scoring_result['recommendation']}")
    print(f"   Archivo: scoring_report.md")
    print("="*60 + "\n")
    
    # Convertir a PDF usando pandoc con formato profesional
    # Output PDF must follow the standard: KAREN_SCHMALBACH_NOMBREEMPRESA.pdf
    empresa_saneada = empresa
    pdf_filename = f"KAREN_SCHMALBACH_{empresa_saneada}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    
    # Get the path to the LaTeX header template
    header_path = "aplicaciones_laborales/plantillas/cv_header.tex"
    
    print("\n" + "="*60)
    print("GENERACIÓN DE PDF DE HOJA DE VIDA")
    print("="*60)
    print(f"Archivo fuente: {dest_adaptada_cv}")
    print(f"Archivo destino: {pdf_path}")
    print(f"Nombre estándar: KAREN_SCHMALBACH_{empresa_saneada}.pdf")
    print("="*60 + "\n")
    
    # Verify source markdown file exists
    if not os.path.exists(dest_adaptada_cv):
        print(f"❌ ERROR CRÍTICO: Archivo fuente no encontrado: {dest_adaptada_cv}")
        print("   El proceso no puede continuar sin el archivo markdown de la hoja de vida.")
        sys.exit(1)
    
    try:
        pandoc_args = [
            "pandoc",
            dest_adaptada_cv,
            "-o", pdf_path,
            "--pdf-engine=xelatex",
            "-V", "geometry:margin=0.75in",
            "-V", "fontsize=11pt",
            "-V", "colorlinks=true",
            "-V", "linkcolor=black",
            "-V", "urlcolor=black",
            "-V", "toccolor=black",
        ]
        
        # Add header include if it exists
        if os.path.exists(header_path):
            pandoc_args.extend(["-H", header_path])
            print(f"✓ Usando header LaTeX personalizado: {header_path}")
        else:
            print(f"ℹ️  No se encontró header LaTeX personalizado en {header_path}")

        print(f"\n🔄 Ejecutando pandoc para generar PDF...")
        print(f"   Comando: {' '.join(pandoc_args)}")
        
        result = subprocess.run(pandoc_args, check=True, capture_output=True, text=True)
        
        # Verify PDF was created
        if not os.path.exists(pdf_path):
            print(f"❌ ERROR CRÍTICO: El PDF no se generó en la ruta esperada: {pdf_path}")
            print("   Pandoc ejecutó sin errores pero el archivo no existe.")
            sys.exit(1)
        
        # Verify PDF has content (size > 0)
        pdf_size = os.path.getsize(pdf_path)
        if pdf_size == 0:
            print(f"❌ ERROR CRÍTICO: El PDF generado está vacío (0 bytes)")
            os.remove(pdf_path)  # Remove empty file
            sys.exit(1)
        
        print(f"✅ CV PDF generado exitosamente!")
        print(f"   Archivo: {pdf_filename}")
        print(f"   Tamaño: {pdf_size:,} bytes")
        print(f"   Ruta completa: {pdf_path}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ ERROR CRÍTICO al convertir a PDF con pandoc")
        print("="*60)
        print(f"Código de salida: {e.returncode}")
        if e.stdout:
            print(f"STDOUT:\n{e.stdout}")
        if e.stderr:
            print(f"STDERR:\n{e.stderr}")
        print("="*60)
        print("\n🔍 DIAGNÓSTICO:")
        print("   1. Verificar que pandoc está instalado correctamente")
        print("   2. Verificar que xelatex está instalado (texlive-xetex)")
        print("   3. Revisar el contenido del archivo markdown por errores de sintaxis")
        print("   4. Verificar que las fuentes necesarias están disponibles")
        print("\n❌ El proceso se detiene aquí. No se puede continuar sin el PDF.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO al generar PDF: {e}")
        print(f"   Tipo de error: {type(e).__name__}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    
    # Convert scoring report to PDF
    scoring_pdf_path = os.path.join(output_dir, "SCORING_REPORT.pdf")
    print("\n" + "="*60)
    print("GENERACIÓN DE PDF DE SCORING REPORT")
    print("="*60)
    try:
        # Create a cleaned version of the scoring report without emojis for PDF
        with open(scoring_report_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove common emojis used in the report
        emoji_replacements = {
            '🟢': '[EXCELLENT]',
            '🟡': '[GOOD]',
            '🔴': '[NEEDS IMPROVEMENT]',
            '🟠': '[WARNING]',
            '✅': '[+]',
            '⚠️': '[!]',
            '❌': '[-]',
            '🎯': '[TARGET]',
            '📊': '[CHART]',
            '█': '#',
            '░': '-',
        }
        
        for emoji, replacement in emoji_replacements.items():
            content = content.replace(emoji, replacement)
        
        # Save cleaned version temporarily
        cleaned_report_path = os.path.join(output_dir, "scoring_report_cleaned.md")
        with open(cleaned_report_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"🔄 Generando PDF del reporte de scoring...")
        
        # Generate PDF from cleaned version
        result = subprocess.run(
            ["pandoc", cleaned_report_path, "-o", scoring_pdf_path,
             "--pdf-engine=xelatex",
             "-V", "geometry:margin=0.75in",
             "-V", "fontsize=11pt"],
            check=True,
            capture_output=True,
            text=True
        )

        # Verify scoring report PDF was created
        if os.path.exists(scoring_pdf_path) and os.path.getsize(scoring_pdf_path) > 0:
            print(f"✅ Scoring Report PDF generado exitosamente")
            print(f"   Archivo: SCORING_REPORT.pdf")
            print(f"   Tamaño: {os.path.getsize(scoring_pdf_path):,} bytes")
        else:
            print(f"⚠️  Advertencia: El PDF del scoring report no se generó correctamente")
            
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Advertencia: Error al convertir scoring report a PDF")
        print(f"   Error: {e.stderr if e.stderr else str(e)}")
        print("   El proceso continúa, pero el reporte PDF no estará disponible")
    except Exception as e:
        print(f"⚠️  Advertencia: Error inesperado al generar scoring report PDF: {e}")
        print("   El proceso continúa, pero el reporte PDF no estará disponible")
    
    print("="*60 + "\n")

    # Mover el YAML procesado dentro de la carpeta de la aplicación procesada
    print("📦 Moviendo archivo YAML procesado a la carpeta de salida...")
    try:
        dest_yaml_path = os.path.join(output_dir, os.path.basename(yaml_path))
        shutil.move(yaml_path, dest_yaml_path)
        print(f"   ✓ YAML movido a: {dest_yaml_path}\n")
    except Exception as e:
        print(f"⚠️  Warning: no se pudo mover el YAML al folder de salida: {e}\n")
    
    # Final summary
    print("\n" + "="*60)
    print("✅ PROCESAMIENTO COMPLETADO EXITOSAMENTE")
    print("="*60)
    print(f"Carpeta de salida: {output_dir}")
    print(f"\nArchivos generados:")
    print(f"   ✓ descripcion.md")
    print(f"   ✓ requerimientos.md")
    print(f"   ✓ hoja_de_vida_adecuada.md")
    print(f"   ✓ {pdf_filename}")
    print(f"   ✓ scoring_report.md")
    if os.path.exists(scoring_pdf_path):
        print(f"   ✓ SCORING_REPORT.pdf")
    print(f"\nPróximos pasos:")
    print(f"   - El workflow copiará estos archivos a: aplicaciones/{fecha}/{folder_name}/")
    print(f"   - El PDF principal es: {pdf_filename}")
    print("="*60 + "\n")
    
    # Validate that the output directory was created successfully
    if not os.path.exists(output_dir):
        print(f"❌ ERROR CRÍTICO: La carpeta de salida no existe: {output_dir}")
        print("   El procesamiento falló en algún paso anterior.")
        sys.exit(1)
    
    # Return folder_name for issue creation and workflow processing
    # NOTE: Do NOT print folder_name here - it will be printed as the final line
    # in the __main__ block to ensure the workflow can capture it correctly
    return folder_name

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python procesar_aplicacion.py <archivo_yaml>")
        sys.exit(1)
    folder_name = main(sys.argv[1])
    
    # Create GitHub issue and add to project if GITHUB_TOKEN is available
    # Note: All informational messages MUST be printed BEFORE the final folder_name output
    # to ensure the workflow can correctly capture the folder name using tail -n 1
    if os.environ.get('GITHUB_TOKEN'):
        print("\n" + "="*60)
        print("Creating GitHub issue and adding to project...")
        print("="*60)
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            issue_script = os.path.join(script_dir, "create_issue_and_add_to_project.py")
            subprocess.run([sys.executable, issue_script, folder_name], check=True)
        except Exception as e:
            print(f"⚠️  Warning: Could not create issue: {e}")
            print("   The application was processed successfully, but issue creation failed.")
    else:
        print("\nℹ️  Skipping issue creation (GITHUB_TOKEN not available)")
    
    # CRITICAL: This MUST be the last line of output for the workflow to capture correctly
    # The workflow uses: tail -n 1 to get the folder name from the script output
    print(f"\n{folder_name}")
