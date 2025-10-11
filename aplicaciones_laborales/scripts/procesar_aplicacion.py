import os
import sys
import shutil
import yaml
import subprocess

# Import the enhanced personalization engine
from cv_personalization_engine import CVPersonalizationEngine

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
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    cargo = sanitize_filename(data['cargo'])
    empresa = sanitize_filename(data['empresa'])
    fecha = data['fecha']
    folder_name = f"{cargo}_{empresa}_{fecha}"

    # Output directory in to_process_procesados
    output_dir = os.path.join("to_process_procesados", folder_name)
    os.makedirs(output_dir, exist_ok=True)

    # descripcion.md
    with open(os.path.join(output_dir, "descripcion.md"), "w", encoding="utf-8") as f:
        f.write(f"# Descripción del Puesto\n\n**Cargo:** {data['cargo']}\n**Empresa:** {data['empresa']}\n**Fecha de aplicación:** {fecha}\n\n## Descripción\n\n{data['descripcion']}\n")

    # requerimientos.md
    with open(os.path.join(output_dir, "requerimientos.md"), "w", encoding="utf-8") as f:
        f.write(f"# Requerimientos del Puesto\n\n")
        for req in data.get('requerimientos', []):
            f.write(f"- {req}\n")

    # hoja_de_vida_adecuada.md (Harvard template con job_alignment_section)
    harvard_cv_path = "aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md"
    dest_adaptada_cv = os.path.join(output_dir, "hoja_de_vida_adecuada.md")
    if os.path.exists(harvard_cv_path):
        with open(harvard_cv_path, "r", encoding="utf-8") as src, open(dest_adaptada_cv, "w", encoding="utf-8") as dst:
            content = src.read()
            content = content.replace("{Cargo}", data['cargo']).replace("{Empresa}", data['empresa'])
            
            # Generate intelligent job alignment
            job_alignment_section = generar_job_alignment(data.get('requerimientos', []))
            content = content.replace("{job_alignment_section}", job_alignment_section)
            
            # Generate personalized professional summary
            personalized_summary = generar_professional_summary(data['cargo'], data.get('requerimientos', []))
            # Replace the static summary with personalized one
            # Find and replace the Professional Summary section
            import re
            summary_pattern = r'## Professional Summary\n\n.*?(?=\n---)'
            replacement_summary = f"## Professional Summary\n\n{personalized_summary}"
            content = re.sub(summary_pattern, replacement_summary, content, flags=re.DOTALL)
            
            content = content.replace("{Nombre Completo}", "Antonio Gutierrez Amaranto")  # Personaliza si lo deseas
            dst.write(content)
    else:
        with open(dest_adaptada_cv, "w", encoding="utf-8") as f:
            f.write(f"# Hoja de Vida Adaptada para {data['cargo']} en {data['empresa']}\n")

    # Convertir a PDF usando pandoc
    pdf_filename = f"ANTONIO_GUTIERREZ_RESUME_{empresa}.pdf"
    pdf_path = os.path.join(output_dir, pdf_filename)
    try:
        subprocess.run(
            ["pandoc", dest_adaptada_cv, "-o", pdf_path],
            check=True
        )
    except Exception as e:
        print(f"Error al convertir a PDF con pandoc: {e}")

    # (Opcional) Mover el YAML procesado
    processed_dir = "to_process_procesados"
    os.makedirs(processed_dir, exist_ok=True)
    shutil.move(yaml_path, os.path.join(processed_dir, os.path.basename(yaml_path)))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python procesar_aplicacion.py <archivo_yaml>")
        sys.exit(1)
    main(sys.argv[1])
