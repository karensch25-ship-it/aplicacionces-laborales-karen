import sys
import os
import yaml
import shutil

def sanitize_filename(s):
    return "".join([c for c in s if c.isalnum() or c in (' ', '_', '-')]).replace(' ', '')

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
    nombre_carpeta = f"{cargo}_{empresa}_{fecha}"

    # Crea la carpeta si no existe
    if not os.path.exists(nombre_carpeta):
        os.makedirs(nombre_carpeta)

    # descripcion.md
    with open(os.path.join(nombre_carpeta, "descripcion.md"), "w", encoding="utf-8") as f:
        f.write(f"# Descripción del Puesto\n\n**Cargo:** {data['cargo']}\n**Empresa:** {data['empresa']}\n**Fecha de aplicación:** {fecha}\n\n## Descripción\n\n{data['descripcion']}\n")

    # requerimientos.md
    with open(os.path.join(nombre_carpeta, "requerimientos.md"), "w", encoding="utf-8") as f:
        f.write(f"# Requerimientos del Puesto\n\n")
        for req in data.get('requerimientos', []):
            f.write(f"- {req}\n")

    # hoja_de_vida_adecuada.md (Harvard template con job_alignment_section)
    harvard_cv_path = "plantillas/hoja_de_vida_harvard_template.md"
    dest_adaptada_cv = os.path.join(nombre_carpeta, "hoja_de_vida_adecuada.md")
    if os.path.exists(harvard_cv_path):
        with open(harvard_cv_path, "r", encoding="utf-8") as src, open(dest_adaptada_cv, "w", encoding="utf-8") as dst:
            content = src.read()
            content = content.replace("{Cargo}", data['cargo']).replace("{Empresa}", data['empresa'])
            job_alignment_section = generar_job_alignment(data.get('requerimientos', []))
            content = content.replace("{job_alignment_section}", job_alignment_section)
            content = content.replace("{Nombre Completo}", "Antonio Gutierrez Amaranto")  # Puedes automatizar esto también
            dst.write(content)
    else:
        with open(dest_adaptada_cv, "w", encoding="utf-8") as f:
            f.write(f"# Hoja de Vida Adaptada para {data['cargo']} en {data['empresa']}\n")

    # hoja_de_vida_original.md (puedes copiar un template vacío o dejar para llenado manual)
    dest_original_cv = os.path.join(nombre_carpeta, "hoja_de_vida_original.md")
    if not os.path.exists(dest_original_cv):
        with open(dest_original_cv, "w", encoding="utf-8") as f:
            f.write("# Hoja de Vida Original\n\n(Pega aquí tu hoja de vida original.)\n")

    # (Opcional) Mover el YAML procesado
    processed_dir = "to_process/procesados"
    if not os.path.exists(processed_dir):
        os.makedirs(processed_dir)
    shutil.move(yaml_path, os.path.join(processed_dir, os.path.basename(yaml_path)))

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python procesar_aplicacion.py <archivo_yaml>")
        sys.exit(1)
    main(sys.argv[1])
