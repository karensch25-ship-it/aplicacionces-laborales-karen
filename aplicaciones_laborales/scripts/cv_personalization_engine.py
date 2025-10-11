"""
CV Personalization Engine - Enhanced CV Generation
Implements intelligent mapping between job requirements and candidate achievements
"""

import re
from typing import List, Dict, Tuple

class CVPersonalizationEngine:
    """
    Engine for personalizing CVs based on job requirements
    """
    
    def __init__(self):
        # Mapping of keywords to specific achievements from Antonio's CV
        self.achievement_mapping = {
            'dashboard': [
                "Architected consolidated dashboard integrating 8 data sources, cutting data preparation time by 70%",
                "Implemented sales and inventory dashboards for Latin America, reducing decision-making time by 40%",
                "Managed Thoughtspot data for 8+ countries with 100% reporting accuracy"
            ],
            'sql': [
                "Built 20+ SQL stored procedures, improving query performance by 40% and reducing error rates by 75%",
                "Optimized database architecture, reducing query time by 65%"
            ],
            'automation': [
                "Developed 15+ automated reports using M-AT and NPR, reducing manual reporting time by 60% for 200+ healthcare professionals",
                "Automated ETL processes, reducing daily processing time from 4 hours to 30 minutes",
                "Automated SAP data analysis, reducing reporting time by 75%",
                "Developed automated tracking system, reducing processing time by 65%"
            ],
            'etl': [
                "Automated ETL processes, reducing daily processing time from 4 hours to 30 minutes",
                "Streamlined ETL processes for 1,000+ transactions, achieving 40% faster processing times",
                "Optimized database architecture, reducing query time by 65% and manual processing time by 87%"
            ],
            'data integration': [
                "Architected consolidated dashboard integrating 8 data sources, cutting data preparation time by 70%",
                "Managed Thoughtspot data for 8+ countries with 100% reporting accuracy"
            ],
            'integration': [
                "Architected consolidated dashboard integrating 8 data sources",
                "Implemented sales and inventory dashboards for Latin America"
            ],
            'bi': [
                "Implemented sales and inventory dashboards for Latin America, reducing decision-making time by 40%",
                "Managed Thoughtspot data for 8+ countries with 100% reporting accuracy"
            ],
            'business intelligence': [
                "Implemented sales and inventory dashboards for Latin America, reducing decision-making time by 40%",
                "Developed 12 KPIs, improving sales visibility by 30% across 5 regions"
            ],
            'stakeholder': [
                "Collaborated with cross-functional teams to optimize healthcare data workflows",
                "Led system transition and trained 15 users, establishing data governance protocols and improving accuracy by 85%",
                "Maintained 98% client satisfaction while managing 50+ regular clients"
            ],
            'collaboration': [
                "Collaborated with cross-functional teams to optimize healthcare data workflows",
                "Led system transition and trained 15 users",
                "Worked with internal teams across multiple departments"
            ],
            'report': [
                "Developed 15+ automated reports using M-AT and NPR, reducing manual reporting time by 60%",
                "Developed 12 KPIs, improving sales visibility by 30% across 5 regions"
            ],
            'data quality': [
                "Increased data accuracy by 95% through quality control measures",
                "Led system transition and trained 15 users, establishing data governance protocols and improving accuracy by 85%"
            ],
            'api': [
                "Experience with data integration and API-based solutions through cross-platform dashboard development"
            ],
            'power bi': [
                "Implemented sales and inventory dashboards for Latin America",
                "Professional experience with Power BI for business intelligence solutions"
            ],
            'data analysis': [
                "Built 20+ SQL stored procedures, improving query performance by 40%",
                "Managed Thoughtspot data for 8+ countries with 100% reporting accuracy",
                "Automated SAP data analysis, reducing reporting time by 75%"
            ],
            'training': [
                "Led system transition and trained 15 users, establishing data governance protocols"
            ],
            'kpi': [
                "Developed 12 KPIs, improving sales visibility by 30% across 5 regions"
            ],
            'data governance': [
                "Led system transition and trained 15 users, establishing data governance protocols and improving accuracy by 85%"
            ],
            'performance': [
                "Built 20+ SQL stored procedures, improving query performance by 40% and reducing error rates by 75%",
                "Optimized database architecture, reducing query time by 65%"
            ]
        }
    
    def extract_keywords(self, text) -> List[str]:
        """
        Extract relevant keywords from requirement text
        Handles both string and dict inputs
        """
        # Handle dict inputs
        if isinstance(text, dict):
            # Combine key and value
            text_parts = []
            for k, v in text.items():
                text_parts.append(str(k))
                text_parts.append(str(v))
            text = " ".join(text_parts)
        
        # Convert to string if needed
        text_str = str(text) if not isinstance(text, str) else text
        
        # Convert to lowercase for matching
        text_lower = text_str.lower()
        
        # Find matching keywords
        found_keywords = []
        for keyword in self.achievement_mapping.keys():
            if keyword in text_lower:
                found_keywords.append(keyword)
        
        return found_keywords
    
    def generar_job_alignment_inteligente(self, requerimientos: List) -> str:
        """
        Generate intelligent job alignment section that maps requirements to specific achievements
        
        Args:
            requerimientos: List of job requirements from YAML (can be strings or dicts)
            
        Returns:
            Formatted markdown section showing how experience aligns with requirements
        """
        alignment_items = []
        
        for req in requerimientos:
            # Skip empty requirements
            if not req:
                continue
            
            # Handle dict requirements
            if isinstance(req, dict):
                # Convert dict to readable format
                req_str = ""
                for k, v in req.items():
                    req_str = f"{k}: {v}"
                    break  # Use first key-value pair
            else:
                # Convert to string if not already
                req_str = str(req)
            
            # Skip "None" strings
            if req_str.strip().lower() == 'none':
                continue
            
            # Extract keywords from requirement
            keywords = self.extract_keywords(req_str)
            
            # Find best matching achievement
            best_achievement = None
            if keywords:
                # Get achievement for first matching keyword
                for keyword in keywords:
                    if keyword in self.achievement_mapping:
                        achievements = self.achievement_mapping[keyword]
                        if achievements:
                            best_achievement = achievements[0]
                            break
            
            # Format the alignment item
            if best_achievement:
                # Capitalize first letter of requirement if needed
                req_formatted = req_str[0].upper() + req_str[1:] if req_str else req_str
                alignment_items.append(f"**{req_formatted}**\n\n{best_achievement}")
            else:
                # Fallback: generic but grammatically correct statement
                req_formatted = req_str[0].upper() + req_str[1:] if req_str else req_str
                # Extract main skill/action from requirement
                req_clean = req_formatted.rstrip('.')
                alignment_items.append(f"**{req_clean}**\n\nRelevant experience demonstrated through data analysis, process optimization, and cross-functional collaboration in enterprise environments.")
        
        if not alignment_items:
            return "Comprehensive experience in data analysis, business intelligence, and process automation aligns well with the requirements of this role."
        
        # Join items with double newline for better formatting
        return "\n\n".join(alignment_items)
    
    def generar_professional_summary_personalizado(self, cargo: str, requerimientos: List) -> str:
        """
        Generate personalized professional summary based on job title and requirements
        
        Args:
            cargo: Job title
            requerimientos: List of job requirements (can be strings or dicts)
            
        Returns:
            Personalized professional summary
        """
        # Base intro
        base = "Data Analyst with 5+ years of experience specializing in"
        
        # Detect focus areas from requirements
        focus_areas = []
        keywords_found = set()
        
        for req in requerimientos:
            if req:
                keywords = self.extract_keywords(req)
                keywords_found.update(keywords)
        
        # Map keywords to focus areas
        if any(kw in keywords_found for kw in ['dashboard', 'bi', 'business intelligence']):
            focus_areas.append("business intelligence and dashboard development")
        
        if any(kw in keywords_found for kw in ['automation', 'etl']):
            focus_areas.append("data automation and ETL processes")
        
        if any(kw in keywords_found for kw in ['integration', 'api', 'data integration']):
            focus_areas.append("data integration and system connectivity")
        
        if any(kw in keywords_found for kw in ['data quality', 'data governance']):
            focus_areas.append("data quality management and governance")
        
        # If no specific focus areas found, use default
        if not focus_areas:
            focus_areas = ["data migration, ETL processes, and data quality management"]
        
        # Build personalized summary
        areas_text = " and ".join(focus_areas[:2])  # Maximum 2 areas for conciseness
        summary = f"{base} {areas_text}. "
        
        summary += "Proven track record in delivering data-driven solutions that reduce operational costs, improve decision-making accuracy, and drive business outcomes. "
        summary += "Effective communicator skilled in stakeholder engagement and cross-functional collaboration, "
        summary += "with experience supporting teams across healthcare, technology, and logistics sectors."
        
        return summary
    
    def calcular_match_score(self, requerimientos: List) -> Dict:
        """
        Calculate how well the candidate matches the job requirements
        
        Args:
            requerimientos: List of job requirements
            
        Returns:
            Dictionary with match analysis
        """
        strong_matches = []
        moderate_matches = []
        weak_matches = []
        
        for req in requerimientos:
            if not req:
                continue
            
            # Convert to string if not already
            req_str = str(req) if not isinstance(req, str) else req
            
            if req_str.strip().lower() == 'none':
                continue
                
            keywords = self.extract_keywords(req_str)
            
            if len(keywords) >= 2:
                strong_matches.append(req_str)
            elif len(keywords) == 1:
                moderate_matches.append(req_str)
            else:
                weak_matches.append(req_str)
        
        total_reqs = len([r for r in requerimientos if r and str(r).strip().lower() != 'none'])
        
        if total_reqs == 0:
            match_percentage = 0
        else:
            match_percentage = ((len(strong_matches) + 0.5 * len(moderate_matches)) / total_reqs) * 100
        
        return {
            'match_percentage': round(match_percentage, 1),
            'strong_matches': len(strong_matches),
            'moderate_matches': len(moderate_matches),
            'weak_matches': len(weak_matches),
            'total_requirements': total_reqs,
            'recommendation': 'Strong fit' if match_percentage >= 70 else 'Good fit' if match_percentage >= 50 else 'Moderate fit'
        }


def generar_job_alignment(requerimientos: List[str]) -> str:
    """
    Enhanced version of job alignment generation (backward compatible)
    
    Args:
        requerimientos: List of job requirements from YAML
        
    Returns:
        Formatted job alignment section
    """
    engine = CVPersonalizationEngine()
    return engine.generar_job_alignment_inteligente(requerimientos)


def generar_professional_summary(cargo: str, requerimientos: List[str]) -> str:
    """
    Generate personalized professional summary
    
    Args:
        cargo: Job title
        requerimientos: List of job requirements
        
    Returns:
        Personalized professional summary
    """
    engine = CVPersonalizationEngine()
    return engine.generar_professional_summary_personalizado(cargo, requerimientos)


# Example usage
if __name__ == "__main__":
    # Test with sample requirements
    sample_reqs = [
        "Build and maintain custom dashboards to support business operations",
        "Clean, transform, and analyze data from multiple systems",
        "Create and manage lightweight integrations between tools using Zapier, APIs, or low-code platforms",
        "Work with internal teams to understand reporting and automation needs",
        "Leverage AI tools (e.g., OpenAI APIs, AI-based automations) to improve workflows"
    ]
    
    engine = CVPersonalizationEngine()
    
    print("=== PERSONALIZED PROFESSIONAL SUMMARY ===")
    summary = engine.generar_professional_summary_personalizado("Data & Automation (BI) Analyst", sample_reqs)
    print(summary)
    print("\n")
    
    print("=== JOB ALIGNMENT SECTION ===")
    alignment = engine.generar_job_alignment_inteligente(sample_reqs)
    print(alignment)
    print("\n")
    
    print("=== MATCH ANALYSIS ===")
    match_score = engine.calcular_match_score(sample_reqs)
    print(f"Match Percentage: {match_score['match_percentage']}%")
    print(f"Strong Matches: {match_score['strong_matches']}")
    print(f"Moderate Matches: {match_score['moderate_matches']}")
    print(f"Weak Matches: {match_score['weak_matches']}")
    print(f"Recommendation: {match_score['recommendation']}")
