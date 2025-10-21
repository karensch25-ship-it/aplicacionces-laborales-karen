#!/usr/bin/env python3
"""
Unit tests for ATS CV Validator
Tests the validation logic for ATS-optimized CV generation.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ats_cv_validator import ATSCVValidator


def test_section_validation():
    """Test that section validation correctly identifies required sections."""
    print("\n" + "="*60)
    print("TEST 1: Section Validation")
    print("="*60)
    
    validator = ATSCVValidator()
    
    # Test CV with all sections (Spanish)
    complete_cv_es = """
    ## Perfil Profesional
    Profesional con experiencia...
    
    ## Habilidades
    - Contabilidad
    - Excel avanzado
    
    ## Experiencia Profesional
    ### Analista Contable
    - Logro 1
    - Logro 2
    
    ## Formación Académica
    Contaduría Pública
    
    ## Idiomas
    - Español (nativo)
    - Inglés (básico)
    """
    
    result = validator.validate_cv(complete_cv_es, language='es')
    section_score = result['section_validation']['score']
    
    print(f"✓ Test CV completo (español): Puntuación = {section_score}/100")
    assert section_score >= 80, f"Expected score >= 80, got {section_score}"
    assert result['section_validation']['total_found'] >= 4, "Should find at least 4 sections"
    
    # Test CV with missing sections
    incomplete_cv_es = """
    ## Perfil Profesional
    Profesional con experiencia...
    
    ## Habilidades
    - Contabilidad
    """
    
    result_incomplete = validator.validate_cv(incomplete_cv_es, language='es')
    incomplete_score = result_incomplete['section_validation']['score']
    
    print(f"✓ Test CV incompleto: Puntuación = {incomplete_score}/100")
    assert incomplete_score < section_score, "Incomplete CV should score lower"
    assert len(result_incomplete['section_validation']['missing_sections']) > 0, "Should identify missing sections"
    
    print("✅ PASSED: Section validation works correctly\n")
    return True


def test_keyword_validation():
    """Test that keyword validation correctly identifies relevant keywords."""
    print("="*60)
    print("TEST 2: Keyword Validation")
    print("="*60)
    
    validator = ATSCVValidator()
    
    # Test CV with many keywords
    keyword_rich_cv = """
    Experiencia en contabilidad, conciliaciones bancarias, cuentas por cobrar,
    cuentas por pagar, reportes financieros, SAP, Excel avanzado, facturación,
    gestión de activos, logística, billing, EFT, Power BI, análisis de datos.
    """
    
    result = validator.validate_cv(keyword_rich_cv, language='es')
    keyword_score = result['keyword_validation']['score']
    keywords_found = result['keyword_validation']['keywords_found']
    
    print(f"✓ Test CV rico en palabras clave: Puntuación = {keyword_score}/100")
    print(f"  Palabras clave encontradas: {keywords_found}")
    assert keyword_score >= 70, f"Expected score >= 70, got {keyword_score}"
    assert keywords_found >= 10, f"Expected at least 10 keywords, found {keywords_found}"
    
    # Test CV with few keywords
    keyword_poor_cv = """
    Profesional trabajador y responsable.
    Experiencia en diferentes áreas.
    """
    
    result_poor = validator.validate_cv(keyword_poor_cv, language='es')
    poor_score = result_poor['keyword_validation']['score']
    
    print(f"✓ Test CV pobre en palabras clave: Puntuación = {poor_score}/100")
    assert poor_score < keyword_score, "Keyword-poor CV should score lower"
    
    print("✅ PASSED: Keyword validation works correctly\n")
    return True


def test_achievement_validation():
    """Test that achievement validation correctly identifies quantifiable metrics."""
    print("="*60)
    print("TEST 3: Achievement Validation")
    print("="*60)
    
    validator = ATSCVValidator()
    
    # Test CV with quantifiable achievements
    achievement_rich_cv = """
    ## Experiencia Profesional
    
    ### Analista Contable
    - Procesé 500+ transacciones mensuales con 99% de precisión
    - Reduje el tiempo de cierre mensual en 25%
    - Gestioné cartera de 100 clientes generando $2M en ingresos
    - Implementé mejoras que ahorraron 15 horas semanales
    - Mantuve cumplimiento del 100% en auditorías
    """
    
    result = validator.validate_cv(achievement_rich_cv, language='es')
    achievement_score = result['achievement_validation']['score']
    total_quantifiable = result['achievement_validation']['total_quantifiable']
    
    print(f"✓ Test CV con logros cuantificables: Puntuación = {achievement_score}/100")
    print(f"  Métricas cuantificables encontradas: {total_quantifiable}")
    assert achievement_score >= 70, f"Expected score >= 70, got {achievement_score}"
    assert total_quantifiable >= 5, f"Expected at least 5 metrics, found {total_quantifiable}"
    
    # Test CV without quantifiable achievements
    achievement_poor_cv = """
    ## Experiencia Profesional
    
    ### Analista Contable
    - Realicé conciliaciones bancarias
    - Elaboré reportes financieros
    - Atendí clientes
    """
    
    result_poor = validator.validate_cv(achievement_poor_cv, language='es')
    poor_score = result_poor['achievement_validation']['score']
    
    print(f"✓ Test CV sin logros cuantificables: Puntuación = {poor_score}/100")
    assert poor_score < achievement_score, "Achievement-poor CV should score lower"
    
    print("✅ PASSED: Achievement validation works correctly\n")
    return True


def test_format_validation():
    """Test that format validation correctly identifies ATS-friendly formatting."""
    print("="*60)
    print("TEST 4: Format Validation")
    print("="*60)
    
    validator = ATSCVValidator()
    
    # Test well-formatted CV
    well_formatted_cv = """
## Perfil Profesional
Profesional con experiencia...

Email: test@example.com
Tel: +57 301 388 6149

## Habilidades
- Skill 1
- Skill 2
- Skill 3
- Skill 4
- Skill 5

## Experiencia
- Achievement 1
- Achievement 2
- Achievement 3
""" + "\n" * 50  # Add lines to meet length requirement
    
    result = validator.validate_cv(well_formatted_cv, language='es')
    format_score = result['format_validation']['score']
    
    print(f"✓ Test CV bien formateado: Puntuación = {format_score}/100")
    assert format_score >= 60, f"Expected score >= 60, got {format_score}"
    assert result['format_validation']['has_email'], "Should detect email"
    assert result['format_validation']['has_phone'], "Should detect phone"
    # Note: bullet points count starts from next line character, so threshold is lower
    assert result['format_validation']['bullet_points'] >= 3, "Should have sufficient bullets"
    
    # Test poorly formatted CV
    poorly_formatted_cv = """
    Experiencia profesional
    Trabajo en contabilidad
    """
    
    result_poor = validator.validate_cv(poorly_formatted_cv, language='es')
    poor_score = result_poor['format_validation']['score']
    
    print(f"✓ Test CV mal formateado: Puntuación = {poor_score}/100")
    assert poor_score < format_score, "Poorly formatted CV should score lower"
    
    print("✅ PASSED: Format validation works correctly\n")
    return True


def test_overall_scoring():
    """Test that overall scoring correctly combines all validation aspects."""
    print("="*60)
    print("TEST 5: Overall Scoring")
    print("="*60)
    
    validator = ATSCVValidator()
    
    # Test highly optimized CV
    optimized_cv = """
    Email: karen@example.com
    Tel: +57 301 388 6149
    
    ## Perfil Profesional
    Profesional en Contaduría con experiencia en conciliaciones bancarias,
    cuentas por cobrar, reportes financieros y gestión de procesos.
    
    ## Habilidades
    - Contabilidad y análisis financiero
    - Conciliaciones bancarias (SAP, Excel)
    - Cuentas por cobrar (AR) y cuentas por pagar (AP)
    - Reportes financieros y Power BI
    - Facturación y billing
    - Gestión de activos
    - Logística y EFT
    
    ## Experiencia Profesional
    
    ### Analista Contable
    UPS - 2024
    - Procesé 500+ transacciones EFT mensuales con 99% de precisión
    - Realicé conciliaciones bancarias para 10+ cuentas internacionales
    - Reduje tiempo de procesamiento en 25% mediante automatización
    - Gestioné cartera AR de $2M con tasa de cobro del 95%
    - Elaboré 50+ reportes financieros mensuales en Excel y SAP
    
    ### Analista RTR
    Accenture - 2024
    - Gestioné 200+ activos con valor total de $5M
    - Ejecuté procesos de depreciación para 100% de activos
    - Mantuve cumplimiento del 100% en auditorías internas
    
    ## Formación Académica
    Contaduría Pública - UMANIZALES (2024)
    Tecnólogo en Distribución Física Internacional - SENA (2015)
    
    ## Certificaciones
    - Power BI (en curso)
    - SAP (experiencia laboral)
    
    ## Idiomas
    - Español (Nativo)
    - Portugués (Avanzado)
    - Inglés (Básico)
    """
    
    result = validator.validate_cv(optimized_cv, language='es')
    overall_score = result['overall_score']
    
    print(f"✓ Test CV altamente optimizado:")
    print(f"  Puntuación General: {overall_score}/100")
    print(f"  Secciones: {result['section_validation']['score']}/100")
    print(f"  Palabras Clave: {result['keyword_validation']['score']}/100")
    print(f"  Logros: {result['achievement_validation']['score']}/100")
    print(f"  Formato: {result['format_validation']['score']}/100")
    print(f"  Estado ATS: {'✅ OPTIMIZADA' if result['is_ats_optimized'] else '⚠️ REQUIERE MEJORAS'}")
    
    assert overall_score >= 75, f"Optimized CV should score >= 75, got {overall_score}"
    
    print("✅ PASSED: Overall scoring works correctly\n")
    return True


def test_report_generation():
    """Test that validation reports are generated correctly."""
    print("="*60)
    print("TEST 6: Report Generation")
    print("="*60)
    
    validator = ATSCVValidator()
    
    cv_content = """
    ## Perfil Profesional
    Profesional en contabilidad con experiencia en conciliaciones bancarias.
    
    ## Habilidades
    - Contabilidad
    - Excel
    - SAP
    
    ## Experiencia Profesional
    Analista Contable - Procesé 100+ transacciones
    
    ## Formación Académica
    Contaduría Pública
    
    ## Idiomas
    - Español
    """
    
    result = validator.validate_cv(cv_content, language='es')
    report_es = validator.format_validation_report(result, "Analista Contable", language='es')
    report_en = validator.format_validation_report(result, "Accounting Analyst", language='en')
    
    print("✓ Reporte en español generado")
    assert "Reporte de Validación ATS" in report_es, "Spanish report should have correct title"
    assert "Puntuación ATS General" in report_es, "Spanish report should have score"
    assert len(report_es) > 500, "Report should have substantial content"
    
    print("✓ Reporte en inglés generado")
    assert "ATS Validation Report" in report_en, "English report should have correct title"
    assert "Overall ATS Score" in report_en, "English report should have score"
    assert len(report_en) > 500, "Report should have substantial content"
    
    print("✅ PASSED: Report generation works correctly\n")
    return True


def test_bilingual_validation():
    """Test that validator works correctly for both Spanish and English."""
    print("="*60)
    print("TEST 7: Bilingual Validation")
    print("="*60)
    
    validator = ATSCVValidator()
    
    # Spanish CV
    cv_es = """
    ## Perfil Profesional
    Profesional en contabilidad con experiencia en conciliaciones y reportes.
    
    ## Habilidades
    Contabilidad, Excel, SAP
    
    ## Experiencia Profesional
    Analista - Gestioné 100+ transacciones
    
    ## Formación Académica
    Contaduría Pública
    
    ## Idiomas
    Español, Inglés
    """
    
    # English CV
    cv_en = """
    ## Professional Summary
    Accounting professional with experience in reconciliations and reports.
    
    ## Skills
    Accounting, Excel, SAP
    
    ## Professional Experience
    Analyst - Managed 100+ transactions
    
    ## Education
    Public Accounting
    
    ## Languages
    Spanish, English
    """
    
    result_es = validator.validate_cv(cv_es, language='es')
    result_en = validator.validate_cv(cv_en, language='en')
    
    print(f"✓ Validación en español: {result_es['overall_score']}/100")
    print(f"✓ Validación en inglés: {result_en['overall_score']}/100")
    
    # Both should have reasonable scores
    assert result_es['overall_score'] > 0, "Spanish CV should have non-zero score"
    assert result_en['overall_score'] > 0, "English CV should have non-zero score"
    
    # Both should detect sections
    assert result_es['section_validation']['total_found'] >= 3, "Should find Spanish sections"
    assert result_en['section_validation']['total_found'] >= 3, "Should find English sections"
    
    print("✅ PASSED: Bilingual validation works correctly\n")
    return True


def run_all_tests():
    """Run all tests and report results."""
    print("\n" + "="*60)
    print("INICIANDO SUITE DE PRUEBAS ATS VALIDATOR")
    print("="*60)
    
    tests = [
        ("Section Validation", test_section_validation),
        ("Keyword Validation", test_keyword_validation),
        ("Achievement Validation", test_achievement_validation),
        ("Format Validation", test_format_validation),
        ("Overall Scoring", test_overall_scoring),
        ("Report Generation", test_report_generation),
        ("Bilingual Validation", test_bilingual_validation),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            test_func()
            passed += 1
        except AssertionError as e:
            print(f"❌ FAILED: {test_name}")
            print(f"   Error: {e}\n")
            failed += 1
        except Exception as e:
            print(f"❌ ERROR in {test_name}: {e}\n")
            failed += 1
    
    # Final summary
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS")
    print("="*60)
    print(f"Total de pruebas: {len(tests)}")
    print(f"✅ Exitosas: {passed}")
    print(f"❌ Fallidas: {failed}")
    print("="*60)
    
    if failed == 0:
        print("\n🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!\n")
        return 0
    else:
        print(f"\n⚠️ {failed} prueba(s) fallaron. Revisar los errores arriba.\n")
        return 1


if __name__ == "__main__":
    exit_code = run_all_tests()
    sys.exit(exit_code)
