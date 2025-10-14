# 🔐 Explicación Visual: PAT vs GITHUB_TOKEN

## 🎯 El Problema

### ❌ Lo que NO funciona (situación actual)

```
┌─────────────────────────────────────────┐
│  aplicaciones_laborales (público)       │
│  GitHub Actions Workflow                │
│                                         │
│  env:                                   │
│    GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
│         ↓                               │
│  Este token SOLO funciona para:        │
│  ✅ aplicaciones_laborales              │
│  ❌ otros repositorios                  │
└──────────────┬──────────────────────────┘
               │
               │ git clone https://...@github.com/
               │ angra8410/todos-mis-documentos.git
               │
               ▼
┌─────────────────────────────────────────┐
│  todos-mis-documentos (PRIVADO)        │
│                                         │
│  🚫 Acceso DENEGADO                     │
│  HTTP 404: "Repository not found"       │
│                                         │
│  Aunque el repo existe, GITHUB_TOKEN   │
│  no tiene permisos para verlo          │
└─────────────────────────────────────────┘

Resultado: ❌ FALLA - PDF NO se copia
```

---

## ✅ La Solución

### ✅ Lo que SÍ funciona (con PAT configurado)

```
┌─────────────────────────────────────────┐
│  aplicaciones_laborales (público)       │
│  GitHub Actions Workflow                │
│                                         │
│  env:                                   │
│    GITHUB_TOKEN: ${{ secrets.PAT_TOKEN }}
│         ↓                               │
│  PAT con scope 'repo' funciona para:   │
│  ✅ aplicaciones_laborales              │
│  ✅ todos-mis-documentos (privado)      │
│  ✅ TODOS tus repos privados            │
└──────────────┬──────────────────────────┘
               │
               │ git clone https://...@github.com/
               │ angra8410/todos-mis-documentos.git
               │ + PAT con permisos 'repo'
               │
               ▼
┌─────────────────────────────────────────┐
│  todos-mis-documentos (PRIVADO)        │
│                                         │
│  ✅ Acceso PERMITIDO                    │
│  HTTP 200: OK                           │
│                                         │
│  ✅ Clone exitoso                       │
│  ✅ Push exitoso                        │
│  ✅ PDF copiado y versionado            │
└─────────────────────────────────────────┘

Resultado: ✅ ÉXITO - PDF se copia automáticamente
```

---

## 🔑 ¿Qué es un PAT?

**Personal Access Token (PAT)** = Una contraseña especial para automation

### Características:

- 🔑 **Formato:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- ⏰ **Expira:** Puedes configurar 90 días, 1 año, o sin expiración
- 🔒 **Permisos granulares:** Solo das acceso a lo que necesitas
- 🚀 **Para automation:** Perfecto para CI/CD, scripts, workflows
- 🔐 **Almacenado seguro:** En GitHub Secrets (encriptado)

### Diferencia con tu password:

| Aspecto | Password Personal | PAT |
|---------|------------------|-----|
| Uso | Login web manual | Automation/scripts |
| Permisos | Acceso total | Granular (solo lo necesario) |
| Rotación | Raramente | Regularmente (90 días) |
| Exposición | Nunca compartir | Se guarda en secrets |
| Revocación | Difícil | Fácil (1 click) |

---

## 📊 Flujo Completo de Autenticación

### Paso a paso cuando ejecutas el workflow:

```
1️⃣ Usuario hace push a aplicaciones_laborales
   │
   ▼
2️⃣ GitHub Actions inicia workflow
   │
   ├─ Lee secrets.PAT_TOKEN ✅ (configurado por ti)
   └─ Asigna a GITHUB_TOKEN en env
   │
   ▼
3️⃣ Workflow ejecuta validación
   │
   ├─ curl -H "Authorization: token $GITHUB_TOKEN"
   │   https://api.github.com/repos/angra8410/todos-mis-documentos
   │
   └─ GitHub API verifica: ¿Este token tiene acceso?
   │
   ▼
4️⃣ GitHub API responde
   │
   ├─ HTTP 200: ✅ Acceso OK (PAT con scope 'repo')
   ├─ HTTP 404: ❌ Repo no existe O token sin permisos
   └─ HTTP 403: ❌ Token existe pero sin permisos suficientes
   │
   ▼
5️⃣ Si HTTP 200: Workflow continúa
   │
   ├─ git clone con PAT en URL
   ├─ Copia PDF a carpeta por fecha
   ├─ git commit con mensaje descriptivo
   └─ git push (también usa PAT)
   │
   ▼
6️⃣ Resultado final
   │
   ✅ PDF en todos-mis-documentos/YYYY-MM-DD/CV.pdf
   ✅ Commit visible en historial
   ✅ Logs auditables en Actions
```

---

## 🔍 Cómo Detectar el Problema

### En los logs del workflow:

#### ❌ Sin PAT configurado (problema actual):

```
Verificando si el repositorio destino existe...

⚠️  Usando GITHUB_TOKEN (puede no funcionar con repos privados)

📊 Código de respuesta HTTP: 404

❌ ERROR: Repositorio no encontrado (HTTP 404)
   Repositorio: angra8410/todos-mis-documentos
```

**Interpretación:** El repo existe pero el token no puede verlo.

---

#### ✅ Con PAT configurado (solución):

```
Verificando si el repositorio destino existe...

🔑 Usando PAT_TOKEN para acceso cross-repo

📊 Código de respuesta HTTP: 200

✅ Repositorio destino encontrado y accesible: angra8410/todos-mis-documentos
```

**Interpretación:** Todo correcto, el workflow puede copiar el PDF.

---

## 🛡️ Seguridad del PAT

### ✅ Prácticas seguras implementadas:

```
1. PAT creado por ti en GitHub
   └─ Solo tú puedes crearlo
   
2. PAT almacenado en GitHub Secrets
   ├─ Encriptado en reposo
   ├─ Solo accesible en workflows
   └─ Nunca visible en logs (GitHub lo redacta)
   
3. Scope mínimo necesario
   └─ Solo 'repo' (no admin, no delete)
   
4. Expira regularmente
   └─ Renovación cada 90 días (configurable)
   
5. Revocable en cualquier momento
   └─ 1 click en GitHub settings
```

### ⚠️ Lo que NUNCA debes hacer:

```
❌ Incluir PAT en código
❌ Compartir PAT en issues/PRs
❌ Guardarlo en archivos de texto
❌ Usar PAT sin expiración (no recomendado)
❌ Dar más permisos de los necesarios
```

---

## 📝 Checklist Visual

Marca cuando completes cada paso:

```
[ ] 1. Crear PAT en GitHub
    └─ URL: https://github.com/settings/tokens/new
    └─ Scope: ☑️  repo
    └─ Copiar token (ghp_...)

[ ] 2. Configurar secret PAT_TOKEN
    └─ URL: https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions
    └─ Name: PAT_TOKEN
    └─ Secret: <pegar token>

[ ] 3. Verificar permisos en todos-mis-documentos
    └─ URL: https://github.com/angra8410/todos-mis-documentos/settings/actions
    └─ Permisos: Read and write

[ ] 4. Ejecutar workflow de prueba
    └─ Crear/modificar aplicación
    └─ Push a aplicaciones_laborales

[ ] 5. Verificar logs
    └─ Ver Actions tab
    └─ Buscar: "🔑 Usando PAT_TOKEN"
    └─ Buscar: "HTTP: 200"

[ ] 6. Confirmar resultado
    └─ Abrir todos-mis-documentos
    └─ Verificar carpeta YYYY-MM-DD/
    └─ Verificar PDF copiado
```

---

## 🆘 Troubleshooting Visual

### Problema: "⚠️  Usando GITHUB_TOKEN"

```
Causa:
┌─────────────────────────────────────┐
│ Secret PAT_TOKEN NO configurado     │
│ o tiene nombre incorrecto           │
└─────────────────────────────────────┘
             │
Solución:    ▼
┌─────────────────────────────────────┐
│ 1. Ve a Settings → Secrets          │
│ 2. Verifica nombre: PAT_TOKEN       │
│ 3. Si no existe, créalo             │
└─────────────────────────────────────┘
```

---

### Problema: "HTTP 404" aunque repo existe

```
Causa:
┌─────────────────────────────────────┐
│ Token sin permisos para ver repo    │
│ privado (GITHUB_TOKEN o PAT sin     │
│ scope correcto)                     │
└─────────────────────────────────────┘
             │
Solución:    ▼
┌─────────────────────────────────────┐
│ 1. Verifica PAT tiene scope 'repo'  │
│ 2. Regenera PAT si es necesario     │
│ 3. Actualiza secret PAT_TOKEN       │
└─────────────────────────────────────┘
```

---

### Problema: "HTTP 403" con PAT configurado

```
Causa:
┌─────────────────────────────────────┐
│ PAT expiró o fue revocado           │
│ O permisos insuficientes            │
└─────────────────────────────────────┘
             │
Solución:    ▼
┌─────────────────────────────────────┐
│ 1. Ve a Settings → Tokens           │
│ 2. Verifica estado del PAT          │
│ 3. Si expiró: genera nuevo PAT      │
│ 4. Actualiza secret PAT_TOKEN       │
└─────────────────────────────────────┘
```

---

## 📚 Recursos Adicionales

- **[GUIA_RAPIDA_PAT.md](GUIA_RAPIDA_PAT.md)** - Configuración en 5 minutos
- **[SETUP_REQUIRED.md](SETUP_REQUIRED.md)** - Guía completa y detallada
- **[SOLUCION_IMPLEMENTADA.md](SOLUCION_IMPLEMENTADA.md)** - Explicación técnica del problema

---

**Creado:** 2025-10-14  
**Propósito:** Ayudar a entender visualmente por qué se necesita PAT y cómo funciona
