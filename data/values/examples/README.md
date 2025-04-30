# Value Expression Examples

This directory contains sample datasets of value expressions used for analysis and simulation.

## Files

- `value_expressions.csv`: A dataset of AI assistant value expressions
  - Format: value name, frequency percentage, example sentence
  - Contains samples across multiple value categories (helpfulness, professionalism, transparency, etc.)
  - Useful for training value extraction algorithms and simulating value-weighted conversations

- `schwartz_values.csv`: A dataset based on Schwartz's Basic Human Values framework
  - Format: value name, higher order dimension, weight, description, example sentence
  - Organizes values into higher-order dimensions: self-enhancement, self-transcendence, openness-to-change, conservation
  - Provides a more structured, theoretically-grounded approach to human values
  - Includes weights representing relative importance across the value system

## Usage

These sample datasets can be used for:

1. Training and validating value extraction algorithms
2. Initializing weighted value sampling in chat simulations
3. Demonstrating value distribution analysis
4. Testing anonymization techniques
5. Comparing different value frameworks (AI-specific vs. human psychological models)
6. Evaluating alignment between AI and human value expressions

The weights/percentages represent the frequency or importance of each value type, which can be used for weighted sampling when simulating conversations or analyzing value distributions.