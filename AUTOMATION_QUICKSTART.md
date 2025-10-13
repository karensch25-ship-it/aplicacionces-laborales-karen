# 🚀 Quick Start: Automatización de Issues y Proyectos

Esta guía te ayudará a comenzar a usar el sistema de creación automática de issues en menos de 5 minutos.

---

## ✅ Pre-requisitos

Antes de empezar, asegúrate de que:

1. **El proyecto "aplicacione-estados" existe en GitHub**
   - Ve a la pestaña "Projects" de tu repositorio
   - Si no existe, créalo con el nombre "aplicacione-estados"
   - Asegúrate de que tiene una columna/status "Aplicados"

2. **El repositorio tiene los permisos correctos**
   - El workflow ya tiene los permisos configurados
   - No necesitas hacer nada adicional

---

## 🎯 Paso 1: Verificar que el proyecto existe

1. Ve a tu repositorio en GitHub
2. Haz clic en la pestaña **"Projects"**
3. Verifica que existe un proyecto llamado **"aplicacione-estados"**

**Si no existe:**
1. Haz clic en **"New project"**
2. Selecciona **"Board"** o **"Table"**
3. Nómbralo: **"aplicacione-estados"**
4. Crea una columna/status llamada **"Aplicados"**

---

## 🧪 Paso 2: Probar con una aplicación de prueba

### Opción A: Crear una nueva aplicación

1. Crea un archivo `test_automation.yaml` en la carpeta `to_process/`:

```yaml
cargo: "Test Automation Engineer"
empresa: "TestCompany"
fecha: "2025-10-13"
descripcion: |
  Esta es una aplicación de prueba para validar la automatización
  de creación de issues y agregado al proyecto GitHub.
requerimientos:
  - Experiencia con GitHub Actions
  - Conocimiento de Python
  - Familiaridad con APIs REST
```

2. Haz commit y push:
```bash
git add to_process/test_automation.yaml
git commit -m "Test: Probar automatización de issues"
git push
```

3. Espera 2-3 minutos a que GitHub Actions termine

4. Verifica que:
   - ✅ Se creó una carpeta en `to_process_procesados/`
   - ✅ Se creó una issue nueva
   - ✅ La issue tiene los labels `aplicacion-procesada` y `Aplicados`
   - ✅ La issue aparece en el proyecto "aplicacione-estados"

### Opción B: Usar una aplicación existente

Si ya tienes aplicaciones procesadas pero sin issues:

1. Encuentra una carpeta en `to_process_procesados/`
2. Copia un YAML de esa carpeta a `to_process/`
3. Renómbralo (ej: `test_automation.yaml`)
4. Haz commit y push
5. El sistema procesará y creará una issue

---

## 🔍 Paso 3: Verificar que funcionó

### Ver la Issue creada

1. Ve a la pestaña **"Issues"** de tu repositorio
2. Busca la issue más reciente
3. Debe tener el formato: **"Aplicación: {Cargo} en {Empresa}"**
4. Verifica que tiene:
   - ✅ Labels: `aplicacion-procesada`, `Aplicados`
   - ✅ Información completa (cargo, empresa, fecha, carpeta)
   - ✅ Checklist de próximos pasos

### Ver la Issue en el Proyecto

1. Ve a la pestaña **"Projects"**
2. Abre el proyecto **"aplicacione-estados"**
3. La issue debe aparecer en la columna **"Aplicados"**
4. Puedes moverla a otras columnas según tu flujo

---

## 📊 Ejemplo de Issue Creada

```markdown
## Nueva Aplicación Procesada

**Cargo:** Test Automation Engineer
**Empresa:** TestCompany
**Fecha de aplicación:** 2025-10-13
**Carpeta:** `to_process_procesados/TestAutomationEngineer_TestCompany_2025-10-13`

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

---
*Esta issue fue creada automáticamente por el workflow de procesamiento de aplicaciones.*
```

---

## ⚙️ Paso 4: Verificar los Logs (Opcional)

Si quieres ver detalles del proceso:

1. Ve a la pestaña **"Actions"** de tu repositorio
2. Haz clic en el workflow más reciente
3. Abre el job **"crear-carpeta-aplicacion"**
4. Expande el step **"Procesar archivo de nueva aplicación"**
5. Busca la sección con logs de creación de issue:

```
============================================================
Creating GitHub issue and adding to project...
============================================================
Processing folder: TestAutomationEngineer_TestCompany_2025-10-13
Parsed metadata: {...}
Repository: angra8410/aplicaciones_laborales
✅ Issue created successfully: #123
   URL: https://github.com/angra8410/aplicaciones_laborales/issues/123
✅ Found project: aplicacione-estados (ID: PVT_...)
✅ Issue added to project successfully
✅ All done! Issue created and added to project.
```

---

## 🛠️ Troubleshooting Rápido

### Problema: "Project not found"

**Solución:**
1. Asegúrate de que el proyecto existe
2. Verifica que el nombre es exactamente "aplicacione-estados" (case-insensitive)
3. Si cambiaste el nombre, actualiza el script en `create_issue_and_add_to_project.py`

### Problema: "Failed to add issue to project"

**Solución:**
1. Verifica que el proyecto es accesible para el repositorio
2. Si el proyecto es organizacional, verifica permisos
3. La issue se creará de todas formas, solo no se agregará al proyecto

### Problema: "Issue already exists"

**Comportamiento esperado:**
- El sistema detecta duplicados y no crea una nueva issue
- Esto es normal si reprocesas una aplicación

### Problema: No se creó ninguna issue

**Solución:**
1. Verifica los logs en GitHub Actions
2. Busca mensajes de error en el step "Procesar archivo de nueva aplicación"
3. Asegúrate de que el YAML tiene el formato correcto

---

## 🎓 Mejores Prácticas

### ✅ DO: Hacer

1. **Mantén el proyecto actualizado**
   - Mueve issues a columnas que reflejen el estado (Aplicados → En Proceso → Completados)

2. **Usa las checklists en las issues**
   - Marca items como completados según avances
   - Agrega notas adicionales si es necesario

3. **Personaliza el proyecto**
   - Agrega columnas según tu flujo (ej: "Seguimiento", "Rechazadas")
   - Agrega campos custom (ej: "Prioridad", "Match Score")

4. **Revisa issues periódicamente**
   - Cierra issues de aplicaciones completadas
   - Mantén el proyecto organizado

### ❌ DON'T: Evitar

1. **No elimines los labels automáticos**
   - `aplicacion-procesada` es usado para prevenir duplicados
   - `Aplicados` es usado para categorización

2. **No cambies el nombre del proyecto sin actualizar el código**
   - Si cambias "aplicacione-estados", actualiza `create_issue_and_add_to_project.py`

3. **No reproceses aplicaciones sin necesidad**
   - Esto puede crear duplicados innecesarios
   - Revisa primero si ya existe la issue

---

## 📈 Próximos Pasos

Ahora que tienes la automatización funcionando:

1. **Procesa tus aplicaciones normalmente**
   - El sistema creará issues automáticamente

2. **Gestiona tu proyecto GitHub**
   - Usa el tablero para seguimiento visual
   - Mueve issues según el estado

3. **Personaliza según tus necesidades**
   - Agrega más campos al proyecto
   - Modifica los templates de issues
   - Implementa mejoras sugeridas en `AUTOMATION_GUIDE.md`

---

## 📞 Soporte

**Documentación completa:** [AUTOMATION_GUIDE.md](AUTOMATION_GUIDE.md)

**Problemas técnicos:**
- Revisa los logs en GitHub Actions
- Consulta la sección de Troubleshooting en `AUTOMATION_GUIDE.md`

**Mejoras y sugerencias:**
- Actualiza el código en `create_issue_and_add_to_project.py`
- Crea un PR con tus mejoras

---

**¡Felicidades! 🎉 Tu sistema de automatización está listo.**

El flujo completo ahora funciona de forma 100% automática desde el YAML hasta el proyecto GitHub.
