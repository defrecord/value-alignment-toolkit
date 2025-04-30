"""
Unit tests for the value analyzer module.
"""
import unittest
import pandas as pd
import numpy as np
from src.analysis.value_analyzer import ValueAnalyzer

class TestValueAnalyzer(unittest.TestCase):
    """Test suite for ValueAnalyzer class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.analyzer = ValueAnalyzer()
        
        # Create sample data
        self.values_list = [
            "helpfulness", "transparency", "clarity", "helpfulness", 
            "efficiency", "thoroughness", "helpfulness"
        ]
        
        # Sample DataFrame for analysis
        self.sample_df = pd.DataFrame({
            'value': ["helpfulness", "transparency", "clarity", "helpfulness", 
                     "efficiency", "thoroughness", "helpfulness"],
            'task': ["advice", "technical", "education", "advice", 
                    "coding", "research", "advice"],
            'response_type': ["support", "support", "neutral", "support", 
                            "support", "neutral", "reframing"],
            'human_value': ["assistance", "transparency", "clarity", "efficiency", 
                          "efficiency", "thoroughness", "self-improvement"]
        })
    
    def test_calculate_value_frequencies(self):
        """Test value frequency calculation."""
        frequencies = self.analyzer.calculate_value_frequencies(self.values_list)
        
        # Check total count
        self.assertEqual(sum(frequencies.values()), len(self.values_list))
        
        # Check specific frequencies
        self.assertEqual(frequencies["helpfulness"], 3)
        self.assertEqual(frequencies["transparency"], 1)
        self.assertEqual(frequencies["clarity"], 1)
        self.assertEqual(frequencies["efficiency"], 1)
        self.assertEqual(frequencies["thoroughness"], 1)
    
    def test_compute_chi_square(self):
        """Test chi-square computation."""
        # Set the analyzer's data
        self.analyzer.values_data = self.sample_df
        
        # Compute chi-square for value and task
        chi2, residuals, p_value = self.analyzer.compute_chi_square(
            self.sample_df, 'value', 'task')
        
        # Check result types
        self.assertIsInstance(chi2, float)
        self.assertIsInstance(residuals, pd.DataFrame)
        self.assertIsInstance(p_value, float)
        
        # Check residuals shape
        self.assertEqual(residuals.shape[0], len(self.sample_df['value'].unique()))
        self.assertEqual(residuals.shape[1], len(self.sample_df['task'].unique()))
    
    def test_analyze_value_task_associations(self):
        """Test value-task association analysis."""
        residuals = self.analyzer.analyze_value_task_associations(self.sample_df)
        
        # Check result type and shape
        self.assertIsInstance(residuals, pd.DataFrame)
        self.assertEqual(residuals.shape[0], len(self.sample_df['value'].unique()))
        self.assertEqual(residuals.shape[1], len(self.sample_df['task'].unique()))
        
        # Check that helpfulness has a positive association with advice
        self.assertGreater(residuals.loc["helpfulness", "advice"], 0)
    
    def test_identify_mirrored_values(self):
        """Test mirrored values identification."""
        # Create a sample with mirrored values
        mirror_df = pd.DataFrame({
            'human_value': ["clarity", "efficiency", "thoroughness", "helpfulness", "transparency"],
            'ai_value': ["clarity", "efficiency", "analytical rigor", "helpfulness", "honesty"]
        })
        
        result = self.analyzer.identify_mirrored_values(mirror_df)
        
        # Check result structure
        self.assertIn('value', result.columns)
        self.assertIn('mirroring_rate', result.columns)
        self.assertIn('mirroring_count', result.columns)
        self.assertIn('total_count', result.columns)
        
        # Check mirroring rates
        clarity_row = result[result['value'] == "clarity"].iloc[0]
        self.assertEqual(clarity_row['mirroring_rate'], 1.0)  # 100% mirrored
        
        efficiency_row = result[result['value'] == "efficiency"].iloc[0]
        self.assertEqual(efficiency_row['mirroring_rate'], 1.0)  # 100% mirrored
        
        thoroughness_row = result[result['value'] == "thoroughness"].iloc[0]
        self.assertEqual(thoroughness_row['mirroring_rate'], 0.0)  # 0% mirrored

if __name__ == "__main__":
    unittest.main()
