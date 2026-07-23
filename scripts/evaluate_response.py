#!/usr/bin/env python3
"""
RFP Response Quality Evaluation

Evaluate the quality of generated RFP responses using multiple metrics:
- Completeness: Are all required sections present?
- Relevance: How well does the response address customer requirements?
- Compliance: Does it address all compliance requirements?
- Clarity: Is the response clear and well-structured?
- Pricing Appropriateness: Is pricing competitive and justified?
- Overall Quality Score: Composite score (0-100)
"""

import json
import re
from typing import Dict, List, Tuple
from pathlib import Path
from argparse import ArgumentParser
from dataclasses import dataclass
from datetime import datetime


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class SectionScore:
    """Score for a single section"""
    section_name: str
    score: float  # 0-100
    max_score: float  # 0-100
    feedback: List[str]
    weight: float  # Importance weight (0-1)

    def weighted_score(self) -> float:
        """Return weighted score"""
        return (self.score / self.max_score) * 100 * self.weight if self.max_score > 0 else 0


@dataclass
class EvaluationResult:
    """Complete evaluation result"""
    timestamp: str
    rfp_filename: str
    response_filename: str
    
    # Section scores
    completeness_score: SectionScore
    relevance_score: SectionScore
    compliance_score: SectionScore
    clarity_score: SectionScore
    pricing_score: SectionScore
    
    # Overall
    overall_score: float  # 0-100
    recommendation: str  # "Excellent", "Good", "Acceptable", "Needs Improvement"
    strengths: List[str]
    weaknesses: List[str]
    improvements: List[str]

    def to_dict(self) -> dict:
        """Convert to dictionary"""
        return {
            "timestamp": self.timestamp,
            "rfp_file": self.rfp_filename,
            "response_file": self.response_filename,
            "sections": {
                "completeness": {
                    "score": self.completeness_score.score,
                    "max": self.completeness_score.max_score,
                    "weight": self.completeness_score.weight,
                    "feedback": self.completeness_score.feedback
                },
                "relevance": {
                    "score": self.relevance_score.score,
                    "max": self.relevance_score.max_score,
                    "weight": self.relevance_score.weight,
                    "feedback": self.relevance_score.feedback
                },
                "compliance": {
                    "score": self.compliance_score.score,
                    "max": self.compliance_score.max_score,
                    "weight": self.compliance_score.weight,
                    "feedback": self.compliance_score.feedback
                },
                "clarity": {
                    "score": self.clarity_score.score,
                    "max": self.clarity_score.max_score,
                    "weight": self.clarity_score.weight,
                    "feedback": self.clarity_score.feedback
                },
                "pricing": {
                    "score": self.pricing_score.score,
                    "max": self.pricing_score.max_score,
                    "weight": self.pricing_score.weight,
                    "feedback": self.pricing_score.feedback
                }
            },
            "overall": {
                "score": self.overall_score,
                "recommendation": self.recommendation
            },
            "analysis": {
                "strengths": self.strengths,
                "weaknesses": self.weaknesses,
                "improvements": self.improvements
            }
        }


# ============================================================================
# EVALUATION FUNCTIONS
# ============================================================================

class ResponseEvaluator:
    """Evaluate RFP responses"""
    
    # Expected sections in a good RFP response
    EXPECTED_SECTIONS = [
        "executive summary",
        "technical approach",
        "pricing",
        "compliance",
        "implementation",
        "timeline",
        "team",
        "support",
        "sla"
    ]
    
    # Compliance keywords to look for
    COMPLIANCE_KEYWORDS = [
        "soc 2", "soc2", "hipaa", "gdpr", "ccpa", "iso 27001",
        "iso27001", "fedramp", "pci-dss", "pcidss", "glba",
        "encryption", "audit", "compliance", "certification"
    ]
    
    # Pricing indicators
    PRICING_INDICATORS = [
        "$", "price", "cost", "budget", "monthly", "annual",
        "per", "fee", "discount", "tier", "volume"
    ]
    
    def __init__(self):
        """Initialize evaluator"""
        pass
    
    def evaluate(self, rfp_text: str, response_text: str, 
                 rfp_file: str = "rfp.txt", response_file: str = "response.txt") -> EvaluationResult:
        """Evaluate RFP response
        
        Args:
            rfp_text: Original RFP document
            response_text: Generated response
            rfp_file: Original filename (for tracking)
            response_file: Response filename (for tracking)
        
        Returns:
            EvaluationResult with scores and feedback
        """
        
        # Score each dimension
        completeness = self._score_completeness(response_text)
        relevance = self._score_relevance(rfp_text, response_text)
        compliance = self._score_compliance(rfp_text, response_text)
        clarity = self._score_clarity(response_text)
        pricing = self._score_pricing(response_text)
        
        # Calculate overall score
        overall_score = (
            completeness.weighted_score() +
            relevance.weighted_score() +
            compliance.weighted_score() +
            clarity.weighted_score() +
            pricing.weighted_score()
        )
        
        # Determine recommendation
        if overall_score >= 85:
            recommendation = "Excellent"
        elif overall_score >= 70:
            recommendation = "Good"
        elif overall_score >= 60:
            recommendation = "Acceptable"
        else:
            recommendation = "Needs Improvement"
        
        # Extract strengths and weaknesses
        strengths = self._extract_strengths(completeness, relevance, compliance, clarity, pricing)
        weaknesses = self._extract_weaknesses(completeness, relevance, compliance, clarity, pricing)
        improvements = self._generate_improvements(weaknesses)
        
        return EvaluationResult(
            timestamp=datetime.now().isoformat(),
            rfp_filename=Path(rfp_file).name,
            response_filename=Path(response_file).name,
            completeness_score=completeness,
            relevance_score=relevance,
            compliance_score=compliance,
            clarity_score=clarity,
            pricing_score=pricing,
            overall_score=overall_score,
            recommendation=recommendation,
            strengths=strengths,
            weaknesses=weaknesses,
            improvements=improvements
        )
    
    def _score_completeness(self, response_text: str) -> SectionScore:
        """Score: Are all required sections present?
        
        Checks for presence of key sections in the response.
        """
        response_lower = response_text.lower()
        found_sections = []
        missing_sections = []
        
        for section in self.EXPECTED_SECTIONS:
            if section in response_lower:
                found_sections.append(section)
            else:
                missing_sections.append(section)
        
        # Score: % of expected sections found
        score = (len(found_sections) / len(self.EXPECTED_SECTIONS)) * 100
        
        feedback = []
        feedback.append(f"Found {len(found_sections)}/{len(self.EXPECTED_SECTIONS)} expected sections")
        if missing_sections:
            feedback.append(f"Missing sections: {', '.join(missing_sections)}")
        if len(found_sections) >= 7:
            feedback.append("✓ Response covers most key areas")
        elif len(found_sections) >= 5:
            feedback.append("⚠ Some sections missing or unclear")
        else:
            feedback.append("✗ Significant gaps in coverage")
        
        return SectionScore(
            section_name="Completeness",
            score=score,
            max_score=100,
            feedback=feedback,
            weight=0.15  # 15% weight
        )
    
    def _score_relevance(self, rfp_text: str, response_text: str) -> SectionScore:
        """Score: How well does response address RFP requirements?
        
        Extracts key requirements from RFP and checks if response addresses them.
        """
        # Extract keywords from RFP
        rfp_requirements = self._extract_keywords(rfp_text)
        response_text_lower = response_text.lower()
        
        # Check how many requirements are mentioned in response
        covered_requirements = 0
        for keyword in rfp_requirements:
            if keyword.lower() in response_text_lower:
                covered_requirements += 1
        
        # Score: % of requirements addressed
        if rfp_requirements:
            score = (covered_requirements / len(rfp_requirements)) * 100
        else:
            score = 50  # Default if no requirements found
        
        feedback = []
        if score >= 80:
            feedback.append(f"✓ Addresses {covered_requirements}/{len(rfp_requirements)} key requirements")
            feedback.append("Response is highly relevant to customer needs")
        elif score >= 60:
            feedback.append(f"⚠ Addresses {covered_requirements}/{len(rfp_requirements)} key requirements")
            feedback.append("Some requirements not explicitly mentioned")
        else:
            feedback.append(f"✗ Only addresses {covered_requirements}/{len(rfp_requirements)} requirements")
            feedback.append("Response may not adequately address customer needs")
        
        return SectionScore(
            section_name="Relevance",
            score=score,
            max_score=100,
            feedback=feedback,
            weight=0.25  # 25% weight (most important)
        )
    
    def _score_compliance(self, rfp_text: str, response_text: str) -> SectionScore:
        """Score: Does response address compliance requirements?
        
        Checks for compliance mentions and certifications.
        """
        # Extract compliance requirements from RFP
        rfp_compliance = []
        rfp_lower = rfp_text.lower()
        
        for keyword in self.COMPLIANCE_KEYWORDS:
            if keyword in rfp_lower:
                rfp_compliance.append(keyword)
        
        # Remove duplicates
        rfp_compliance = list(set(rfp_compliance))
        
        # Check response mentions
        response_lower = response_text.lower()
        covered_compliance = 0
        
        for keyword in rfp_compliance:
            if keyword in response_lower:
                covered_compliance += 1
        
        # Score
        if rfp_compliance:
            score = (covered_compliance / len(rfp_compliance)) * 100
        else:
            # If no compliance requirements in RFP, check if response proactively addresses compliance
            score = 50 if any(kw in response_lower for kw in self.COMPLIANCE_KEYWORDS) else 30
        
        feedback = []
        if rfp_compliance:
            if score >= 80:
                feedback.append(f"✓ Addresses {covered_compliance}/{len(rfp_compliance)} compliance requirements")
            else:
                feedback.append(f"⚠ Only {covered_compliance}/{len(rfp_compliance)} compliance items addressed")
        else:
            if score > 40:
                feedback.append("✓ Proactively addresses security and compliance")
            else:
                feedback.append("⚠ Limited compliance and security detail")
        
        return SectionScore(
            section_name="Compliance",
            score=score,
            max_score=100,
            feedback=feedback,
            weight=0.20  # 20% weight
        )
    
    def _score_clarity(self, response_text: str) -> SectionScore:
        """Score: Is the response clear and well-structured?
        
        Evaluates structure, length, and organization.
        """
        # Check for good structure
        has_headings = len(re.findall(r'^#{1,3} ', response_text, re.MULTILINE)) > 3
        has_lists = len(re.findall(r'[-•*]', response_text)) > 5
        
        # Check word count (should be substantial but not excessive)
        word_count = len(response_text.split())
        word_count_score = min(100, (word_count / 500) * 100) if word_count < 3000 else 100
        
        # Check for paragraphs (well-formatted text)
        paragraphs = len(re.split(r'\n\n+', response_text))
        
        # Calculate clarity score
        structure_bonus = 20 if (has_headings and has_lists) else 0
        base_score = word_count_score
        clarity_score = min(100, base_score + structure_bonus)
        
        feedback = []
        feedback.append(f"Word count: {word_count}")
        feedback.append(f"Paragraphs: {paragraphs}")
        
        if has_headings:
            feedback.append("✓ Well-structured with clear headings")
        if has_lists:
            feedback.append("✓ Uses lists for clarity")
        if word_count < 200:
            feedback.append("⚠ Response may be too brief")
        if word_count > 5000:
            feedback.append("⚠ Response is quite lengthy")
        
        return SectionScore(
            section_name="Clarity",
            score=clarity_score,
            max_score=100,
            feedback=feedback,
            weight=0.15  # 15% weight
        )
    
    def _score_pricing(self, response_text: str) -> SectionScore:
        """Score: Does response include appropriate pricing information?
        
        Checks for presence of pricing details and structure.
        """
        response_lower = response_text.lower()
        
        # Check for pricing indicators
        price_mentions = 0
        for indicator in self.PRICING_INDICATORS:
            price_mentions += len(re.findall(rf'\b{re.escape(indicator)}\b', response_lower))
        
        # Check for price details
        has_price_section = any(phrase in response_lower for phrase in 
                               ["pricing", "cost", "commercial terms", "investment"])
        has_specific_prices = len(re.findall(r'\$\d+', response_text)) > 0
        has_payment_terms = any(phrase in response_lower for phrase in 
                               ["monthly", "annual", "contract", "payment", "billing"])
        
        # Calculate score
        score = 0
        if has_price_section:
            score += 30
        if has_specific_prices:
            score += 40
        if has_payment_terms:
            score += 30
        
        feedback = []
        if has_price_section:
            feedback.append("✓ Includes pricing section")
        if has_specific_prices:
            feedback.append(f"✓ Specific pricing mentioned ({len(re.findall(r'\$\d+', response_text))} instances)")
        if has_payment_terms:
            feedback.append("✓ Payment terms included")
        
        if score < 50:
            feedback.append("⚠ Limited pricing information")
        if score == 0:
            feedback.append("✗ No pricing details provided")
        
        return SectionScore(
            section_name="Pricing",
            score=score,
            max_score=100,
            feedback=feedback,
            weight=0.25  # 25% weight
        )
    
    def _extract_keywords(self, text: str, limit: int = 30) -> List[str]:
        """Extract key terms from text for requirement matching"""
        # Convert to lowercase and remove punctuation
        text = re.sub(r'[^a-z0-9\s]', ' ', text.lower())
        
        # Extract 2-3 word phrases
        words = text.split()
        keywords = []
        
        for i in range(len(words) - 1):
            # 2-word phrases
            phrase = f"{words[i]} {words[i+1]}"
            if len(phrase) > 5 and phrase not in keywords:
                keywords.append(phrase)
        
        # Return most common keywords
        return keywords[:limit]
    
    def _extract_strengths(self, *scores) -> List[str]:
        """Extract strengths from score objects"""
        strengths = []
        
        for score in scores:
            if score.score >= 80:
                strengths.append(f"Strong {score.section_name.lower()}: {score.score:.0f}/100")
        
        return strengths if strengths else ["Solid overall structure"]
    
    def _extract_weaknesses(self, *scores) -> List[str]:
        """Extract weaknesses from score objects"""
        weaknesses = []
        
        for score in scores:
            if score.score < 70:
                weaknesses.append(f"Weak {score.section_name.lower()}: {score.score:.0f}/100")
        
        return weaknesses if weaknesses else ["No significant weaknesses"]
    
    def _generate_improvements(self, weaknesses: List[str]) -> List[str]:
        """Generate improvement suggestions based on weaknesses"""
        improvements = []
        
        for weakness in weaknesses:
            if "completeness" in weakness.lower():
                improvements.append("Add missing sections (Executive Summary, Timeline, Team)")
            elif "relevance" in weakness.lower():
                improvements.append("Explicitly reference customer requirements and pain points")
            elif "compliance" in weakness.lower():
                improvements.append("Highlight relevant certifications and security measures")
            elif "clarity" in weakness.lower():
                improvements.append("Use headings, bullet points, and concise paragraphs")
            elif "pricing" in weakness.lower():
                improvements.append("Include specific pricing breakdown and payment terms")
        
        if not improvements:
            improvements.append("Response is well-structured; focus on fine-tuning details")
        
        return improvements


# ============================================================================
# OUTPUT FORMATTING
# ============================================================================

def print_evaluation_report(result: EvaluationResult) -> None:
    """Print formatted evaluation report"""
    
    print("\n" + "="*70)
    print("📊 RFP RESPONSE EVALUATION REPORT")
    print("="*70)
    print(f"\nTimestamp: {result.timestamp}")
    print(f"RFP File: {result.rfp_filename}")
    print(f"Response File: {result.response_filename}")
    
    # Overall Score
    print("\n" + "="*70)
    print("🎯 OVERALL SCORE")
    print("="*70)
    print(f"Score: {result.overall_score:.1f}/100")
    print(f"Recommendation: {result.recommendation}")
    
    # Score breakdown
    print("\n" + "="*70)
    print("📈 SCORE BREAKDOWN")
    print("="*70)
    
    scores = [
        ("Completeness", result.completeness_score),
        ("Relevance", result.relevance_score),
        ("Compliance", result.compliance_score),
        ("Clarity", result.clarity_score),
        ("Pricing", result.pricing_score),
    ]
    
    for name, score in scores:
        bar_length = int(score.score / 5)
        bar = "█" * bar_length + "░" * (20 - bar_length)
        print(f"\n{name:<12} {bar} {score.score:.0f}/100 (weight: {score.weight*100:.0f}%)")
        for feedback in score.feedback:
            print(f"  {feedback}")
    
    # Strengths
    print("\n" + "="*70)
    print("💪 STRENGTHS")
    print("="*70)
    for strength in result.strengths:
        print(f"  ✓ {strength}")
    
    # Weaknesses
    if result.weaknesses and result.weaknesses[0] != "No significant weaknesses":
        print("\n" + "="*70)
        print("⚠️  WEAKNESSES")
        print("="*70)
        for weakness in result.weaknesses:
            print(f"  ✗ {weakness}")
    
    # Improvements
    print("\n" + "="*70)
    print("🎯 RECOMMENDED IMPROVEMENTS")
    print("="*70)
    for i, improvement in enumerate(result.improvements, 1):
        print(f"  {i}. {improvement}")
    
    print("\n" + "="*70 + "\n")


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Main entry point"""
    
    parser = ArgumentParser(description="Evaluate RFP response quality")
    
    parser.add_argument(
        "--rfp",
        type=str,
        required=True,
        help="Path to original RFP file"
    )
    parser.add_argument(
        "--response",
        type=str,
        required=True,
        help="Path to generated response file"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output JSON report file"
    )
    parser.add_argument(
        "--format",
        choices=["text", "json", "both"],
        default="both",
        help="Output format"
    )
    
    args = parser.parse_args()
    
    # Load files
    try:
        with open(args.rfp, 'r') as f:
            rfp_text = f.read()
    except FileNotFoundError:
        print(f"❌ RFP file not found: {args.rfp}")
        return
    
    try:
        with open(args.response, 'r') as f:
            response_text = f.read()
    except FileNotFoundError:
        print(f"❌ Response file not found: {args.response}")
        return
    
    # Evaluate
    print("\n🔍 Evaluating response...\n")
    evaluator = ResponseEvaluator()
    result = evaluator.evaluate(rfp_text, response_text, args.rfp, args.response)
    
    # Output
    if args.format in ["text", "both"]:
        print_evaluation_report(result)
    
    if args.format in ["json", "both"]:
        output_file = args.output or "evaluation_report.json"
        with open(output_file, 'w') as f:
            json.dump(result.to_dict(), f, indent=2)
        print(f"💾 Report saved to: {output_file}")


if __name__ == "__main__":
    main()
