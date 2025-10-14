#!/usr/bin/env python3
"""
Script to copy generated CV PDFs to the todos-mis-documentos repository.
Organizes PDFs by application date in YYYY-MM-DD folders.

This script is designed to be called from GitHub Actions after PDF generation.
It clones the target repository, creates date-based folder structure,
copies the PDF, and commits/pushes the changes.

Author: GitHub Actions Bot
"""

import os
import sys
import subprocess
import shutil
from datetime import datetime
from pathlib import Path


def run_command(cmd, cwd=None, capture_output=False):
    """Execute a shell command and handle errors."""
    try:
        if capture_output:
            result = subprocess.run(
                cmd, 
                cwd=cwd, 
                check=True, 
                capture_output=True, 
                text=True
            )
            return result.stdout.strip()
        else:
            subprocess.run(cmd, cwd=cwd, check=True)
            return None
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando comando: {' '.join(cmd)}")
        print(f"Error: {e}")
        if capture_output and e.stderr:
            print(f"Stderr: {e.stderr}")
        raise


def extract_date_from_folder_name(folder_name):
    """
    Extract date from folder name format: Cargo_Empresa_YYYY-MM-DD
    
    Args:
        folder_name: String like "DataAnalyst_Adoreal_2025-10-13"
    
    Returns:
        Date string in YYYY-MM-DD format
    """
    parts = folder_name.split('_')
    if len(parts) >= 2:
        # The date should be the last part
        date_str = parts[-1]
        # Validate date format
        try:
            datetime.strptime(date_str, '%Y-%m-%d')
            return date_str
        except ValueError:
            print(f"⚠️  Warning: Could not parse date from folder name: {folder_name}")
            # Fallback to today's date
            return datetime.now().strftime('%Y-%m-%d')
    else:
        print(f"⚠️  Warning: Unexpected folder name format: {folder_name}")
        return datetime.now().strftime('%Y-%m-%d')


def copy_pdf_to_documents_repo(pdf_path, application_date, empresa, cargo):
    """
    Copy PDF to todos-mis-documentos repository organized by date.
    
    Args:
        pdf_path: Path to the generated PDF file
        application_date: Date of application in YYYY-MM-DD format
        empresa: Company name (for commit message)
        cargo: Job title (for commit message)
    """
    # Get GitHub token
    github_token = os.environ.get('GITHUB_TOKEN')
    if not github_token:
        print("❌ Error: GITHUB_TOKEN not available")
        print("   This script requires GITHUB_TOKEN to push to todos-mis-documentos")
        return False
    
    # Configuration
    target_repo = "angra8410/todos-mis-documentos"
    target_repo_url = f"https://x-access-token:{github_token}@github.com/{target_repo}.git"
    
    # Create temporary directory for cloning
    temp_dir = "/tmp/todos-mis-documentos-clone"
    
    # Clean up if directory exists
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
    
    print("\n" + "="*60)
    print("📂 Copiando PDF al repositorio todos-mis-documentos")
    print("="*60)
    
    try:
        # Clone the target repository
        print(f"📥 Clonando repositorio {target_repo}...")
        try:
            run_command([
                "git", "clone", 
                "--depth=1",  # Shallow clone for efficiency
                target_repo_url, 
                temp_dir
            ])
        except subprocess.CalledProcessError as e:
            # Check if it's a "repository not found" error
            print("\n" + "="*60)
            print("❌ ERROR: No se pudo clonar el repositorio destino")
            print("="*60)
            print(f"\nRepositorio: {target_repo}")
            print(f"Error: El repositorio no existe o no es accesible")
            print("\n📋 ACCIÓN REQUERIDA:")
            print("   1. Crea el repositorio 'todos-mis-documentos' en GitHub")
            print(f"      URL: https://github.com/new")
            print(f"      Nombre: todos-mis-documentos")
            print("      Visibilidad: Público o Privado (tu elección)")
            print("\n   2. Configura los permisos de GitHub Actions:")
            print(f"      - Ve a: https://github.com/{target_repo}/settings/actions")
            print("      - En 'Workflow permissions', selecciona:")
            print("        ☑️  'Read and write permissions'")
            print("      - Guarda los cambios")
            print("\n   3. Una vez creado el repositorio, ejecuta de nuevo el workflow")
            print("\n📖 Documentación completa: Ver SETUP_REQUIRED.md en este repositorio")
            print("="*60 + "\n")
            raise
        
        # Create date-based folder structure
        date_folder = os.path.join(temp_dir, application_date)
        os.makedirs(date_folder, exist_ok=True)
        print(f"📁 Carpeta creada/verificada: {application_date}/")
        
        # Copy PDF to the date folder
        pdf_filename = os.path.basename(pdf_path)
        dest_pdf_path = os.path.join(date_folder, pdf_filename)
        
        # Check if file already exists
        if os.path.exists(dest_pdf_path):
            print(f"⚠️  El archivo {pdf_filename} ya existe en {application_date}/")
            print(f"   Sobrescribiendo con la nueva versión...")
        
        shutil.copy2(pdf_path, dest_pdf_path)
        print(f"✅ PDF copiado: {application_date}/{pdf_filename}")
        
        # Configure git in the cloned repo
        run_command([
            "git", "config", "user.email", 
            "github-actions[bot]@users.noreply.github.com"
        ], cwd=temp_dir)
        
        run_command([
            "git", "config", "user.name", 
            "github-actions[bot]"
        ], cwd=temp_dir)
        
        # Add the PDF file
        run_command(["git", "add", dest_pdf_path], cwd=temp_dir)
        
        # Check if there are changes to commit
        status_output = run_command(
            ["git", "status", "--porcelain"],
            cwd=temp_dir,
            capture_output=True
        )
        
        if not status_output:
            print("ℹ️  No hay cambios para commitear (archivo idéntico ya existe)")
            return True
        
        # Commit the changes
        commit_message = f"📄 CV generado: {cargo} - {empresa} ({application_date})"
        run_command([
            "git", "commit", "-m", commit_message
        ], cwd=temp_dir)
        print(f"💾 Commit creado: {commit_message}")
        
        # Push to remote
        print("🚀 Enviando cambios al repositorio remoto...")
        run_command(["git", "push"], cwd=temp_dir)
        print("✅ PDF copiado exitosamente al repositorio todos-mis-documentos")
        
        # Print summary
        print("\n" + "="*60)
        print("📊 Resumen de la operación:")
        print("="*60)
        print(f"   Repositorio destino: {target_repo}")
        print(f"   Carpeta: {application_date}/")
        print(f"   Archivo: {pdf_filename}")
        print(f"   Empresa: {empresa}")
        print(f"   Cargo: {cargo}")
        print("="*60 + "\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Error al copiar PDF al repositorio: {e}")
        return False
    
    finally:
        # Clean up temporary directory
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
            print("🧹 Limpieza: directorio temporal eliminado")


def main():
    """Main function to process command line arguments and copy PDF."""
    if len(sys.argv) != 2:
        print("Uso: python copy_pdf_to_documents_repo.py <folder_name>")
        print("Ejemplo: python copy_pdf_to_documents_repo.py DataAnalyst_Adoreal_2025-10-13")
        sys.exit(1)
    
    folder_name = sys.argv[1]
    
    # Extract date from folder name
    application_date = extract_date_from_folder_name(folder_name)
    
    # Parse folder name to extract empresa and cargo
    parts = folder_name.split('_')
    if len(parts) >= 2:
        # Remove date from parts
        cargo = parts[0]
        empresa = '_'.join(parts[1:-1])  # Handle multi-part company names
    else:
        cargo = "Unknown"
        empresa = "Unknown"
    
    # Find the PDF file
    output_dir = os.path.join("to_process_procesados", folder_name)
    
    if not os.path.exists(output_dir):
        print(f"❌ Error: Carpeta no encontrada: {output_dir}")
        sys.exit(1)
    
    # Look for CV PDF (not scoring report)
    pdf_files = [f for f in os.listdir(output_dir) 
                 if f.startswith("ANTONIO_GUTIERREZ_RESUME_") and f.endswith(".pdf")]
    
    if not pdf_files:
        print(f"❌ Error: No se encontró PDF del CV en {output_dir}")
        sys.exit(1)
    
    pdf_path = os.path.join(output_dir, pdf_files[0])
    
    if not os.path.exists(pdf_path):
        print(f"❌ Error: Archivo PDF no encontrado: {pdf_path}")
        sys.exit(1)
    
    print(f"📄 PDF encontrado: {pdf_path}")
    
    # Copy PDF to documents repository
    success = copy_pdf_to_documents_repo(pdf_path, application_date, empresa, cargo)
    
    if success:
        print("✅ Proceso completado exitosamente")
        sys.exit(0)
    else:
        print("❌ Proceso falló")
        sys.exit(1)


if __name__ == "__main__":
    main()
