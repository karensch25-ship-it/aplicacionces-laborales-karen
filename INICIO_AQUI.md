# 🚀 INICIO AQUÍ - Configuración del Workflow CI/CD

> **⏱️ Tiempo requerido:** 5 minutos  
> **🎯 Objetivo:** Hacer que el workflow copie PDFs automáticamente a `todos-mis-documentos`

---

## ⚡ Quick Start (3 pasos)

### 1️⃣ Crear Personal Access Token (PAT)

**Ir a:** https://github.com/settings/tokens/new

**Configurar:**
- **Note:** `CI/CD PDF Copy`
- **Expiration:** `90 days`
- **Scopes:** Marcar ☑️  `repo`

**Click:** `Generate token`

**Copiar el token:** `ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

⚠️ Solo se muestra una vez - ¡cópialo ahora!

---

### 2️⃣ Configurar Secret PAT_APLICACION_LABORAL

**Ir a:** https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions

**Click:** `New repository secret`

**Configurar:**
- **Name:** `PAT_APLICACION_LABORAL` (exactamente este nombre)
- **Secret:** Pegar el token del paso 1

**Click:** `Add secret`

---

### 3️⃣ Verificar Permisos

**Ir a:** https://github.com/angra8410/todos-mis-documentos/settings/actions

**Seleccionar:**
- 🔘 `Read and write permissions`

**Click:** `Save`

---

## ✅ ¡Listo!

El workflow ahora puede copiar PDFs automáticamente.

**Para probar:**
1. Crear una nueva aplicación en `aplicaciones_laborales`
2. Ver logs en Actions
3. Buscar: `🔑 Usando PAT_APLICACION_LABORAL para acceso cross-repo`
4. Verificar PDF en `todos-mis-documentos`

---

## 📚 ¿Quieres más detalles?

- **Guía paso a paso:** [GUIA_RAPIDA_PAT.md](GUIA_RAPIDA_PAT.md)
- **Diagramas visuales:** [EXPLICACION_VISUAL_PAT.md](EXPLICACION_VISUAL_PAT.md)
- **Guía completa:** [SETUP_REQUIRED.md](SETUP_REQUIRED.md)
- **Detalles técnicos:** [SOLUCION_IMPLEMENTADA.md](SOLUCION_IMPLEMENTADA.md)

---

## ❓ ¿Por qué necesito hacer esto?

El repositorio `todos-mis-documentos` es **privado**. 

El workflow necesita un **Personal Access Token (PAT)** para acceder a repositorios privados. El `GITHUB_TOKEN` por defecto no funciona para esto.

**Más detalles:** Ver [EXPLICACION_VISUAL_PAT.md](EXPLICACION_VISUAL_PAT.md)

---

## 🆘 ¿Problemas?

Ver sección de troubleshooting en [GUIA_RAPIDA_PAT.md](GUIA_RAPIDA_PAT.md)

---

**Última actualización:** 2025-10-14
