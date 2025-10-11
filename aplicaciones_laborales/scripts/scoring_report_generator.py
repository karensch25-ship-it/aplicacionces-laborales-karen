"""
Scoring Report Generator - Creates comprehensive match analysis reports
Generates detailed markdown reports from scoring engine results
"""

from typing import Dict
from datetime import datetime


class ScoringReportGenerator:
    """
    Generates detailed scoring reports in markdown format
    """
    
    def __init__(self):
        """Initialize report generator"""
        self.candidate_name = "Antonio Gutierrez Amaranto"
    
    def _get_score_emoji(self, score: float) -> str:
        """Get emoji for score level"""
        if score >= 85:
            return "🟢"
        elif score >= 70:
            return "🟢"
        elif score >= 55:
            return "🟡"
        elif score >= 40:
            return "🟠"
        else:
            return "🔴"
    
    def _format_percentage_bar(self, score: float) -> str:
        """Create a visual percentage bar"""
        filled = int(score / 10)
        empty = 10 - filled
        return "█" * filled + "░" * empty
    
    def generate_report(self, scoring_result: Dict, job_title: str, 
                       company: str, date: str) -> str:
        """
        Generate complete scoring report in markdown format
        
        Args:
            scoring_result: Output from AdvancedScoringEngine
            job_title: Job title
            company: Company name
            date: Application date
            
        Returns:
            Markdown formatted report
        """
        report = []
        
        # Header
        report.append("# Job Match Scoring Report")
        report.append("")
        report.append(f"**Candidate:** {self.candidate_name}")
        report.append(f"**Position:** {job_title}")
        report.append(f"**Company:** {company}")
        report.append(f"**Date:** {date}")
        report.append(f"**Report Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        report.append("---")
        report.append("")
        
        # Overall Score
        global_score = scoring_result['global_score']
        recommendation = scoring_result['recommendation_level']
        emoji = self._get_score_emoji(global_score)
        
        report.append(f"## Overall Match Score: {global_score}% - {recommendation} {emoji}")
        report.append("")
        report.append(f"**{self._format_percentage_bar(global_score)}** `{global_score}%`")
        report.append("")
        
        # Recommendation
        report.append("### Recommendation")
        report.append(f"**{recommendation}**")
        report.append("")
        report.append(scoring_result['recommendation_text'])
        report.append("")
        report.append("---")
        report.append("")
        
        # Dimensional Analysis
        report.append("## Dimensional Analysis")
        report.append("")
        
        dimensions = scoring_result['dimensions']
        contributions = scoring_result['dimension_contributions']
        
        dimension_names = {
            'technical_skills': '1. Technical Skills Match',
            'experience_depth': '2. Experience Depth & Relevance',
            'domain_knowledge': '3. Domain Knowledge',
            'soft_skills': '4. Soft Skills & Cultural Fit',
            'achievement_quality': '5. Achievement Quality'
        }
        
        dimension_weights = {
            'technical_skills': '30%',
            'experience_depth': '25%',
            'domain_knowledge': '20%',
            'soft_skills': '15%',
            'achievement_quality': '10%'
        }
        
        for dim_key, dim_name in dimension_names.items():
            dim_data = dimensions[dim_key]
            score = dim_data['score']
            level = dim_data['level']
            contribution = contributions[dim_key]
            weight = dimension_weights[dim_key]
            emoji = self._get_score_emoji(score)
            
            report.append(f"### {dim_name}: {score}% {emoji}")
            report.append(f"**Weight:** {weight} | **Contribution to Global Score:** {contribution}%")
            report.append("")
            report.append(f"**{self._format_percentage_bar(score)}** `{score}%` - {level}")
            report.append("")
            report.append(f"**Analysis:** {dim_data['details']}")
            report.append("")
            
            # Add dimension-specific details
            if dim_key == 'technical_skills':
                if dim_data['matched_skills']:
                    report.append("✅ **Matched Skills:**")
                    for skill in dim_data['matched_skills']:
                        report.append(f"- {skill}")
                    report.append("")
                
                if dim_data['missing_skills']:
                    report.append("⚠️ **Missing Skills:**")
                    for skill in dim_data['missing_skills']:
                        report.append(f"- {skill}")
                    report.append("")
            
            elif dim_key == 'experience_depth':
                report.append(f"- **Years of Experience:** {dim_data['years_experience']}+ years")
                report.append(f"- **Quantifiable Achievements:** {dim_data['achievements_count']}")
                report.append(f"- **Years Score:** {dim_data['years_score']}%")
                report.append(f"- **Responsibility Level:** {dim_data['responsibility_score']}%")
                report.append(f"- **Impact Score:** {dim_data['impact_score']}%")
                report.append("")
            
            elif dim_key == 'domain_knowledge':
                if dim_data['matched_domains']:
                    report.append("✅ **Relevant Domains:**")
                    for domain in dim_data['matched_domains']:
                        report.append(f"- {domain.replace('_', ' ').title()}")
                    report.append("")
            
            elif dim_key == 'soft_skills':
                if dim_data['matched_skills']:
                    report.append("✅ **Demonstrated Soft Skills:**")
                    for skill in dim_data['matched_skills']:
                        report.append(f"- {skill.replace('_', ' ').title()}")
                    report.append("")
            
            elif dim_key == 'achievement_quality':
                report.append(f"- **High Quality Matches:** {dim_data['high_quality_matches']}")
                report.append(f"- **Medium Quality Matches:** {dim_data['medium_quality_matches']}")
                report.append(f"- **Low Quality Matches:** {dim_data['low_quality_matches']}")
                report.append(f"- **Total Requirements:** {dim_data['total_requirements']}")
                report.append("")
            
            report.append("---")
            report.append("")
        
        # Strengths
        if scoring_result['strengths']:
            report.append("## Key Strengths for This Role")
            report.append("")
            
            for i, strength in enumerate(scoring_result['strengths'], 1):
                report.append(f"### {i}. {strength['area']}")
                report.append("")
                report.append(f"**{strength['description']}**")
                report.append("")
                report.append(f"*Evidence:* {strength['evidence']}")
                report.append("")
            
            report.append("---")
            report.append("")
        
        # Gaps and Mitigation
        if scoring_result['gaps']:
            report.append("## Gaps & Mitigation Strategies")
            report.append("")
            
            for gap in scoring_result['gaps']:
                impact_emoji = "🟡" if gap['impact'] == 'Medium' else "🟢" if gap['impact'] == 'Low' else "🔴"
                report.append(f"### {impact_emoji} Gap: {gap['skill'].title()}")
                report.append(f"**Area:** {gap['area']} | **Impact:** {gap['impact']}")
                report.append("")
                report.append(f"**Mitigation Strategy:** {gap['mitigation']}")
                report.append("")
            
            report.append("---")
            report.append("")
        
        # Actionable Recommendations
        report.append("## Actionable Recommendations")
        report.append("")
        
        for i, rec in enumerate(scoring_result['actionable_recommendations'], 1):
            priority_emoji = "🔴" if rec['priority'] == 'High' else "🟡"
            report.append(f"### {i}. {priority_emoji} [{rec['priority']} Priority] {rec['action']}")
            report.append("")
            report.append(rec['details'])
            report.append("")
        
        report.append("---")
        report.append("")
        
        # Detailed Requirement Matching
        report.append("## Detailed Requirement Matching")
        report.append("")
        report.append("| Match Level | Requirement | Evidence |")
        report.append("|------------|------------|----------|")
        
        for req in scoring_result['requirement_details']:
            req_text = req['requirement'][:50] + "..." if len(req['requirement']) > 50 else req['requirement']
            evidence = req['evidence'][:60] + "..." if len(req['evidence']) > 60 else req['evidence']
            report.append(f"| {req['icon']} {req['match_level']} | {req_text} | {evidence} |")
        
        report.append("")
        report.append("---")
        report.append("")
        
        # Next Steps
        report.append("## Next Steps")
        report.append("")
        
        if global_score >= 70:
            report.append("### ✅ Recommended Actions:")
            report.append("")
            report.append("1. **Apply within 24-48 hours** - This is a strong match")
            report.append("2. **Preparation time:** 2-3 hours recommended")
            report.append("3. **Focus areas:** Review the strengths above and prepare specific examples")
            report.append("4. **Cover letter:** Emphasize key achievements that align with requirements")
        elif global_score >= 55:
            report.append("### 🟡 Recommended Actions:")
            report.append("")
            report.append("1. **Review gaps carefully** before applying")
            report.append("2. **Preparation time:** 3-4 hours recommended")
            report.append("3. **Cover letter strategy:** Address potential gaps proactively")
            report.append("4. **Highlight transferable skills** for missing requirements")
        else:
            report.append("### ⚠️ Consider Carefully:")
            report.append("")
            report.append("1. **Evaluate strategic fit** - Is this a growth opportunity?")
            report.append("2. **Preparation time:** 4-5 hours recommended")
            report.append("3. **Alternative approach:** Consider if there's a better-fit role")
            report.append("4. **If applying:** Focus heavily on transferable experience")
        
        report.append("")
        report.append("---")
        report.append("")
        
        # Footer
        report.append("## About This Report")
        report.append("")
        report.append("This report was generated automatically by the **Advanced CV Personalization & Scoring System**.")
        report.append("")
        report.append("**Scoring Methodology:**")
        report.append("- **Multi-dimensional analysis** across 5 key areas")
        report.append("- **Weighted scoring** based on importance of each dimension")
        report.append("- **Evidence-based matching** using candidate's actual achievements")
        report.append("- **Transparent calculation** with detailed breakdowns")
        report.append("")
        report.append("**Confidence Level:** This scoring is based on keyword matching and achievement mapping. ")
        report.append("Individual job requirements may vary, and human judgment should be used to complement this analysis.")
        report.append("")
        report.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M:%S')}*")
        report.append("")
        
        return "\n".join(report)
    
    def generate_summary_card(self, scoring_result: Dict, job_title: str, company: str) -> str:
        """
        Generate a brief summary card for quick reference
        
        Args:
            scoring_result: Output from AdvancedScoringEngine
            job_title: Job title
            company: Company name
            
        Returns:
            Brief markdown summary
        """
        global_score = scoring_result['global_score']
        recommendation = scoring_result['recommendation_level']
        emoji = self._get_score_emoji(global_score)
        
        summary = []
        summary.append("## Quick Match Summary")
        summary.append("")
        summary.append(f"**Position:** {job_title} @ {company}")
        summary.append(f"**Match Score:** {global_score}% {emoji}")
        summary.append(f"**Recommendation:** {recommendation}")
        summary.append("")
        summary.append("**Dimension Scores:**")
        
        for dim_key, dim_data in scoring_result['dimensions'].items():
            dim_name = dim_key.replace('_', ' ').title()
            score = dim_data['score']
            emoji = self._get_score_emoji(score)
            summary.append(f"- {dim_name}: {score}% {emoji}")
        
        summary.append("")
        summary.append(f"**Top Strength:** {scoring_result['strengths'][0]['area'] if scoring_result['strengths'] else 'N/A'}")
        summary.append(f"**Key Gap:** {scoring_result['gaps'][0]['skill'].title() if scoring_result['gaps'] else 'None identified'}")
        summary.append("")
        
        return "\n".join(summary)


# Convenience function
def generate_scoring_report(scoring_result: Dict, job_title: str, 
                           company: str, date: str) -> str:
    """
    Generate complete scoring report
    
    Args:
        scoring_result: Result from AdvancedScoringEngine.calculate_comprehensive_score()
        job_title: Job title
        company: Company name
        date: Application date (YYYY-MM-DD)
        
    Returns:
        Markdown formatted report
    """
    generator = ScoringReportGenerator()
    return generator.generate_report(scoring_result, job_title, company, date)


# Example usage
if __name__ == "__main__":
    # Mock scoring result for testing
    mock_result = {
        'global_score': 75.5,
        'recommendation_level': 'STRONG FIT',
        'recommendation_text': 'Apply with confidence. Emphasize your dashboard development and automation experience.',
        'dimensions': {
            'technical_skills': {
                'score': 85.0,
                'level': 'Excellent',
                'matched_skills': ['dashboard', 'sql', 'etl', 'automation'],
                'missing_skills': ['zapier'],
                'required_skills_count': 5,
                'matched_skills_count': 4,
                'details': '4/5 technical skills matched'
            },
            'experience_depth': {
                'score': 90.0,
                'level': 'Excellent',
                'years_score': 100,
                'responsibility_score': 90,
                'impact_score': 100,
                'years_experience': 5,
                'achievements_count': 6,
                'details': '5+ years with 6 quantifiable achievements'
            },
            'domain_knowledge': {
                'score': 75.0,
                'level': 'Strong',
                'matched_domains': ['bi_reporting', 'analytics'],
                'required_domains': ['bi_reporting', 'analytics', 'operations'],
                'matched_count': 2,
                'required_count': 3,
                'details': '2/3 domain areas matched'
            },
            'soft_skills': {
                'score': 70.0,
                'level': 'Strong',
                'matched_skills': ['stakeholder', 'collaboration'],
                'required_skills': ['stakeholder', 'collaboration', 'communication'],
                'matched_count': 2,
                'required_count': 3,
                'details': '2/3 soft skills demonstrated'
            },
            'achievement_quality': {
                'score': 75.0,
                'level': 'Strong',
                'high_quality_matches': 5,
                'medium_quality_matches': 2,
                'low_quality_matches': 1,
                'total_requirements': 8,
                'details': '5 high-quality achievements mapped'
            }
        },
        'dimension_contributions': {
            'technical_skills': 25.5,
            'experience_depth': 22.5,
            'domain_knowledge': 15.0,
            'soft_skills': 10.5,
            'achievement_quality': 7.5
        },
        'strengths': [
            {
                'area': 'Technical Skills',
                'description': 'Strong match in dashboard and automation',
                'evidence': 'dashboard, sql, etl, automation'
            },
            {
                'area': 'Experience',
                'description': '5+ years with proven track record',
                'evidence': '6 quantifiable achievements'
            }
        ],
        'gaps': [
            {
                'area': 'Technical Skills',
                'skill': 'zapier',
                'impact': 'Low',
                'mitigation': 'Highlight experience with similar automation tools. Zapier is intuitive for technical users.'
            }
        ],
        'actionable_recommendations': [
            {
                'priority': 'High',
                'action': 'Prepare specific examples',
                'details': 'Ready 2-3 stories highlighting: dashboard, automation, sql'
            },
            {
                'priority': 'Medium',
                'action': 'Review Zapier basics',
                'details': 'Spend 30 minutes reviewing Zapier documentation'
            }
        ],
        'requirement_details': [
            {
                'requirement': 'Build and maintain custom dashboards',
                'match_level': 'Strong',
                'icon': '🟢',
                'evidence': 'Architected consolidated dashboard integrating 8 data sources',
                'keywords_matched': ['dashboard']
            },
            {
                'requirement': 'Automate ETL processes',
                'match_level': 'Strong',
                'icon': '🟢',
                'evidence': 'Automated ETL processes, reducing processing time from 4 hours to 30 minutes',
                'keywords_matched': ['etl', 'automation']
            }
        ]
    }
    
    generator = ScoringReportGenerator()
    report = generator.generate_report(
        mock_result,
        "Data & Automation (BI) Analyst",
        "SAGAN",
        "2025-10-10"
    )
    
    print(report)
    print("\n" + "="*80 + "\n")
    
    summary = generator.generate_summary_card(
        mock_result,
        "Data & Automation (BI) Analyst",
        "SAGAN"
    )
    print(summary)
