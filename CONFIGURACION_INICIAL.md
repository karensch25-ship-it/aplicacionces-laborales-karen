# 🚀 Configuración Inicial: Copia Automática de CV PDF

## ⚠️ IMPORTANTE: Configuración Requerida

Para que el flujo CI/CD copie automáticamente los CV generados al repositorio `todos-mis-documentos`, **DEBES** completar esta configuración inicial:

---

## Paso 1: Crear el Repositorio Destino

### 1.1 Crear Nuevo Repositorio

1. **Ve a GitHub y crea un nuevo repositorio:**
   - 🔗 URL: https://github.com/new
   - 📝 Nombre del repositorio: **`todos-mis-documentos`** (exactamente este nombre)
   - 👁️ Visibilidad: **Privado** (recomendado para proteger tus CVs)
   - ☑️ **NO** inicialices con README, .gitignore o licencia (déjalo vacío)

2. **Haz clic en "Create repository"**

### 1.2 Verificación

Después de crear el repositorio, verifica que puedas acceder a:
```
https://github.com/angra8410/todos-mis-documentos
```

---

## Paso 2: Configurar Permisos de GitHub Actions

**IMPORTANTE:** Esta configuración debe hacerse en el repositorio **`todos-mis-documentos`** (no en `aplicaciones_laborales`).

### 2.1 Acceder a Configuración

1. Ve al repositorio `todos-mis-documentos` que acabas de crear
2. Haz clic en **"Settings"** (⚙️)

### 2.2 Configurar Permisos de Workflow

1. En el menú lateral izquierdo, haz clic en **"Actions"** → **"General"**
2. Scroll hacia abajo hasta la sección **"Workflow permissions"**
3. Selecciona: **☑️ "Read and write permissions"**
4. Opcionalmente, marca: **☑️ "Allow GitHub Actions to create and approve pull requests"**
5. Haz clic en **"Save"**

### 2.3 Diagrama Visual

```
Settings > Actions > General > Workflow permissions

⚪ Read repository contents and packages permissions
🔘 Read and write permissions  ← SELECCIONAR ESTA OPCIÓN

☑️ Allow GitHub Actions to create and approve pull requests (opcional)

[Save]  ← HACER CLIC AQUÍ
```

---

## Paso 3: Verificar la Configuración

### 3.1 Ejecutar una Prueba

1. En el repositorio `aplicaciones_laborales`, crea un nuevo archivo YAML en `to_process/`
2. Haz commit y push
3. Ve a la pestaña **"Actions"** en `aplicaciones_laborales`
4. Observa la ejecución del workflow

### 3.2 Qué Esperar

**✅ Configuración Correcta:**
```
Validar configuración de repositorio destino
✅ Repositorio destino encontrado: angra8410/todos-mis-documentos

Copiar CV PDF a repositorio todos-mis-documentos
📂 Copiando PDF al repositorio todos-mis-documentos
📥 Clonando repositorio angra8410/todos-mis-documentos...
📁 Carpeta creada/verificada: 2025-10-15/
✅ PDF copiado: 2025-10-15/ANTONIO_GUTIERREZ_RESUME_EmpresaX.pdf
💾 Commit creado: 📄 CV generado: Data Analyst - EmpresaX (2025-10-15)
🚀 Enviando cambios al repositorio remoto...
✅ PDF copiado exitosamente al repositorio todos-mis-documentos
```

**⚠️ Configuración Incompleta:**
```
Validar configuración de repositorio destino
⚠️  ADVERTENCIA: Repositorio destino no existe o no es accesible
   Repositorio: angra8410/todos-mis-documentos
   
📋 Para habilitar la copia automática de PDFs:
   1. Crea el repositorio 'todos-mis-documentos' en: https://github.com/new
   ...
```

---

## Paso 4: Verificar Resultados

Después de ejecutar el workflow correctamente:

1. Ve al repositorio `todos-mis-documentos`
2. Deberías ver una estructura de carpetas como:
   ```
   todos-mis-documentos/
   ├── 2025-10-15/
   │   ├── ANTONIO_GUTIERREZ_RESUME_EmpresaA.pdf
   │   └── ANTONIO_GUTIERREZ_RESUME_EmpresaB.pdf
   ├── 2025-10-14/
   │   ├── ANTONIO_GUTIERREZ_RESUME_EmpresaC.pdf
   │   └── ANTONIO_GUTIERREZ_RESUME_EmpresaD.pdf
   └── ...
   ```

3. Cada carpeta agrupa todos los CVs generados en esa fecha
4. Los commits tendrán mensajes descriptivos:
   ```
   📄 CV generado: Data Analyst - EmpresaX (2025-10-15)
   📄 CV generado: Business Analyst - EmpresaY (2025-10-15)
   ```

---

## 🐛 Solución de Problemas

### Error: "Repository not found"

**Causa:** El repositorio `todos-mis-documentos` no existe o no es accesible.

**Solución:**
1. Verifica que el repositorio existe: https://github.com/angra8410/todos-mis-documentos
2. Si no existe, créalo siguiendo el Paso 1
3. Asegúrate de que el nombre es exactamente `todos-mis-documentos` (sin espacios, sin mayúsculas)

### Error: "Permission denied" al hacer push

**Causa:** Los permisos de GitHub Actions no están configurados correctamente.

**Solución:**
1. Ve a `todos-mis-documentos` → Settings → Actions → General
2. Verifica que está seleccionado "Read and write permissions"
3. Guarda los cambios
4. Vuelve a ejecutar el workflow (Re-run en Actions)

### Error: "GITHUB_TOKEN not available"

**Causa:** El token no está configurado en el workflow.

**Solución:**
- El workflow ya tiene configurado `GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}`
- Este error no debería ocurrir en la configuración actual
- Si ocurre, revisa que el archivo `.github/workflows/crear_aplicacion.yml` tiene la configuración correcta

### El workflow se ejecuta pero no copia PDFs

**Causa:** La validación detectó que el repositorio no existe.

**Solución:**
1. Revisa los logs del step "Validar configuración de repositorio destino"
2. Si muestra una advertencia, sigue las instrucciones del Paso 1 y Paso 2
3. El step "Copiar CV PDF..." se saltará si el repositorio no existe

---

## 📊 Diagrama de Flujo Completo

```
┌─────────────────────────────────────────┐
│ Usuario crea archivo YAML              │
│ en to_process/ y hace push             │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ GitHub Actions se activa                │
│ - Instala dependencias                  │
│ - Genera CV PDF personalizado           │
│ - Crea scoring report                   │
└──────────────────┬──────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────┐
│ Valida si repo destino existe           │
│ (todos-mis-documentos)                  │
└──────────────────┬──────────────────────┘
                   │
         ┌─────────┴─────────┐
         │                   │
         ▼                   ▼
    ✅ Existe          ⚠️ No existe
         │                   │
         ▼                   ▼
┌──────────────────┐  ┌─────────────────┐
│ Copia PDF        │  │ Muestra         │
│ - Clona repo     │  │ advertencia y   │
│ - Crea carpeta   │  │ salta este step │
│   YYYY-MM-DD     │  └─────────────────┘
│ - Copia archivo  │
│ - Commit & Push  │
└──────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│ ✅ PDFs organizados por fecha en        │
│    todos-mis-documentos                 │
└─────────────────────────────────────────┘
```

---

## 🔒 Consideraciones de Seguridad

### ✅ Seguro

- ✅ Usar `GITHUB_TOKEN` (automático, no requiere crear tokens adicionales)
- ✅ El repositorio `todos-mis-documentos` puede ser **privado** (recomendado)
- ✅ Los commits se hacen como `github-actions[bot]`
- ✅ El token solo tiene acceso a repositorios del mismo usuario/organización

### ⚠️ Ten en Cuenta

- Si `todos-mis-documentos` es **público**, los CVs serán visibles para todos
- **Recomendación:** Haz el repositorio **privado** para proteger información sensible
- El `GITHUB_TOKEN` se genera automáticamente por GitHub Actions y no necesitas configurarlo manualmente
- El token solo funciona durante la ejecución del workflow y expira automáticamente

---

## ✅ Checklist de Configuración

Usa esta lista para verificar que todo está configurado correctamente:

- [ ] **Paso 1.1:** Crear repositorio `todos-mis-documentos` en GitHub
- [ ] **Paso 1.2:** Verificar acceso al repositorio
- [ ] **Paso 2.2:** Configurar permisos "Read and write" en Settings → Actions
- [ ] **Paso 3.1:** Ejecutar una prueba con un archivo YAML nuevo
- [ ] **Paso 3.2:** Verificar logs del workflow - debe mostrar "✅ Repositorio destino encontrado"
- [ ] **Paso 4:** Confirmar que los PDFs aparecen en `todos-mis-documentos` organizados por fecha

---

## 📚 Documentación Adicional

- **Guía Completa:** `SETUP_REQUIRED.md` - Información detallada de configuración
- **Troubleshooting:** `AUTOMATION_PDF_COPY_GUIDE.md` - Solución de problemas comunes
- **Diagrama de Flujo:** `WORKFLOW_DIAGRAM.md` - Visualización del proceso completo
- **Quick Start:** `AUTOMATION_PDF_COPY_QUICKSTART.md` - Inicio rápido para usuarios avanzados

---

## 🎯 Resultado Final

Una vez completada la configuración, cada vez que crees una nueva aplicación laboral:

1. ✅ Se genera automáticamente un CV personalizado en PDF
2. ✅ Se crea un scoring report de compatibilidad
3. ✅ El CV se copia automáticamente a `todos-mis-documentos`
4. ✅ Los CVs se organizan por fecha (YYYY-MM-DD)
5. ✅ Todas las aplicaciones del mismo día se agrupan en la misma carpeta
6. ✅ Tienes trazabilidad completa con commits descriptivos

**¡Tu flujo CI/CD estará completamente automatizado! 🎉**

---

## 💬 ¿Necesitas Ayuda?

Si encuentras algún problema durante la configuración:

1. Revisa la sección **"Solución de Problemas"** arriba
2. Consulta los logs detallados en GitHub Actions (pestaña "Actions")
3. Verifica la documentación adicional en los archivos mencionados
4. Asegúrate de haber seguido todos los pasos en orden

---

**Última actualización:** 2025-10-14  
**Versión:** 1.0
