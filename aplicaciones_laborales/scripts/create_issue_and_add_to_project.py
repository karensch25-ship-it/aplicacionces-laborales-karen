#!/usr/bin/env python3
"""
Script to create GitHub issues and add them to a project when a new folder is created.
This script is designed to be run from GitHub Actions after processing a job application.
"""

import os
import sys
import json
import requests
from datetime import datetime

def get_github_token():
    """Get GitHub token from environment variable."""
    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        raise ValueError("GITHUB_TOKEN environment variable is not set")
    return token

def get_repo_info():
    """Extract repository owner and name from environment or default."""
    repo = os.environ.get('GITHUB_REPOSITORY', 'angra8410/aplicaciones_laborales')
    owner, repo_name = repo.split('/')
    return owner, repo_name

def parse_folder_metadata(folder_name):
    """
    Parse metadata from folder name.
    Expected format: {Cargo}_{Empresa}_{Fecha}
    
    Example: DataAnalyst_CompanyX_2025-10-13
    """
    parts = folder_name.split('_')
    if len(parts) < 3:
        return None
    
    # The date is always the last part
    fecha = parts[-1]
    # The empresa is the second to last part
    empresa = parts[-2]
    # Everything else is the cargo
    cargo = '_'.join(parts[:-2])
    
    return {
        'cargo': cargo,
        'empresa': empresa,
        'fecha': fecha,
        'folder_name': folder_name
    }

def check_issue_exists(owner, repo_name, folder_name, token):
    """
    Check if an issue already exists for this folder.
    Uses a label to identify issues created by this automation.
    """
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Search for issues with the automation label and folder name in title
    url = f'https://api.github.com/repos/{owner}/{repo_name}/issues'
    params = {
        'labels': 'aplicacion-procesada',
        'state': 'all',
        'per_page': 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            # Check if the folder name is mentioned in the issue body
            if folder_name in issue.get('body', ''):
                return True
    
    return False

def create_issue(owner, repo_name, metadata, token):
    """Create a GitHub issue for the processed application."""
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Format issue title
    title = f"Aplicación: {metadata['cargo']} en {metadata['empresa']}"
    
    # Format issue body
    body = f"""## Nueva Aplicación Procesada

**Cargo:** {metadata['cargo']}
**Empresa:** {metadata['empresa']}
**Fecha de aplicación:** {metadata['fecha']}
**Carpeta:** `to_process_procesados/{metadata['folder_name']}`

### Archivos generados:
- ✅ Descripción del puesto
- ✅ Requerimientos
- ✅ Hoja de vida adaptada
- ✅ CV en PDF
- ✅ Reporte de scoring

### Próximos pasos:
- [ ] Revisar CV generado
- [ ] Verificar scoring report
- [ ] Personalizar si es necesario
- [ ] Enviar aplicación

---
*Esta issue fue creada automáticamente por el workflow de procesamiento de aplicaciones.*
*Folder: {metadata['folder_name']}*
"""
    
    # Create the issue
    url = f'https://api.github.com/repos/{owner}/{repo_name}/issues'
    data = {
        'title': title,
        'body': body,
        'labels': ['aplicacion-procesada', 'Aplicados']
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 201:
        issue_data = response.json()
        print(f"✅ Issue created successfully: #{issue_data['number']}")
        print(f"   URL: {issue_data['html_url']}")
        return issue_data
    else:
        print(f"❌ Failed to create issue: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def get_project_id(owner, token):
    """
    Get the project ID for 'aplicacione-estados' using GraphQL API.
    """
    headers = {
        'Authorization': f'bearer {token}',
        'Content-Type': 'application/json'
    }
    
    query = """
    query($owner: String!) {
      user(login: $owner) {
        projectsV2(first: 20) {
          nodes {
            id
            title
            number
          }
        }
      }
      organization(login: $owner) {
        projectsV2(first: 20) {
          nodes {
            id
            title
            number
          }
        }
      }
    }
    """
    
    variables = {
        'owner': owner
    }
    
    response = requests.post(
        'https://api.github.com/graphql',
        headers=headers,
        json={'query': query, 'variables': variables}
    )
    
    if response.status_code == 200:
        data = response.json()
        
        # Try user projects first
        projects = data.get('data', {}).get('user', {}).get('projectsV2', {}).get('nodes', [])
        if not projects:
            # Try organization projects
            projects = data.get('data', {}).get('organization', {}).get('projectsV2', {}).get('nodes', [])
        
        # Find the project by name
        for project in projects:
            if 'aplicacione-estados' in project['title'].lower() or 'aplicacion' in project['title'].lower():
                print(f"✅ Found project: {project['title']} (ID: {project['id']})")
                return project['id']
        
        print(f"⚠️  Project 'aplicacione-estados' not found. Available projects:")
        for project in projects:
            print(f"   - {project['title']}")
        return None
    else:
        print(f"❌ Failed to get projects: {response.status_code}")
        print(f"   Response: {response.text}")
        return None

def add_issue_to_project(project_id, issue_node_id, token):
    """
    Add an issue to a GitHub Project (Projects v2) using GraphQL API.
    """
    headers = {
        'Authorization': f'bearer {token}',
        'Content-Type': 'application/json'
    }
    
    mutation = """
    mutation($projectId: ID!, $contentId: ID!) {
      addProjectV2ItemById(input: {projectId: $projectId, contentId: $contentId}) {
        item {
          id
        }
      }
    }
    """
    
    variables = {
        'projectId': project_id,
        'contentId': issue_node_id
    }
    
    response = requests.post(
        'https://api.github.com/graphql',
        headers=headers,
        json={'query': mutation, 'variables': variables}
    )
    
    if response.status_code == 200:
        data = response.json()
        if 'errors' in data:
            print(f"❌ GraphQL errors: {data['errors']}")
            return False
        print(f"✅ Issue added to project successfully")
        return True
    else:
        print(f"❌ Failed to add issue to project: {response.status_code}")
        print(f"   Response: {response.text}")
        return False

def main():
    """Main function to create issue and add to project."""
    if len(sys.argv) != 2:
        print("Usage: python create_issue_and_add_to_project.py <folder_name>")
        sys.exit(1)
    
    folder_name = sys.argv[1]
    print(f"Processing folder: {folder_name}")
    
    # Parse folder metadata
    metadata = parse_folder_metadata(folder_name)
    if not metadata:
        print(f"❌ Could not parse folder name: {folder_name}")
        sys.exit(1)
    
    print(f"Parsed metadata: {json.dumps(metadata, indent=2)}")
    
    # Get GitHub credentials and repository info
    try:
        token = get_github_token()
        owner, repo_name = get_repo_info()
        print(f"Repository: {owner}/{repo_name}")
    except Exception as e:
        print(f"❌ Error getting GitHub credentials: {e}")
        sys.exit(1)
    
    # Check if issue already exists
    if check_issue_exists(owner, repo_name, folder_name, token):
        print(f"ℹ️  Issue already exists for folder: {folder_name}")
        return
    
    # Create the issue
    issue_data = create_issue(owner, repo_name, metadata, token)
    if not issue_data:
        print("❌ Failed to create issue")
        sys.exit(1)
    
    # Get project ID
    project_id = get_project_id(owner, token)
    if not project_id:
        print("⚠️  Could not find project, skipping project assignment")
        print("ℹ️  Issue was created successfully but not added to project")
        return
    
    # Add issue to project
    issue_node_id = issue_data['node_id']
    if add_issue_to_project(project_id, issue_node_id, token):
        print("✅ All done! Issue created and added to project.")
    else:
        print("⚠️  Issue created but could not be added to project")

if __name__ == '__main__':
    main()
