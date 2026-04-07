"""
Machine Learning Model Training Script
Trains multiple models for disease prediction and selects the best one
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

class DiseasePredictor:
    """Disease prediction model trainer and evaluator"""
    
    def __init__(self):
        self.models = {}
        self.best_model = None
        self.label_encoder = LabelEncoder()
        self.feature_names = None
        
    def load_data(self):
        """Load and prepare training data"""
        print("Loading training data...")
        df = pd.read_csv('datasets/Training.csv')
        
        # Separate features and target
        X = df.iloc[:, :-1]
        y = df.iloc[:, -1]
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Encode target labels
        y_encoded = self.label_encoder.fit_transform(y)
        
        print(f" Data loaded: {X.shape[0]} samples, {X.shape[1]} features")
        print(f" Number of classes: {len(self.label_encoder.classes_)}")
        
        return X, y_encoded, y
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state, stratify=y
        )
        print(f" Data split: {len(X_train)} train, {len(X_test)} test samples")
        return X_train, X_test, y_train, y_test
    
    def initialize_models(self):
        """Initialize multiple ML models"""
        self.models = {
            'Random Forest': RandomForestClassifier(
                n_estimators=100, 
                random_state=42, 
                n_jobs=-1
            ),
            'Gradient Boosting': GradientBoostingClassifier(
                n_estimators=100, 
                random_state=42
            ),
            'XGBoost': xgb.XGBClassifier(
                n_estimators=100,
                random_state=42,
                eval_metric='mlogloss',
                use_label_encoder=False
            ),
            'SVM': SVC(
                kernel='rbf',
                random_state=42,
                probability=True
            ),
            'K-Nearest Neighbors': KNeighborsClassifier(
                n_neighbors=5
            ),
            'Naive Bayes': GaussianNB()
        }
        print(f" Initialized {len(self.models)} models")
    
    def train_and_evaluate(self, X_train, X_test, y_train, y_test):
        """Train all models and evaluate performance"""
        results = {}
        
        print("\n" + "=" * 80)
        print("TRAINING AND EVALUATING MODELS")
        print("=" * 80)
        
        for name, model in self.models.items():
            print(f"\nTraining {name}...")
            
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred_train = model.predict(X_train)
            y_pred_test = model.predict(X_test)
            
            # Calculate accuracies
            train_acc = accuracy_score(y_train, y_pred_train)
            test_acc = accuracy_score(y_test, y_pred_test)
            
            # Cross-validation score
            cv_scores = cross_val_score(model, X_train, y_train, cv=5)
            cv_mean = cv_scores.mean()
            
            results[name] = {
                'model': model,
                'train_accuracy': train_acc,
                'test_accuracy': test_acc,
                'cv_score': cv_mean,
                'cv_std': cv_scores.std()
            }
            
            print(f"  Train Accuracy: {train_acc:.4f}")
            print(f"  Test Accuracy:  {test_acc:.4f}")
            print(f"  CV Score:       {cv_mean:.4f} (+/- {cv_scores.std():.4f})")
        
        return results
    
    def select_best_model(self, results):
        """Select the best performing model"""
        best_name = max(results, key=lambda x: results[x]['test_accuracy'])
        self.best_model = results[best_name]['model']
        
        print("\n" + "=" * 80)
        print("BEST MODEL SELECTION")
        print("=" * 80)
        print(f"\nBest Model: {best_name}")
        print(f"Test Accuracy: {results[best_name]['test_accuracy']:.4f}")
        print(f"CV Score: {results[best_name]['cv_score']:.4f}")
        
        return best_name, results[best_name]
    
    def optimize_best_model(self, X_train, y_train):
        """Optimize the best model using GridSearchCV"""
        print("\n" + "=" * 80)
        print("OPTIMIZING BEST MODEL")
        print("=" * 80)
        
        # Define parameter grid for Random Forest (typically the best)
        param_grid = {
            'n_estimators': [100, 200, 300],
            'max_depth': [10, 20, 30, None],
            'min_samples_split': [2, 5, 10],
            'min_samples_leaf': [1, 2, 4]
        }
        
        print("\nPerforming Grid Search (this may take a few minutes)...")
        grid_search = GridSearchCV(
            RandomForestClassifier(random_state=42, n_jobs=-1),
            param_grid,
            cv=3,
            scoring='accuracy',
            n_jobs=-1,
            verbose=1
        )
        
        grid_search.fit(X_train, y_train)
        
        print(f"\n Best Parameters: {grid_search.best_params_}")
        print(f" Best CV Score: {grid_search.best_score_:.4f}")
        
        self.best_model = grid_search.best_estimator_
        return grid_search.best_estimator_
    
    def visualize_results(self, results, X_test, y_test):
        """Create visualizations of model performance"""
        Path('visualizations').mkdir(exist_ok=True)
        
        # 1. Model comparison bar chart
        plt.figure(figsize=(12, 6))
        model_names = list(results.keys())
        test_accs = [results[m]['test_accuracy'] for m in model_names]
        cv_scores = [results[m]['cv_score'] for m in model_names]
        
        x = np.arange(len(model_names))
        width = 0.35
        
        plt.bar(x - width/2, test_accs, width, label='Test Accuracy', color='steelblue')
        plt.bar(x + width/2, cv_scores, width, label='CV Score', color='coral')
        
        plt.xlabel('Model', fontsize=12)
        plt.ylabel('Accuracy', fontsize=12)
        plt.title('Model Performance Comparison', fontsize=16, fontweight='bold')
        plt.xticks(x, model_names, rotation=45, ha='right')
        plt.legend()
        plt.ylim(0.8, 1.0)
        plt.tight_layout()
        plt.savefig('visualizations/model_comparison.png', dpi=300, bbox_inches='tight')
        print("\n Saved: visualizations/model_comparison.png")
        plt.close()
        
        # 2. Confusion Matrix for best model
        y_pred = self.best_model.predict(X_test)
        cm = confusion_matrix(y_test, y_pred)
        
        plt.figure(figsize=(16, 14))
        sns.heatmap(cm, annot=False, fmt='d', cmap='Blues', square=True,
                    xticklabels=self.label_encoder.classes_,
                    yticklabels=self.label_encoder.classes_)
        plt.title('Confusion Matrix - Best Model', fontsize=16, fontweight='bold')
        plt.ylabel('True Label', fontsize=12)
        plt.xlabel('Predicted Label', fontsize=12)
        plt.xticks(rotation=45, ha='right', fontsize=8)
        plt.yticks(rotation=0, fontsize=8)
        plt.tight_layout()
        plt.savefig('visualizations/confusion_matrix.png', dpi=300, bbox_inches='tight')
        print(" Saved: visualizations/confusion_matrix.png")
        plt.close()
        
        # 3. Feature importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            importances = self.best_model.feature_importances_
            indices = np.argsort(importances)[-20:]  # Top 20 features
            
            plt.figure(figsize=(10, 8))
            plt.barh(range(len(indices)), importances[indices], color='mediumseagreen')
            plt.yticks(range(len(indices)), [self.feature_names[i] for i in indices])
            plt.xlabel('Importance', fontsize=12)
            plt.title('Top 20 Feature Importances', fontsize=16, fontweight='bold')
            plt.tight_layout()
            plt.savefig('visualizations/feature_importance.png', dpi=300, bbox_inches='tight')
            print(" Saved: visualizations/feature_importance.png")
            plt.close()
    
    def generate_classification_report(self, X_test, y_test):
        """Generate detailed classification report"""
        y_pred = self.best_model.predict(X_test)
        
        print("\n" + "=" * 80)
        print("CLASSIFICATION REPORT")
        print("=" * 80)
        
        report = classification_report(
            y_test, 
            y_pred, 
            target_names=self.label_encoder.classes_,
            zero_division=0
        )
        print(report)
        
        # Save report to file
        with open('model_performance_report.txt', 'w') as f:
            f.write("DISEASE PREDICTION MODEL - CLASSIFICATION REPORT\n")
            f.write("=" * 80 + "\n\n")
            f.write(report)
        
        print("\n Saved: model_performance_report.txt")
    
    def save_model(self):
        """Save the trained model and label encoder"""
        Path('models').mkdir(exist_ok=True)
        
        joblib.dump(self.best_model, 'models/disease_predictor.pkl')
        joblib.dump(self.label_encoder, 'models/label_encoder.pkl')
        joblib.dump(self.feature_names, 'models/feature_names.pkl')
        
        print("\n Model saved: models/disease_predictor.pkl")
        print(" Label encoder saved: models/label_encoder.pkl")
        print(" Feature names saved: models/feature_names.pkl")

def main():
    """Main execution function"""
    print("\n" + "=" * 80)
    print("INTELLIGENT MEDICINE & HEALTH RECOMMENDATION SYSTEM")
    print("MACHINE LEARNING MODEL TRAINING")
    print("=" * 80)
    
    # Initialize predictor
    predictor = DiseasePredictor()
    
    # Load data
    X, y_encoded, y_original = predictor.load_data()
    
    # Split data
    X_train, X_test, y_train, y_test = predictor.split_data(X, y_encoded)
    
    # Initialize models
    predictor.initialize_models()
    
    # Train and evaluate all models
    results = predictor.train_and_evaluate(X_train, X_test, y_train, y_test)
    
    # Select best model
    best_name, best_result = predictor.select_best_model(results)
    
    # Optimize best model (optional - can be time-consuming)
    optimize = input("\nDo you want to optimize the best model? (y/n): ").lower()
    if optimize == 'y':
        predictor.optimize_best_model(X_train, y_train)
    
    # Visualize results
    print("\nGenerating visualizations...")
    predictor.visualize_results(results, X_test, y_test)
    
    # Generate classification report
    predictor.generate_classification_report(X_test, y_test)
    
    # Save model
    predictor.save_model()
    
    print("\n" + "=" * 80)
    print("MODEL TRAINING COMPLETED SUCCESSFULLY!")
    print("=" * 80)
    print("\nNext Steps:")
    print("1. Review visualizations in 'visualizations/' directory")
    print("2. Check model performance in 'model_performance_report.txt'")
    print("3. Run the Streamlit app: streamlit run app.py")
    print("=" * 80)

if __name__ == "__main__":
    main()
