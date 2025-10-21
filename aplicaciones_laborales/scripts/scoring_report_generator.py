#!/usr/bin/env python3
"""
Scoring Report Generator
Generates formatted markdown reports from scoring results.
"""


class ScoringReportGenerator:
    """Generator for creating formatted scoring reports."""
    
    def generate_report(self, scoring_result, job_title, company, application_date):
        """
        Generate a formatted markdown scoring report.
        
        Args:
            scoring_result: Dictionary with scoring data
            job_title: Job title
            company: Company name
            application_date: Application date
            
        Returns:
            Formatted markdown report as string
        """
        report = f"""# Reporte de Evaluación de Aplicación

## Información General

- **Cargo:** {job_title}
- **Empresa:** {company}
- **Fecha de Aplicación:** {application_date}
- **Candidata:** Karen Schmalbach

---

## Puntuación Global

**Puntuación Total:** {scoring_result['global_score']}/100

**Recomendación:** {scoring_result['recommendation']}

---

## Desglose de Puntuación

- **Puntuación Base:** {scoring_result['base_score']}/100
- **Ajuste por Factores:** {scoring_result['bonus_score']:+d} puntos
- **Puntuación Final:** {scoring_result['global_score']}/100

---

## Análisis de Habilidades

### Coincidencia de Competencias

- **Habilidades del Perfil Evaluadas:** {scoring_result['skills_breakdown']['total_profile_keywords']}
- **Habilidades Coincidentes:** {scoring_result['skills_breakdown']['matched_count']}
- **Porcentaje de Coincidencia:** {scoring_result['skills_breakdown']['match_percentage']}%

### Habilidades Coincidentes Detectadas

"""
        
        # Add matched skills
        matched_skills = scoring_result['skills_breakdown']['matched_skills']
        if matched_skills:
            for skill in matched_skills:
                report += f"- {skill.title()}\n"
        else:
            report += "- No se detectaron coincidencias directas con palabras clave del perfil\n"
        
        report += """
---

## Análisis de Requerimientos

"""
        
        report += f"**Total de Requerimientos Listados:** {scoring_result['requirements_count']}\n\n"
        
        # Add recommendation details
        report += """---

## Recomendación Detallada

"""
        
        if scoring_result['recommendation_level'] == 'high':
            report += """
Esta aplicación muestra una **alta alineación** con el perfil de la candidata. 
Las competencias y experiencia de Karen se alinean bien con los requerimientos del puesto.

**Acción Recomendada:** Aplicar con confianza. El perfil es sólido para esta posición.
"""
        elif scoring_result['recommendation_level'] == 'medium':
            report += """
Esta aplicación muestra una **buena alineación** con el perfil de la candidata.
Hay coincidencias significativas, aunque pueden existir algunos requerimientos 
que requieran desarrollo adicional.

**Acción Recomendada:** Aplicar. Destacar las competencias coincidentes en la carta de presentación.
"""
        elif scoring_result['recommendation_level'] == 'low':
            report += """
Esta aplicación muestra una **alineación moderada** con el perfil de la candidata.
Se recomienda revisar cuidadosamente los requerimientos y evaluar si las 
competencias transferibles son suficientes.

**Acción Recomendada:** Aplicar con precaución. Preparar explicación de competencias transferibles.
"""
        else:
            report += """
Esta aplicación muestra **baja alineación** con el perfil de la candidata.
Es posible que varios requerimientos clave no se alineen con la experiencia actual.

**Acción Recomendada:** Revisar requerimientos. Considerar si el desarrollo de habilidades 
adicionales es viable antes de aplicar.
"""
        
        report += """
---

## Notas

Este reporte es generado automáticamente basado en el análisis de palabras clave 
y no reemplaza el juicio profesional. Se recomienda revisar manualmente los 
requerimientos específicos y evaluar competencias transferibles.

---

*Reporte generado automáticamente el {date}*
""".format(date=application_date)
        
        return report
