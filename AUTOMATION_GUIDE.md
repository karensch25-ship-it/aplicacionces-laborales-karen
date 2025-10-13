# Guía de Automatización: Creación Automática de Issues y Gestión de Proyecto

## 📋 Descripción General

Este sistema automatiza completamente el flujo de gestión de aplicaciones laborales, creando automáticamente issues en GitHub y agregándolas al proyecto "aplicacione-estados" cada vez que se procesa una nueva aplicación.

## 🔄 Flujo Automatizado

```
1. Usuario crea YAML en to_process/
         ↓
2. GitHub Actions detecta el cambio
         ↓
3. Procesa aplicación (genera CV, scoring, etc.)
         ↓
4. Crea carpeta en to_process_procesados/
         ↓
5. ⭐ NUEVO: Crea issue automáticamente
         ↓
6. ⭐ NUEVO: Agrega issue al proyecto "aplicacione-estados"
         ↓
7. Commit y push de cambios
```

## ✨ Características del Sistema

### 1. Creación Automática de Issues

Cada vez que se procesa una aplicación, el sistema crea automáticamente una issue con:

**Título:**
```
Aplicación: {Cargo} en {Empresa}
```

**Contenido:**
- ✅ Información del cargo y empresa
- ✅ Fecha de aplicación
- ✅ Ruta a la carpeta con archivos generados
- ✅ Lista de archivos creados (CV, scoring, etc.)
- ✅ Checklist de próximos pasos
- ✅ Labels automáticos: `aplicacion-procesada`, `Aplicados`

**Ejemplo de Issue:**
```markdown
## Nueva Aplicación Procesada

**Cargo:** Data Analyst
**Empresa:** CompanyX
**Fecha de aplicación:** 2025-10-13
**Carpeta:** `to_process_procesados/DataAnalyst_CompanyX_2025-10-13`

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
```

### 2. Integración con GitHub Projects

El sistema automáticamente:
- 🔍 Busca el proyecto "aplicacione-estados"
- ➕ Agrega la issue al proyecto
- 🏷️ La issue aparece en la columna "Aplicados"

### 3. Prevención de Duplicados

- ✅ Verifica si ya existe una issue para la misma carpeta
- ✅ Usa el label `aplicacion-procesada` para identificación
- ✅ Evita crear múltiples issues para la misma aplicación

### 4. Manejo Robusto de Errores

- ⚠️ Si falla la creación de issue, el procesamiento continúa
- 📝 Logs detallados para debugging
- ℹ️ Mensajes informativos de progreso

## 🛠️ Componentes Técnicos

### Scripts

1. **`create_issue_and_add_to_project.py`**
   - Parsea metadatos de la carpeta creada
   - Crea issues usando GitHub REST API
   - Busca proyectos usando GraphQL API
   - Agrega issues a proyectos usando Projects v2 API

2. **`procesar_aplicacion.py` (modificado)**
   - Retorna el nombre de la carpeta creada
   - Invoca automáticamente el script de creación de issues
   - Maneja errores gracefully

### Workflow

**`.github/workflows/crear_aplicacion.yml` (actualizado)**
```yaml
permissions:
  contents: write
  issues: write          # ⭐ NUEVO
  repository-projects: write  # ⭐ NUEVO

- name: Instalar dependencias
  run: |
    pip install pyyaml requests  # ⭐ requests agregado

- name: Procesar archivo de nueva aplicación
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}  # ⭐ Token disponible
  run: |
    for file in to_process/*.yaml; do
      python aplicaciones_laborales/scripts/procesar_aplicacion.py "$file"
    done
```

## 📊 APIs Utilizadas

### GitHub REST API v3
- **Crear Issues:** `POST /repos/{owner}/{repo}/issues`
- **Listar Issues:** `GET /repos/{owner}/{repo}/issues`

### GitHub GraphQL API (Projects v2)
- **Buscar Proyectos:**
  ```graphql
  query {
    user(login: $owner) {
      projectsV2(first: 20) {
        nodes {
          id
          title
        }
      }
    }
  }
  ```

- **Agregar Issue a Proyecto:**
  ```graphql
  mutation {
    addProjectV2ItemById(
      input: {projectId: $projectId, contentId: $contentId}
    ) {
      item { id }
    }
  }
  ```

## 🔐 Permisos Necesarios

El workflow requiere los siguientes permisos:

```yaml
permissions:
  contents: write              # Para commit y push
  issues: write                # Para crear issues
  repository-projects: write   # Para agregar a proyectos
```

Estos permisos son automáticamente proporcionados por `GITHUB_TOKEN`.

## 🧪 Testing Local

Para probar el script localmente (sin crear issues reales):

```bash
# 1. Simular variables de entorno
export GITHUB_TOKEN="your_token_here"
export GITHUB_REPOSITORY="angra8410/aplicaciones_laborales"

# 2. Ejecutar el script
python aplicaciones_laborales/scripts/create_issue_and_add_to_project.py \
  "DataAnalyst_TestCompany_2025-10-13"
```

**Nota:** Esto creará una issue real. Para testing, considera usar un repositorio de prueba.

## 📝 Logs y Debugging

### Convención de Nombres de Carpetas

El sistema espera carpetas con el formato: `{Cargo}_{Empresa}_{Fecha}`

**Ejemplos válidos:**
- `DataAnalyst_CompanyX_2025-10-13`
- `Senior_Data_Engineer_TechCorp_2025-11-01`
- `DataAnalyst-ColombiaRemote_Konduit_2025-10-11` (guiones permitidos en Cargo)

**Nota:** La empresa debe ser una sola palabra o usar CamelCase (ej: `TechCorp`, `LaTeam`). Si la empresa tiene múltiples palabras, se debe usar el script `sanitize_filename()` que elimina espacios.

### Logs del Script

El script proporciona logs detallados:

```
✅ Issue created successfully: #123
   URL: https://github.com/angra8410/aplicaciones_laborales/issues/123
✅ Found project: aplicacione-estados (ID: PVT_...)
✅ Issue added to project successfully
✅ All done! Issue created and added to project.
```

En caso de error:
```
❌ Failed to create issue: 403
   Response: {"message": "Resource not accessible by integration"}
```

## 🔍 Troubleshooting

### Problema: "GITHUB_TOKEN not available"

**Causa:** El token no está disponible en el entorno.

**Solución:** 
- En GitHub Actions, esto nunca debería ocurrir
- Localmente, define `export GITHUB_TOKEN="..."`

### Problema: "Project not found"

**Causa:** El nombre del proyecto no coincide exactamente.

**Solución:**
- Verifica que existe un proyecto con "aplicacione-estados" o "aplicacion" en el nombre
- El script busca de forma flexible (case-insensitive)
- Si no existe, crea el proyecto en GitHub

### Problema: "Failed to add issue to project"

**Causa:** Permisos insuficientes o proyecto no accesible.

**Solución:**
- Verifica que el workflow tiene `repository-projects: write`
- Asegúrate de que el proyecto es accesible para el repositorio
- Si el proyecto es organizacional, verifica configuración de acceso

### Problema: "Issue already exists"

**Causa:** Ya existe una issue para esta carpeta.

**Comportamiento:** El script detecta esto y termina exitosamente sin crear duplicado.

**Mensaje:**
```
ℹ️  Issue already exists for folder: DataAnalyst_CompanyX_2025-10-13
```

## 🎯 Mejoras Futuras

### Sugerencias de Expansión

1. **Columnas Personalizadas:**
   - Detectar el scoring y mover a columnas según match (Excellent → "Alta Prioridad")

2. **Campos Personalizados:**
   - Agregar campos custom al proyecto (fecha, empresa, scoring)

3. **Notificaciones:**
   - Enviar notificación cuando se crea la issue
   - Mencionar usuarios relevantes

4. **Métricas:**
   - Trackear tiempo entre aplicación y respuesta
   - Dashboard de aplicaciones por mes/empresa

5. **Integración con Calendar:**
   - Crear eventos de seguimiento automáticamente

## 📚 Referencias

- [GitHub REST API - Issues](https://docs.github.com/en/rest/issues/issues)
- [GitHub GraphQL API - Projects](https://docs.github.com/en/graphql/reference/objects#projectv2)
- [GitHub Actions - Permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication)

## 🤝 Contribuciones

Para mejorar el sistema:

1. Modifica `create_issue_and_add_to_project.py`
2. Actualiza esta documentación
3. Prueba con casos edge
4. Crea PR con descripción detallada

---

**Última actualización:** 2025-10-13  
**Versión:** 1.0 (Automatización Fase 1)  
**Autor:** GitHub Copilot - Consultor en Automatización DevOps
