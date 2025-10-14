# ⚙️ Configuración Requerida: Copia Automática de PDFs

## 🎯 Pasos Obligatorios

Para que la copia automática de PDFs funcione correctamente, el usuario **DEBE** completar los siguientes pasos:

---

## 1. 📦 Crear el Repositorio `todos-mis-documentos`

### Opción A: Via GitHub Web UI

1. Ve a [https://github.com/new](https://github.com/new)
2. **Repository name:** `todos-mis-documentos`
3. **Description:** (opcional) `Repositorio centralizado de todos los CV PDFs generados automáticamente`
4. **Visibility:** Elige **Public** o **Private** según prefieras
5. **No inicialices** con README, .gitignore o licencia (el repo puede estar vacío)
6. Click **Create repository**

### Opción B: Via GitHub CLI

```bash
# Asegúrate de tener gh CLI instalado
gh auth login  # Si no has autenticado antes

# Crear repositorio público
gh repo create angra8410/todos-mis-documentos --public

# O crear repositorio privado
gh repo create angra8410/todos-mis-documentos --private
```

### Opción C: Via Git Commands

```bash
# 1. Crear repositorio en GitHub primero (opción A)
# 2. Luego inicializar localmente (opcional):
mkdir todos-mis-documentos
cd todos-mis-documentos
git init
echo "# CVs Generados Automáticamente" > README.md
git add README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/angra8410/todos-mis-documentos.git
git push -u origin main
```

---

## 2. 🔐 Configurar Permisos de GitHub Actions

**IMPORTANTE:** Esto debe hacerse en el repositorio **`todos-mis-documentos`** (no en `aplicaciones_laborales`).

### Pasos:

1. Ve al repositorio `todos-mis-documentos` en GitHub
2. Click en **Settings** (⚙️)
3. En el menú lateral, click en **Actions** → **General**
4. Scroll hasta la sección **"Workflow permissions"**
5. Selecciona ☑️ **"Read and write permissions"**
6. Marca ☑️ **"Allow GitHub Actions to create and approve pull requests"** (opcional pero recomendado)
7. Click **Save**

### Verificación Visual:

```
Settings > Actions > General > Workflow permissions

⚪ Read repository contents and packages permissions
🔘 Read and write permissions  ← SELECCIONAR ESTA

☑️ Allow GitHub Actions to create and approve pull requests

[Save]  ← CLICK AQUÍ
```

---

## 3. ✅ Verificar la Configuración

### Test Rápido

Una vez completados los pasos anteriores, realiza una aplicación de prueba:

```bash
# En el repo aplicaciones_laborales
cat > to_process/test_configuracion.yaml << 'EOF'
cargo: "Test Configuration"
empresa: "TestSetup"
fecha: "2025-10-14"
descripcion: "Verificando que la copia automática funciona"
requerimientos:
  - Configuración correcta
  - Permisos habilitados
EOF

git add to_process/test_configuracion.yaml
git commit -m "Test: Verificar configuración de copia automática"
git push
```

### Verificar Resultados

Después de ~2-3 minutos:

1. **En `aplicaciones_laborales`:**
   - Ve a **Actions**
   - Verifica que el workflow se ejecutó correctamente
   - Busca el paso **"Copiar CV PDF a repositorio todos-mis-documentos"**
   - Debe mostrar: ✅ Sin errores

2. **En `todos-mis-documentos`:**
   - Verifica que existe la carpeta `2025-10-14/`
   - Dentro debe estar `ANTONIO_GUTIERREZ_RESUME_TestSetup.pdf`
   - Verifica el commit: `📄 CV generado: TestConfiguration - TestSetup (2025-10-14)`

---

## ❌ Errores Comunes y Soluciones

### Error: "remote: Permission to angra8410/todos-mis-documentos.git denied"

**Causa:** Los permisos de GitHub Actions no están configurados correctamente.

**Solución:**
1. Ve a `todos-mis-documentos` → Settings → Actions → General
2. Cambia a "Read and write permissions"
3. Click Save
4. Reintenta el workflow (re-run en Actions)

### Error: "fatal: repository 'https://github.com/angra8410/todos-mis-documentos.git/' not found"

**Causa:** El repositorio no existe.

**Solución:**
1. Crea el repositorio siguiendo el paso 1
2. Asegúrate de que el nombre es exactamente `todos-mis-documentos`
3. Reintenta el workflow

### Error: "Carpeta no encontrada: to_process_procesados/..."

**Causa:** El procesamiento de la aplicación falló antes de llegar al paso de copia.

**Solución:**
1. Revisa los logs del paso anterior "Procesar archivo de nueva aplicación"
2. Verifica que el YAML tiene el formato correcto
3. Asegúrate de que pandoc y LaTeX se instalaron correctamente

---

## 🔒 Consideraciones de Seguridad

### ✅ Seguro
- Usar `GITHUB_TOKEN` (automático, no requiere secrets adicionales)
- Repositorio `todos-mis-documentos` puede ser privado
- Los commits se hacen como `github-actions[bot]`

### ⚠️ Ten en Cuenta
- Si `todos-mis-documentos` es público, los CVs serán visibles públicamente
- **Recomendación:** Hacer el repo privado si contiene información sensible
- El `GITHUB_TOKEN` solo tiene acceso a repos del mismo usuario/org

---

## 📝 Checklist Final

Antes de usar la funcionalidad, verifica:

- [ ] ✅ Repositorio `todos-mis-documentos` creado
- [ ] ✅ Permisos de GitHub Actions configurados (Read and write)
- [ ] ✅ Test de aplicación ejecutado
- [ ] ✅ PDF aparece en `todos-mis-documentos`
- [ ] ✅ Commit visible con formato correcto
- [ ] ✅ No hay errores en el workflow

---

## 🎉 ¡Listo para Usar!

Una vez completados todos los pasos, la copia automática funcionará para **todas** las futuras aplicaciones sin necesidad de intervención manual.

**Cada vez que crees una nueva aplicación:**
1. Push del YAML a `to_process/`
2. ✨ El sistema automáticamente copia el PDF a `todos-mis-documentos`
3. ✨ Organizado por fecha
4. ✨ Con commit descriptivo

---

## 🆘 ¿Necesitas Ayuda?

Si sigues teniendo problemas después de seguir estos pasos:

1. **Revisa los logs del workflow** en Actions
2. **Consulta la guía completa:** [AUTOMATION_PDF_COPY_GUIDE.md](AUTOMATION_PDF_COPY_GUIDE.md)
3. **Quick Start:** [AUTOMATION_PDF_COPY_QUICKSTART.md](AUTOMATION_PDF_COPY_QUICKSTART.md)
4. **Diagrama de flujo:** [WORKFLOW_DIAGRAM.md](WORKFLOW_DIAGRAM.md)

---

**Última actualización:** 2025-10-14  
**Versión:** 1.0
