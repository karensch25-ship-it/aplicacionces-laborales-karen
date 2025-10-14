# Guía de Automatización: Copia Automática de CV PDF al Repositorio todos-mis-documentos

## 📋 Resumen

Esta guía documenta la automatización que copia los CV PDF generados al repositorio `todos-mis-documentos`, organizándolos por fecha de aplicación en carpetas con formato YYYY-MM-DD.

---

## 🎯 Objetivo

Automatizar la copia de cada CV PDF generado (ej: `ANTONIO_GUTIERREZ_RESUME_EMPRESA.pdf`) al repositorio `angra8410/todos-mis-documentos`, organizando los documentos en carpetas por fecha de aplicación para facilitar la trazabilidad y el versionado documental.

---

## 🏗️ Arquitectura del Flujo

```
to_process/
  └── nueva_aplicacion.yaml  (datos de la vacante)
        ↓
GitHub Actions Workflow (.github/workflows/crear_aplicacion.yml)
        ↓
Script Python (procesar_aplicacion.py)
        ↓
to_process_procesados/
  └── [Cargo_Empresa_YYYY-MM-DD]/
      ├── descripcion.md
      ├── requerimientos.md
      ├── hoja_de_vida_adecuada.md
      ├── ANTONIO_GUTIERREZ_RESUME_[Empresa].pdf  ← Este archivo
      └── SCORING_REPORT.pdf
        ↓
Script Python (copy_pdf_to_documents_repo.py)
        ↓
Repositorio: angra8410/todos-mis-documentos
  └── YYYY-MM-DD/  (carpeta por fecha)
      ├── ANTONIO_GUTIERREZ_RESUME_Empresa1.pdf
      ├── ANTONIO_GUTIERREZ_RESUME_Empresa2.pdf
      └── ANTONIO_GUTIERREZ_RESUME_Empresa3.pdf
```

---

## 🔧 Componentes Implementados

### 1. Script de Copia de PDF

**Archivo:** `aplicaciones_laborales/scripts/copy_pdf_to_documents_repo.py`

**Funcionalidad:**
- Extrae la fecha de aplicación del nombre de la carpeta (formato: `Cargo_Empresa_YYYY-MM-DD`)
- Clona el repositorio `todos-mis-documentos` en un directorio temporal
- Crea la estructura de carpetas por fecha (`YYYY-MM-DD/`) si no existe
- Copia el PDF del CV a la carpeta correspondiente
- Crea un commit con mensaje descriptivo: `📄 CV generado: [Cargo] - [Empresa] (YYYY-MM-DD)`
- Hace push al repositorio remoto
- Limpia el directorio temporal

**Características:**
- ✅ Manejo robusto de errores
- ✅ Validación de fecha
- ✅ Detección automática de PDFs existentes (sobrescribe si es necesario)
- ✅ Mensajes informativos durante el proceso
- ✅ Limpieza automática de archivos temporales

### 2. Integración en GitHub Actions

**Archivo:** `.github/workflows/crear_aplicacion.yml`

**Nuevo paso agregado:**
```yaml
- name: Copiar CV PDF a repositorio todos-mis-documentos
  env:
    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
  run: |
    for folder in to_process_procesados/*/; do
      if [ -d "$folder" ]; then
        folder_name=$(basename "$folder")
        if [[ "$folder_name" != *.yaml ]]; then
          echo "Procesando copia de PDF para: $folder_name"
          python aplicaciones_laborales/scripts/copy_pdf_to_documents_repo.py "$folder_name" || echo "⚠️  Advertencia: No se pudo copiar PDF para $folder_name"
        fi
      fi
    done
```

**Orden de ejecución:**
1. Checkout del repositorio
2. Instalación de Python y dependencias
3. Instalación de pandoc y LaTeX
4. **Procesamiento de aplicación** (genera PDF)
5. **✨ NUEVO: Copia de PDF a todos-mis-documentos**
6. Commit y push de cambios locales

---

## 📊 Estructura de Carpetas Resultante

### En `aplicaciones_laborales` (repositorio actual):

```
to_process_procesados/
├── DataAnalyst_Adoreal_2025-10-13/
│   ├── ANTONIO_GUTIERREZ_RESUME_Adoreal.pdf
│   ├── SCORING_REPORT.pdf
│   ├── descripcion.md
│   ├── hoja_de_vida_adecuada.md
│   └── requerimientos.md
├── DataAnalyst_LaTeam_2025-10-11/
│   ├── ANTONIO_GUTIERREZ_RESUME_LaTeam.pdf
│   └── ...
└── BusinessAnalyst_Applaudo_2025-10-14/
    ├── ANTONIO_GUTIERREZ_RESUME_Applaudo.pdf
    └── ...
```

### En `todos-mis-documentos` (repositorio destino):

```
todos-mis-documentos/
├── 2025-10-11/
│   ├── ANTONIO_GUTIERREZ_RESUME_LaTeam.pdf
│   └── ANTONIO_GUTIERREZ_RESUME_Konduit.pdf
├── 2025-10-13/
│   ├── ANTONIO_GUTIERREZ_RESUME_Adoreal.pdf
│   └── ANTONIO_GUTIERREZ_RESUME_INDI.pdf
└── 2025-10-14/
    ├── ANTONIO_GUTIERREZ_RESUME_Applaudo.pdf
    ├── ANTONIO_GUTIERREZ_RESUME_Hyland.pdf
    └── ANTONIO_GUTIERREZ_RESUME_Wizeline.pdf
```

**Ventajas de esta estructura:**
- 📅 Organización cronológica clara
- 🔍 Fácil búsqueda de aplicaciones por fecha
- 📦 Agrupación de todas las aplicaciones del mismo día
- 📈 Trazabilidad completa del historial

---

## 🔐 Configuración de Seguridad

### Permisos Requeridos

El workflow requiere los siguientes permisos (ya configurados):

```yaml
permissions:
  contents: write              # Para commit y push
  issues: write                # Para crear issues
  repository-projects: write   # Para agregar a proyectos
```

### Token de Acceso

El script utiliza `GITHUB_TOKEN` proporcionado automáticamente por GitHub Actions. Este token tiene permisos para:
- ✅ Clonar repositorios públicos del mismo usuario/organización
- ✅ Hacer push a repositorios con permisos de escritura
- ✅ Crear commits en nombre de `github-actions[bot]`

**Importante:** El repositorio `todos-mis-documentos` debe:
- Existir en la cuenta `angra8410`
- Ser accesible con el `GITHUB_TOKEN` del workflow
- Tener habilitado el acceso de escritura para GitHub Actions

---

## 🧪 Testing

### Testing Local (Opcional)

Para probar el script localmente sin crear commits reales:

```bash
# 1. Configurar variables de entorno
export GITHUB_TOKEN="tu_token_aqui"

# 2. Asegurarse de tener una carpeta procesada
ls -la to_process_procesados/

# 3. Ejecutar el script
python aplicaciones_laborales/scripts/copy_pdf_to_documents_repo.py \
  DataAnalyst_TestCompany_2025-10-13
```

**Nota:** Esto creará un commit real en `todos-mis-documentos`. Para testing, considera:
- Usar un repositorio de prueba
- Revisar el código antes de ejecutar
- Hacer pruebas en una rama separada

### Verificación del Workflow

Después de hacer push de un archivo YAML a `to_process/`:

1. Ve a **Actions** en GitHub
2. Verifica que el workflow `Crear carpeta de nueva aplicación laboral` se ejecutó
3. Revisa los logs del paso `Copiar CV PDF a repositorio todos-mis-documentos`
4. Verifica en `angra8410/todos-mis-documentos` que:
   - Se creó la carpeta con la fecha correcta
   - El PDF está presente
   - El commit tiene el mensaje apropiado

---

## 📝 Ejemplo de Uso

### Paso 1: Crear Aplicación

Crea un archivo YAML en `to_process/`:

```yaml
# to_process/nueva_aplicacion.yaml
cargo: "Data Analyst"
empresa: "TechCorp"
fecha: "2025-10-15"
descripcion: |
  Exciting opportunity for a data analyst...
requerimientos:
  - SQL expertise
  - Power BI experience
  - Python skills
```

### Paso 2: Push al Repositorio

```bash
git add to_process/nueva_aplicacion.yaml
git commit -m "Nueva aplicación: Data Analyst en TechCorp"
git push
```

### Paso 3: Verificar Resultados

**En `aplicaciones_laborales`:**
- Carpeta creada: `to_process_procesados/DataAnalyst_TechCorp_2025-10-15/`
- PDF generado: `ANTONIO_GUTIERREZ_RESUME_TechCorp.pdf`
- Issue creada en GitHub

**En `todos-mis-documentos`:**
- Carpeta creada: `2025-10-15/`
- PDF copiado: `ANTONIO_GUTIERREZ_RESUME_TechCorp.pdf`
- Commit: `📄 CV generado: DataAnalyst - TechCorp (2025-10-15)`

---

## 🔍 Trazabilidad y Auditoría

### Mensajes de Commit

El script genera commits con el siguiente formato:

```
📄 CV generado: [Cargo] - [Empresa] (YYYY-MM-DD)
```

**Ejemplo:**
```
📄 CV generado: DataAnalyst - TechCorp (2025-10-15)
```

Esto permite:
- 🔎 Búsqueda rápida por cargo o empresa en el historial
- 📅 Filtrado por fecha
- 🔗 Correlación con issues en `aplicaciones_laborales`

### Vinculación con Issues

Cada aplicación genera:
1. **Issue en `aplicaciones_laborales`:** Con título `Aplicación: [Cargo] en [Empresa]`
2. **Commit en `aplicaciones_laborales`:** `Automatización: Nueva aplicación laboral creada por workflow`
3. **Commit en `todos-mis-documentos`:** `📄 CV generado: [Cargo] - [Empresa] (YYYY-MM-DD)`

Puedes vincular manualmente la issue con el commit en `todos-mis-documentos` añadiendo un comentario en la issue con el link al commit.

---

## 🐛 Troubleshooting

### Problema: "GITHUB_TOKEN not available"

**Causa:** El token no está configurado en el entorno del workflow.

**Solución:**
- Verifica que el workflow tiene `env: GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}`
- Revisa los permisos del workflow en `.github/workflows/crear_aplicacion.yml`

### Problema: "Permission denied" al hacer push

**Causa:** El token no tiene permisos de escritura en `todos-mis-documentos`.

**Solución:**
1. Verifica que el repositorio `todos-mis-documentos` existe
2. Verifica que GitHub Actions tiene permisos de escritura:
   - Ve a Settings → Actions → General
   - En "Workflow permissions", selecciona "Read and write permissions"

### Problema: "Repository not found"

**Causa:** El repositorio `todos-mis-documentos` no existe o no es accesible.

**Solución:**
- Crea el repositorio `angra8410/todos-mis-documentos` en GitHub
- Asegúrate de que es público o que el token tiene acceso

### Problema: "PDF not found"

**Causa:** El PDF no se generó correctamente en el paso anterior.

**Solución:**
- Revisa los logs del paso "Procesar archivo de nueva aplicación"
- Verifica que pandoc y LaTeX se instalaron correctamente
- Asegúrate de que el archivo YAML tiene el formato correcto

---

## 📈 Mejoras Futuras

### Fase Actual: Implementado ✅
- ✅ Copia automática de PDF a `todos-mis-documentos`
- ✅ Organización por fecha (YYYY-MM-DD)
- ✅ Commits descriptivos con trazabilidad
- ✅ Manejo de errores y validaciones

### Mejoras Propuestas
- **Notificaciones:** Enviar notificación (email, Slack) cuando se copia un PDF
- **Metadata:** Crear archivo `metadata.json` en cada carpeta de fecha con detalles de las aplicaciones
- **Índice automático:** Generar un `README.md` en `todos-mis-documentos` con índice de todas las aplicaciones
- **Backup:** Implementar copia de seguridad adicional a Google Drive o S3
- **Estadísticas:** Generar dashboard con métricas de aplicaciones por fecha/empresa/cargo
- **Versionado:** Mantener múltiples versiones si se genera más de un CV para la misma empresa

---

## 📚 Referencias

### Documentación del Proyecto
- [AUTOMATION_QUICKSTART.md](AUTOMATION_QUICKSTART.md) - Inicio rápido
- [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md) - Guía de automatización de issues
- [README.md](README.md) - Visión general del proyecto

### Archivos de Código
- [`copy_pdf_to_documents_repo.py`](aplicaciones_laborales/scripts/copy_pdf_to_documents_repo.py) - Script principal
- [`procesar_aplicacion.py`](aplicaciones_laborales/scripts/procesar_aplicacion.py) - Generación de CV
- [`.github/workflows/crear_aplicacion.yml`](.github/workflows/crear_aplicacion.yml) - Workflow de CI/CD

### Recursos Externos
- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [Git Documentation](https://git-scm.com/doc)
- [Python subprocess module](https://docs.python.org/3/library/subprocess.html)

---

## ✅ Checklist de Implementación

Para verificar que la automatización está funcionando correctamente:

- [x] Script `copy_pdf_to_documents_repo.py` creado
- [x] Workflow actualizado con nuevo paso
- [x] Permisos configurados correctamente
- [ ] Repositorio `todos-mis-documentos` creado y accesible
- [ ] Primera aplicación de prueba procesada exitosamente
- [ ] PDF copiado correctamente a `todos-mis-documentos`
- [ ] Commit visible en el historial de `todos-mis-documentos`
- [ ] Estructura de carpetas por fecha funcionando

---

**Última actualización:** 2025-10-14  
**Versión:** 1.0  
**Autor:** GitHub Actions Automation Team
