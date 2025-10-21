import os
import sys
import shutil
import yaml
import subprocess

# Import the enhanced personalization engine and scoring system
from cv_personalization_engine import CVPersonalizationEngine
from scoring_engine import AdvancedScoringEngine
from scoring_report_generator import ScoringReportGenerator
from ats_cv_validator import ATSCVValidator

def sanitize_filename(s):
    return "".join(c for c in s if c.isalnum() or c in (' ', '_', '-')).replace(" ", "")

def generar_job_alignment(requerimientos, language='es'):
    """
    Generate intelligent job alignment using the personalization engine
    """
    engine = CVPersonalizationEngine()
    return engine.generar_job_alignment_inteligente(requerimientos, language)

def generar_professional_summary(cargo, requerimientos, language='es'):
    """
    Generate personalized professional summary
    """
    engine = CVPersonalizationEngine()
    return engine.generar_professional_summary_personalizado(cargo, requerimientos, language)

def generar_cv_personalizado(template_path, output_path, data, requerimientos, language='es'):
    """
    Generate a personalized CV from template.
    
    Args:
        template_path: Path to the CV template file
        output_path: Path where to save the generated CV
        data: YAML data dictionary
        requerimientos: List of job requirements
        language: Language code ('es' or 'en')
    """
    if not os.path.exists(template_path):
        print(f"   ⚠️  Template not found: {template_path}")
        return False
    
    print(f"   ✓ Template found: {template_path}")
    with open(template_path, "r", encoding="utf-8") as src, open(output_path, "w", encoding="utf-8") as dst:
        content = src.read()
        content = content.replace("{Cargo}", data['cargo']).replace("{Empresa}", data['empresa'])
        
        # Generate intelligent job alignment
        print(f"   🔄 Generating job alignment section ({language})...")
        job_alignment_section = generar_job_alignment(requerimientos, language)
        content = content.replace("{job_alignment_section}", job_alignment_section)
        
        # Generate personalized professional summary
        print(f"   🔄 Generating personalized professional summary ({language})...")
        personalized_summary = generar_professional_summary(data['cargo'], requerimientos, language)
        
        # Replace the static summary with personalized one
        import re
        summary_pattern = r'##\s*(Professional Summary|Perfil Profesional)\n\n.*?(?=(\n##|$))'
        
        if language == 'en':
            replacement_summary = f"## Professional Summary\n\n{personalized_summary}"
        else:
            replacement_summary = f"## Perfil Profesional\n\n{personalized_summary}"
        
        content = re.sub(summary_pattern, replacement_summary, content, flags=re.DOTALL)

        # Ensure standardized name in template
        content = content.replace("{Nombre Completo}", "KAREN SCHMALBACH")
        dst.write(content)
    
    print(f"   ✓ CV created and personalized ({language})\n")
    return True

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

    # Generate CVs in both Spanish and English
    print("\n" + "="*60)
    print("GENERACIÓN DE HOJAS DE VIDA (ESPAÑOL E INGLÉS)")
    print("="*60)
    
    # Spanish CV (hoja_de_vida_adecuada.md)
    print("\n📝 Generando hoja de vida en ESPAÑOL...")
    harvard_cv_path_es = "aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md"
    dest_adaptada_cv_es = os.path.join(output_dir, "hoja_de_vida_adecuada.md")
    
    cv_es_generated = generar_cv_personalizado(
        harvard_cv_path_es,
        dest_adaptada_cv_es,
        data,
        data.get('requerimientos', []),
        language='es'
    )
    
    if not cv_es_generated:
        print("   📝 Creando hoja de vida básica en español...")
        with open(dest_adaptada_cv_es, "w", encoding="utf-8") as f:
            f.write(f"# Hoja de Vida Adaptada para {data['cargo']} en {data['empresa']}\n")
        print("   ✓ hoja_de_vida_adecuada.md creada (versión básica)\n")
    
    # English CV (hoja_de_vida_adecuada_en.md)
    print("📝 Generando hoja de vida en INGLÉS...")
    harvard_cv_path_en = "aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template_en.md"
    dest_adaptada_cv_en = os.path.join(output_dir, "hoja_de_vida_adecuada_en.md")
    
    cv_en_generated = generar_cv_personalizado(
        harvard_cv_path_en,
        dest_adaptada_cv_en,
        data,
        data.get('requerimientos', []),
        language='en'
    )
    
    if not cv_en_generated:
        print("   ⚠️  English template not found, English CV will not be generated\n")
    
    print("="*60 + "\n")

    # Validate CVs for ATS optimization
    print("\n" + "="*60)
    print("VALIDACIÓN ATS DE HOJAS DE VIDA GENERADAS")
    print("="*60)
    
    ats_validator = ATSCVValidator()
    
    # Validate Spanish CV
    if os.path.exists(dest_adaptada_cv_es):
        print("\n📋 Validando CV en ESPAÑOL para optimización ATS...")
        with open(dest_adaptada_cv_es, 'r', encoding='utf-8') as f:
            cv_es_content = f.read()
        
        ats_results_es = ats_validator.validate_cv(cv_es_content, language='es')
        
        print(f"   Puntuación ATS: {ats_results_es['overall_score']}/100")
        print(f"   Estado: {'✅ OPTIMIZADA' if ats_results_es['is_ats_optimized'] else '⚠️ REQUIERE MEJORAS'}")
        
        # Save ATS validation report for Spanish CV
        ats_report_es_path = os.path.join(output_dir, "ats_validation_report_es.md")
        ats_report_es = ats_validator.format_validation_report(
            ats_results_es,
            data['cargo'],
            language='es'
        )
        with open(ats_report_es_path, 'w', encoding='utf-8') as f:
            f.write(ats_report_es)
        print(f"   ✓ Reporte ATS guardado: ats_validation_report_es.md")
        
        # Display warnings if any
        if ats_results_es['warnings']:
            print(f"\n   ⚠️ Advertencias ATS ({len(ats_results_es['warnings'])}):")
            for warning in ats_results_es['warnings'][:3]:  # Show first 3
                print(f"      - {warning}")
            if len(ats_results_es['warnings']) > 3:
                print(f"      ... y {len(ats_results_es['warnings']) - 3} más (ver reporte completo)")
    
    # Validate English CV
    if os.path.exists(dest_adaptada_cv_en):
        print("\n📋 Validando CV en INGLÉS para optimización ATS...")
        with open(dest_adaptada_cv_en, 'r', encoding='utf-8') as f:
            cv_en_content = f.read()
        
        ats_results_en = ats_validator.validate_cv(cv_en_content, language='en')
        
        print(f"   Puntuación ATS: {ats_results_en['overall_score']}/100")
        print(f"   Estado: {'✅ OPTIMIZED' if ats_results_en['is_ats_optimized'] else '⚠️ NEEDS IMPROVEMENT'}")
        
        # Save ATS validation report for English CV
        ats_report_en_path = os.path.join(output_dir, "ats_validation_report_en.md")
        ats_report_en = ats_validator.format_validation_report(
            ats_results_en,
            data['cargo'],
            language='en'
        )
        with open(ats_report_en_path, 'w', encoding='utf-8') as f:
            f.write(ats_report_en)
        print(f"   ✓ Reporte ATS guardado: ats_validation_report_en.md")
        
        # Display warnings if any
        if ats_results_en['warnings']:
            print(f"\n   ⚠️ ATS Warnings ({len(ats_results_en['warnings'])}):")
            for warning in ats_results_en['warnings'][:3]:  # Show first 3
                print(f"      - {warning}")
            if len(ats_results_en['warnings']) > 3:
                print(f"      ... and {len(ats_results_en['warnings']) - 3} more (see full report)")
    
    print("\n" + "="*60 + "\n")

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
    
    # Generate PDFs for both Spanish and English CVs
    print("\n" + "="*60)
    print("GENERACIÓN DE PDFS DE HOJAS DE VIDA (ESPAÑOL E INGLÉS)")
    print("="*60)
    
    empresa_saneada = empresa
    header_path = "aplicaciones_laborales/plantillas/cv_header.tex"
    
    # Generate Spanish PDF
    pdf_filename_es = f"KAREN_SCHMALBACH_{empresa_saneada}_es.pdf"
    pdf_path_es = os.path.join(output_dir, pdf_filename_es)
    
    print(f"\n📄 Generando PDF en ESPAÑOL...")
    print(f"   Archivo fuente: {dest_adaptada_cv_es}")
    print(f"   Archivo destino: {pdf_filename_es}")
    
    if not os.path.exists(dest_adaptada_cv_es):
        print(f"   ❌ ERROR: Archivo fuente no encontrado: {dest_adaptada_cv_es}")
        sys.exit(1)
    
    try:
        pandoc_args = [
            "pandoc",
            dest_adaptada_cv_es,
            "-o", pdf_path_es,
            "--pdf-engine=xelatex",
            "-V", "geometry:margin=0.75in",
            "-V", "fontsize=11pt",
            "-V", "colorlinks=true",
            "-V", "linkcolor=black",
            "-V", "urlcolor=black",
            "-V", "toccolor=black",
        ]
        
        if os.path.exists(header_path):
            pandoc_args.extend(["-H", header_path])
        
        result = subprocess.run(pandoc_args, check=True, capture_output=True, text=True)
        
        if not os.path.exists(pdf_path_es) or os.path.getsize(pdf_path_es) == 0:
            print(f"   ❌ ERROR: PDF español no se generó correctamente")
            sys.exit(1)
        
        print(f"   ✅ PDF español generado exitosamente!")
        print(f"   Tamaño: {os.path.getsize(pdf_path_es):,} bytes")
        
    except subprocess.CalledProcessError as e:
        print(f"\n   ❌ ERROR al convertir CV español a PDF")
        print(f"   Código de salida: {e.returncode}")
        if e.stderr:
            print(f"   STDERR: {e.stderr}")
        sys.exit(1)
    
    # Generate English PDF
    pdf_filename_en = f"KAREN_SCHMALBACH_{empresa_saneada}_en.pdf"
    pdf_path_en = os.path.join(output_dir, pdf_filename_en)
    
    print(f"\n📄 Generando PDF en INGLÉS...")
    print(f"   Archivo fuente: {dest_adaptada_cv_en}")
    print(f"   Archivo destino: {pdf_filename_en}")
    
    if os.path.exists(dest_adaptada_cv_en):
        try:
            pandoc_args = [
                "pandoc",
                dest_adaptada_cv_en,
                "-o", pdf_path_en,
                "--pdf-engine=xelatex",
                "-V", "geometry:margin=0.75in",
                "-V", "fontsize=11pt",
                "-V", "colorlinks=true",
                "-V", "linkcolor=black",
                "-V", "urlcolor=black",
                "-V", "toccolor=black",
            ]
            
            if os.path.exists(header_path):
                pandoc_args.extend(["-H", header_path])
            
            result = subprocess.run(pandoc_args, check=True, capture_output=True, text=True)
            
            if not os.path.exists(pdf_path_en) or os.path.getsize(pdf_path_en) == 0:
                print(f"   ⚠️  Advertencia: PDF inglés no se generó correctamente")
            else:
                print(f"   ✅ PDF inglés generado exitosamente!")
                print(f"   Tamaño: {os.path.getsize(pdf_path_en):,} bytes")
            
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Advertencia: Error al convertir CV inglés a PDF")
            print(f"   El proceso continúa pero el PDF inglés no estará disponible")
    else:
        print(f"   ⚠️  CV en inglés no fue generado, saltando PDF inglés")
    
    print("\n" + "="*60)
    
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
    print(f"   ✓ hoja_de_vida_adecuada.md (español)")
    if os.path.exists(dest_adaptada_cv_en):
        print(f"   ✓ hoja_de_vida_adecuada_en.md (inglés)")
    print(f"   ✓ {pdf_filename_es} (español)")
    if os.path.exists(pdf_path_en):
        print(f"   ✓ {pdf_filename_en} (inglés)")
    print(f"   ✓ scoring_report.md")
    if os.path.exists(scoring_pdf_path):
        print(f"   ✓ SCORING_REPORT.pdf")
    
    # Show ATS validation results
    ats_report_es_path = os.path.join(output_dir, "ats_validation_report_es.md")
    ats_report_en_path = os.path.join(output_dir, "ats_validation_report_en.md")
    if os.path.exists(ats_report_es_path):
        print(f"   ✓ ats_validation_report_es.md")
    if os.path.exists(ats_report_en_path):
        print(f"   ✓ ats_validation_report_en.md")
    
    print(f"\nPróximos pasos:")
    print(f"   - El workflow copiará estos archivos a: aplicaciones/{fecha}/{folder_name}/")
    print(f"   - PDFs generados:")
    print(f"     • Español: {pdf_filename_es}")
    if os.path.exists(pdf_path_en):
        print(f"     • Inglés: {pdf_filename_en}")
    
    # Display ATS validation summary
    if os.path.exists(ats_report_es_path) or os.path.exists(ats_report_en_path):
        print(f"\n   📊 Validación ATS:")
        if os.path.exists(ats_report_es_path):
            # Read and display score from Spanish report
            with open(ats_report_es_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract score from report
                import re
                score_match = re.search(r'Puntuación ATS General:\*\* (\d+)/100', content)
                if score_match:
                    score = int(score_match.group(1))
                    status = '✅ OPTIMIZADA' if score >= 80 else '⚠️ REQUIERE MEJORAS'
                    print(f"     • CV Español: {score}/100 {status}")
        
        if os.path.exists(ats_report_en_path):
            # Read and display score from English report
            with open(ats_report_en_path, 'r', encoding='utf-8') as f:
                content = f.read()
                # Extract score from report
                import re
                score_match = re.search(r'Overall ATS Score:\*\* (\d+)/100', content)
                if score_match:
                    score = int(score_match.group(1))
                    status = '✅ OPTIMIZED' if score >= 80 else '⚠️ NEEDS IMPROVEMENT'
                    print(f"     • CV English: {score}/100 {status}")
    
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
