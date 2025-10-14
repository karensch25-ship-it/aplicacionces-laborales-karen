# 🚀 Quick Start: Copia Automática de CV PDFs

## ⚡ Setup en 5 Minutos

Esta guía te ayudará a configurar la copia automática de CV PDFs al repositorio `todos-mis-documentos`.

---

## 📋 Pre-requisitos

### 1. Crear el Repositorio Destino

El repositorio `todos-mis-documentos` debe existir antes de usar esta funcionalidad:

```bash
# Opción 1: Crear via web
# Ve a https://github.com/new y crea el repositorio "todos-mis-documentos"

# Opción 2: Crear via CLI (requiere gh CLI)
gh repo create angra8410/todos-mis-documentos --public
```

### 2. Configurar Permisos de GitHub Actions

En el repositorio `todos-mis-documentos`:

1. Ve a **Settings → Actions → General**
2. En "Workflow permissions", selecciona **"Read and write permissions"**
3. Marca ✅ **"Allow GitHub Actions to create and approve pull requests"**
4. Click **Save**

---

## ✅ Verificar que Todo Funciona

### Paso 1: Crear una Aplicación de Prueba

Crea un archivo en `to_process/test_aplicacion.yaml`:

```yaml
cargo: "Test Data Analyst"
empresa: "TestCorp"
fecha: "2025-10-14"
descripcion: |
  Esta es una aplicación de prueba para verificar que la copia automática funciona.
requerimientos:
  - SQL
  - Python
  - Power BI
```

### Paso 2: Hacer Commit y Push

```bash
git add to_process/test_aplicacion.yaml
git commit -m "Test: Verificar copia automática de PDF"
git push
```

### Paso 3: Verificar la Ejecución

1. Ve a **Actions** en GitHub
2. Busca el workflow "Crear carpeta de nueva aplicación laboral"
3. Verifica que todos los pasos se ejecutaron exitosamente:
   - ✅ Procesar archivo de nueva aplicación
   - ✅ **Copiar CV PDF a repositorio todos-mis-documentos** ← Este es el nuevo paso
   - ✅ Commit y push de cambios

### Paso 4: Verificar el Resultado

En el repositorio `todos-mis-documentos`:

1. Verifica que existe la carpeta `2025-10-14/`
2. Dentro debe estar el archivo `ANTONIO_GUTIERREZ_RESUME_TestCorp.pdf`
3. Revisa el commit history - debe haber un commit: `📄 CV generado: TestData_Analyst - TestCorp (2025-10-14)`

---

## 📊 Estructura Resultante

### En `aplicaciones_laborales`:

```
to_process_procesados/
└── TestDataAnalyst_TestCorp_2025-10-14/
    ├── ANTONIO_GUTIERREZ_RESUME_TestCorp.pdf  ← Original
    ├── SCORING_REPORT.pdf
    ├── descripcion.md
    ├── hoja_de_vida_adecuada.md
    └── requerimientos.md
```

### En `todos-mis-documentos`:

```
2025-10-14/
└── ANTONIO_GUTIERREZ_RESUME_TestCorp.pdf  ← Copia automática
```

---

## 🔍 Troubleshooting Rápido

### ❌ Error: "Permission denied"

**Solución:** Verifica permisos en Settings → Actions → General del repo `todos-mis-documentos`

### ❌ Error: "Repository not found"

**Solución:** Crea el repositorio `angra8410/todos-mis-documentos` en GitHub

### ❌ El PDF no se copió

**Solución:** 
1. Revisa los logs del workflow en Actions
2. Verifica que el paso "Copiar CV PDF..." se ejecutó
3. Busca mensajes de error en los logs

### ⚠️ Warning: "No se pudo copiar PDF"

**Causa:** El script encontró un problema pero continuó con el flujo normal

**Solución:** Revisa los logs detallados del workflow para más información

---

## 📚 Siguiente Paso

Para más detalles técnicos, consulta la [Guía Completa](AUTOMATION_PDF_COPY_GUIDE.md).

---

## ✨ Ejemplo de Uso Real

```bash
# 1. Crear aplicación
cat > to_process/nueva_aplicacion.yaml << EOF
cargo: "Senior Data Analyst"
empresa: "Microsoft"
fecha: "2025-10-15"
descripcion: |
  Exciting opportunity at Microsoft...
requerimientos:
  - SQL
  - Azure
  - Power BI
EOF

# 2. Push
git add to_process/nueva_aplicacion.yaml
git commit -m "Nueva aplicación: Senior Data Analyst en Microsoft"
git push

# 3. Espera 2-3 minutos

# 4. Verifica en GitHub:
# - aplicaciones_laborales/to_process_procesados/SeniorDataAnalyst_Microsoft_2025-10-15/
# - todos-mis-documentos/2025-10-15/ANTONIO_GUTIERREZ_RESUME_Microsoft.pdf
```

---

## 🎉 ¡Listo!

Tu sistema ahora copia automáticamente cada CV PDF generado al repositorio `todos-mis-documentos`, organizándolos por fecha para fácil acceso y trazabilidad.

**Beneficios:**
- 📅 Organización cronológica automática
- 🔍 Fácil búsqueda de CVs por fecha
- 📦 Backup centralizado de todos los CVs
- 📈 Trazabilidad completa con commits descriptivos
- 🚀 Zero esfuerzo manual

---

**¿Preguntas?** Consulta la [Guía Completa](AUTOMATION_PDF_COPY_GUIDE.md) para más detalles.
