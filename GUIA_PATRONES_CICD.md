# Guía Rápida: Patrones de Diseño para Scripts CI/CD

## 🎯 Objetivo
Prevenir errores en workflows CI/CD causados por mezcla de logs y valores de retorno.

## ✅ Patrón Correcto

### Script que retorna valor para workflow
```python
def main(yaml_path):
    # ... procesar ...
    result = process_data(yaml_path)
    
    # ✅ Logs informativos dentro de la función
    print(f"Procesamiento completado")
    
    # ✅ NO imprimir el valor de retorno aquí
    return result

if __name__ == "__main__":
    result = main(sys.argv[1])
    
    # ✅ Operaciones adicionales (con sus logs)
    if os.environ.get('SOME_VAR'):
        print("Realizando operación adicional...")
        do_something(result)
    else:
        print("ℹ️  Operación adicional no disponible")
    
    # ✅ CRÍTICO: Valor de retorno SIEMPRE al final
    print(f"\n{result}")
```

### Captura en Workflow
```yaml
- name: Procesar
  run: |
    # Captura la última línea (el valor de retorno)
    RESULT=$(python script.py input.yaml 2>&1 | tail -n 1)
    echo "Resultado: $RESULT"
    
    # Usar el resultado
    if [ -d "output/$RESULT" ]; then
      echo "✓ Carpeta encontrada"
    fi
```

## ❌ Patrón Incorrecto

### Lo que NO hacer
```python
def main(yaml_path):
    result = process_data(yaml_path)
    
    # ❌ Imprimir valor de retorno en medio
    print(result)
    
    return result

if __name__ == "__main__":
    result = main(sys.argv[1])
    
    # ❌ Logs después del valor de retorno
    if not os.environ.get('SOME_VAR'):
        print("ℹ️  Operación no disponible")  # ← Esto será capturado por tail -n 1
```

## 🔍 Checklist de Validación

Antes de hacer commit de un script usado por CI/CD:

- [ ] El valor de retorno se imprime en la ÚLTIMA línea
- [ ] Los logs informativos están ANTES del valor de retorno
- [ ] El script valida que los datos/archivos existen antes de retornar
- [ ] Hay comentarios explicando el orden de salida
- [ ] Se probó el script con las mismas condiciones del workflow
- [ ] Se simuló el comando del workflow (con `tail -n 1`, etc.)

## 📝 Ejemplos de Validación

### Validar antes de retornar
```python
def main(yaml_path):
    folder_name = generate_folder(yaml_path)
    output_dir = os.path.join("output", folder_name)
    
    # ✅ Validar que existe
    if not os.path.exists(output_dir):
        print(f"❌ ERROR: Carpeta no existe: {output_dir}")
        sys.exit(1)
    
    return folder_name
```

### Validar formato de salida
```python
def main(yaml_path):
    result = process_data(yaml_path)
    
    # ✅ Validar formato esperado
    if not re.match(r'^[A-Za-z0-9_-]+$', result):
        print(f"❌ ERROR: Formato inválido: {result}")
        sys.exit(1)
    
    return result
```

## 🧪 Template de Test

```python
import subprocess

def test_script_output():
    """Test que el script retorna el valor correcto como última línea"""
    result = subprocess.run(
        ["python", "script.py", "input.yaml"],
        capture_output=True,
        text=True
    )
    
    last_line = result.stdout.strip().split('\n')[-1]
    
    # Validar formato
    assert not any(indicator in last_line for indicator in ['ℹ️', '✓', '❌', 'Error'])
    assert re.match(r'^[A-Za-z0-9_-]+$', last_line)
    
    # Validar que existe
    assert os.path.exists(f"output/{last_line}")
```

## 🚨 Señales de Alerta

Si ves estos patrones, probablemente hay un problema:

1. ❌ `print(valor); return valor` en la misma función
2. ❌ Logs después de `return` en el bloque `__main__`
3. ❌ Condicionales que imprimen después del valor de retorno
4. ❌ No hay validación de existencia de archivos/carpetas
5. ❌ No hay comentarios sobre el orden de salida

## 💡 Mejores Prácticas

1. **Un solo output por script**: Si necesitas retornar múltiples valores, usa JSON
2. **Logs a stderr**: Considera usar `sys.stderr.write()` para logs
3. **Archivos intermedios**: Para datos complejos, usa archivos temporales
4. **Variables de entorno**: Para pasar datos entre pasos del workflow
5. **Validación temprana**: Fail fast si algo está mal

## 🔗 Referencias

- Documentación completa: `FIX_FOLDER_NAME_RETURN.md`
- Issue original: "Corregir retorno de nombre de carpeta procesada en script..."
- Tests: `/tmp/test_folder_name_return.py` y `/tmp/workflow_integration_test.sh`
