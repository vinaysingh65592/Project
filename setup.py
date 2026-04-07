"""
Setup Script for Medicine & Health Recommendation System
Automates the setup process
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    """Print formatted header"""
    print("\n" + "=" * 80)
    print(text.center(80))
    print("=" * 80 + "\n")

def print_step(step_num, text):
    """Print step information"""
    print(f"\n{'='*80}")
    print(f"STEP {step_num}: {text}")
    print(f"{'='*80}\n")

def check_python_version():
    """Check if Python version is compatible"""
    print_step(1, "Checking Python Version")
    
    version = sys.version_info
    print(f"Current Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Error: Python 3.8 or higher is required!")
        print("Please upgrade your Python installation.")
        return False
    
    print("✅ Python version is compatible!")
    return True

def install_dependencies():
    """Install required packages"""
    print_step(2, "Installing Dependencies")
    
    print("Installing packages from requirements.txt...")
    print("This may take a few minutes...\n")
    
    try:
        subprocess.check_call([
            sys.executable, 
            "-m", 
            "pip", 
            "install", 
            "-r", 
            "requirements.txt",
            "--quiet"
        ])
        print("\n✅ All dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error installing dependencies: {e}")
        return False

def create_directories():
    """Create necessary directories"""
    print_step(3, "Creating Project Directories")
    
    directories = ['models', 'visualizations']
    
    for directory in directories:
        path = Path(directory)
        if not path.exists():
            path.mkdir(parents=True)
            print(f"✅ Created directory: {directory}/")
        else:
            print(f"✓ Directory already exists: {directory}/")
    
    return True

def verify_datasets():
    """Verify that all datasets are present"""
    print_step(4, "Verifying Datasets")
    
    required_datasets = [
        'Training.csv',
        'description.csv',
        'medications.csv',
        'diets.csv',
        'precautions_df.csv',
        'workout_df.csv',
        'Symptom-severity.csv',
        'symtoms_df.csv'
    ]
    
    datasets_path = Path('datasets')
    
    if not datasets_path.exists():
        print("❌ Error: 'datasets' folder not found!")
        return False
    
    missing_files = []
    for dataset in required_datasets:
        if not (datasets_path / dataset).exists():
            missing_files.append(dataset)
    
    if missing_files:
        print("❌ Missing dataset files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    print(f"✅ All {len(required_datasets)} dataset files found!")
    return True

def test_imports():
    """Test if all required packages can be imported"""
    print_step(5, "Testing Package Imports")
    
    packages = [
        ('pandas', 'pandas'),
        ('numpy', 'numpy'),
        ('sklearn', 'scikit-learn'),
        ('xgboost', 'xgboost'),
        ('streamlit', 'streamlit'),
        ('matplotlib', 'matplotlib'),
        ('seaborn', 'seaborn'),
        ('plotly', 'plotly'),
        ('shap', 'shap'),
        ('joblib', 'joblib')
    ]
    
    failed_imports = []
    
    for import_name, package_name in packages:
        try:
            __import__(import_name)
            print(f"✅ {package_name}")
        except ImportError:
            print(f"❌ {package_name}")
            failed_imports.append(package_name)
    
    if failed_imports:
        print(f"\n❌ Failed to import: {', '.join(failed_imports)}")
        return False
    
    print("\n✅ All packages imported successfully!")
    return True

def display_next_steps():
    """Display next steps for the user"""
    print_header("SETUP COMPLETED SUCCESSFULLY!")
    
    print("""
🎉 Your Medicine & Health Recommendation System is ready to use!

📋 NEXT STEPS:

1️⃣  EXPLORE THE DATA (Optional - 2 minutes)
   Run: python data_exploration.py
   
   This will generate visualizations showing:
   - Disease distribution
   - Symptom correlations
   - Data statistics

2️⃣  TRAIN THE MODEL (Required - 3-5 minutes)
   Run: python model_training.py
   
   This will:
   - Train 6 different ML models
   - Compare their performance
   - Save the best model
   - Generate performance reports
   
   Note: When asked about optimization, type 'n' for quick training
         or 'y' for better accuracy (takes longer)

3️⃣  LAUNCH THE WEB APP (Required)
   Run: streamlit run app.py
   
   This will:
   - Start the interactive web interface
   - Open in your browser at http://localhost:8501
   - Allow you to make predictions and get recommendations

4️⃣  OPTIONAL FEATURES:

   Test Recommendation Engine:
   Run: python recommendation_engine.py
   
   Generate SHAP Explanations:
   Run: python model_explainability.py

📚 DOCUMENTATION:
   - README.md - Complete documentation
   - QUICKSTART.md - Quick start guide
   - index.html - Project overview page

⚠️  IMPORTANT REMINDER:
   This system is for educational purposes only.
   Always consult healthcare professionals for medical advice.

""")
    
    print("=" * 80)
    print("Ready to start? Run: python model_training.py")
    print("=" * 80 + "\n")

def main():
    """Main setup function"""
    print_header("MEDICINE & HEALTH RECOMMENDATION SYSTEM - SETUP")
    
    print("""
Welcome! This script will set up your environment for the
Intelligent Medicine & Health Recommendation System.

The setup process includes:
1. Checking Python version
2. Installing dependencies
3. Creating necessary directories
4. Verifying datasets
5. Testing package imports

This will take approximately 3-5 minutes.
""")
    
    input("Press Enter to continue...")
    
    # Run setup steps
    steps = [
        ("Checking Python version", check_python_version),
        ("Installing dependencies", install_dependencies),
        ("Creating directories", create_directories),
        ("Verifying datasets", verify_datasets),
        ("Testing imports", test_imports)
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Setup failed at: {step_name}")
            print("Please fix the errors above and run setup again.")
            sys.exit(1)
    
    # Display next steps
    display_next_steps()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error during setup: {e}")
        sys.exit(1)
