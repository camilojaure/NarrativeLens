# NarrativeLens

NarrativeLens is a powerful solution for analyzing and extracting visual and narrative elements from paid social ads. Developed as part of my Master’s thesis in Management and Analytics at the Instituto Tecnológico de Buenos Aires (ITBA), it benchmarks creative elements against top-performing campaigns to deliver actionable insights and best practices for optimizing ad creative.

⸻

## Overview

Brands face intense competition in the social media advertising space and need fast, data-driven feedback on what makes ads effective. NarrativeLens addresses this by:
- Scene Segmentation: Automatically splitting ads into discrete scenes for detailed analysis.
- Multimodal Feature Extraction: Using computer vision, NLP, and audio analysis to capture rich creative signals.
- Benchmark Comparison: Evaluating extracted features against a repository of high-performing ads.
- Insights & Recommendations: Generating clear, data-driven suggestions to guide future creative strategies.

-----

## Workflow
1.	Video Input
- We begin with a dataset of just over 500 TikTok Video Ads sourced from the TikTok Top Ads feed.

2.	Pre-processing
- Run featureExtractor.py, which extracts Creative Diversity Score dimensions using Gemini.
- Optionally run a UGC detector to classify whether an ad is user-generated content.
- Both scripts validate outputs with a Pydantic data model to ensure label accuracy.
- Prompt configurations for Gemini are stored in the prompts/ directory.
- All extracted labels are saved to a MongoDB collection.

3.	Data Preparation & Exploration
- Execute etl.py to transform raw feature data into an analytical format.
- Run the exploratory data analysis notebook to understand distributions, clean data, and prep for modeling.

4.	Modeling
- In the modeling/ section, find the regression analysis notebook. This implements OLS and Random Forest analyses precisely for the thesis.

![Sequence Diagram](image.png)