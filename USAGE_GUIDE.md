# 📖 Complete Usage Guide

## Intelligent Medicine & Health Recommendation System

This guide provides detailed instructions on how to use every feature of the system.

---

## 🚀 Getting Started

### Option 1: Using Batch Files (Windows - Easiest)

Simply double-click the batch files in order:

1. **1_setup.bat** - Install dependencies
2. **2_train_model.bat** - Train the ML model
3. **3_launch_app.bat** - Start the web application

### Option 2: Using Command Line

```bash
# Step 1: Setup
python setup.py

# Step 2: Train Model
python model_training.py

# Step 3: Launch App
streamlit run app.py
```

---

## 📊 Module-by-Module Guide

### 1. Setup Script (`setup.py`)

**Purpose**: Automated environment setup

**What it does**:
- Checks Python version (requires 3.8+)
- Installs all dependencies
- Creates necessary directories
- Verifies dataset files
- Tests package imports

**How to run**:
```bash
python setup.py
```

**Expected output**:
```
✅ Python version is compatible!
✅ All dependencies installed successfully!
✅ Created directory: models/
✅ All 8 dataset files found!
✅ All packages imported successfully!
```

**Troubleshooting**:
- If Python version error: Upgrade to Python 3.8+
- If package install fails: Run `pip install --upgrade pip` first
- If dataset missing: Ensure all CSV files are in `datasets/` folder

---

### 2. Data Exploration (`data_exploration.py`)

**Purpose**: Analyze and visualize the medical dataset

**What it does**:
- Loads all 8 datasets
- Analyzes disease distribution
- Calculates symptom statistics
- Creates correlation heatmaps
- Generates visualizations

**How to run**:
```bash
python data_exploration.py
# Or double-click: 5_explore_data.bat
```

**Generated visualizations**:
1. `disease_distribution.png` - Bar chart of disease frequencies
2. `symptom_severity_distribution.png` - Severity weight distribution
3. `symptom_correlation_heatmap.png` - Top 20 symptom correlations
4. `top_symptoms.png` - Most frequent symptoms

**Key insights**:
- Total diseases: 41
- Total symptoms: 132
- Severity range: 1-7
- Most common symptoms: itching, skin_rash, vomiting

**Use cases**:
- Understanding the dataset
- Identifying patterns
- Preparing reports
- Academic presentations

---

### 3. Model Training (`model_training.py`)

**Purpose**: Train and evaluate machine learning models

**What it does**:
- Loads training data (4,920 records)
- Trains 6 different ML models
- Compares performance metrics
- Selects best model
- Saves trained model
- Generates performance report

**How to run**:
```bash
python model_training.py
# Or double-click: 2_train_model.bat
```

**Interactive prompts**:
```
Do you want to optimize the best model? (y/n):
```
- Type **n** for quick training (3 minutes)
- Type **y** for optimized model (10-15 minutes, better accuracy)

**Models trained**:
1. Random Forest Classifier ⭐ (Usually best)
2. XGBoost Classifier
3. Gradient Boosting Classifier
4. Support Vector Machine (SVM)
5. K-Nearest Neighbors (KNN)
6. Naive Bayes

**Output files**:
- `models/disease_predictor.pkl` - Trained model (45 MB)
- `models/label_encoder.pkl` - Label encoder
- `models/feature_names.pkl` - Feature names
- `model_performance_report.txt` - Detailed metrics
- `visualizations/model_comparison.png` - Performance chart
- `visualizations/confusion_matrix.png` - Confusion matrix
- `visualizations/feature_importance.png` - Top features

**Expected performance**:
```
Best Model: Random Forest
Test Accuracy: 98.5%
CV Score: 97.8%
Training Time: ~2 minutes
```

**Troubleshooting**:
- If memory error: Close other applications
- If slow training: Choose 'n' for optimization
- If accuracy low: Check dataset integrity

---

### 4. Recommendation Engine (`recommendation_engine.py`)

**Purpose**: Core prediction and recommendation system

**What it does**:
- Loads trained model
- Predicts diseases from symptoms
- Calculates severity scores
- Retrieves recommendations
- Generates comprehensive reports

**How to run**:
```bash
python recommendation_engine.py
```

**Test output**:
```
🔍 PREDICTION:
   Disease: Fungal infection
   Confidence: 98.5%

📊 TOP 3 PREDICTIONS:
   1. Fungal infection: 98.5%
   2. Allergy: 1.2%
   3. Drug Reaction: 0.3%

💊 MEDICATIONS:
   • Antifungal Cream
   • Fluconazole
   • Terbinafine

🥗 DIET RECOMMENDATIONS:
   • Antifungal Diet
   • Probiotics
   • Garlic
```

**API Usage** (for developers):
```python
from recommendation_engine import HealthRecommendationEngine

# Initialize
engine = HealthRecommendationEngine()
engine.load_model()
engine.load_recommendation_data()

# Predict
symptoms = {'itching': 1, 'skin_rash': 1}
report = engine.generate_comprehensive_report(symptoms)

# Access results
print(report['prediction']['disease'])
print(report['medications'])
print(report['diet'])
```

---

### 5. Model Explainability (`model_explainability.py`)

**Purpose**: Explain model predictions using SHAP

**What it does**:
- Creates SHAP explainer
- Analyzes feature contributions
- Generates waterfall plots
- Shows global feature importance

**How to run**:
```bash
python model_explainability.py
```

**Generated visualizations**:
- `shap_waterfall.png` - Individual prediction explanation
- `shap_summary.png` - Global feature importance

**Interpretation**:
- **Positive SHAP values** (green): Push prediction toward disease
- **Negative SHAP values** (red): Push prediction away from disease
- **Magnitude**: Strength of contribution

**Use cases**:
- Understanding why a prediction was made
- Identifying key symptoms
- Building trust in the model
- Medical validation

---

### 6. Web Application (`app.py`)

**Purpose**: Interactive user interface

**How to run**:
```bash
streamlit run app.py
# Or double-click: 3_launch_app.bat
```

**Access**: Open browser at `http://localhost:8501`

**Features**:

#### A. Symptom Selection
- **Search bar**: Type to filter symptoms
- **Checkboxes**: Select multiple symptoms
- **Counter**: Shows selected count
- **Clear button**: Reset all selections

**Tips**:
- Use search for quick finding
- Select all relevant symptoms
- More symptoms = better accuracy

#### B. Prediction Results
- **Disease name**: Primary diagnosis
- **Confidence score**: Prediction certainty (%)
- **Severity level**: Low/Moderate/High
- **Top-3 predictions**: Alternative diagnoses

#### C. Recommendations (Tabs)
1. **💊 Medications**: 5 recommended medicines
2. **🥗 Diet Plan**: Dietary suggestions
3. **🏃 Lifestyle**: Exercise and lifestyle tips
4. **⚕️ Precautions**: Safety measures

#### D. Report Export
- Click "Download Report as Text"
- Saves comprehensive health report
- Includes all predictions and recommendations
- Timestamped filename

**Keyboard shortcuts**:
- `Ctrl + R`: Refresh page
- `Ctrl + F`: Search symptoms
- `Esc`: Close dialogs

---

### 7. System Testing (`test_system.py`)

**Purpose**: Verify system integrity

**What it does**:
- Tests package imports
- Checks dataset availability
- Verifies data loading
- Tests model files
- Validates recommendation engine
- Checks documentation

**How to run**:
```bash
python test_system.py
# Or double-click: 4_test_system.bat
```

**Test results**:
```
✅ PASS - Package Imports
✅ PASS - Dataset Availability
✅ PASS - Data Loading
⚠️  SKIP - Model Files (needs training)
✅ PASS - Python Scripts
✅ PASS - Documentation
```

**When to run**:
- After initial setup
- Before training model
- After system updates
- When troubleshooting

---

## 🎯 Common Use Cases

### Use Case 1: Basic Disease Prediction

**Scenario**: Patient has itching and skin rash

**Steps**:
1. Launch app: `streamlit run app.py`
2. Search "itching" and check it
3. Search "skin_rash" and check it
4. Click "Get Diagnosis & Recommendations"
5. Review results and recommendations

**Expected result**: Fungal infection (95%+ confidence)

---

### Use Case 2: Multiple Symptom Analysis

**Scenario**: Patient has fever, cough, and fatigue

**Steps**:
1. Select symptoms: high_fever, cough, fatigue
2. Add more if present: breathlessness, chest_pain
3. Get diagnosis
4. Check Top-3 predictions
5. Compare confidence scores

**Possible results**: Pneumonia, Common Cold, or Bronchial Asthma

---

### Use Case 3: Severity Assessment

**Scenario**: Determine urgency of condition

**Steps**:
1. Enter all symptoms
2. Check severity score (1-7)
3. Note severity level:
   - **Low (1-2)**: Monitor at home
   - **Moderate (3-5)**: Consult doctor soon
   - **High (6-7)**: Seek immediate care

---

### Use Case 4: Lifestyle Recommendations

**Scenario**: Patient wants preventive care

**Steps**:
1. Get disease prediction
2. Go to "Lifestyle & Exercise" tab
3. Review workout recommendations
4. Go to "Diet Plan" tab
5. Note dietary suggestions
6. Download report for reference

---

### Use Case 5: Model Analysis

**Scenario**: Understand model decisions

**Steps**:
1. Train model: `python model_training.py`
2. Review performance report
3. Check confusion matrix
4. Run explainability: `python model_explainability.py`
5. Analyze SHAP plots

---

## 🔧 Advanced Usage

### Custom Symptom Input (API)

```python
from recommendation_engine import HealthRecommendationEngine

engine = HealthRecommendationEngine()
engine.load_model()
engine.load_recommendation_data()

# Custom symptoms
symptoms = {
    'fever': 1,
    'cough': 1,
    'fatigue': 1,
    'breathlessness': 1
}

# Get report
report = engine.generate_comprehensive_report(symptoms)

# Access specific data
disease = report['prediction']['disease']
confidence = report['prediction']['confidence']
medications = report['medications']
severity = report['severity']['level']

print(f"Disease: {disease}")
print(f"Confidence: {confidence:.1%}")
print(f"Severity: {severity}")
```

### Batch Predictions

```python
import pandas as pd
from recommendation_engine import HealthRecommendationEngine

engine = HealthRecommendationEngine()
engine.load_model()
engine.load_recommendation_data()

# Multiple patients
patients = [
    {'itching': 1, 'skin_rash': 1},
    {'fever': 1, 'cough': 1},
    {'headache': 1, 'nausea': 1}
]

# Process all
results = []
for symptoms in patients:
    report = engine.generate_comprehensive_report(symptoms)
    results.append({
        'disease': report['prediction']['disease'],
        'confidence': report['prediction']['confidence']
    })

df = pd.DataFrame(results)
print(df)
```

### Model Retraining

```python
# To retrain with different parameters
from model_training import DiseasePredictor

predictor = DiseasePredictor()
X, y_encoded, y = predictor.load_data()
X_train, X_test, y_train, y_test = predictor.split_data(X, y_encoded)

# Train with custom parameters
from sklearn.ensemble import RandomForestClassifier

custom_model = RandomForestClassifier(
    n_estimators=200,
    max_depth=30,
    random_state=42
)

custom_model.fit(X_train, y_train)
# Evaluate and save...
```

---

## 📈 Performance Optimization

### Speed Up Training
- Choose 'n' for optimization prompt
- Use fewer estimators (n_estimators=50)
- Reduce cross-validation folds (cv=3)

### Reduce Memory Usage
- Close other applications
- Use smaller sample for SHAP (sample_size=50)
- Clear visualizations folder

### Improve Accuracy
- Choose 'y' for optimization
- Increase n_estimators (200-300)
- Use ensemble methods

---

## 🐛 Troubleshooting Guide

### Issue: "Model not found"
**Solution**: Train the model first
```bash
python model_training.py
```

### Issue: "Package not found"
**Solution**: Install dependencies
```bash
pip install -r requirements.txt
```

### Issue: Streamlit won't start
**Solution**: Check port availability
```bash
streamlit run app.py --server.port 8502
```

### Issue: Low prediction confidence
**Possible causes**:
- Insufficient symptoms selected
- Ambiguous symptom combination
- Rare disease presentation

**Solution**: Add more specific symptoms

### Issue: Slow performance
**Solutions**:
- Close other applications
- Reduce visualization complexity
- Use faster model (Naive Bayes)

---

## 💡 Best Practices

### For Users
1. ✅ Select all relevant symptoms
2. ✅ Use search function efficiently
3. ✅ Review Top-3 predictions
4. ✅ Download reports for records
5. ✅ Consult healthcare professionals

### For Developers
1. ✅ Test after modifications
2. ✅ Document code changes
3. ✅ Validate data integrity
4. ✅ Monitor model performance
5. ✅ Keep dependencies updated

### For Researchers
1. ✅ Review model explainability
2. ✅ Analyze confusion matrix
3. ✅ Compare multiple models
4. ✅ Document findings
5. ✅ Validate with domain experts

---

## 📞 Getting Help

### Documentation
- **README.md**: Complete documentation
- **QUICKSTART.md**: Quick start guide
- **PROJECT_SUMMARY.md**: Project overview
- **This file**: Detailed usage guide

### Testing
- Run: `python test_system.py`
- Check error messages
- Review log files

### Common Questions

**Q: How accurate is the system?**
A: 98.5% test accuracy, but always consult doctors.

**Q: Can I add more diseases?**
A: Yes, add data to Training.csv and retrain.

**Q: Is it suitable for production?**
A: Educational purposes only, not for clinical use.

**Q: How to update recommendations?**
A: Edit CSV files in datasets/ folder.

---

## 🎓 Learning Resources

### Understanding the Code
- Read inline comments
- Check function docstrings
- Review module structure

### Machine Learning Concepts
- Random Forest: Ensemble of decision trees
- XGBoost: Gradient boosting framework
- SHAP: Model explanation method

### Healthcare Domain
- Symptom-disease relationships
- Medical terminology
- Treatment guidelines

---

## ⚠️ Important Reminders

1. **Not a diagnostic tool** - Educational only
2. **Consult professionals** - Always seek medical advice
3. **Data privacy** - No data is stored or transmitted
4. **Regular updates** - Keep dependencies current
5. **Ethical use** - Follow medical ethics guidelines

---

**Last Updated**: 2024
**Version**: 1.0.0

*For more information, see README.md*
