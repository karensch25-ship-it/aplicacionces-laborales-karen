#!/usr/bin/env python3
"""
Advanced Scoring Engine
Calculates match scores between candidate profile and job requirements.
"""


class AdvancedScoringEngine:
    """Engine for scoring job application fit based on requirements."""
    
    def __init__(self):
        """Initialize scoring engine with Karen's profile keywords."""
        # Karen's core competencies and skills
        self.profile_keywords = {
            'contabilidad', 'conciliaciones', 'bancarias', 'cuentas por cobrar', 
            'ar', 'reportes', 'financieros', 'sap', 'excel', 'facturación',
            'activos', 'logística', 'portugués', 'billing', 'eft', 
            'corrección monetaria', 'depreciación', 'power bi'
        }
        
    def calculate_comprehensive_score(self, requirements, job_description, job_title):
        """
        Calculate comprehensive match score for the job application.
        
        Args:
            requirements: List of job requirements
            job_description: Job description text
            job_title: Job title
            
        Returns:
            Dictionary with scoring results
        """
        # Combine all text for analysis
        all_text = ' '.join(requirements) + ' ' + job_description + ' ' + job_title
        all_text_lower = all_text.lower()
        
        # Count matching keywords
        matches = 0
        total_keywords = len(self.profile_keywords)
        matched_skills = []
        
        for keyword in self.profile_keywords:
            if keyword in all_text_lower:
                matches += 1
                matched_skills.append(keyword)
        
        # Calculate base score (0-100)
        if total_keywords > 0:
            base_score = int((matches / total_keywords) * 100)
        else:
            base_score = 50
        
        # Adjust score based on specific criteria
        bonus_score = 0
        
        # Bonus for accounting/finance roles
        if any(keyword in all_text_lower for keyword in ['contab', 'financ', 'accounting', 'finance']):
            bonus_score += 10
        
        # Bonus for bilingual requirements (Spanish is native, Portuguese advanced)
        if any(keyword in all_text_lower for keyword in ['español', 'portugués', 'spanish', 'portuguese']):
            bonus_score += 5
        
        # Penalty for advanced English requirement (basic level)
        if any(keyword in all_text_lower for keyword in ['english c1', 'english c2', 'fluent english', 'advanced english']):
            bonus_score -= 15
        
        # Calculate final score (capped at 100)
        final_score = min(100, max(0, base_score + bonus_score))
        
        # Determine recommendation level
        if final_score >= 80:
            recommendation = "ALTAMENTE RECOMENDADA"
            recommendation_level = "high"
        elif final_score >= 60:
            recommendation = "RECOMENDADA"
            recommendation_level = "medium"
        elif final_score >= 40:
            recommendation = "CONSIDERAR"
            recommendation_level = "low"
        else:
            recommendation = "REVISAR REQUERIMIENTOS"
            recommendation_level = "very_low"
        
        # Generate detailed breakdown
        skills_breakdown = {
            'matched_skills': matched_skills,
            'match_percentage': int((matches / total_keywords) * 100) if total_keywords > 0 else 0,
            'total_profile_keywords': total_keywords,
            'matched_count': matches
        }
        
        return {
            'global_score': final_score,
            'base_score': base_score,
            'bonus_score': bonus_score,
            'recommendation': recommendation,
            'recommendation_level': recommendation_level,
            'skills_breakdown': skills_breakdown,
            'requirements_count': len(requirements)
        }
