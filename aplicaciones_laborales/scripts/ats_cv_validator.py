#!/usr/bin/env python3
"""
ATS CV Validator
Validates that generated CVs follow ATS-optimized patterns for maximum employability.

This module checks:
- Keyword presence and density
- Section structure and completeness
- Quantifiable achievements
- ATS-friendly formatting
- Language-appropriate content
"""

import re
from typing import Dict, List, Tuple


class ATSCVValidator:
    """Validator for ensuring CVs are optimized for ATS systems."""
    
    # Essential sections that must be present in a well-structured CV
    REQUIRED_SECTIONS_ES = [
        'perfil profesional',
        'habilidades',
        'experiencia profesional',
        'formación académica',
        'idiomas'
    ]
    
    REQUIRED_SECTIONS_EN = [
        'professional summary',
        'skills',
        'professional experience',
        'education',
        'languages'
    ]
    
    # Keywords that indicate ATS-friendly content
    ATS_KEYWORDS = {
        'es': [
            'contabilidad', 'conciliaciones', 'bancarias', 'cuentas por cobrar',
            'cuentas por pagar', 'ar', 'ap', 'reportes', 'financieros', 'sap',
            'excel', 'facturación', 'activos', 'logística', 'billing', 'eft',
            'power bi', 'análisis', 'gestión', 'procesos'
        ],
        'en': [
            'accounting', 'reconciliations', 'accounts receivable', 'accounts payable',
            'ar', 'ap', 'reports', 'financial', 'sap', 'excel', 'billing',
            'assets', 'logistics', 'eft', 'power bi', 'analysis', 'management',
            'processes'
        ]
    }
    
    def __init__(self):
        """Initialize the ATS validator."""
        self.validation_results = {}
    
    def validate_cv(self, cv_content: str, language: str = 'es') -> Dict:
        """
        Perform comprehensive ATS validation on CV content.
        
        Args:
            cv_content: The CV content as a string
            language: Language code ('es' or 'en')
            
        Returns:
            Dictionary with validation results
        """
        results = {
            'overall_score': 0,
            'is_ats_optimized': False,
            'section_validation': {},
            'keyword_validation': {},
            'achievement_validation': {},
            'format_validation': {},
            'warnings': [],
            'recommendations': []
        }
        
        # Validate sections
        section_score, section_details = self._validate_sections(cv_content, language)
        results['section_validation'] = section_details
        
        # Validate keywords
        keyword_score, keyword_details = self._validate_keywords(cv_content, language)
        results['keyword_validation'] = keyword_details
        
        # Validate achievements
        achievement_score, achievement_details = self._validate_achievements(cv_content, language)
        results['achievement_validation'] = achievement_details
        
        # Validate format
        format_score, format_details = self._validate_format(cv_content)
        results['format_validation'] = format_details
        
        # Calculate overall score (weighted average)
        results['overall_score'] = int(
            section_score * 0.30 +
            keyword_score * 0.30 +
            achievement_score * 0.25 +
            format_score * 0.15
        )
        
        # Determine if CV is ATS optimized (threshold: 80%)
        results['is_ats_optimized'] = results['overall_score'] >= 80
        
        # Generate warnings and recommendations
        results['warnings'] = self._generate_warnings(results)
        results['recommendations'] = self._generate_recommendations(results, language)
        
        return results
    
    def _validate_sections(self, cv_content: str, language: str) -> Tuple[int, Dict]:
        """
        Validate that all essential sections are present.
        
        Returns:
            Tuple of (score, details_dict)
        """
        cv_lower = cv_content.lower()
        required_sections = (self.REQUIRED_SECTIONS_ES if language == 'es' 
                           else self.REQUIRED_SECTIONS_EN)
        
        found_sections = []
        missing_sections = []
        
        for section in required_sections:
            # Look for section headers (with ## or bold formatting)
            if section in cv_lower:
                found_sections.append(section)
            else:
                missing_sections.append(section)
        
        score = int((len(found_sections) / len(required_sections)) * 100)
        
        details = {
            'score': score,
            'found_sections': found_sections,
            'missing_sections': missing_sections,
            'total_required': len(required_sections),
            'total_found': len(found_sections)
        }
        
        return score, details
    
    def _validate_keywords(self, cv_content: str, language: str) -> Tuple[int, Dict]:
        """
        Validate keyword presence and density.
        
        Returns:
            Tuple of (score, details_dict)
        """
        cv_lower = cv_content.lower()
        keywords = self.ATS_KEYWORDS.get(language, self.ATS_KEYWORDS['es'])
        
        found_keywords = []
        keyword_counts = {}
        
        for keyword in keywords:
            count = cv_lower.count(keyword)
            if count > 0:
                found_keywords.append(keyword)
                keyword_counts[keyword] = count
        
        # Calculate keyword density score
        keyword_coverage = (len(found_keywords) / len(keywords)) * 100
        
        # Bonus for multiple occurrences (shows depth of experience)
        multiple_occurrences = sum(1 for count in keyword_counts.values() if count > 1)
        bonus = min(20, multiple_occurrences * 2)
        
        score = int(min(100, keyword_coverage + bonus))
        
        details = {
            'score': score,
            'found_keywords': found_keywords,
            'keyword_counts': keyword_counts,
            'total_keywords': len(keywords),
            'keywords_found': len(found_keywords),
            'coverage_percentage': int(keyword_coverage)
        }
        
        return score, details
    
    def _validate_achievements(self, cv_content: str, language: str) -> Tuple[int, Dict]:
        """
        Validate presence of quantifiable achievements.
        
        Looks for numbers, percentages, and quantifiable metrics.
        
        Returns:
            Tuple of (score, details_dict)
        """
        # Patterns for quantifiable achievements
        number_pattern = r'\b\d+(?:,\d{3})*(?:\.\d+)?\b'
        percentage_pattern = r'\d+%'
        
        # Find all numbers and percentages
        numbers = re.findall(number_pattern, cv_content)
        percentages = re.findall(percentage_pattern, cv_content)
        
        # Count achievement indicators in experience section
        experience_section = self._extract_experience_section(cv_content, language)
        
        achievements_in_experience = 0
        if experience_section:
            achievements_in_experience = len(re.findall(number_pattern, experience_section))
        
        # Score based on quantifiable content
        # Good CVs should have at least 5-10 quantifiable achievements
        total_quantifiable = len(numbers) + len(percentages)
        
        if total_quantifiable >= 10:
            score = 100
        elif total_quantifiable >= 7:
            score = 85
        elif total_quantifiable >= 5:
            score = 70
        elif total_quantifiable >= 3:
            score = 50
        else:
            score = 30
        
        details = {
            'score': score,
            'total_numbers': len(numbers),
            'total_percentages': len(percentages),
            'achievements_in_experience': achievements_in_experience,
            'total_quantifiable': total_quantifiable,
            'has_sufficient_metrics': total_quantifiable >= 5
        }
        
        return score, details
    
    def _validate_format(self, cv_content: str) -> Tuple[int, Dict]:
        """
        Validate ATS-friendly formatting.
        
        Checks:
        - Use of bullet points
        - Clear section headers
        - Appropriate length (not too long)
        - No complex formatting that breaks ATS parsing
        
        Returns:
            Tuple of (score, details_dict)
        """
        score = 100
        issues = []
        
        # Check for bullet points (- or •)
        bullet_count = cv_content.count('\n-') + cv_content.count('•')
        if bullet_count < 5:
            score -= 20
            issues.append('Insufficient use of bullet points')
        
        # Check for section headers (## or bold)
        header_count = cv_content.count('##') + cv_content.count('**')
        if header_count < 4:
            score -= 15
            issues.append('Insufficient section headers')
        
        # Check length (should be reasonable, not too short or too long)
        line_count = len(cv_content.split('\n'))
        if line_count < 50:
            score -= 20
            issues.append('CV content too brief')
        elif line_count > 200:
            score -= 10
            issues.append('CV content may be too long')
        
        # Check for contact information
        has_email = '@' in cv_content
        has_phone = bool(re.search(r'\+?\d{1,3}[-.\s]?\d{3}[-.\s]?\d{3}[-.\s]?\d{4}', cv_content))
        
        if not has_email:
            score -= 15
            issues.append('Email address not found')
        if not has_phone:
            score -= 10
            issues.append('Phone number not found')
        
        details = {
            'score': max(0, score),
            'bullet_points': bullet_count,
            'headers': header_count,
            'line_count': line_count,
            'has_email': has_email,
            'has_phone': has_phone,
            'formatting_issues': issues
        }
        
        return max(0, score), details
    
    def _extract_experience_section(self, cv_content: str, language: str) -> str:
        """Extract the experience section from CV content."""
        if language == 'es':
            pattern = r'experiencia profesional(.*?)(?=\n##|\Z)'
        else:
            pattern = r'professional experience(.*?)(?=\n##|\Z)'
        
        match = re.search(pattern, cv_content.lower(), re.DOTALL)
        return match.group(1) if match else ""
    
    def _generate_warnings(self, results: Dict) -> List[str]:
        """Generate warnings based on validation results."""
        warnings = []
        
        # Section warnings
        if results['section_validation']['score'] < 80:
            missing = results['section_validation']['missing_sections']
            if missing:
                warnings.append(f"Missing essential sections: {', '.join(missing)}")
        
        # Keyword warnings
        if results['keyword_validation']['score'] < 70:
            warnings.append(
                f"Low keyword coverage ({results['keyword_validation']['coverage_percentage']}%). "
                "CV may not match well with ATS keyword scanning."
            )
        
        # Achievement warnings
        if not results['achievement_validation']['has_sufficient_metrics']:
            warnings.append(
                "Insufficient quantifiable achievements. Add numbers, percentages, or metrics "
                "to demonstrate impact."
            )
        
        # Format warnings
        format_issues = results['format_validation'].get('formatting_issues', [])
        for issue in format_issues:
            warnings.append(f"Format issue: {issue}")
        
        return warnings
    
    def _generate_recommendations(self, results: Dict, language: str) -> List[str]:
        """Generate actionable recommendations for improvement."""
        recommendations = []
        
        # Section recommendations
        missing_sections = results['section_validation'].get('missing_sections', [])
        if missing_sections:
            if language == 'es':
                recommendations.append(
                    f"Agregar las siguientes secciones faltantes: {', '.join(missing_sections)}"
                )
            else:
                recommendations.append(
                    f"Add the following missing sections: {', '.join(missing_sections)}"
                )
        
        # Keyword recommendations
        if results['keyword_validation']['score'] < 80:
            if language == 'es':
                recommendations.append(
                    "Incorporar más palabras clave relevantes de la descripción del puesto "
                    "en las secciones de experiencia y habilidades."
                )
            else:
                recommendations.append(
                    "Incorporate more relevant keywords from the job description "
                    "in the experience and skills sections."
                )
        
        # Achievement recommendations
        if results['achievement_validation']['score'] < 70:
            if language == 'es':
                recommendations.append(
                    "Cuantificar logros con números específicos, porcentajes, o métricas "
                    "(ej: 'Procesé 500+ transacciones mensuales con 99% de precisión')"
                )
            else:
                recommendations.append(
                    "Quantify achievements with specific numbers, percentages, or metrics "
                    "(e.g., 'Processed 500+ monthly transactions with 99% accuracy')"
                )
        
        # Overall recommendation
        if results['overall_score'] >= 90:
            if language == 'es':
                recommendations.append(
                    "✅ CV está muy bien optimizada para ATS. Continuar manteniendo este estándar."
                )
            else:
                recommendations.append(
                    "✅ CV is very well optimized for ATS. Continue maintaining this standard."
                )
        elif results['overall_score'] >= 80:
            if language == 'es':
                recommendations.append(
                    "✓ CV está bien optimizada para ATS. Pequeñas mejoras pueden incrementar la puntuación."
                )
            else:
                recommendations.append(
                    "✓ CV is well optimized for ATS. Minor improvements can increase the score."
                )
        else:
            if language == 'es':
                recommendations.append(
                    "⚠️ CV necesita mejoras significativas para maximizar la compatibilidad con ATS. "
                    "Priorizar las recomendaciones anteriores."
                )
            else:
                recommendations.append(
                    "⚠️ CV needs significant improvements to maximize ATS compatibility. "
                    "Prioritize the above recommendations."
                )
        
        return recommendations
    
    def format_validation_report(self, results: Dict, job_title: str, language: str = 'es') -> str:
        """
        Format validation results as a readable report.
        
        Args:
            results: Validation results dictionary
            job_title: Job title for context
            language: Language code ('es' or 'en')
            
        Returns:
            Formatted markdown report
        """
        if language == 'es':
            report = f"""# Reporte de Validación ATS

## Información General

- **Cargo:** {job_title}
- **Puntuación ATS General:** {results['overall_score']}/100
- **Estado:** {'✅ OPTIMIZADA PARA ATS' if results['is_ats_optimized'] else '⚠️ REQUIERE MEJORAS'}

---

## Desglose de Validación

### 1. Estructura de Secciones ({results['section_validation']['score']}/100)

- **Secciones Requeridas:** {results['section_validation']['total_required']}
- **Secciones Encontradas:** {results['section_validation']['total_found']}
- **Estado:** {'✅ Completa' if results['section_validation']['score'] >= 80 else '⚠️ Incompleta'}

"""
            if results['section_validation']['missing_sections']:
                report += "**Secciones Faltantes:**\n"
                for section in results['section_validation']['missing_sections']:
                    report += f"- {section.title()}\n"
                report += "\n"
            
            report += f"""### 2. Palabras Clave ({results['keyword_validation']['score']}/100)

- **Cobertura de Palabras Clave:** {results['keyword_validation']['coverage_percentage']}%
- **Palabras Clave Encontradas:** {results['keyword_validation']['keywords_found']}/{results['keyword_validation']['total_keywords']}
- **Estado:** {'✅ Excelente' if results['keyword_validation']['score'] >= 80 else '⚠️ Mejorable'}

**Palabras Clave Principales Detectadas:**
"""
            for keyword, count in sorted(results['keyword_validation']['keyword_counts'].items(), 
                                        key=lambda x: x[1], reverse=True)[:10]:
                report += f"- {keyword.title()} (×{count})\n"
            
            report += f"""

### 3. Logros Cuantificables ({results['achievement_validation']['score']}/100)

- **Métricas Totales:** {results['achievement_validation']['total_quantifiable']}
- **Números en Experiencia:** {results['achievement_validation']['achievements_in_experience']}
- **Estado:** {'✅ Suficientes' if results['achievement_validation']['has_sufficient_metrics'] else '⚠️ Insuficientes'}

### 4. Formato ATS-Friendly ({results['format_validation']['score']}/100)

- **Puntos de Viñeta:** {results['format_validation']['bullet_points']}
- **Encabezados de Sección:** {results['format_validation']['headers']}
- **Longitud del CV:** {results['format_validation']['line_count']} líneas
- **Email Incluido:** {'✅' if results['format_validation']['has_email'] else '❌'}
- **Teléfono Incluido:** {'✅' if results['format_validation']['has_phone'] else '❌'}

"""
        else:  # English
            report = f"""# ATS Validation Report

## General Information

- **Position:** {job_title}
- **Overall ATS Score:** {results['overall_score']}/100
- **Status:** {'✅ ATS OPTIMIZED' if results['is_ats_optimized'] else '⚠️ NEEDS IMPROVEMENT'}

---

## Validation Breakdown

### 1. Section Structure ({results['section_validation']['score']}/100)

- **Required Sections:** {results['section_validation']['total_required']}
- **Sections Found:** {results['section_validation']['total_found']}
- **Status:** {'✅ Complete' if results['section_validation']['score'] >= 80 else '⚠️ Incomplete'}

"""
            if results['section_validation']['missing_sections']:
                report += "**Missing Sections:**\n"
                for section in results['section_validation']['missing_sections']:
                    report += f"- {section.title()}\n"
                report += "\n"
            
            report += f"""### 2. Keywords ({results['keyword_validation']['score']}/100)

- **Keyword Coverage:** {results['keyword_validation']['coverage_percentage']}%
- **Keywords Found:** {results['keyword_validation']['keywords_found']}/{results['keyword_validation']['total_keywords']}
- **Status:** {'✅ Excellent' if results['keyword_validation']['score'] >= 80 else '⚠️ Needs Improvement'}

**Top Detected Keywords:**
"""
            for keyword, count in sorted(results['keyword_validation']['keyword_counts'].items(), 
                                        key=lambda x: x[1], reverse=True)[:10]:
                report += f"- {keyword.title()} (×{count})\n"
            
            report += f"""

### 3. Quantifiable Achievements ({results['achievement_validation']['score']}/100)

- **Total Metrics:** {results['achievement_validation']['total_quantifiable']}
- **Numbers in Experience:** {results['achievement_validation']['achievements_in_experience']}
- **Status:** {'✅ Sufficient' if results['achievement_validation']['has_sufficient_metrics'] else '⚠️ Insufficient'}

### 4. ATS-Friendly Format ({results['format_validation']['score']}/100)

- **Bullet Points:** {results['format_validation']['bullet_points']}
- **Section Headers:** {results['format_validation']['headers']}
- **CV Length:** {results['format_validation']['line_count']} lines
- **Email Included:** {'✅' if results['format_validation']['has_email'] else '❌'}
- **Phone Included:** {'✅' if results['format_validation']['has_phone'] else '❌'}

"""
        
        # Add warnings section
        if results['warnings']:
            if language == 'es':
                report += "---\n\n## ⚠️ Advertencias\n\n"
            else:
                report += "---\n\n## ⚠️ Warnings\n\n"
            
            for warning in results['warnings']:
                report += f"- {warning}\n"
            report += "\n"
        
        # Add recommendations section
        if results['recommendations']:
            if language == 'es':
                report += "---\n\n## 💡 Recomendaciones\n\n"
            else:
                report += "---\n\n## 💡 Recommendations\n\n"
            
            for i, recommendation in enumerate(results['recommendations'], 1):
                report += f"{i}. {recommendation}\n\n"
        
        # Add summary
        if language == 'es':
            report += """---

## Resumen

Este CV ha sido validado automáticamente para optimización ATS. Las métricas evalúan:
- Presencia de secciones esenciales
- Densidad de palabras clave relevantes
- Logros cuantificables con métricas
- Formato compatible con sistemas ATS

**Criterio de Aprobación:** Puntuación ≥ 80/100

"""
        else:
            report += """---

## Summary

This CV has been automatically validated for ATS optimization. Metrics evaluate:
- Presence of essential sections
- Relevant keyword density
- Quantifiable achievements with metrics
- ATS-compatible formatting

**Approval Criteria:** Score ≥ 80/100

"""
        
        return report
