#!/usr/bin/env python3
"""
CV Personalization Engine
Generates personalized job alignment sections and professional summaries
for job applications based on requirements.
"""


class CVPersonalizationEngine:
    """Engine for personalizing CV content based on job requirements."""
    
    def generar_job_alignment_inteligente(self, requerimientos):
        """
        Generate intelligent job alignment section based on requirements.
        
        Args:
            requerimientos: List of job requirements
            
        Returns:
            Formatted markdown section explaining alignment with requirements
        """
        if not requerimientos:
            return "Mis habilidades y experiencia profesional me permiten adaptarme a los requerimientos de este puesto."
        
        # Generate alignment section
        alignment_text = "A continuación detallo cómo mi experiencia se alinea con los requerimientos clave:\n\n"
        
        for req in requerimientos[:5]:  # Limit to top 5 requirements for brevity
            # Map common requirement keywords to Karen's experience
            req_lower = req.lower()
            
            if any(keyword in req_lower for keyword in ['conciliaci', 'bancari', 'bank']):
                alignment_text += f"- **{req}**: Experiencia sólida en conciliaciones bancarias nacionales e internacionales en UPS y Accenture, gestionando procesos EFT y aplicaciones de pagos.\n\n"
            elif any(keyword in req_lower for keyword in ['cuentas por cobrar', 'ar', 'accounts receivable']):
                alignment_text += f"- **{req}**: Gestión de cuentas por cobrar (AR) en UPS, incluyendo seguimiento de transacciones y cambios de estado de facturas.\n\n"
            elif any(keyword in req_lower for keyword in ['excel', 'reportes', 'reports']):
                alignment_text += f"- **{req}**: Elaboración de reportes financieros y contables utilizando Excel avanzado, con experiencia en automatización de procesos.\n\n"
            elif any(keyword in req_lower for keyword in ['sap', 'erp', 'sistema']):
                alignment_text += f"- **{req}**: Manejo de SAP y otros sistemas financieros en roles previos, facilitando la adaptación a nuevas plataformas.\n\n"
            elif any(keyword in req_lower for keyword in ['inglés', 'english', 'bilingu']):
                alignment_text += f"- **{req}**: Experiencia bilingüe (español-portugués) en atención al cliente y comunicación con equipos internacionales. Nivel básico de inglés en desarrollo.\n\n"
            elif any(keyword in req_lower for keyword in ['power bi', 'bi', 'visualizaci']):
                alignment_text += f"- **{req}**: Cursando capacitación en Power BI para fortalecer habilidades en visualización de datos y análisis.\n\n"
            elif any(keyword in req_lower for keyword in ['facturaci', 'invoic', 'billing']):
                alignment_text += f"- **{req}**: Experiencia en facturación y procesos de billing en múltiples roles, incluyendo radicación de facturas y gestión documental.\n\n"
            elif any(keyword in req_lower for keyword in ['activo', 'asset']):
                alignment_text += f"- **{req}**: Gestión de enajenaciones e ingreso de activos al sistema en Accenture, con seguimiento de cambios de estatus.\n\n"
            elif any(keyword in req_lower for keyword in ['logística', 'logistic', 'operaci']):
                alignment_text += f"- **{req}**: Sólida experiencia en logística y operaciones en Casa Luker y Siscom, coordinando transporte y control documental.\n\n"
            else:
                # Generic alignment for other requirements
                alignment_text += f"- **{req}**: Mi formación en Contaduría Pública y experiencia en roles contables y financieros me proporciona una base sólida para este requerimiento.\n\n"
        
        alignment_text += "\nEstoy comprometida con el aprendizaje continuo y la adaptación rápida a nuevos desafíos y herramientas del puesto."
        
        return alignment_text
    
    def generar_professional_summary_personalizado(self, cargo, requerimientos):
        """
        Generate personalized professional summary based on job title and requirements.
        
        Args:
            cargo: Job title
            requerimientos: List of job requirements
            
        Returns:
            Personalized professional summary in Spanish
        """
        # Base summary focusing on Karen's core competencies
        base_summary = (
            "Profesional en formación en Contaduría Pública con experiencia práctica en contabilidad, "
            "análisis financiero y operaciones logísticas. Me especializo en conciliaciones bancarias, "
            "gestión de cuentas por cobrar, generación de reportes financieros y optimización de procesos contables. "
        )
        
        # Add job-specific focus based on requirements
        req_keywords = ' '.join(requerimientos).lower() if requerimientos else ''
        
        additional_focus = ""
        if any(keyword in req_keywords for keyword in ['billing', 'facturaci', 'invoic']):
            additional_focus += "Con experiencia específica en procesos de facturación y billing. "
        
        if any(keyword in req_keywords for keyword in ['power bi', 'bi', 'visual', 'datos', 'data']):
            additional_focus += "Actualmente desarrollando competencias en Power BI y análisis de datos. "
        
        if any(keyword in req_keywords for keyword in ['sap', 'erp']):
            additional_focus += "Familiarizada con SAP y otros sistemas ERP corporativos. "
        
        if any(keyword in req_keywords for keyword in ['inglés', 'english', 'bilingu']):
            additional_focus += "Experiencia en entornos bilingües y multiculturales. "
        
        closing = (
            "He trabajado en entornos de servicios compartidos y empresas multinacionales, "
            "adaptándome a equipos diversos y aportando atención al detalle para mejorar eficiencia "
            "y soporte a la toma de decisiones. Orientada a resultados y comprometida con el desarrollo "
            "profesional continuo."
        )
        
        return base_summary + additional_focus + closing
