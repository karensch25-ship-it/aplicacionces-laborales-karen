"""
Advanced Scoring Engine - Multi-dimensional Job Match Analysis
Implements comprehensive scoring across 5 dimensions for transparent job matching
"""

from typing import List, Dict, Set, Tuple
import re
from collections import defaultdict


class AdvancedScoringEngine:
    """
    Advanced multi-dimensional scoring system for job matching
    
    Evaluates candidates across 5 dimensions:
    1. Technical Skills Match (30%)
    2. Experience Depth & Relevance (25%)
    3. Domain Knowledge (20%)
    4. Soft Skills & Cultural Fit (15%)
    5. Achievement Quality (10%)
    """
    
    def __init__(self):
        """Initialize scoring engine with keyword mappings and weights"""
        
        # Dimension weights
        self.dimension_weights = {
            'technical_skills': 0.30,
            'experience_depth': 0.25,
            'domain_knowledge': 0.20,
            'soft_skills': 0.15,
            'achievement_quality': 0.10
        }
        
        # Technical keywords with importance weights
        self.technical_keywords = {
            # Core data skills - high weight
            'sql': 1.5,
            'python': 1.5,
            'power bi': 1.5,
            'tableau': 1.5,
            'etl': 1.5,
            
            # BI and analytics - high weight
            'dashboard': 1.4,
            'bi': 1.4,
            'business intelligence': 1.4,
            'data visualization': 1.4,
            'analytics': 1.3,
            
            # Data processing - medium weight
            'data integration': 1.2,
            'data pipeline': 1.2,
            'data quality': 1.2,
            'data governance': 1.2,
            'automation': 1.2,
            
            # Tools and platforms - medium weight
            'api': 1.0,
            'excel': 1.0,
            'thoughtspot': 1.0,
            'sap': 1.0,
            
            # Nice-to-have - lower weight
            'zapier': 0.8,
            'low-code': 0.7,
            'ai tools': 0.8,
            'openai': 0.7,
        }
        
        # Synonyms for better matching
        self.technical_synonyms = {
            'bi': ['business intelligence', 'analytics', 'reporting'],
            'etl': ['extract transform load', 'data pipeline', 'data integration'],
            'dashboard': ['dashboards', 'reporting', 'visualization'],
            'sql': ['database', 'query', 'stored procedure'],
            'automation': ['automate', 'automated', 'automating'],
            'api': ['apis', 'integration', 'connector'],
        }
        
        # Domain knowledge keywords
        self.domain_keywords = {
            # Business domains
            'healthcare': ['healthcare', 'medical', 'pharmaceutical', 'clinical'],
            'e-commerce': ['e-commerce', 'ecommerce', 'retail', 'sales'],
            'logistics': ['logistics', 'supply chain', 'inventory', 'tracking'],
            'finance': ['finance', 'financial', 'banking', 'accounting'],
            'technology': ['technology', 'tech', 'software', 'saas'],
            
            # Functional domains
            'bi_reporting': ['business intelligence', 'reporting', 'dashboard', 'kpi'],
            'data_governance': ['data governance', 'data quality', 'compliance', 'audit'],
            'analytics': ['analytics', 'analysis', 'insights', 'metrics'],
            'operations': ['operations', 'operational', 'process optimization'],
        }
        
        # Soft skills keywords
        self.soft_skills_keywords = {
            'stakeholder': ['stakeholder', 'client', 'customer', 'user'],
            'collaboration': ['collaboration', 'collaborate', 'cross-functional', 'team'],
            'communication': ['communication', 'communicate', 'present', 'presentation'],
            'training': ['training', 'train', 'mentor', 'teach'],
            'leadership': ['leadership', 'lead', 'manage', 'coordinate'],
            'problem-solving': ['problem', 'solution', 'troubleshoot', 'resolve'],
            'autonomy': ['autonomous', 'self-directed', 'independent', 'initiative'],
        }
        
        # Antonio's profile - hardcoded for now, could be loaded from config
        self.candidate_profile = {
            'years_experience': 5,
            'technical_skills': [
                'sql', 'python', 'power bi', 'thoughtspot', 'excel', 'sap',
                'etl', 'dashboard', 'automation', 'data integration', 'api',
                'data quality', 'data governance', 'business intelligence'
            ],
            'achievements': [
                {
                    'description': "Architected consolidated dashboard integrating 8 data sources, cutting data preparation time by 70%",
                    'keywords': ['dashboard', 'data integration', 'automation'],
                    'metrics': ['70%', '8'],
                    'quality': 'high'
                },
                {
                    'description': "Built 20+ SQL stored procedures, improving query performance by 40% and reducing error rates by 75%",
                    'keywords': ['sql', 'performance', 'automation'],
                    'metrics': ['40%', '75%', '20+'],
                    'quality': 'high'
                },
                {
                    'description': "Developed 15+ automated reports using M-AT and NPR, reducing manual reporting time by 60% for 200+ healthcare professionals",
                    'keywords': ['automation', 'reporting', 'healthcare'],
                    'metrics': ['60%', '15+', '200+'],
                    'quality': 'high'
                },
                {
                    'description': "Automated ETL processes, reducing daily processing time from 4 hours to 30 minutes",
                    'keywords': ['etl', 'automation', 'performance'],
                    'metrics': ['4 hours to 30 minutes'],
                    'quality': 'high'
                },
                {
                    'description': "Led system transition and trained 15 users, establishing data governance protocols and improving accuracy by 85%",
                    'keywords': ['training', 'data governance', 'leadership'],
                    'metrics': ['85%', '15'],
                    'quality': 'high'
                },
                {
                    'description': "Maintained 98% client satisfaction while managing 50+ regular clients",
                    'keywords': ['stakeholder', 'collaboration'],
                    'metrics': ['98%', '50+'],
                    'quality': 'high'
                },
            ],
            'domains': ['healthcare', 'e-commerce', 'logistics', 'technology'],
            'soft_skills': ['stakeholder', 'collaboration', 'training', 'leadership', 'communication']
        }
    
    def extract_keywords_from_text(self, text: str, keyword_dict: Dict) -> Set[str]:
        """
        Extract keywords from text using dictionary and synonyms
        
        Args:
            text: Text to analyze
            keyword_dict: Dictionary of keywords to search for
            
        Returns:
            Set of matched keywords
        """
        if not text:
            return set()
        
        text_lower = str(text).lower()
        matched = set()
        
        for keyword in keyword_dict.keys():
            # Direct match
            if keyword in text_lower:
                matched.add(keyword)
            
            # Synonym match (for technical keywords)
            if keyword in self.technical_synonyms:
                for synonym in self.technical_synonyms[keyword]:
                    if synonym in text_lower:
                        matched.add(keyword)
                        break
        
        return matched
    
    def calculate_technical_skills_score(self, requirements: List) -> Dict:
        """
        Dimension 1: Technical Skills Match (30% weight)
        
        Calculates match between required technical skills and candidate's skills
        
        Returns:
            {
                'score': 0-100,
                'matched_skills': [...],
                'missing_skills': [...],
                'details': {...}
            }
        """
        required_skills = set()
        matched_skills = set()
        
        # Extract technical keywords from requirements
        for req in requirements:
            if not req:
                continue
            req_str = str(req) if not isinstance(req, str) else req
            if req_str.strip().lower() == 'none':
                continue
            
            req_keywords = self.extract_keywords_from_text(req_str, self.technical_keywords)
            required_skills.update(req_keywords)
        
        # Check which required skills the candidate has
        candidate_skills = set(self.candidate_profile['technical_skills'])
        matched_skills = required_skills.intersection(candidate_skills)
        missing_skills = required_skills - matched_skills
        
        # Calculate weighted score
        if not required_skills:
            score = 100  # No technical requirements = perfect match
        else:
            # Weight by importance
            total_weight = sum(self.technical_keywords.get(skill, 1.0) for skill in required_skills)
            matched_weight = sum(self.technical_keywords.get(skill, 1.0) for skill in matched_skills)
            score = (matched_weight / total_weight) * 100 if total_weight > 0 else 0
        
        return {
            'score': round(score, 1),
            'matched_skills': list(matched_skills),
            'missing_skills': list(missing_skills),
            'required_skills_count': len(required_skills),
            'matched_skills_count': len(matched_skills),
            'level': self._get_level(score),
            'details': f"{len(matched_skills)}/{len(required_skills)} technical skills matched"
        }
    
    def calculate_experience_depth_score(self, requirements: List, job_description: str) -> Dict:
        """
        Dimension 2: Experience Depth & Relevance (25% weight)
        
        Evaluates years of experience, responsibility level, and impact
        
        Returns:
            {
                'score': 0-100,
                'years_score': 0-100,
                'responsibility_score': 0-100,
                'impact_score': 0-100,
                'details': {...}
            }
        """
        # Years of experience score (40% of dimension)
        # 5+ years = 100%, 3-4 years = 80%, 2 years = 60%, <2 years = 40%
        years = self.candidate_profile['years_experience']
        if years >= 5:
            years_score = 100
        elif years >= 3:
            years_score = 80
        elif years >= 2:
            years_score = 60
        else:
            years_score = 40
        
        # Responsibility level score (30% of dimension)
        # Check for leadership indicators in requirements
        req_text = ' '.join([str(r) for r in requirements if r])
        desc_text = str(job_description) if job_description else ''
        combined_text = req_text + ' ' + desc_text
        
        leadership_indicators = ['lead', 'manage', 'senior', 'principal', 'architect']
        has_leadership_req = any(ind in combined_text.lower() for ind in leadership_indicators)
        
        # Antonio has some leadership (trained 15 users, led transition)
        if has_leadership_req:
            responsibility_score = 70  # Has some leadership, not full manager
        else:
            responsibility_score = 90  # Individual contributor role, good fit
        
        # Impact score (30% of dimension)
        # Based on number of achievements with quantifiable impact
        achievements_with_metrics = [a for a in self.candidate_profile['achievements'] 
                                     if a.get('metrics') and len(a['metrics']) > 0]
        impact_score = min(100, (len(achievements_with_metrics) / 5) * 100)  # 5+ = 100%
        
        # Combined score
        score = (years_score * 0.4 + responsibility_score * 0.3 + impact_score * 0.3)
        
        return {
            'score': round(score, 1),
            'years_score': years_score,
            'responsibility_score': responsibility_score,
            'impact_score': round(impact_score, 1),
            'years_experience': years,
            'achievements_count': len(achievements_with_metrics),
            'level': self._get_level(score),
            'details': f"{years}+ years with {len(achievements_with_metrics)} quantifiable achievements"
        }
    
    def calculate_domain_knowledge_score(self, requirements: List, job_description: str) -> Dict:
        """
        Dimension 3: Domain Knowledge (20% weight)
        
        Evaluates familiarity with business domain and functional areas
        
        Returns:
            {
                'score': 0-100,
                'matched_domains': [...],
                'details': {...}
            }
        """
        # Extract domain keywords from requirements and description
        combined_text = ' '.join([str(r) for r in requirements if r])
        if job_description:
            combined_text += ' ' + str(job_description)
        
        required_domains = set()
        matched_domains = set()
        
        # Check each domain category
        for domain_category, domain_keywords in self.domain_keywords.items():
            for keyword in domain_keywords:
                if keyword in combined_text.lower():
                    required_domains.add(domain_category)
                    
                    # Check if candidate has experience in this domain
                    # Check both explicit domains and achievement keywords
                    if domain_category in self.candidate_profile['domains']:
                        matched_domains.add(domain_category)
                    else:
                        # Check if any achievements mention this domain
                        for achievement in self.candidate_profile['achievements']:
                            if keyword in achievement['description'].lower():
                                matched_domains.add(domain_category)
                                break
                    break
        
        # Calculate score
        if not required_domains:
            score = 80  # No specific domain requirements = good general fit
        else:
            score = (len(matched_domains) / len(required_domains)) * 100
        
        return {
            'score': round(score, 1),
            'matched_domains': list(matched_domains),
            'required_domains': list(required_domains),
            'matched_count': len(matched_domains),
            'required_count': len(required_domains),
            'level': self._get_level(score),
            'details': f"{len(matched_domains)}/{len(required_domains)} domain areas matched"
        }
    
    def calculate_soft_skills_score(self, requirements: List, job_description: str) -> Dict:
        """
        Dimension 4: Soft Skills & Cultural Fit (15% weight)
        
        Evaluates collaboration, communication, and interpersonal skills
        
        Returns:
            {
                'score': 0-100,
                'matched_skills': [...],
                'details': {...}
            }
        """
        # Extract soft skill keywords from requirements
        combined_text = ' '.join([str(r) for r in requirements if r])
        if job_description:
            combined_text += ' ' + str(job_description)
        
        required_soft_skills = set()
        matched_soft_skills = set()
        
        for skill_category, skill_keywords in self.soft_skills_keywords.items():
            for keyword in skill_keywords:
                if keyword in combined_text.lower():
                    required_soft_skills.add(skill_category)
                    
                    # Check if candidate demonstrates this soft skill
                    if skill_category in self.candidate_profile['soft_skills']:
                        matched_soft_skills.add(skill_category)
                    else:
                        # Check achievements for evidence
                        for achievement in self.candidate_profile['achievements']:
                            if any(kw in achievement['description'].lower() for kw in skill_keywords):
                                matched_soft_skills.add(skill_category)
                                break
                    break
        
        # Calculate score
        if not required_soft_skills:
            score = 75  # No specific soft skill requirements = assume moderate fit
        else:
            score = (len(matched_soft_skills) / len(required_soft_skills)) * 100
        
        return {
            'score': round(score, 1),
            'matched_skills': list(matched_soft_skills),
            'required_skills': list(required_soft_skills),
            'matched_count': len(matched_soft_skills),
            'required_count': len(required_soft_skills),
            'level': self._get_level(score),
            'details': f"{len(matched_soft_skills)}/{len(required_soft_skills)} soft skills demonstrated"
        }
    
    def calculate_achievement_quality_score(self, requirements: List) -> Dict:
        """
        Dimension 5: Achievement Quality (10% weight)
        
        Evaluates quality of evidence mapped to requirements
        
        Returns:
            {
                'score': 0-100,
                'high_quality_matches': int,
                'details': {...}
            }
        """
        # Analyze each requirement to see quality of mapping
        high_quality = 0
        medium_quality = 0
        low_quality = 0
        total_reqs = 0
        
        for req in requirements:
            if not req:
                continue
            req_str = str(req) if not isinstance(req, str) else req
            if req_str.strip().lower() == 'none':
                continue
            
            total_reqs += 1
            
            # Extract keywords from requirement
            req_keywords = self.extract_keywords_from_text(req_str, self.technical_keywords)
            
            # Find matching achievements
            matching_achievements = []
            for achievement in self.candidate_profile['achievements']:
                achievement_keywords = set(achievement['keywords'])
                if req_keywords.intersection(achievement_keywords):
                    matching_achievements.append(achievement)
            
            # Determine quality based on match and metrics
            if matching_achievements:
                # Check quality of best match
                best_match = matching_achievements[0]
                if best_match.get('quality') == 'high' and len(best_match.get('metrics', [])) >= 1:
                    high_quality += 1
                elif best_match.get('metrics'):
                    medium_quality += 1
                else:
                    low_quality += 1
            else:
                low_quality += 1
        
        # Calculate score
        if total_reqs == 0:
            score = 0
        else:
            score = ((high_quality * 1.0 + medium_quality * 0.6 + low_quality * 0.2) / total_reqs) * 100
        
        return {
            'score': round(score, 1),
            'high_quality_matches': high_quality,
            'medium_quality_matches': medium_quality,
            'low_quality_matches': low_quality,
            'total_requirements': total_reqs,
            'level': self._get_level(score),
            'details': f"{high_quality} high-quality achievements mapped to {total_reqs} requirements"
        }
    
    def _get_level(self, score: float) -> str:
        """Convert numeric score to level description"""
        if score >= 85:
            return "Excellent"
        elif score >= 70:
            return "Strong"
        elif score >= 55:
            return "Good"
        elif score >= 40:
            return "Moderate"
        else:
            return "Weak"
    
    def _get_recommendation(self, global_score: float) -> Tuple[str, str]:
        """
        Get recommendation based on global score
        
        Returns:
            (recommendation_level, recommendation_text)
        """
        if global_score >= 85:
            return ("EXCELLENT FIT", "Apply with high confidence. This is an exceptional match.")
        elif global_score >= 70:
            return ("STRONG FIT", "Apply with confidence. Emphasize your key strengths.")
        elif global_score >= 55:
            return ("GOOD FIT", "Apply and address potential gaps in your cover letter.")
        elif global_score >= 40:
            return ("MODERATE FIT", "Consider carefully. Highlight transferable skills.")
        else:
            return ("WEAK FIT", "Not recommended unless there's a strategic reason.")
    
    def identify_strengths_and_gaps(self, requirements: List, 
                                    dimension_scores: Dict) -> Dict:
        """
        Identify top strengths and key gaps
        
        Returns:
            {
                'strengths': [...],
                'gaps': [...],
                'recommendations': [...]
            }
        """
        strengths = []
        gaps = []
        recommendations = []
        
        # Analyze technical skills
        tech_score = dimension_scores['technical_skills']
        if tech_score['score'] >= 80:
            strengths.append({
                'area': 'Technical Skills',
                'description': f"Strong match in {len(tech_score['matched_skills'])} key technical areas",
                'evidence': ', '.join(tech_score['matched_skills'][:3])
            })
        
        if tech_score['missing_skills']:
            for skill in tech_score['missing_skills'][:2]:  # Top 2 gaps
                gaps.append({
                    'area': 'Technical Skills',
                    'skill': skill,
                    'impact': 'Medium' if self.technical_keywords.get(skill, 1.0) > 1.0 else 'Low',
                    'mitigation': self._get_mitigation_strategy(skill)
                })
        
        # Analyze experience
        exp_score = dimension_scores['experience_depth']
        if exp_score['score'] >= 70:
            strengths.append({
                'area': 'Experience',
                'description': f"{exp_score['years_experience']}+ years with proven track record",
                'evidence': f"{exp_score['achievements_count']} quantifiable achievements"
            })
        
        # Analyze domain knowledge
        domain_score = dimension_scores['domain_knowledge']
        if domain_score['matched_domains']:
            strengths.append({
                'area': 'Domain Knowledge',
                'description': "Relevant industry experience",
                'evidence': ', '.join(domain_score['matched_domains'])
            })
        
        # Generate recommendations
        if dimension_scores['technical_skills']['score'] < 70:
            recommendations.append({
                'priority': 'High',
                'action': 'Review missing technical skills before applying',
                'details': f"Focus on: {', '.join(tech_score['missing_skills'][:2])}"
            })
        
        if dimension_scores['achievement_quality']['score'] < 60:
            recommendations.append({
                'priority': 'Medium',
                'action': 'Strengthen your achievement examples',
                'details': 'Add more quantifiable metrics to your experience'
            })
        
        # Always include application prep recommendation
        recommendations.append({
            'priority': 'High',
            'action': 'Prepare specific examples',
            'details': f"Ready 2-3 stories highlighting: {', '.join(tech_score['matched_skills'][:3])}"
        })
        
        return {
            'strengths': strengths[:5],  # Top 5
            'gaps': gaps[:3],  # Top 3
            'recommendations': recommendations[:5]  # Top 5
        }
    
    def _get_mitigation_strategy(self, skill: str) -> str:
        """Get mitigation strategy for missing skill"""
        strategies = {
            'zapier': 'Highlight experience with similar automation tools. Zapier is intuitive for technical users.',
            'ai tools': 'Emphasize adaptability and quick learning. Consider completing OpenAI API tutorial.',
            'openai': 'Review OpenAI documentation and API basics (2-3 hours prep time).',
            'tableau': 'Emphasize Power BI and Thoughtspot expertise. Visualization principles transfer well.',
            'python': 'Highlight SQL and data analysis skills. Many tasks are achievable with existing skills.',
        }
        
        return strategies.get(skill, f'Highlight transferable skills and willingness to learn {skill}.')
    
    def calculate_comprehensive_score(self, requirements: List, 
                                     job_description: str = "", 
                                     job_title: str = "") -> Dict:
        """
        Calculate complete multi-dimensional match score
        
        Args:
            requirements: List of job requirements
            job_description: Job description text
            job_title: Job title
            
        Returns:
            Complete scoring report with all dimensions and recommendations
        """
        # Calculate each dimension
        dimension_scores = {
            'technical_skills': self.calculate_technical_skills_score(requirements),
            'experience_depth': self.calculate_experience_depth_score(requirements, job_description),
            'domain_knowledge': self.calculate_domain_knowledge_score(requirements, job_description),
            'soft_skills': self.calculate_soft_skills_score(requirements, job_description),
            'achievement_quality': self.calculate_achievement_quality_score(requirements)
        }
        
        # Calculate global score (weighted average)
        global_score = sum(
            dimension_scores[dim]['score'] * self.dimension_weights[dim]
            for dim in self.dimension_weights.keys()
        )
        
        # Get recommendation
        recommendation_level, recommendation_text = self._get_recommendation(global_score)
        
        # Identify strengths and gaps
        analysis = self.identify_strengths_and_gaps(requirements, dimension_scores)
        
        # Calculate detailed requirement matching
        requirement_analysis = self._analyze_requirements_detailed(requirements)
        
        return {
            'global_score': round(global_score, 1),
            'recommendation_level': recommendation_level,
            'recommendation_text': recommendation_text,
            'dimensions': dimension_scores,
            'dimension_contributions': {
                dim: round(dimension_scores[dim]['score'] * self.dimension_weights[dim], 1)
                for dim in self.dimension_weights.keys()
            },
            'strengths': analysis['strengths'],
            'gaps': analysis['gaps'],
            'actionable_recommendations': analysis['recommendations'],
            'requirement_details': requirement_analysis,
            'job_title': job_title
        }
    
    def _analyze_requirements_detailed(self, requirements: List) -> List[Dict]:
        """
        Analyze each requirement in detail
        
        Returns:
            List of requirement analyses
        """
        analyses = []
        
        for req in requirements:
            if not req:
                continue
            req_str = str(req) if not isinstance(req, str) else req
            if req_str.strip().lower() == 'none':
                continue
            
            # Extract keywords
            tech_keywords = self.extract_keywords_from_text(req_str, self.technical_keywords)
            
            # Find matching achievements
            matching_achievements = []
            for achievement in self.candidate_profile['achievements']:
                achievement_keywords = set(achievement['keywords'])
                if tech_keywords.intersection(achievement_keywords):
                    matching_achievements.append(achievement['description'])
            
            # Determine match level
            if len(tech_keywords) >= 2 and matching_achievements:
                match_level = "Strong"
                icon = "🟢"
            elif len(tech_keywords) >= 1 and matching_achievements:
                match_level = "Moderate"
                icon = "🟡"
            else:
                match_level = "Weak"
                icon = "🟠"
            
            evidence = matching_achievements[0] if matching_achievements else "No direct evidence, transferable skills applicable"
            
            analyses.append({
                'requirement': req_str,
                'match_level': match_level,
                'icon': icon,
                'evidence': evidence,
                'keywords_matched': list(tech_keywords)
            })
        
        return analyses


# Convenience function for backward compatibility
def calculate_match_score(requirements: List, job_description: str = "", job_title: str = "") -> Dict:
    """
    Convenience wrapper for advanced scoring
    
    Args:
        requirements: List of job requirements
        job_description: Optional job description
        job_title: Optional job title
        
    Returns:
        Complete scoring analysis
    """
    engine = AdvancedScoringEngine()
    return engine.calculate_comprehensive_score(requirements, job_description, job_title)


# Example usage and testing
if __name__ == "__main__":
    # Test with sample requirements
    sample_reqs = [
        "Build and maintain custom dashboards to support business operations",
        "Clean, transform, and analyze data from multiple systems",
        "Create and manage lightweight integrations between tools using Zapier, APIs, or low-code platforms",
        "Work with internal teams to understand reporting and automation needs",
        "Leverage AI tools (e.g., OpenAI APIs, AI-based automations) to improve workflows",
        "Collaborate with stakeholders to continuously refine reports and processes",
        "Ensure accuracy, consistency, and usability of data across tools"
    ]
    
    sample_description = """
    We're looking for an Integration and Business Intelligence Specialist who can 
    drive insights through clean, well-structured data while building automations 
    and exploring light AI implementations.
    """
    
    engine = AdvancedScoringEngine()
    result = engine.calculate_comprehensive_score(
        sample_reqs, 
        sample_description, 
        "Data & Automation (BI) Analyst"
    )
    
    print("=" * 80)
    print("ADVANCED SCORING ENGINE - TEST RESULTS")
    print("=" * 80)
    print(f"\nGlobal Score: {result['global_score']}%")
    print(f"Recommendation: {result['recommendation_level']}")
    print(f"Message: {result['recommendation_text']}")
    
    print("\n" + "=" * 80)
    print("DIMENSIONAL BREAKDOWN")
    print("=" * 80)
    
    for dim_name, dim_data in result['dimensions'].items():
        contribution = result['dimension_contributions'][dim_name]
        print(f"\n{dim_name.replace('_', ' ').title()}: {dim_data['score']}% ({dim_data['level']})")
        print(f"  Contribution to global score: {contribution}%")
        print(f"  {dim_data['details']}")
    
    print("\n" + "=" * 80)
    print("STRENGTHS")
    print("=" * 80)
    for strength in result['strengths']:
        print(f"\n✅ {strength['area']}: {strength['description']}")
        print(f"   Evidence: {strength['evidence']}")
    
    print("\n" + "=" * 80)
    print("GAPS & MITIGATION")
    print("=" * 80)
    for gap in result['gaps']:
        print(f"\n⚠️  {gap['area']}: {gap['skill']} (Impact: {gap['impact']})")
        print(f"   Mitigation: {gap['mitigation']}")
    
    print("\n" + "=" * 80)
    print("ACTIONABLE RECOMMENDATIONS")
    print("=" * 80)
    for i, rec in enumerate(result['actionable_recommendations'], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['action']}")
        print(f"   {rec['details']}")
    
    print("\n" + "=" * 80)
    print("DETAILED REQUIREMENT ANALYSIS")
    print("=" * 80)
    for req_detail in result['requirement_details']:
        print(f"\n{req_detail['icon']} {req_detail['match_level']}: {req_detail['requirement'][:60]}...")
        print(f"   Evidence: {req_detail['evidence'][:80]}...")
    
    print("\n" + "=" * 80)
