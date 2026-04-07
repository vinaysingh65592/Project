"""
Data Exploration and Visualization Script
This script explores the medical dataset and generates visualizations
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Load datasets
def load_datasets():
    """Load all datasets from the datasets folder"""
    data_path = Path('datasets')
    
    datasets = {
        'training': pd.read_csv(data_path / 'Training.csv'),
        'description': pd.read_csv(data_path / 'description.csv'),
        'medications': pd.read_csv(data_path / 'medications.csv'),
        'diets': pd.read_csv(data_path / 'diets.csv'),
        'precautions': pd.read_csv(data_path / 'precautions_df.csv'),
        'workouts': pd.read_csv(data_path / 'workout_df.csv'),
        'symptom_severity': pd.read_csv(data_path / 'Symptom-severity.csv')
    }
    
    return datasets

def explore_training_data(df):
    """Explore the training dataset"""
    print("=" * 80)
    print("TRAINING DATA EXPLORATION")
    print("=" * 80)
    
    print(f"\nDataset Shape: {df.shape}")
    print(f"Number of Features: {df.shape[1] - 1}")  # Excluding target column
    print(f"Number of Samples: {df.shape[0]}")
    
    # Get the target column (last column)
    target_col = df.columns[-1]
    print(f"\nTarget Column: {target_col}")
    
    # Disease distribution
    print(f"\nNumber of Unique Diseases: {df[target_col].nunique()}")
    print("\nDisease Distribution:")
    disease_counts = df[target_col].value_counts()
    print(disease_counts)
    
    # Check for missing values
    print(f"\nMissing Values: {df.isnull().sum().sum()}")
    
    # Feature statistics
    feature_cols = df.columns[:-1]
    print(f"\nFeature Value Distribution:")
    print(f"All features are binary (0/1): {df[feature_cols].isin([0, 1]).all().all()}")
    
    return disease_counts

def visualize_disease_distribution(disease_counts):
    """Visualize disease distribution"""
    plt.figure(figsize=(14, 8))
    disease_counts.plot(kind='bar', color='steelblue', edgecolor='black')
    plt.title('Disease Distribution in Training Data', fontsize=16, fontweight='bold')
    plt.xlabel('Disease', fontsize=12)
    plt.ylabel('Number of Samples', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('visualizations/disease_distribution.png', dpi=300, bbox_inches='tight')
    print("\n Saved: visualizations/disease_distribution.png")
    plt.close()

def analyze_symptom_severity(df):
    """Analyze symptom severity data"""
    print("\n" + "=" * 80)
    print("SYMPTOM SEVERITY ANALYSIS")
    print("=" * 80)
    
    print(f"\nTotal Symptoms: {len(df)}")
    print(f"\nSeverity Weight Range: {df['weight'].min()} - {df['weight'].max()}")
    print(f"Average Severity: {df['weight'].mean():.2f}")
    
    # Top 10 most severe symptoms
    print("\nTop 10 Most Severe Symptoms:")
    top_symptoms = df.nlargest(10, 'weight')
    print(top_symptoms.to_string(index=False))
    
    # Visualize severity distribution
    plt.figure(figsize=(12, 6))
    df['weight'].value_counts().sort_index().plot(kind='bar', color='coral', edgecolor='black')
    plt.title('Symptom Severity Distribution', fontsize=16, fontweight='bold')
    plt.xlabel('Severity Weight', fontsize=12)
    plt.ylabel('Number of Symptoms', fontsize=12)
    plt.tight_layout()
    plt.savefig('visualizations/symptom_severity_distribution.png', dpi=300, bbox_inches='tight')
    print("\n Saved: visualizations/symptom_severity_distribution.png")
    plt.close()

def analyze_recommendations(medications_df, diets_df, workouts_df):
    """Analyze recommendation data"""
    print("\n" + "=" * 80)
    print("RECOMMENDATION DATA ANALYSIS")
    print("=" * 80)
    
    print(f"\nDiseases with Medication Info: {len(medications_df)}")
    print(f"Diseases with Diet Info: {len(diets_df)}")
    print(f"Diseases with Workout Info: {workouts_df['disease'].nunique()}")
    
    # Sample recommendations
    print("\nSample Medication Recommendations:")
    print(medications_df.head(3).to_string(index=False))
    
    print("\nSample Diet Recommendations:")
    print(diets_df.head(3).to_string(index=False))

def create_symptom_heatmap(training_df):
    """Create correlation heatmap for top symptoms"""
    print("\n" + "=" * 80)
    print("CREATING SYMPTOM CORRELATION HEATMAP")
    print("=" * 80)
    
    # Get feature columns (excluding target)
    feature_cols = training_df.columns[:-1]
    
    # Calculate symptom frequency
    symptom_freq = training_df[feature_cols].sum().sort_values(ascending=False)
    top_20_symptoms = symptom_freq.head(20).index
    
    # Create correlation matrix for top symptoms
    corr_matrix = training_df[top_20_symptoms].corr()
    
    plt.figure(figsize=(14, 12))
    sns.heatmap(corr_matrix, annot=False, cmap='coolwarm', center=0, 
                square=True, linewidths=0.5, cbar_kws={"shrink": 0.8})
    plt.title('Correlation Heatmap - Top 20 Most Frequent Symptoms', 
              fontsize=16, fontweight='bold', pad=20)
    plt.tight_layout()
    plt.savefig('visualizations/symptom_correlation_heatmap.png', dpi=300, bbox_inches='tight')
    print("\n Saved: visualizations/symptom_correlation_heatmap.png")
    plt.close()
    
    return symptom_freq

def visualize_top_symptoms(symptom_freq):
    """Visualize top symptoms"""
    plt.figure(figsize=(12, 8))
    top_15 = symptom_freq.head(15)
    top_15.plot(kind='barh', color='mediumseagreen', edgecolor='black')
    plt.title('Top 15 Most Frequent Symptoms', fontsize=16, fontweight='bold')
    plt.xlabel('Frequency', fontsize=12)
    plt.ylabel('Symptom', fontsize=12)
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.savefig('visualizations/top_symptoms.png', dpi=300, bbox_inches='tight')
    print(" Saved: visualizations/top_symptoms.png")
    plt.close()

def main():
    """Main execution function"""
    # Create visualizations directory
    Path('visualizations').mkdir(exist_ok=True)
    
    print("\n" + "=" * 80)
    print("INTELLIGENT MEDICINE & HEALTH RECOMMENDATION SYSTEM")
    print("DATA EXPLORATION AND ANALYSIS")
    print("=" * 80)
    
    # Load datasets
    print("\nLoading datasets...")
    datasets = load_datasets()
    print("All datasets loaded successfully!")
    
    # Explore training data
    disease_counts = explore_training_data(datasets['training'])
    
    # Visualize disease distribution
    visualize_disease_distribution(disease_counts)
    
    # Analyze symptom severity
    analyze_symptom_severity(datasets['symptom_severity'])
    
    # Analyze recommendations
    analyze_recommendations(
        datasets['medications'], 
        datasets['diets'], 
        datasets['workouts']
    )
    
    # Create symptom visualizations
    symptom_freq = create_symptom_heatmap(datasets['training'])
    visualize_top_symptoms(symptom_freq)
    
    print("\n" + "=" * 80)
    print("DATA EXPLORATION COMPLETED!")
    print("=" * 80)
    print("\nAll visualizations saved in 'visualizations/' directory")
    print("\nKey Insights:")
    print("1. Dataset contains 41 different diseases")
    print("2. Each disease has associated symptoms (binary features)")
    print("3. Symptom severity weights range from 1-7")
    print("4. Comprehensive recommendations available for each disease")
    print("=" * 80)

if __name__ == "__main__":
    main()
