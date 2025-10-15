# ⚙️ Configuración Requerida: Copia Automática de PDFs

> **⚠️ ATENCIÓN:** Este documento contiene instrucciones de configuración inicial.  
> **🚀 ¿Primera vez?** Lee primero: **[CONFIGURACION_INICIAL.md](CONFIGURACION_INICIAL.md)** - Guía paso a paso simplificada

---

## 📋 Resumen Ejecutivo

Para que el flujo CI/CD copie automáticamente los CV generados al repositorio `todas-mis-aplicaciones`, necesitas:

1. ✅ Crear el repositorio destino `angra8410/todas-mis-aplicaciones` (si no existe)
2. ✅ Configurar un Personal Access Token (PAT) para acceso cross-repo a repos privados
3. ✅ Configurar permisos de escritura para GitHub Actions en el repositorio destino

**Estado actual según evidencia:** 
- ✅ El repositorio `todas-mis-aplicaciones` EXISTE y es PRIVADO
- ❌ El workflow usa `GITHUB_TOKEN` que NO puede acceder a repos privados
- ❌ Se necesita configurar `PAT_APLICACION_LABORAL` para autenticación cross-repo

**Acción requerida:** Configurar PAT (Paso 2 a continuación)

---

## 🎯 Pasos Obligatorios

### ⚠️ IMPORTANTE: Repositorios Privados
Si `todas-mis-aplicaciones` es **PRIVADO** (como en este caso), el `GITHUB_TOKEN` por defecto **NO funcionará** para operaciones cross-repo. Debes usar un Personal Access Token (PAT).

---

## 1. 📦 Crear el Repositorio `todas-mis-aplicaciones`

### Opción A: Via GitHub Web UI

1. Ve a [https://github.com/new](https://github.com/new)
2. **Repository name:** `todas-mis-aplicaciones`
3. **Description:** (opcional) `Repositorio centralizado de todos los CV PDFs generados automáticamente, organizados por fecha en /aplicaciones/YYYY-MM-DD/`
4. **Visibility:** Elige **Public** o **Private** según prefieras
5. **No inicialices** con README, .gitignore o licencia (el repo puede estar vacío)
6. Click **Create repository**

### Opción B: Via GitHub CLI

```bash
# Asegúrate de tener gh CLI instalado
gh auth login  # Si no has autenticado antes

# Crear repositorio público
gh repo create angra8410/todas-mis-aplicaciones --public

# O crear repositorio privado
gh repo create angra8410/todas-mis-aplicaciones --private
```

### Opción C: Via Git Commands

```bash
# 1. Crear repositorio en GitHub primero (opción A)
# 2. Luego inicializar localmente (opcional):
mkdir todas-mis-aplicaciones
cd todas-mis-aplicaciones
git init
echo "# CVs Generados Automáticamente" > README.md
mkdir -p aplicaciones
git add README.md aplicaciones
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/angra8410/todas-mis-aplicaciones.git
git push -u origin main
```

---

## 2. 🔑 Configurar Personal Access Token (PAT) - CRÍTICO para Repos Privados

### ¿Por qué necesito un PAT?

El `GITHUB_TOKEN` por defecto que GitHub Actions proporciona **solo puede acceder al repositorio actual**. Para operaciones cross-repo con repositorios privados, necesitas un Personal Access Token con permisos `repo`.

### Paso 2.1: Crear Personal Access Token

1. **Ve a GitHub Settings:**
   - URL directa: [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)
   - O: Tu perfil → Settings → Developer settings → Personal access tokens → Tokens (classic) → Generate new token

2. **Configura el token:**
   ```
   Token name: CI/CD PDF Copy to todas-mis-aplicaciones
   Expiration: 90 días (o "No expiration" si prefieres)
   
   Scopes (permisos):
   ☑️  repo (Full control of private repositories)
       ├─ ☑️  repo:status
       ├─ ☑️  repo_deployment
       ├─ ☑️  public_repo
       └─ ☑️  repo:invite
   ```

3. **Generar y copiar token:**
   - Click en **"Generate token"** al final de la página
   - ⚠️ **IMPORTANTE:** Copia el token inmediatamente (solo se muestra una vez)
   - Formato: `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

### Paso 2.2: Configurar Secret en aplicaciones_laborales

1. **Ve al repositorio aplicaciones_laborales:**
   - URL directa: [https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions](https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions)
   - O: Settings → Secrets and variables → Actions

2. **Crear nuevo secret:**
   - Click en **"New repository secret"**
   - **Name:** `PAT_APLICACION_LABORAL` (exactamente este nombre)
   - **Secret:** Pega el token que copiaste en Paso 2.1
   - Click **"Add secret"**

3. **Verificar:**
   - Deberías ver `PAT_APLICACION_LABORAL` en la lista de secrets
   - El valor estará oculto (••••••)

### 📊 Diagrama Visual del Flujo de Autenticación

```
┌─────────────────────────────────────┐
│ aplicaciones_laborales (público)    │
│                                     │
│  GitHub Actions Workflow            │
│  ├─ usa: PAT_APLICACION_LABORAL    │
│  └─ autenticación cross-repo ✅    │
└────────────┬────────────────────────┘
             │
             │ PAT con permisos 'repo'
             │ permite acceso privado
             ▼
┌─────────────────────────────────────┐
│ todas-mis-aplicaciones (PRIVADO)   │
│                                     │
│  ✅ Clone permitido                 │
│  ✅ Push permitido                  │
│  ✅ Operaciones exitosas            │
└─────────────────────────────────────┘

VS

┌─────────────────────────────────────┐
│ aplicaciones_laborales (público)    │
│                                     │
│  GitHub Actions Workflow            │
│  ├─ usa: GITHUB_TOKEN (default)    │
│  └─ NO puede acceder otros repos ❌│
└────────────┬────────────────────────┘
             │
             │ GITHUB_TOKEN solo para
             │ repo actual
             ▼
┌─────────────────────────────────────┐
│ todas-mis-aplicaciones (PRIVADO)   │
│                                     │
│  ❌ Clone DENEGADO                  │
│  ❌ HTTP 404/403                    │
│  ❌ "Repository not found"          │
└─────────────────────────────────────┘
```

---

## 3. 🔐 Configurar Permisos en todas-mis-aplicaciones

**IMPORTANTE:** Esto debe hacerse en el repositorio **`todas-mis-aplicaciones`** (no en `aplicaciones_laborales`).

### Pasos:

1. Ve al repositorio `todas-mis-aplicaciones` en GitHub
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

## 4. ✅ Verificar la Configuración

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
   - Busca el paso **"Copiar CV PDF a repositorio todas-mis-aplicaciones"**
   - Debe mostrar: ✅ Sin errores

2. **En `todas-mis-aplicaciones`:**
   - Verifica que existe la carpeta `aplicaciones/2025-10-14/`
   - Dentro debe estar `ANTONIO_GUTIERREZ_RESUME_TestSetup.pdf`
   - Verifica el commit: `📄 CV generado: TestConfiguration - TestSetup (2025-10-14)`

---

## ❌ Errores Comunes y Soluciones

### Error: "Repository not found" (HTTP 404) con repo privado

**Causa:** El repositorio es privado y estás usando `GITHUB_TOKEN` en lugar de `PAT_APLICACION_LABORAL`.

**Solución:**
1. Verifica que el repositorio existe: https://github.com/angra8410/todas-mis-aplicaciones
2. Si es privado, configura `PAT_APLICACION_LABORAL` siguiendo el Paso 2 de este documento
3. Re-ejecuta el workflow

### Error: "Permission denied" o HTTP 403

**Causa:** El PAT no tiene los permisos correctos o no está configurado.

**Solución:**
1. Verifica que el PAT tiene scope `repo` marcado
2. Verifica que el secret se llama exactamente `PAT_APLICACION_LABORAL` (respeta mayúsculas)
3. Regenera el PAT si es necesario (pueden haber expirado)
4. Configura nuevamente el secret con el nuevo token

### Error: "remote: Permission to angra8410/todas-mis-aplicaciones.git denied"

**Causa:** Los permisos de GitHub Actions no están configurados correctamente.

**Solución:**
1. Ve a `todas-mis-aplicaciones` → Settings → Actions → General
2. Cambia a "Read and write permissions"
3. Click Save
4. Reintenta el workflow (re-run en Actions)

### Error: "fatal: repository 'https://github.com/angra8410/todas-mis-aplicaciones.git/' not found"

**Causa:** El repositorio no existe.

**Solución:**
1. Crea el repositorio siguiendo el paso 1
2. Asegúrate de que el nombre es exactamente `todas-mis-aplicaciones`
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
- Usar `PAT_APLICACION_LABORAL` almacenado en GitHub Secrets (encriptado y seguro)
- Repositorio `todos-mis-documentos` puede ser privado
- Los commits se hacen como `github-actions[bot]`
- El PAT solo se usa en el workflow, nunca se expone en logs

### ⚠️ Ten en Cuenta
- **NUNCA** compartas tu PAT o lo incluyas en código
- El PAT da acceso completo a todos tus repositorios privados con scope `repo`
- Configura expiración del PAT (90 días recomendado) para seguridad
- Regenera el PAT si crees que fue comprometido
- Si `todos-mis-documentos` es público, los CVs serán visibles públicamente
- **Recomendación:** Hacer el repo privado si contiene información sensible

### 🔄 Renovación de PAT

Los PAT pueden expirar. Cuando esto ocurra:

1. Genera un nuevo PAT (mismo proceso del Paso 2.1)
2. Actualiza el secret `PAT_APLICACION_LABORAL` con el nuevo valor
3. No necesitas cambiar nada más en el workflow

---

## 📝 Checklist Final

Antes de usar la funcionalidad, verifica:

- [ ] ✅ Repositorio `todos-mis-documentos` creado
- [ ] ✅ Personal Access Token (PAT) creado con scope `repo`
- [ ] ✅ Secret `PAT_APLICACION_LABORAL` configurado en aplicaciones_laborales
- [ ] ✅ Permisos de GitHub Actions configurados en todos-mis-documentos (Read and write)
- [ ] ✅ Test de aplicación ejecutado
- [ ] ✅ Logs del workflow muestran "🔑 Usando PAT_APLICACION_LABORAL para acceso cross-repo"
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
