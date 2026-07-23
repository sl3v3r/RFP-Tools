#!/usr/bin/env python3
"""
Batch Evaluation Tool

Evaluate multiple RFP responses at once and generate summary reports.
"""

import json
from pathlib import Path
from typing import List
from argparse import ArgumentParser
from datetime import datetime
import sys

sys.path.insert(0, str(Path(__file__).parent.parent))

from scripts.evaluate_response import ResponseEvaluator, EvaluationResult


class BatchEvaluator:
    """Evaluate multiple responses and generate reports"""
    
    def __init__(self, output_dir: str = "evaluation_results"):
        """Initialize batch evaluator
        
        Args:
            output_dir: Directory to save evaluation results
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.evaluator = ResponseEvaluator()
        self.results = []
    
    def evaluate_batch(self, rfp_dir: str, response_dir: str) -> List[EvaluationResult]:
        """Evaluate all RFP/response pairs in directories
        
        Matches files by basename (e.g., rfp_001.txt with response_001.json)
        
        Args:
            rfp_dir: Directory containing RFP files
            response_dir: Directory containing response files
        
        Returns:
            List of evaluation results
        """
        rfp_path = Path(rfp_dir)
        response_path = Path(response_dir)
        
        # Find RFP files
        rfp_files = list(rfp_path.glob("*.txt")) + list(rfp_path.glob("*.md"))
        
        if not rfp_files:
            print(f"❌ No RFP files found in {rfp_dir}")
            return []
        
        print(f"\n🔍 Found {len(rfp_files)} RFP files")
        
        # Evaluate each RFP
        for i, rfp_file in enumerate(rfp_files, 1):
            # Find corresponding response
            response_file = response_path / (rfp_file.stem + ".json")
            
            if not response_file.exists():
                response_file = response_path / (rfp_file.stem + ".txt")
            
            if not response_file.exists():
                print(f"⚠️  No response found for {rfp_file.name}")
                continue
            
            # Load and evaluate
            print(f"  [{i}/{len(rfp_files)}] Evaluating {rfp_file.name}...")
            
            try:
                with open(rfp_file) as f:
                    rfp_text = f.read()
                
                with open(response_file) as f:
                    response_text = f.read()
                
                # If response is JSON, extract text
                if response_file.suffix == ".json":
                    try:
                        data = json.load(open(response_file))
                        if isinstance(data, dict):
                            if "sections" in data:
                                response_text = " ".join(str(v) for v in data["sections"].values())
                            elif "response" in data:
                                response_text = data["response"]
                    except:
                        pass
                
                result = self.evaluator.evaluate(
                    rfp_text,
                    response_text,
                    str(rfp_file),
                    str(response_file)
                )
                
                self.results.append(result)
                print(f"     Score: {result.overall_score:.1f} - {result.recommendation}")
            
            except Exception as e:
                print(f"❌ Error evaluating {rfp_file.name}: {e}")
        
        return self.results
    
    def generate_summary(self) -> dict:
        """Generate summary statistics from all evaluations"""
        
        if not self.results:
            return {}
        
        scores = [r.overall_score for r in self.results]
        
        return {
            "total_evaluated": len(self.results),
            "average_score": sum(scores) / len(scores),
            "min_score": min(scores),
            "max_score": max(scores),
            "median_score": sorted(scores)[len(scores)//2],
            "excellent": len([s for s in scores if s >= 85]),
            "good": len([s for s in scores if 70 <= s < 85]),
            "acceptable": len([s for s in scores if 60 <= s < 70]),
            "needs_improvement": len([s for s in scores if s < 60]),
        }
    
    def save_results(self) -> None:
        """Save all evaluation results to files"""
        
        # Individual results
        for result in self.results:
            filename = self.output_dir / f"evaluation_{result.response_filename}.json"
            with open(filename, 'w') as f:
                json.dump(result.to_dict(), f, indent=2)
        
        # Summary report
        summary = self.generate_summary()
        all_results = [r.to_dict() for r in self.results]
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "results": all_results
        }
        
        report_file = self.output_dir / "batch_evaluation_report.json"
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n💾 Results saved to {self.output_dir}/")
    
    def print_summary(self) -> None:
        """Print summary report to console"""
        
        summary = self.generate_summary()
        
        if not summary:
            print("❌ No results to summarize")
            return
        
        print("\n" + "="*70)
        print("📊 BATCH EVALUATION SUMMARY")
        print("="*70)
        print(f"\nTotal Evaluated: {summary['total_evaluated']}")
        print(f"Average Score: {summary['average_score']:.1f}/100")
        print(f"Score Range: {summary['min_score']:.1f} - {summary['max_score']:.1f}")
        
        print("\nScore Distribution:")
        print(f"  Excellent (≥85): {summary['excellent']} ({summary['excellent']/summary['total_evaluated']*100:.0f}%)")
        print(f"  Good (70-84):    {summary['good']} ({summary['good']/summary['total_evaluated']*100:.0f}%)")
        print(f"  Acceptable (60-69): {summary['acceptable']} ({summary['acceptable']/summary['total_evaluated']*100:.0f}%)")
        print(f"  Needs Improvement (<60): {summary['needs_improvement']} ({summary['needs_improvement']/summary['total_evaluated']*100:.0f}%)")
        
        print("\nDetailed Results:")
        for result in self.results:
            status = "✓" if result.overall_score >= 70 else "✗"
            print(f"  {status} {result.response_filename}: {result.overall_score:.1f} - {result.recommendation}")
        
        print("\n" + "="*70 + "\n")


def main():
    """Main entry point"""
    
    parser = ArgumentParser(description="Batch evaluate RFP responses")
    
    parser.add_argument(
        "--rfp-dir",
        type=str,
        default="./rfps",
        help="Directory containing RFP files"
    )
    parser.add_argument(
        "--response-dir",
        type=str,
        default="./responses",
        help="Directory containing response files"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="./evaluation_results",
        help="Directory to save evaluation results"
    )
    parser.add_argument(
        "--no-summary",
        action="store_true",
        help="Don't print summary report"
    )
    
    args = parser.parse_args()
    
    # Create evaluator
    batch_eval = BatchEvaluator(output_dir=args.output_dir)
    
    # Evaluate
    results = batch_eval.evaluate_batch(args.rfp_dir, args.response_dir)
    
    if results:
        batch_eval.save_results()
        
        if not args.no_summary:
            batch_eval.print_summary()
    else:
        print("❌ No evaluations completed")


if __name__ == "__main__":
    main()
