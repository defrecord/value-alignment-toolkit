"""
Analysis tools for value frequencies, associations, and context-dependencies.
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Any, Optional
from collections import defaultdict

class ValueAnalyzer:
    """
    Analyzes value expressions, distributions, and associations across contexts.
    
    Implements statistical analysis methods for understanding how values manifest
    in different contexts and tasks.
    """
    
    def __init__(self, values_data=None):
        """
        Initialize the value analyzer.
        
        Args:
            values_data: Optional dictionary or DataFrame of value data
        """
        self.values_data = values_data
    
    def load_data(self, data_path: str):
        """
        Load value data from a file.
        
        Args:
            data_path: Path to the data file (CSV or JSON)
            
        Returns:
            Loaded data as DataFrame
        """
        if data_path.endswith('.csv'):
            self.values_data = pd.read_csv(data_path)
        elif data_path.endswith('.json'):
            self.values_data = pd.read_json(data_path)
        else:
            raise ValueError("Unsupported file format. Use CSV or JSON.")
        
        return self.values_data
    
    def calculate_value_frequencies(self, values_list: List[str]) -> Dict[str, int]:
        """
        Calculate the frequency of each value in a list.
        
        Args:
            values_list: List of value strings
            
        Returns:
            Dictionary mapping values to their frequencies
        """
        frequencies = defaultdict(int)
        for value in values_list:
            frequencies[value] += 1
        
        return dict(frequencies)
    
    def compute_chi_square(self, 
                           observed_df: pd.DataFrame, 
                           row_var: str, 
                           col_var: str) -> Tuple[float, pd.DataFrame, pd.DataFrame]:
        """
        Compute chi-square test for independence between two variables.
        
        Args:
            observed_df: DataFrame with the data
            row_var: Column name for the row variable
            col_var: Column name for the column variable
            
        Returns:
            Tuple of (chi-square statistic, DataFrame of adjusted residuals, p-value)
        """
        # Create contingency table
        contingency = pd.crosstab(observed_df[row_var], observed_df[col_var])
        
        # Calculate expected frequencies
        row_totals = contingency.sum(axis=1).values.reshape(-1, 1)
        col_totals = contingency.sum(axis=0).values
        total = contingency.sum().sum()
        expected = np.outer(row_totals, col_totals) / total
        
        # Chi-square statistic
        chi2 = ((contingency.values - expected) ** 2 / expected).sum()
        
        # Adjusted residuals
        E = expected
        O = contingency.values
        row_props = row_totals / total
        col_props = col_totals / total
        
        adj_residuals = pd.DataFrame(
            (O - E) / np.sqrt(E * (1 - row_props) * (1 - col_props[:, np.newaxis].T)),
            index=contingency.index,
            columns=contingency.columns
        )
        
        # Degrees of freedom
        df = (contingency.shape[0] - 1) * (contingency.shape[1] - 1)
        
        # P-value
        from scipy.stats import chi2
        p_value = 1 - chi2.cdf(chi2, df)
        
        return chi2, adj_residuals, p_value
    
    def analyze_value_task_associations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze associations between values and tasks.
        
        Args:
            df: DataFrame with 'value' and 'task' columns
            
        Returns:
            DataFrame of adjusted residuals showing value-task associations
        """
        _, residuals, _ = self.compute_chi_square(df, 'value', 'task')
        return residuals
    
    def analyze_value_response_associations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Analyze associations between values and response types.
        
        Args:
            df: DataFrame with 'value' and 'response_type' columns
            
        Returns:
            DataFrame of adjusted residuals showing value-response associations
        """
        _, residuals, _ = self.compute_chi_square(df, 'value', 'response_type')
        return residuals
    
    def identify_mirrored_values(self, 
                                df: pd.DataFrame, 
                                human_val_col: str = 'human_value', 
                                ai_val_col: str = 'ai_value') -> pd.DataFrame:
        """
        Identify instances where AI mirrors human-expressed values.
        
        Args:
            df: DataFrame with human and AI value columns
            human_val_col: Column name for human values
            ai_val_col: Column name for AI values
            
        Returns:
            DataFrame with mirroring analysis
        """
        # Create a mirroring indicator
        df['mirrored'] = df[human_val_col] == df[ai_val_col]
        
        # Calculate mirroring rates by value
        mirroring_rates = df.groupby(human_val_col)['mirrored'].mean().reset_index()
        mirroring_rates.columns = ['value', 'mirroring_rate']
        
        # Calculate mirroring counts
        mirroring_counts = df.groupby(human_val_col)['mirrored'].sum().reset_index()
        mirroring_counts.columns = ['value', 'mirroring_count']
        
        # Merge rates and counts
        result = pd.merge(mirroring_rates, mirroring_counts, on='value')
        
        # Get total occurrences of each value
        value_counts = df[human_val_col].value_counts().reset_index()
        value_counts.columns = ['value', 'total_count']
        
        # Merge with result
        result = pd.merge(result, value_counts, on='value')
        
        return result.sort_values('mirroring_rate', ascending=False)

# Example usage
if __name__ == "__main__":
    analyzer = ValueAnalyzer()
    
    # Example value list
    values = ["helpfulness", "transparency", "clarity", "helpfulness", 
              "efficiency", "thoroughness", "helpfulness"]
    
    # Calculate frequencies
    frequencies = analyzer.calculate_value_frequencies(values)
    print("Value frequencies:")
    for value, count in sorted(frequencies.items(), key=lambda x: x[1], reverse=True):
        print(f"  {value}: {count}")
