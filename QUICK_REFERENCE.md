# 🚀 Referencia Rápida: Copia Automática de PDFs

## ⚡ Configuración en 3 Pasos (3 minutos)

### 1️⃣ Crear Repositorio (2 min)
```
https://github.com/new
├─ Nombre: todos-mis-documentos
├─ Visibilidad: Privado ✓
└─ NO inicializar con README
```

### 2️⃣ Configurar Permisos (1 min)
```
https://github.com/angra8410/todos-mis-documentos/settings/actions
├─ Workflow permissions
└─ ☑️ Read and write permissions
```

### 3️⃣ Verificar
```
Run workflow → Check logs:
✅ "Repositorio destino encontrado"
✅ "PDF copiado exitosamente"
```

---

## 🔍 Diagnóstico Rápido

### ✅ Todo Funciona
```
Logs muestran:
✅ Repositorio destino encontrado
✅ PDF copiado: 2025-10-15/ANTONIO_GUTIERREZ_RESUME_X.pdf
✅ Commit creado: 📄 CV generado: ...
```

### ⚠️ Repo No Existe
```
Logs muestran:
⚠️  ADVERTENCIA: Repositorio destino no existe
   HTTP Status: 404
```
**Solución:** Ir al Paso 1️⃣ arriba

### ❌ Sin Permisos
```
Logs muestran:
remote: Permission denied to github-actions[bot]
fatal: ... error: 403
```
**Solución:** Ir al Paso 2️⃣ arriba

---

## 📖 Documentación Completa

| Documento | Uso | Tiempo |
|-----------|-----|--------|
| [CONFIGURACION_INICIAL.md](CONFIGURACION_INICIAL.md) | 🌟 Primera vez | 5 min |
| [TROUBLESHOOTING_RAPIDO.md](TROUBLESHOOTING_RAPIDO.md) | 🔧 Problemas | 5 min |
| [EJEMPLO_VISUAL_WORKFLOW.md](EJEMPLO_VISUAL_WORKFLOW.md) | 👁️ Ver ejemplos | 10 min |
| [SOLUCION_IMPLEMENTADA.md](SOLUCION_IMPLEMENTADA.md) | 📊 Resumen técnico | 15 min |

---

## 🎯 Resultado Final

```
Usuario crea YAML
       ↓
Workflow ejecuta
       ↓
    ✅ PDF generado
    ✅ Scoring report
    ✅ Issue creada
    ✅ PDF → todos-mis-documentos/YYYY-MM-DD/
       ↓
Trazabilidad completa ✓
```

---

## 💡 Tips Pro

### Ver logs del último workflow
```bash
https://github.com/angra8410/aplicaciones_laborales/actions
→ Click en workflow más reciente
→ Expandir steps para ver detalles
```

### Verificar repo destino
```bash
curl -s -o /dev/null -w "%{http_code}" \
  https://github.com/angra8410/todos-mis-documentos
# Debe retornar: 200 (existe) o 404 (no existe)
```

### Ver estructura de PDFs
```
todos-mis-documentos/
├── 2025-10-15/
│   ├── ANTONIO_GUTIERREZ_RESUME_EmpresaA.pdf
│   └── ANTONIO_GUTIERREZ_RESUME_EmpresaB.pdf
├── 2025-10-14/
│   └── ANTONIO_GUTIERREZ_RESUME_EmpresaC.pdf
└── ...
```

---

**🆘 ¿Problemas?** → [TROUBLESHOOTING_RAPIDO.md](TROUBLESHOOTING_RAPIDO.md)
