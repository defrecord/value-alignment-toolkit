# Values in the Wild: Research Summary

This document summarizes the key findings and methodologies from the "Values in the Wild" paper by Anthropic, which serves as the foundation for this toolkit.

## Overview

The "Values in the Wild" paper presents a novel empirical approach to understanding how values manifest in AI assistant interactions. The research analyzes hundreds of thousands of real-world Claude conversations to extract and categorize AI values across different contexts.

## Key Findings

1. **Value Taxonomy**: The research identified 3,307 unique AI values, organized into a hierarchical taxonomy with five top-level categories:
   - Practical Values (31.4%)
   - Epistemic Values (22.2%)
   - Social Values (21.4%) 
   - Protective Values (13.9%)
   - Personal Values (11.1%)

2. **Common Values**: The most frequently expressed AI values were service-oriented:
   - Helpfulness (23.4%)
   - Professionalism (22.9%)
   - Transparency (17.4%)
   - Clarity (16.6%)
   - Thoroughness (14.3%)

3. **Context Dependence**: AI values vary significantly by task context:
   - "Healthy boundaries" in relationship advice
   - "Historical accuracy" for controversial historical events
   - "Human agency" in technology ethics discussions

4. **Human-AI Value Relationships**: AI values relate to human-expressed values in complex ways:
   - Often mirroring positive values (e.g., "authenticity")
   - Countering problematic values with opposing values (e.g., "ethical integrity")

5. **Response Types**: Claude's responses to human values vary:
   - Predominantly supportive (43% of conversations)
   - Reframing when appropriate (6.6%)
   - Rarely resistant (5.4%)

## Methodology

The research employed a privacy-preserving approach to analyze AI conversations:

1. **Data Collection**: Random sample of anonymized Claude.ai conversations, filtered for subjective interactions (44% of total)

2. **Feature Extraction**: Used language models to extract:
   - AI values
   - Human values
   - Response types
   - Task categories

3. **Taxonomy Construction**: Hierarchically organized values into a four-level taxonomy

4. **Statistical Analysis**: Applied chi-square analysis to identify significant associations between values and contexts

5. **Privacy Protection**: Implemented anonymization techniques including:
   - Pseudonymization
   - Context-specific identifiers
   - Demographic generalization
   - K-anonymity

## Implications

This research provides a foundation for:

1. **Empirical Evaluation**: Evidence-based assessment of AI value alignment
2. **AI-Native Value Frameworks**: Understanding values as they manifest in AI systems
3. **Transparency**: Visibility into how AI systems behave in real-world contexts
4. **Design Insights**: Guidance for developing more aligned AI systems

## References

Full paper: [Values in the Wild: Discovering and Analyzing Values in Real-World Language Model Interactions](https://huggingface.co/datasets/Anthropic/values-in-the-wild)
