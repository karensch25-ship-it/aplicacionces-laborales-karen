#!/usr/bin/env python3
"""
CV Personalization Engine
Generates personalized job alignment sections and professional summaries
for job applications based on requirements.
"""


class CVPersonalizationEngine:
    """Engine for personalizing CV content based on job requirements."""
    
    def generar_job_alignment_inteligente(self, requerimientos, language='es'):
        """
        Generate intelligent job alignment section based on requirements.
        
        Args:
            requerimientos: List of job requirements
            language: Language code ('es' for Spanish, 'en' for English)
            
        Returns:
            Formatted markdown section explaining alignment with requirements
        """
        if not requerimientos:
            if language == 'en':
                return "My skills and professional experience allow me to adapt to the requirements of this position."
            return "Mis habilidades y experiencia profesional me permiten adaptarme a los requerimientos de este puesto."
        
        # Generate alignment section
        if language == 'en':
            alignment_text = "Below I detail how my experience aligns with the key requirements:\n\n"
        else:
            alignment_text = "A continuación detallo cómo mi experiencia se alinea con los requerimientos clave:\n\n"
        
        for req in requerimientos[:5]:  # Limit to top 5 requirements for brevity
            # Map common requirement keywords to Karen's experience
            req_lower = req.lower()
            
            if any(keyword in req_lower for keyword in ['conciliaci', 'bancari', 'bank', 'reconciliation']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Strong experience in national and international bank reconciliations at UPS and Accenture, managing EFT processes and payment applications.\n\n"
                else:
                    alignment_text += f"- **{req}**: Experiencia sólida en conciliaciones bancarias nacionales e internacionales en UPS y Accenture, gestionando procesos EFT y aplicaciones de pagos.\n\n"
            elif any(keyword in req_lower for keyword in ['cuentas por cobrar', 'ar', 'accounts receivable', 'receivable']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Accounts receivable (AR) management at UPS, including transaction tracking and invoice status changes.\n\n"
                else:
                    alignment_text += f"- **{req}**: Gestión de cuentas por cobrar (AR) en UPS, incluyendo seguimiento de transacciones y cambios de estado de facturas.\n\n"
            elif any(keyword in req_lower for keyword in ['excel', 'reportes', 'reports', 'reporting']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Preparation of financial and accounting reports using advanced Excel, with experience in process automation.\n\n"
                else:
                    alignment_text += f"- **{req}**: Elaboración de reportes financieros y contables utilizando Excel avanzado, con experiencia en automatización de procesos.\n\n"
            elif any(keyword in req_lower for keyword in ['sap', 'erp', 'sistema', 'system']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Experience with SAP and other financial systems in previous roles, facilitating adaptation to new platforms.\n\n"
                else:
                    alignment_text += f"- **{req}**: Manejo de SAP y otros sistemas financieros en roles previos, facilitando la adaptación a nuevas plataformas.\n\n"
            elif any(keyword in req_lower for keyword in ['inglés', 'english', 'bilingu']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Bilingual experience (Spanish-Portuguese) in customer service and communication with international teams. Basic English level in development.\n\n"
                else:
                    alignment_text += f"- **{req}**: Experiencia bilingüe (español-portugués) en atención al cliente y comunicación con equipos internacionales. Nivel básico de inglés en desarrollo.\n\n"
            elif any(keyword in req_lower for keyword in ['power bi', 'bi', 'visualizaci', 'visualization']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Currently taking Power BI training to strengthen data visualization and analysis skills.\n\n"
                else:
                    alignment_text += f"- **{req}**: Cursando capacitación en Power BI para fortalecer habilidades en visualización de datos y análisis.\n\n"
            elif any(keyword in req_lower for keyword in ['facturaci', 'invoic', 'billing']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Experience in billing and invoicing processes in multiple roles, including invoice filing and document management.\n\n"
                else:
                    alignment_text += f"- **{req}**: Experiencia en facturación y procesos de billing en múltiples roles, incluyendo radicación de facturas y gestión documental.\n\n"
            elif any(keyword in req_lower for keyword in ['activo', 'asset']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Management of asset disposals and entry into the system at Accenture, with status change tracking.\n\n"
                else:
                    alignment_text += f"- **{req}**: Gestión de enajenaciones e ingreso de activos al sistema en Accenture, con seguimiento de cambios de estatus.\n\n"
            elif any(keyword in req_lower for keyword in ['logística', 'logistic', 'operaci', 'operation']):
                if language == 'en':
                    alignment_text += f"- **{req}**: Strong experience in logistics and operations at Casa Luker and Siscom, coordinating transportation and document control.\n\n"
                else:
                    alignment_text += f"- **{req}**: Sólida experiencia en logística y operaciones en Casa Luker y Siscom, coordinando transporte y control documental.\n\n"
            else:
                # Generic alignment for other requirements
                if language == 'en':
                    alignment_text += f"- **{req}**: My education in Public Accounting and experience in accounting and financial roles provides a solid foundation for this requirement.\n\n"
                else:
                    alignment_text += f"- **{req}**: Mi formación en Contaduría Pública y experiencia en roles contables y financieros me proporciona una base sólida para este requerimiento.\n\n"
        
        if language == 'en':
            alignment_text += "\nI am committed to continuous learning and rapid adaptation to new challenges and tools of the position."
        else:
            alignment_text += "\nEstoy comprometida con el aprendizaje continuo y la adaptación rápida a nuevos desafíos y herramientas del puesto."
        
        return alignment_text
    
    def generar_professional_summary_personalizado(self, cargo, requerimientos, language='es'):
        """
        Generate personalized professional summary based on job title and requirements.
        
        Args:
            cargo: Job title
            requerimientos: List of job requirements
            language: Language code ('es' for Spanish, 'en' for English)
            
        Returns:
            Personalized professional summary
        """
        # Base summary focusing on Karen's core competencies
        if language == 'en':
            base_summary = (
                "Accounting Public student with hands-on experience in accounting, "
                "financial analysis, and logistics operations. I specialize in bank reconciliations, "
                "accounts receivable management, financial reporting, and accounting process optimization. "
            )
        else:
            base_summary = (
                "Profesional en formación en Contaduría Pública con experiencia práctica en contabilidad, "
                "análisis financiero y operaciones logísticas. Me especializo en conciliaciones bancarias, "
                "gestión de cuentas por cobrar, generación de reportes financieros y optimización de procesos contables. "
            )
        
        # Add job-specific focus based on requirements
        req_keywords = ' '.join(requerimientos).lower() if requerimientos else ''
        
        additional_focus = ""
        if any(keyword in req_keywords for keyword in ['billing', 'facturaci', 'invoic']):
            if language == 'en':
                additional_focus += "With specific experience in billing and invoicing processes. "
            else:
                additional_focus += "Con experiencia específica en procesos de facturación y billing. "
        
        if any(keyword in req_keywords for keyword in ['power bi', 'bi', 'visual', 'datos', 'data']):
            if language == 'en':
                additional_focus += "Currently developing competencies in Power BI and data analysis. "
            else:
                additional_focus += "Actualmente desarrollando competencias en Power BI y análisis de datos. "
        
        if any(keyword in req_keywords for keyword in ['sap', 'erp']):
            if language == 'en':
                additional_focus += "Familiar with SAP and other corporate ERP systems. "
            else:
                additional_focus += "Familiarizada con SAP y otros sistemas ERP corporativos. "
        
        if any(keyword in req_keywords for keyword in ['inglés', 'english', 'bilingu']):
            if language == 'en':
                additional_focus += "Experience in bilingual and multicultural environments. "
            else:
                additional_focus += "Experiencia en entornos bilingües y multiculturales. "
        
        if language == 'en':
            closing = (
                "I have worked in shared services environments and multinational companies, "
                "adapting to diverse teams and providing attention to detail to improve efficiency "
                "and support decision-making. Results-oriented and committed to continuous "
                "professional development."
            )
        else:
            closing = (
                "He trabajado en entornos de servicios compartidos y empresas multinacionales, "
                "adaptándome a equipos diversos y aportando atención al detalle para mejorar eficiencia "
                "y soporte a la toma de decisiones. Orientada a resultados y comprometida con el desarrollo "
                "profesional continuo."
            )
        
        return base_summary + additional_focus + closing
