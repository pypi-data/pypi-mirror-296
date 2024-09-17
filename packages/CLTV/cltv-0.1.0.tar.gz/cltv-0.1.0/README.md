# Customer Lifetime Value (CLTV) Analysis

## Overview

This package provides tools for Customer Lifetime Value (CLTV) analysis, including data processing, visualization, and predictive modeling. It utilizes the BetaGeoFitter and GammaGammaFitter from the `lifetimes` library to calculate and analyze customer lifetime value.

## Features

- **Data Processing and Visualization**: 
  - Clean and preprocess data
  - Calculate CLTV using BG/NBD and Gamma-Gamma models
  - Visualize CLTV and customer segments

- **Logistic Regression**:
  - Train a logistic regression model to classify high-value customers
  - Evaluate model performance using various metrics

- **Enhanced Visualizations**:
  - Generate correlation heatmaps
  - Cluster customers using K-Means and visualize clusters

## Requirements

To use this package, you need the following Python packages:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `lifetimes`
- `scikit-learn`

You can install these dependencies using:

```bash
pip install -r requirements.txt
```
## Usage
To import the package and run the main function, use the following format:
```bash
from CLTV.cltv import main
```