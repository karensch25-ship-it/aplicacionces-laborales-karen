import os
import sys
import shutil
import yaml

def sanitize_filename(s):
    return "".join(c for c in s if c.isalnum() or c in (' ', '_', '-')).replace(" ", "")

def generar_job_alignment(requerimientos):
    bullets = []
    for req in requerimientos:
        bullets.append(f"- Demonstrated experience in {req.lower()}.")
    return "\n".join(bullets)

def main(yaml_path):
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    cargo = sanitize_filename(data['cargo'])
    empresa = sanitize_filename(data['empresa'])
    fecha = data['fecha']
    folder_name = f"{cargo}_{empresa}_{fecha}"

    # Output directory in to_process/procesados
    output_dir = os.path.join("to_process", "procesados", folder_name)
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
    harvard_cv_path = "aplicaciones_laborales/aplicaciones_laborales/plantillas/hoja_de_vida_harvard_template.md"
    dest_adaptada_cv = os.path.join(output_dir, "hoja_de_vida_adecuada.md")
    if os.path.exists(harvard_cv_path):
        with open(harvard_cv_path, "r", encoding="utf-8") as src, open(dest_adaptada_cv, "w", encoding="utf-8") as dst:
            content = src.read()
            content = content.replace("{Cargo}", data['cargo']).replace("{Empresa}", data['empresa'])
            job_alignment_section = generar_job_alignment(data.get('requerimientos', []))
            content = content.replace("{job_alignment_section}", job_alignment_section)
            content = content.replace("{Nombre Completo}", "Antonio Gutierrez Amaranto")  # Personaliza si lo deseas
            dst.write(content)
    else:
        with open(dest_adaptada_cv, "w", encoding="utf-8") as f:
            f.write(f"# Hoja de Vida Adaptada para {data['cargo']} en {data['empresa']}\n")

    # hoja_de_vida_original.md (copia la hoja de vida base si existe)
    original_cv_path = "aplicaciones_laborales/hoja_de_vida_original.md"
    dest_original_cv = os.path.join(output_dir, "hoja_de_vida_original.md")
    if os.path.exists(original_cv_path):
        shutil.copyfile(original_cv_path, dest_original_cv)
    else:
        with open(dest_original_cv, "w", encoding="utf-8") as f:
            f.write("# Hoja de Vida Original\n\n(Pega aquí tu hoja de vida original.)\n")

    # (Opcional) Mover el YAML procesado
    processed_dir = os.path.join("to_process", "procesados")
    os.makedirs(processed_dir, exist_ok=True)
    shutil.move(yaml_path, os.path.join(processed_dir, os.path.basename(yaml_path)))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python procesar_aplicacion.py <archivo_yaml>")
        sys.exit(1)
    main(sys.argv[1])
