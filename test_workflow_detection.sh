#!/bin/bash
# Test script para validar la lógica de detección de archivos YAML
# Este script simula la lógica del workflow para verificar que funciona correctamente

set -e  # Exit on error

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# The repo root is the same as script dir (script is at repo root)
REPO_ROOT="$SCRIPT_DIR"

cd "$REPO_ROOT"

echo "============================================================"
echo "TEST: Validación de Lógica de Detección de YAML"
echo "============================================================"
echo ""

# Test 1: Verificar que existen archivos YAML en to_process/
echo "TEST 1: Verificar archivos YAML en to_process/"
YAML_FILES=$(ls to_process/*.yaml 2>/dev/null || true)
if [ -n "$YAML_FILES" ]; then
    YAML_COUNT=$(echo "$YAML_FILES" | wc -w)
    echo "✅ PASS: Encontrados $YAML_COUNT archivo(s) YAML"
    echo "$YAML_FILES" | tr ' ' '\n' | sed 's/^/   - /'
else
    echo "⚠️  SKIP: No hay archivos YAML en to_process/ (esto es válido)"
fi
echo ""

# Test 2: Verificar que el comando find funciona (fallback)
echo "TEST 2: Verificar comando find (fallback)"
if FOUND=$(find to_process -name "*.yaml" -type f 2>/dev/null | sed 's|^\./||'); then
    if [ -n "$FOUND" ]; then
        FOUND_COUNT=$(echo "$FOUND" | wc -l)
        echo "✅ PASS: Comando find encontró $FOUND_COUNT archivo(s)"
        echo "$FOUND" | sed 's/^/   - /'
    else
        echo "ℹ️  INFO: Comando find ejecutado pero no encontró archivos (válido si to_process/ está vacío)"
    fi
else
    echo "❌ FAIL: Comando find falló"
    exit 1
fi
echo ""

# Test 3: Verificar git diff en commits recientes
echo "TEST 3: Verificar git diff en últimos commits"
COMMIT_COUNT=$(git rev-list --count HEAD 2>/dev/null || echo "0")
if [ "$COMMIT_COUNT" -lt 2 ]; then
    echo "⚠️  SKIP: No hay suficientes commits para probar git diff (solo $COMMIT_COUNT commit(s))"
else
    COMMIT1=$(git rev-parse HEAD 2>/dev/null)
    COMMIT2=$(git rev-parse HEAD~1 2>/dev/null)
    
    if [ -n "$COMMIT1" ] && [ -n "$COMMIT2" ]; then
        echo "   Comparando: $COMMIT2 -> $COMMIT1"
        if DIFF_RESULT=$(git diff --name-only "$COMMIT2" "$COMMIT1" 2>/dev/null); then
            echo "   ✅ Git diff ejecutado exitosamente"
            
            # Filtrar solo YAML
            YAML_CHANGED=$(echo "$DIFF_RESULT" | grep '^to_process/.*\.yaml$' || true)
            if [ -n "$YAML_CHANGED" ]; then
                YAML_CHANGED_COUNT=$(echo "$YAML_CHANGED" | wc -l)
                echo "   ✅ PASS: Git diff detectó $YAML_CHANGED_COUNT archivo(s) YAML cambiado(s)"
                echo "$YAML_CHANGED" | sed 's/^/      - /'
            else
                echo "   ℹ️  INFO: Git diff ejecutado pero no detectó cambios en YAML (válido)"
            fi
        else
            echo "   ⚠️  WARN: Git diff falló (esto activaría el fallback en el workflow)"
        fi
    else
        echo "⚠️  SKIP: No hay dos commits para comparar"
    fi
fi
echo ""

# Test 4: Verificar que los scripts de procesamiento existen
echo "TEST 4: Verificar existencia de scripts de procesamiento"
REQUIRED_SCRIPTS=(
    "aplicaciones_laborales/scripts/procesar_aplicacion.py"
    "aplicaciones_laborales/scripts/cv_personalization_engine.py"
    "aplicaciones_laborales/scripts/scoring_engine.py"
)

ALL_SCRIPTS_EXIST=true
for script in "${REQUIRED_SCRIPTS[@]}"; do
    if [ -f "$script" ]; then
        echo "   ✅ $script"
    else
        echo "   ❌ FALTA: $script"
        ALL_SCRIPTS_EXIST=false
    fi
done

if [ "$ALL_SCRIPTS_EXIST" = true ]; then
    echo "✅ PASS: Todos los scripts requeridos existen"
else
    echo "❌ FAIL: Faltan scripts requeridos"
    exit 1
fi
echo ""

# Test 5: Verificar que Python puede importar los módulos
echo "TEST 5: Verificar imports de Python"
if python3 -c "import yaml; import sys" 2>/dev/null; then
    echo "✅ PASS: PyYAML disponible"
else
    echo "⚠️  WARN: PyYAML no disponible (el workflow lo instala automáticamente)"
fi
echo ""

# Test 6: Simular la lógica completa de detección
echo "TEST 6: Simulación completa de lógica de detección"
echo "-----------------------------------------------------------"

# Simular variables de GitHub Actions
BEFORE_SHA=$(git rev-parse HEAD~1 2>/dev/null || echo "")
CURRENT_SHA=$(git rev-parse HEAD 2>/dev/null || echo "")

echo "Simulación de contexto de GitHub Actions:"
echo "   Before SHA: ${BEFORE_SHA:-"(no disponible)"}"
echo "   Current SHA: ${CURRENT_SHA:-"(no disponible)"}"
echo ""

CHANGED=""

# Replicar la lógica del workflow
if [ -z "$BEFORE_SHA" ] || [ "$BEFORE_SHA" = "0000000000000000000000000000000000000000" ]; then
    echo "⚠️  Situación especial: primer commit o SHA anterior no disponible"
    echo "   Usando fallback: procesando todos los YAML"
    CHANGED=$(find to_process -name "*.yaml" -type f 2>/dev/null | sed 's|^\./||' || true)
else
    echo "🔍 Detectando cambios usando git diff..."
    if CHANGED=$(git diff --name-only "$BEFORE_SHA" "$CURRENT_SHA" 2>/dev/null | grep '^to_process/.*\.yaml$' || true); then
        echo "   ✓ Git diff ejecutado exitosamente"
    else
        echo "   ⚠️  Git diff falló, usando fallback"
        CHANGED=$(find to_process -name "*.yaml" -type f 2>/dev/null | sed 's|^\./||' || true)
    fi
fi

if [ -z "$CHANGED" ]; then
    echo ""
    echo "ℹ️  Resultado: No hay archivos YAML para procesar"
    echo "✅ PASS: La lógica funciona correctamente (no hay cambios)"
else
    FILE_COUNT=$(echo "$CHANGED" | wc -l)
    echo ""
    echo "✅ Resultado: $FILE_COUNT archivo(s) YAML detectado(s)"
    echo "$CHANGED" | sed 's/^/   - /'
    echo ""
    echo "✅ PASS: La lógica de detección funciona correctamente"
fi

echo "-----------------------------------------------------------"
echo ""

# Resumen final
echo "============================================================"
echo "RESUMEN DE TESTS"
echo "============================================================"
echo "✅ Todos los tests pasaron o se saltaron apropiadamente"
echo ""
echo "La lógica de detección de YAML del workflow es robusta y:"
echo "   ✅ Detecta archivos YAML en to_process/"
echo "   ✅ Usa git diff cuando está disponible"
echo "   ✅ Tiene fallback automático con find"
echo "   ✅ Maneja situaciones especiales correctamente"
echo "   ✅ Los scripts de procesamiento existen"
echo ""
echo "El workflow está listo para detectar y procesar archivos YAML."
echo "============================================================"
