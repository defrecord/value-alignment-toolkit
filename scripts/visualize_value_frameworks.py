#!/usr/bin/env python3
"""
Value Framework Visualization Script

This script demonstrates visualization of different value frameworks for comparison.
It reads the example value datasets and creates comparative visualizations.
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import sys
from pathlib import Path

# Add the project root to the path so we can import the package
sys.path.insert(0, str(Path(__file__).parent.parent))

def load_data():
    """Load the sample value datasets."""
    base_dir = Path(__file__).parent.parent / "data" / "values" / "examples"
    
    # Load AI assistant values
    ai_values_path = base_dir / "value_expressions.csv"
    ai_values = pd.read_csv(ai_values_path)
    
    # Load Schwartz human values
    schwartz_path = base_dir / "schwartz_values.csv"
    schwartz_values = pd.read_csv(schwartz_path)
    
    return ai_values, schwartz_values

def preprocess_ai_values(ai_values):
    """Process the AI values for visualization."""
    # Group by value and take the first percentage for each
    ai_summary = ai_values.groupby('value')['percentage'].first().reset_index()
    # Sort by percentage descending
    ai_summary = ai_summary.sort_values('percentage', ascending=False)
    return ai_summary

def preprocess_schwartz_values(schwartz_values):
    """Process the Schwartz values for visualization."""
    # Group by value and take the first weight for each
    schwartz_summary = schwartz_values.groupby('value')['weight'].first().reset_index()
    # Sort by weight descending
    schwartz_summary = schwartz_summary.sort_values('weight', ascending=False)
    return schwartz_summary

def plot_top_values(ai_summary, schwartz_summary, output_dir):
    """Create a bar chart of top values from each framework."""
    # Take top 10 values from each
    ai_top = ai_summary.head(10)
    schwartz_top = schwartz_summary.head(10)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot AI values
    ax1.bar(ai_top['value'], ai_top['percentage'], color='skyblue')
    ax1.set_title('Top 10 AI Assistant Values')
    ax1.set_ylabel('Percentage')
    ax1.set_xlabel('Value')
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot Schwartz values
    ax2.bar(schwartz_top['value'], schwartz_top['weight'], color='lightgreen')
    ax2.set_title('Top 10 Schwartz Human Values')
    ax2.set_ylabel('Weight')
    ax2.set_xlabel('Value')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_values_comparison.png'))
    plt.close()

def plot_schwartz_dimensions(schwartz_values, output_dir):
    """Create a visualization of the Schwartz higher-order dimensions."""
    # Group by higher order dimension and sum weights
    dimensions = schwartz_values.groupby('higher_order_dimension')['weight'].sum().reset_index()
    
    # Create a pie chart
    plt.figure(figsize=(10, 10))
    plt.pie(dimensions['weight'], labels=dimensions['higher_order_dimension'], 
            autopct='%1.1f%%', startangle=90, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
    plt.axis('equal')
    plt.title('Schwartz Higher-Order Value Dimensions')
    plt.savefig(os.path.join(output_dir, 'schwartz_dimensions.png'))
    plt.close()

def plot_value_distributions(ai_summary, schwartz_summary, output_dir):
    """Create a visualization comparing value distributions."""
    # Normalize weights to percentages for comparison
    schwartz_summary['normalized'] = schwartz_summary['weight'] / schwartz_summary['weight'].sum() * 100
    
    plt.figure(figsize=(12, 6))
    
    # Plot kernel density estimates
    ai_density = ai_summary['percentage']
    schwartz_density = schwartz_summary['normalized']
    
    plt.hist(ai_density, alpha=0.5, label='AI Assistant Values', bins=10, density=True)
    plt.hist(schwartz_density, alpha=0.5, label='Schwartz Human Values', bins=10, density=True)
    
    plt.title('Distribution of Value Weights')
    plt.xlabel('Percentage/Normalized Weight')
    plt.ylabel('Density')
    plt.legend()
    plt.savefig(os.path.join(output_dir, 'value_distributions.png'))
    plt.close()

def main():
    """Main function to create visualizations."""
    print("Visualizing value frameworks...")
    
    # Create output directory
    output_dir = Path(__file__).parent.parent / "data" / "output"
    output_dir.mkdir(exist_ok=True)
    
    # Load and process data
    ai_values, schwartz_values = load_data()
    ai_summary = preprocess_ai_values(ai_values)
    schwartz_summary = preprocess_schwartz_values(schwartz_values)
    
    # Create visualizations
    plot_top_values(ai_summary, schwartz_summary, output_dir)
    plot_schwartz_dimensions(schwartz_values, output_dir)
    plot_value_distributions(ai_summary, schwartz_summary, output_dir)
    
    print(f"Visualizations created in {output_dir}")

if __name__ == "__main__":
    main()