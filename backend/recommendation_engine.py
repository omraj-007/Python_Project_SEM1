import numpy as np
from typing import List, Dict, Any, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import re

class RecommendationEngine:
    def __init__(self, data_processor):
        """
        Enhanced recommendation engine with improved matching algorithms
        """
        self.data_processor = data_processor
        self.internships = data_processor.get_all_internships()
        self.tfidf_vectorizer = None
        self.internship_vectors = None
        self._prepare_vectors()
        
        print(f"Recommendation engine initialized with {len(self.internships)} internships")
    
    def _prepare_vectors(self):
        """Prepare TF-IDF vectors for internship content"""
        try:
            # Create content strings for each internship
            internship_content = []
            for internship in self.internships:
                content = f"{internship['title']} {internship['company']} {internship['domain']} {' '.join(internship['skills'])}"
                internship_content.append(content.lower())
            
            # Create TF-IDF vectors
            self.tfidf_vectorizer = TfidfVectorizer(
                max_features=1000,
                stop_words='english',
                ngram_range=(1, 2)
            )
            
            self.internship_vectors = self.tfidf_vectorizer.fit_transform(internship_content)
            print(" TF-IDF vectors prepared successfully")
            
        except Exception as e:
            print(f"⚠️ Warning: Could not prepare TF-IDF vectors: {str(e)}")
            self.tfidf_vectorizer = None
            self.internship_vectors = None
    
    def get_recommendations(self, user_profile: Dict[str, Any], num_recommendations: int = 10) -> List[Dict[str, Any]]:
        """
        Get personalized internship recommendations
        
        Args:
            user_profile: {
                'skills': List[str],
                'education': str,
                'location_preference': str,
                'min_stipend': int,
                'preferred_domains': List[str] (optional)
            }
            num_recommendations: Number of recommendations to return
        """
        try:
            print(f"🔍 Generating recommendations for user profile: {user_profile}")
            
            # Get filtered internships based on hard constraints
            filtered_internships = self._apply_filters(user_profile)
            print(f"📊 {len(filtered_internships)} internships match basic criteria")
            
            if not filtered_internships:
                print("⚠️ No internships match the basic criteria")
                return []
            
            # Calculate match scores for filtered internships
            scored_internships = []
            for internship in filtered_internships:
                score = self._calculate_match_score(user_profile, internship)
                scored_internships.append({
                    **internship,
                    'match_score': score,
                    'match_percentage': min(100, int(score * 100))
                })
            
            # Sort by match score
            scored_internships.sort(key=lambda x: x['match_score'], reverse=True)
            
            # Return top recommendations
            recommendations = scored_internships[:num_recommendations]
            
            print(f"✅ Generated {len(recommendations)} recommendations")
            return recommendations
            
        except Exception as e:
            print(f"❌ Error generating recommendations: {str(e)}")
            return []
    
    def _apply_filters(self, user_profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply hard filters based on user preferences"""
        filtered = self.internships.copy()
        
        # Location filter
        location_pref = user_profile.get('location_preference', '').lower()
        if location_pref and location_pref != 'any':
            if location_pref == 'work from home':
                filtered = [i for i in filtered if i['work_mode'] == 'Remote']
            else:
                filtered = [i for i in filtered if 
                          location_pref in i['location'].lower() or i['work_mode'] == 'Remote']
        
        # Stipend filter
        min_stipend = user_profile.get('min_stipend', 0)
        if min_stipend > 0:
            filtered = [i for i in filtered if i['stipend_amount'] >= min_stipend]
        
        return filtered
    
    def _calculate_match_score(self, user_profile: Dict[str, Any], internship: Dict[str, Any]) -> float:
        """Calculate comprehensive match score between user and internship"""
        total_score = 0.0
        max_score = 0.0
        
        # 1. Skills matching (40% weight)
        skills_score = self._calculate_skills_match(user_profile.get('skills', []), internship['skills'])
        total_score += skills_score * 0.4
        max_score += 0.4
        
        # 2. Education relevance (25% weight)
        education_score = self._calculate_education_match(user_profile.get('education', ''), internship)
        total_score += education_score * 0.25
        max_score += 0.25
        
        # 3. Location preference (15% weight)
        location_score = self._calculate_location_match(user_profile.get('location_preference', ''), internship)
        total_score += location_score * 0.15
        max_score += 0.15
        
        # 4. Stipend attractiveness (10% weight)
        stipend_score = self._calculate_stipend_score(user_profile.get('min_stipend', 0), internship['stipend_amount'])
        total_score += stipend_score * 0.1
        max_score += 0.1
        
        # 5. Company and role prestige (10% weight)
        prestige_score = self._calculate_prestige_score(internship)
        total_score += prestige_score * 0.1
        max_score += 0.1
        
        # Normalize score
        final_score = total_score / max_score if max_score > 0 else 0
        return min(1.0, final_score)
    
    def _calculate_skills_match(self, user_skills: List[str], internship_skills: List[str]) -> float:
        """Calculate skills matching score"""
        if not user_skills or not internship_skills:
            return 0.0
        
        user_skills_lower = [skill.lower() for skill in user_skills]
        internship_skills_lower = [skill.lower() for skill in internship_skills]
        
        # Direct matches
        direct_matches = len(set(user_skills_lower) & set(internship_skills_lower))
        
        # Partial matches (e.g., "Python" in "Python Development")
        partial_matches = 0
        for user_skill in user_skills_lower:
            for int_skill in internship_skills_lower:
                if user_skill in int_skill or int_skill in user_skill:
                    partial_matches += 0.5
        
        total_matches = direct_matches + partial_matches
        max_possible_matches = max(len(user_skills), len(internship_skills))
        
        return min(1.0, total_matches / max_possible_matches)
    
    def _calculate_education_match(self, user_education: str, internship: Dict[str, Any]) -> float:
        """Calculate education relevance score"""
        if not user_education:
            return 0.5  # Neutral score
        
        education_lower = user_education.lower()
        title_lower = internship['title'].lower()
        domain_lower = internship['domain'].lower()
        
        # Direct field matches
        field_matches = {
            'computer science': ['software', 'programming', 'development', 'tech', 'it', 'coding'],
            'information technology': ['software', 'programming', 'development', 'tech', 'it'],
            'business': ['business', 'management', 'sales', 'marketing', 'finance'],
            'design': ['design', 'ui', 'ux', 'graphic', 'creative'],
            'engineering': ['engineering', 'technical', 'development'],
            'marketing': ['marketing', 'digital', 'social', 'content'],
            'finance': ['finance', 'accounting', 'investment', 'banking']
        }
        
        for field, keywords in field_matches.items():
            if field in education_lower:
                for keyword in keywords:
                    if keyword in title_lower or keyword in domain_lower:
                        return 1.0
        
        return 0.6  # Decent match for other fields
    
    def _calculate_location_match(self, user_location_pref: str, internship: Dict[str, Any]) -> float:
        """Calculate location preference match"""
        if not user_location_pref or user_location_pref.lower() == 'any':
            return 1.0
        
        user_pref_lower = user_location_pref.lower()
        
        # Perfect match for remote preference
        if user_pref_lower == 'work from home' and internship['work_mode'] == 'Remote':
            return 1.0
        
        # Good match for city preference
        if user_pref_lower in internship['location'].lower():
            return 1.0
        
        # Remote is always an option
        if internship['work_mode'] == 'Remote':
            return 0.8
        
        return 0.3  # Different location
    
    def _calculate_stipend_score(self, user_min_stipend: int, internship_stipend: int) -> float:
        """Calculate stipend attractiveness score"""
        if user_min_stipend == 0:
            return 1.0 if internship_stipend > 0 else 0.5
        
        if internship_stipend < user_min_stipend:
            return 0.0
        
        # Higher stipend = higher score
        if internship_stipend >= user_min_stipend * 1.5:
            return 1.0
        elif internship_stipend >= user_min_stipend * 1.2:
            return 0.8
        else:
            return 0.6
    
    def _calculate_prestige_score(self, internship: Dict[str, Any]) -> float:
        """Calculate company and role prestige score"""
        company = internship['company'].lower()
        title = internship['title'].lower()
        
        # High-prestige indicators
        prestige_companies = ['google', 'microsoft', 'amazon', 'apple', 'facebook', 'netflix', 'uber']
        prestige_roles = ['machine learning', 'data scientist', 'software engineer', 'product manager']
        
        score = 0.5  # Base score
        
        # Company prestige
        for prestige_company in prestige_companies:
            if prestige_company in company:
                score += 0.3
                break
        
        # Role prestige
        for prestige_role in prestige_roles:
            if prestige_role in title:
                score += 0.2
                break
        
        # High stipend indicates prestige
        if internship['stipend_amount'] > 25000:
            score += 0.2
        elif internship['stipend_amount'] > 15000:
            score += 0.1
        
        return min(1.0, score)
    
    def get_similar_internships(self, internship_id: int, num_similar: int = 5) -> List[Dict[str, Any]]:
        """Get internships similar to a given internship"""
        try:
            target_internship = self.data_processor.get_internship_by_id(internship_id)
            if not target_internship:
                return []
            
            similar_internships = []
            
            for internship in self.internships:
                if internship['id'] == internship_id:
                    continue
                
                # Calculate similarity based on domain, skills, and company
                similarity = 0.0
                
                # Domain similarity
                if internship['domain'] == target_internship['domain']:
                    similarity += 0.4
                
                # Skills similarity
                common_skills = set(internship['skills']) & set(target_internship['skills'])
                skills_similarity = len(common_skills) / max(len(internship['skills']), len(target_internship['skills']))
                similarity += skills_similarity * 0.4
                
                # Location similarity
                if internship['work_mode'] == target_internship['work_mode']:
                    similarity += 0.2
                
                similar_internships.append({
                    **internship,
                    'similarity_score': similarity
                })
            
            # Sort by similarity
            similar_internships.sort(key=lambda x: x['similarity_score'], reverse=True)
            
            return similar_internships[:num_similar]
            
        except Exception as e:
            print(f"❌ Error finding similar internships: {str(e)}")
            return []
    
    def get_trending_internships(self, num_trending: int = 5) -> List[Dict[str, Any]]:
        """Get trending internships based on current market demand"""
        # Trending domains and skills
        trending_keywords = [
            'artificial intelligence', 'machine learning', 'data science',
            'python', 'react', 'node.js', 'cloud', 'devops', 'cybersecurity'
        ]
        
        trending_internships = []
        
        for internship in self.internships:
            trend_score = 0.0
            content = f"{internship['title']} {' '.join(internship['skills'])}".lower()
            
            for keyword in trending_keywords:
                if keyword in content:
                    trend_score += 1.0
            
            # Boost score for high-paying internships
            if internship['stipend_amount'] > 20000:
                trend_score += 0.5
            
            # Boost score for remote internships
            if internship['work_mode'] == 'Remote':
                trend_score += 0.3
            
            trending_internships.append({
                **internship,
                'trend_score': trend_score
            })
        
        # Sort by trend score
        trending_internships.sort(key=lambda x: x['trend_score'], reverse=True)
        
        return trending_internships[:num_trending]

# Test the recommendation engine
if __name__ == "__main__":
    from data_processor import DataProcessor
    
    processor = DataProcessor("../data/internship.csv")
    engine = RecommendationEngine(processor)
    
    # Test recommendations
    test_profile = {
        'skills': ['Python', 'Machine Learning', 'Data Science'],
        'education': 'Computer Science',
        'location_preference': 'Work From Home',
        'min_stipend': 20000
    }
    
    recommendations = engine.get_recommendations(test_profile)
    print(f"\n🎯 Top recommendations:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"{i}. {rec['title']} at {rec['company']} - Match: {rec['match_percentage']}%")