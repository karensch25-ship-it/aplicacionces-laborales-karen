# 🔑 Guía Rápida: Configurar Personal Access Token (PAT)

> **⏱️ Tiempo estimado:** 5 minutos  
> **🎯 Objetivo:** Configurar autenticación para copiar PDFs a repositorio privado `todos-mis-documentos`

---

## ❓ ¿Por qué necesito esto?

El repositorio `todos-mis-documentos` **ya existe** y es **PRIVADO**. 

El problema actual es que GitHub Actions usa `GITHUB_TOKEN` por defecto, el cual **NO puede acceder a otros repositorios privados**. Por eso ves el error:

```
❌ Repository not found (HTTP 404)
```

Aunque el repositorio existe, el token no tiene permisos para verlo.

**Solución:** Configurar un Personal Access Token (PAT) con permisos para acceder a repos privados.

---

## 🚀 Pasos Rápidos (5 minutos)

### Paso 1: Crear el PAT (2 minutos)

1. **Abre esta URL:** [https://github.com/settings/tokens/new](https://github.com/settings/tokens/new)

2. **Rellena el formulario:**
   ```
   Note: CI/CD PDF Copy to todos-mis-documentos
   Expiration: 90 days (recomendado)
   ```

3. **Marca SOLO este scope:**
   ```
   ☑️  repo
       Full control of private repositories
   ```
   
   > 💡 **Tip:** Despliega la sección `repo` y verás sub-opciones. Todas se marcarán automáticamente.

4. **Scroll abajo y click:**
   ```
   [Generate token]
   ```

5. **COPIA EL TOKEN INMEDIATAMENTE:**
   ```
   ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   ```
   
   ⚠️ **IMPORTANTE:** Solo se muestra una vez. Si lo pierdes, deberás crear uno nuevo.

---

### Paso 2: Configurar el Secret (2 minutos)

1. **Abre esta URL:** [https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions](https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions)

2. **Click en:**
   ```
   [New repository secret]
   ```

3. **Rellena:**
   ```
   Name: PAT_APLICACION_LABORAL
   Secret: <pega el token que copiaste>
   ```
   
   ⚠️ **IMPORTANTE:** El nombre debe ser exactamente `PAT_APLICACION_LABORAL` (respeta mayúsculas).

4. **Click:**
   ```
   [Add secret]
   ```

5. **Verifica:**
   - Deberías ver `PAT_APLICACION_LABORAL` en la lista
   - El valor estará oculto: `••••••••`

---

### Paso 3: Verificar Permisos en todos-mis-documentos (1 minuto)

1. **Abre:** [https://github.com/angra8410/todos-mis-documentos/settings/actions](https://github.com/angra8410/todos-mis-documentos/settings/actions)

2. **En "Workflow permissions", selecciona:**
   ```
   🔘 Read and write permissions
   ```

3. **Click:**
   ```
   [Save]
   ```

---

### Paso 4: Probar (Automático)

1. **Crea una nueva aplicación** en `aplicaciones_laborales`:
   ```bash
   # Ejemplo: crear archivo YAML en to_process/
   git add to_process/test.yaml
   git commit -m "Test: Verificar PAT funciona"
   git push
   ```

2. **Ve a Actions:** [https://github.com/angra8410/aplicaciones_laborales/actions](https://github.com/angra8410/aplicaciones_laborales/actions)

3. **Busca en los logs:**
   ```
   ✅ Debe mostrar: "🔑 Usando PAT_APLICACION_LABORAL para acceso cross-repo"
   ✅ Debe mostrar: "📊 Código de respuesta HTTP: 200"
   ✅ Debe mostrar: "✅ Repositorio destino encontrado y accesible"
   ```

4. **Verifica en todos-mis-documentos:**
   - Debe aparecer una nueva carpeta con la fecha
   - Debe contener el PDF del CV
   - Debe haber un commit: `📄 CV generado: ...`

---

## ✅ Checklist de Verificación

Confirma que completaste todo:

- [ ] PAT creado con scope `repo`
- [ ] Token copiado (formato `ghp_...`)
- [ ] Secret `PAT_APLICACION_LABORAL` configurado en aplicaciones_laborales
- [ ] Permisos "Read and write" en todos-mis-documentos
- [ ] Workflow de prueba ejecutado
- [ ] Logs muestran "🔑 Usando PAT_APLICACION_LABORAL"
- [ ] Logs muestran "HTTP: 200"
- [ ] PDF aparece en todos-mis-documentos

---

## ❌ Problemas Comunes

### "❌ HTTP 403: Forbidden"

**Causa:** PAT no tiene permisos correctos.

**Solución:**
1. Ve a [https://github.com/settings/tokens](https://github.com/settings/tokens)
2. Click en el token que creaste
3. Verifica que `repo` esté marcado
4. Si no, crea un nuevo token con permisos correctos
5. Actualiza el secret `PAT_APLICACION_LABORAL` con el nuevo valor

---

### "⚠️ Usando GITHUB_TOKEN" en logs

**Causa:** Secret `PAT_APLICACION_LABORAL` no está configurado o tiene nombre incorrecto.

**Solución:**
1. Ve a [Settings → Secrets](https://github.com/angra8410/aplicaciones_laborales/settings/secrets/actions)
2. Verifica que existe un secret llamado exactamente `PAT_APLICACION_LABORAL`
3. Si no existe o tiene otro nombre, créalo/renómbralo

---

### PAT expiró

**Síntoma:** Funcionaba antes pero ahora falla con HTTP 401.

**Solución:**
1. Crea un nuevo PAT (Paso 1)
2. Actualiza el secret `PAT_APLICACION_LABORAL` con el nuevo valor
3. No necesitas cambiar nada más

---

## 🔒 Seguridad

### ✅ Buenas Prácticas

- ✅ PAT almacenado en GitHub Secrets (encriptado)
- ✅ PAT nunca aparece en logs
- ✅ Configurar expiración (90 días recomendado)
- ✅ Renovar PAT regularmente

### ⚠️ NUNCA hagas esto

- ❌ NO compartas tu PAT con nadie
- ❌ NO lo incluyas en código
- ❌ NO lo guardes en archivos de texto sin encriptar
- ❌ NO lo publiques en issues/PRs/comentarios

---

## 📚 Documentación Relacionada

- **[SETUP_REQUIRED.md](SETUP_REQUIRED.md)** - Guía completa y detallada
- **[SOLUCION_IMPLEMENTADA.md](SOLUCION_IMPLEMENTADA.md)** - Explicación técnica
- **[AUTOMATION_PDF_COPY_GUIDE.md](AUTOMATION_PDF_COPY_GUIDE.md)** - Guía de automatización

---

## 🆘 ¿Aún tienes problemas?

1. Revisa los logs completos del workflow en Actions
2. Busca el código HTTP en el paso "Validar configuración"
3. Consulta la sección de troubleshooting en SETUP_REQUIRED.md
4. Verifica que seguiste todos los pasos exactamente como se indican

---

**Última actualización:** 2025-10-14  
**Versión:** 1.0  
**Propósito:** Configuración rápida de PAT para acceso cross-repo a repositorio privado
