"""
System Testing Script
Tests all components of the Medicine & Health Recommendation System
"""

import sys
import os
from pathlib import Path
import warnings
warnings.filterwarnings('ignore')

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def test_imports():
    """Test if all required packages are available"""
    print_header("TEST 1: Package Imports")
    
    packages = {
        'pandas': 'Data manipulation',
        'numpy': 'Numerical computing',
        'sklearn': 'Machine learning',
        'xgboost': 'Gradient boosting',
        'streamlit': 'Web framework',
        'matplotlib': 'Plotting',
        'seaborn': 'Statistical visualization',
        'plotly': 'Interactive charts',
        'shap': 'Model explainability',
        'joblib': 'Model serialization'
    }
    
    failed = []
    passed = []
    
    for package, description in packages.items():
        try:
            __import__(package)
            print(f"✅ {package:15} - {description}")
            passed.append(package)
        except ImportError:
            print(f"❌ {package:15} - {description}")
            failed.append(package)
    
    print(f"\nResult: {len(passed)}/{len(packages)} packages available")
    
    if failed:
        print(f"Failed: {', '.join(failed)}")
        return False
    return True

def test_datasets():
    """Test if all datasets are present and readable"""
    print_header("TEST 2: Dataset Availability")
    
    datasets = {
        'Training.csv': 'Main training data',
        'description.csv': 'Disease descriptions',
        'medications.csv': 'Medicine recommendations',
        'diets.csv': 'Diet plans',
        'precautions_df.csv': 'Safety precautions',
        'workout_df.csv': 'Lifestyle tips',
        'Symptom-severity.csv': 'Symptom weights',
        'symtoms_df.csv': 'Additional symptom data'
    }
    
    datasets_path = Path('datasets')
    
    if not datasets_path.exists():
        print("❌ 'datasets' folder not found!")
        return False
    
    failed = []
    passed = []
    
    for dataset, description in datasets.items():
        file_path = datasets_path / dataset
        if file_path.exists():
            size_kb = file_path.stat().st_size / 1024
            print(f"✅ {dataset:25} - {description:30} ({size_kb:.1f} KB)")
            passed.append(dataset)
        else:
            print(f"❌ {dataset:25} - {description}")
            failed.append(dataset)
    
    print(f"\nResult: {len(passed)}/{len(datasets)} datasets available")
    
    if failed:
        print(f"Missing: {', '.join(failed)}")
        return False
    return True

def test_data_loading():
    """Test if datasets can be loaded"""
    print_header("TEST 3: Data Loading")
    
    try:
        import pandas as pd
        
        # Test loading main dataset
        print("Loading Training.csv...")
        df = pd.read_csv('datasets/Training.csv')
        print(f"✅ Loaded {len(df)} records with {len(df.columns)} columns")
        
        # Test loading recommendation data
        print("Loading recommendation datasets...")
        desc = pd.read_csv('datasets/description.csv')
        meds = pd.read_csv('datasets/medications.csv')
        diets = pd.read_csv('datasets/diets.csv')
        
        print(f"✅ Descriptions: {len(desc)} diseases")
        print(f"✅ Medications: {len(meds)} diseases")
        print(f"✅ Diets: {len(diets)} diseases")
        
        return True
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return False

def test_model_files():
    """Test if model files exist"""
    print_header("TEST 4: Model Files")
    
    models_path = Path('models')
    
    if not models_path.exists():
        print("⚠️  'models' folder not found - Model needs to be trained")
        print("   Run: python model_training.py")
        return None  # Not a failure, just needs training
    
    model_files = {
        'disease_predictor.pkl': 'Trained ML model',
        'label_encoder.pkl': 'Label encoder',
        'feature_names.pkl': 'Feature names'
    }
    
    all_present = True
    for file, description in model_files.items():
        file_path = models_path / file
        if file_path.exists():
            size_mb = file_path.stat().st_size / (1024 * 1024)
            print(f"✅ {file:25} - {description:20} ({size_mb:.1f} MB)")
        else:
            print(f"⚠️  {file:25} - {description}")
            all_present = False
    
    if not all_present:
        print("\n⚠️  Some model files missing - Train the model first")
        print("   Run: python model_training.py")
        return None
    
    return True

def test_recommendation_engine():
    """Test recommendation engine functionality"""
    print_header("TEST 5: Recommendation Engine")
    
    # Check if model exists first
    if not Path('models/disease_predictor.pkl').exists():
        print("⚠️  Model not trained yet - Skipping this test")
        print("   Run: python model_training.py first")
        return None
    
    try:
        from recommendation_engine import HealthRecommendationEngine
        
        print("Initializing recommendation engine...")
        engine = HealthRecommendationEngine()
        
        print("Loading model...")
        if not engine.load_model():
            print("❌ Failed to load model")
            return False
        print("✅ Model loaded successfully")
        
        print("Loading recommendation data...")
        if not engine.load_recommendation_data():
            print("❌ Failed to load recommendation data")
            return False
        print("✅ Recommendation data loaded")
        
        # Test prediction
        print("\nTesting prediction with sample symptoms...")
        test_symptoms = {
            'itching': 1,
            'skin_rash': 1,
            'nodal_skin_eruptions': 1
        }
        
        disease, confidence, top_3 = engine.predict_disease(test_symptoms)
        print(f"✅ Prediction: {disease} (Confidence: {confidence:.1%})")
        
        # Test recommendations
        print("\nTesting recommendation generation...")
        report = engine.generate_comprehensive_report(test_symptoms)
        
        print(f"✅ Medications: {len(report['medications'])} items")
        print(f"✅ Diet: {len(report['diet'])} items")
        print(f"✅ Workouts: {len(report['workouts'])} items")
        print(f"✅ Precautions: {len(report['precautions'])} items")
        
        return True
    except Exception as e:
        print(f"❌ Error testing recommendation engine: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_scripts():
    """Test if all Python scripts are present"""
    print_header("TEST 6: Python Scripts")
    
    scripts = {
        'app.py': 'Streamlit web application',
        'model_training.py': 'Model training script',
        'recommendation_engine.py': 'Recommendation engine',
        'data_exploration.py': 'Data exploration',
        'model_explainability.py': 'SHAP explainability',
        'setup.py': 'Setup script',
        'test_system.py': 'This test script'
    }
    
    all_present = True
    for script, description in scripts.items():
        if Path(script).exists():
            print(f"✅ {script:30} - {description}")
        else:
            print(f"❌ {script:30} - {description}")
            all_present = False
    
    return all_present

def test_documentation():
    """Test if documentation files are present"""
    print_header("TEST 7: Documentation")
    
    docs = {
        'README.md': 'Main documentation',
        'QUICKSTART.md': 'Quick start guide',
        'PROJECT_SUMMARY.md': 'Project summary',
        'requirements.txt': 'Dependencies list',
        'index.html': 'Landing page'
    }
    
    all_present = True
    for doc, description in docs.items():
        if Path(doc).exists():
            print(f"✅ {doc:30} - {description}")
        else:
            print(f"❌ {doc:30} - {description}")
            all_present = False
    
    return all_present

def display_summary(results):
    """Display test summary"""
    print_header("TEST SUMMARY")
    
    total_tests = len(results)
    passed = sum(1 for r in results.values() if r is True)
    failed = sum(1 for r in results.values() if r is False)
    skipped = sum(1 for r in results.values() if r is None)
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⚠️  Skipped: {skipped}")
    
    print("\nDetailed Results:")
    for test_name, result in results.items():
        if result is True:
            status = "✅ PASS"
        elif result is False:
            status = "❌ FAIL"
        else:
            status = "⚠️  SKIP"
        print(f"  {status} - {test_name}")
    
    print("\n" + "=" * 80)
    
    if failed > 0:
        print("❌ SOME TESTS FAILED")
        print("\nPlease fix the issues above before proceeding.")
    elif skipped > 0:
        print("⚠️  SYSTEM PARTIALLY READY")
        print("\nSome components need to be set up:")
        if results.get('Model Files') is None:
            print("  • Run: python model_training.py")
    else:
        print("✅ ALL TESTS PASSED - SYSTEM READY!")
        print("\nYou can now:")
        print("  • Run: streamlit run app.py")
        print("  • Or explore: python data_exploration.py")
    
    print("=" * 80)

def main():
    """Main test function"""
    print_header("MEDICINE & HEALTH RECOMMENDATION SYSTEM - SYSTEM TEST")
    
    print("""
This script will test all components of the system to ensure
everything is properly set up and working correctly.

Running comprehensive tests...
""")
    
    # Run all tests
    results = {}
    
    results['Package Imports'] = test_imports()
    results['Dataset Availability'] = test_datasets()
    results['Data Loading'] = test_data_loading()
    results['Model Files'] = test_model_files()
    results['Recommendation Engine'] = test_recommendation_engine()
    results['Python Scripts'] = test_scripts()
    results['Documentation'] = test_documentation()
    
    # Display summary
    display_summary(results)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during testing: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
