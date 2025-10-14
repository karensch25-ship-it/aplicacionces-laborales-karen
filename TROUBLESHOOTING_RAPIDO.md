# 🔧 Guía Rápida de Troubleshooting: Copia Automática de PDFs

## 🎯 Síntomas Comunes y Soluciones Rápidas

---

### ❌ Síntoma 1: "Repositorio destino no existe o no es accesible"

**Lo que ves en los logs:**
```
⚠️  ADVERTENCIA: Repositorio destino no existe o no es accesible
   Repositorio: angra8410/todos-mis-documentos
   HTTP Status: 404
```

**Causa:**
El repositorio `todos-mis-documentos` no ha sido creado.

**Solución (2 minutos):**
1. Ve a https://github.com/new
2. Nombre del repositorio: `todos-mis-documentos` (exacto, sin mayúsculas)
3. Visibilidad: Privado (recomendado)
4. NO marques "Initialize with README"
5. Click "Create repository"

**Verificación:**
- Debes poder acceder a: https://github.com/angra8410/todos-mis-documentos
- Ejecuta el workflow de nuevo (Re-run all jobs)
- Verifica que ahora muestra: `✅ Repositorio destino encontrado`

---

### ❌ Síntoma 2: "Permission denied" al hacer push

**Lo que ves en los logs:**
```
remote: Permission to angra8410/todos-mis-documentos.git denied to github-actions[bot].
fatal: unable to access 'https://github.com/angra8410/todos-mis-documentos.git/': 
The requested URL returned error: 403
```

**Causa:**
GitHub Actions no tiene permisos de escritura en el repositorio destino.

**Solución (1 minuto):**
1. Ve a https://github.com/angra8410/todos-mis-documentos/settings/actions
2. Scroll hasta "Workflow permissions"
3. Selecciona: **"Read and write permissions"**
4. Click "Save"

**Verificación:**
- Ejecuta el workflow de nuevo (Re-run all jobs)
- El push debe completarse exitosamente

---

### ❌ Síntoma 3: Step "Copiar CV PDF" aparece como "skipped"

**Lo que ves en GitHub Actions:**
```
⊘ Copiar CV PDF a repositorio todos-mis-documentos (SKIPPED)
```

**Causa:**
El step de validación detectó que el repositorio no existe o no es accesible.

**Solución:**
1. Revisa los logs del step "Validar configuración de repositorio destino"
2. Sigue las instrucciones que aparecen ahí
3. Típicamente será crear el repositorio (Solución del Síntoma 1)

**Verificación:**
- Después de crear el repo, el step no debe aparecer como skipped

---

### ❌ Síntoma 4: "GITHUB_TOKEN not available"

**Lo que ves en los logs:**
```
❌ Error: GITHUB_TOKEN not available
   This script requires GITHUB_TOKEN to push to todos-mis-documentos
```

**Causa:**
El workflow no tiene configurado el token de GitHub (muy raro, no debería pasar).

**Solución:**
1. Verifica que el archivo `.github/workflows/crear_aplicacion.yml` contiene:
   ```yaml
   env:
     GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
   ```
2. Si no lo tiene, agrégalo bajo el step correspondiente
3. Commit y push el cambio

**Verificación:**
- El error no debe aparecer en la siguiente ejecución

---

### ⚠️ Síntoma 5: El workflow se ejecuta pero no se generan PDFs

**Lo que ves:**
- Workflow completa exitosamente
- No hay PDFs en `to_process_procesados/`

**Causa:**
El archivo YAML de la aplicación tiene errores de formato.

**Solución:**
1. Verifica que tu archivo YAML en `to_process/` tiene el formato correcto:
   ```yaml
   cargo: "Data Analyst"
   empresa: "EmpresaX"
   descripcion: |
     Descripción del trabajo...
   requisitos:
     - Requisito 1
     - Requisito 2
   ```
2. Revisa los logs del step "Procesar archivo de nueva aplicación"
3. Busca mensajes de error relacionados con YAML

**Verificación:**
- PDFs deben aparecer en `to_process_procesados/[Cargo]_[Empresa]_[Fecha]/`

---

### ⚠️ Síntoma 6: PDF se copia pero no aparece organizado por fecha

**Lo que ves:**
- PDF copiado exitosamente
- Pero no está en carpeta con formato YYYY-MM-DD

**Causa:**
El nombre de la carpeta procesada no tiene el formato esperado.

**Solución:**
- Los nombres de carpeta deben terminar con `_YYYY-MM-DD`
- Ejemplo: `DataAnalyst_EmpresaX_2025-10-15`
- El script extrae la fecha del nombre de la carpeta

**Verificación:**
- Verifica que la carpeta en `to_process_procesados/` tiene el formato correcto
- La fecha debe ser la última parte después del último guión bajo

---

## 🔍 Cómo Leer los Logs del Workflow

### Ubicación de los Logs

1. Ve a la pestaña **"Actions"** en el repositorio
2. Click en el workflow más reciente
3. Click en el job **"crear-carpeta-aplicacion"**
4. Expande los steps para ver logs detallados

### Logs Importantes

#### Step: "Validar configuración de repositorio destino"
```
✅ Si ves:
Verificando si el repositorio destino existe...
✅ Repositorio destino encontrado: angra8410/todos-mis-documentos

➡️ Todo está bien, continúa al siguiente step

❌ Si ves:
⚠️  ADVERTENCIA: Repositorio destino no existe o no es accesible
   HTTP Status: 404

➡️ Necesitas crear el repositorio (ver Síntoma 1)
```

#### Step: "Copiar CV PDF a repositorio todos-mis-documentos"
```
✅ Si ves:
📂 Copiando PDF al repositorio todos-mis-documentos
📥 Clonando repositorio angra8410/todos-mis-documentos...
📁 Carpeta creada/verificada: 2025-10-15/
✅ PDF copiado: 2025-10-15/ANTONIO_GUTIERREZ_RESUME_EmpresaX.pdf
💾 Commit creado: 📄 CV generado: Data Analyst - EmpresaX (2025-10-15)
🚀 Enviando cambios al repositorio remoto...
✅ PDF copiado exitosamente

➡️ ¡Perfecto! Todo funcionó correctamente

❌ Si ves:
Error ejecutando comando: git push
remote: Permission to ... denied

➡️ Problema de permisos (ver Síntoma 2)
```

---

## 📋 Checklist de Verificación Rápida

Usa esta lista para verificar que todo está correctamente configurado:

### Requisitos Previos
- [ ] Repositorio `todos-mis-documentos` existe
- [ ] Puedo acceder a: https://github.com/angra8410/todos-mis-documentos
- [ ] Permisos de GitHub Actions configurados en "Read and write"

### Durante la Ejecución
- [ ] Step "Validar configuración" muestra: ✅ Repositorio encontrado
- [ ] Step "Copiar CV PDF" NO está marcado como (skipped)
- [ ] Logs muestran: ✅ PDF copiado exitosamente

### Después de la Ejecución
- [ ] Repositorio `todos-mis-documentos` tiene carpeta con fecha (YYYY-MM-DD)
- [ ] Carpeta contiene el PDF del CV
- [ ] Commit tiene mensaje descriptivo: "📄 CV generado: ..."

---

## 🆘 Solución Rápida Universal

Si nada de lo anterior funciona, sigue estos pasos en orden:

1. **Verifica que el repositorio existe:**
   ```bash
   curl -s https://github.com/angra8410/todos-mis-documentos
   # Debe retornar código 200, no 404
   ```

2. **Verifica permisos:**
   - Ve a: https://github.com/angra8410/todos-mis-documentos/settings/actions
   - Confirma: "Read and write permissions" está seleccionado

3. **Re-ejecuta el workflow:**
   - Ve a: https://github.com/angra8410/aplicaciones_laborales/actions
   - Click en el workflow fallido
   - Click "Re-run all jobs"

4. **Revisa los logs nuevamente:**
   - Sigue la sección "Cómo Leer los Logs del Workflow" arriba

5. **Si aún falla:**
   - Copia los logs completos
   - Revisa la documentación completa en:
     - [CONFIGURACION_INICIAL.md](CONFIGURACION_INICIAL.md)
     - [EJEMPLO_VISUAL_WORKFLOW.md](EJEMPLO_VISUAL_WORKFLOW.md)

---

## 📞 Recursos Adicionales

- **Guía Paso a Paso:** [CONFIGURACION_INICIAL.md](CONFIGURACION_INICIAL.md)
- **Ejemplos Visuales:** [EJEMPLO_VISUAL_WORKFLOW.md](EJEMPLO_VISUAL_WORKFLOW.md)
- **Documentación Técnica:** [SETUP_REQUIRED.md](SETUP_REQUIRED.md)
- **Resumen Ejecutivo:** [SOLUCION_IMPLEMENTADA.md](SOLUCION_IMPLEMENTADA.md)

---

## 💡 Tips Pro

### Tip 1: Verifica el Estado con la API de GitHub
```bash
# Verifica si el repo existe
curl -H "Authorization: token YOUR_TOKEN" \
  https://api.github.com/repos/angra8410/todos-mis-documentos

# Debe retornar JSON con información del repo
# Si retorna 404, el repo no existe
```

### Tip 2: Prueba Local del Script
```bash
# Desde el directorio raíz del repositorio
export GITHUB_TOKEN="your_token_here"
python aplicaciones_laborales/scripts/copy_pdf_to_documents_repo.py \
  "DataAnalyst_TestCompany_2025-10-15"
```

### Tip 3: Revisa los Commits en todos-mis-documentos
```bash
# Clona el repo destino para verificar
git clone https://github.com/angra8410/todos-mis-documentos.git
cd todos-mis-documentos
git log --oneline

# Debes ver commits con mensajes como:
# 📄 CV generado: Data Analyst - EmpresaX (2025-10-15)
```

---

**Última actualización:** 2025-10-14  
**Versión:** 1.0  
**Tiempo estimado de resolución:** 5-10 minutos para la mayoría de problemas
