"""
Recommendation Engine
Provides personalized medicine, diet, workout, and precaution recommendations
"""

import pandas as pd
import numpy as np
import joblib
import ast
import difflib
from pathlib import Path

class HealthRecommendationEngine:
    """Engine for generating health recommendations based on predicted disease"""
    
    def __init__(self):
        self.model = None
        self.label_encoder = None
        self.feature_names = None
        self.feature_index = {}  # name -> index for O(1) lookup
        self._sorted_symptoms = None  # cached sorted list
        self.recommendations_data = {}
        self.symptom_severity = {}
        self.lookup_cache = {}
        
    def load_model(self):
        """Load trained model and encoders"""
        try:
            self.model = joblib.load('models/disease_predictor.pkl')
            self.label_encoder = joblib.load('models/label_encoder.pkl')
            self.feature_names = joblib.load('models/feature_names.pkl')
            # Build index map for O(1) feature lookup
            self.feature_index = {name: i for i, name in enumerate(self.feature_names)}
            self._sorted_symptoms = sorted(self.feature_names)
            print("Model loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
    
    def load_recommendation_data(self):
        """Load all recommendation datasets"""
        try:
            data_path = Path('datasets')
            
            # Load recommendation data
            self.recommendations_data['description'] = pd.read_csv(
                data_path / 'description.csv'
            )
            self.recommendations_data['medications'] = pd.read_csv(
                data_path / 'medications.csv'
            )
            self.recommendations_data['diets'] = pd.read_csv(
                data_path / 'diets.csv'
            )
            self.recommendations_data['precautions'] = pd.read_csv(
                data_path / 'precautions_df.csv'
            )
            self.recommendations_data['workouts'] = pd.read_csv(
                data_path / 'workout_df.csv'
            )
            
            # Load symptom severity
            severity_df = pd.read_csv(data_path / 'Symptom-severity.csv')
            self.symptom_severity = dict(zip(
                severity_df['Symptom'], 
                severity_df['weight']
            ))
            
            # Pre-calculate normalized lookups for performance
            self._prepare_lookup_cache()
            
            print("Recommendation data loaded successfully")
            return True
        except Exception as e:
            print(f"Error loading recommendation data: {e}")
            return False

    def _prepare_lookup_cache(self):
        """Pre-normalize disease columns and create lookups"""
        for key, df in self.recommendations_data.items():
            # Standardize column name
            disease_col = "Disease" if "Disease" in df.columns else "disease"
            if disease_col not in df.columns:
                # Try to find it
                for col in df.columns:
                    if col.lower() == "disease":
                        disease_col = col
                        break
            
            if disease_col in df.columns:
                # Create a normalized version of the disease column
                df['_norm_disease'] = df[disease_col].astype(str).str.strip().str.lower()
                # Create a lookup for fast access
                self.lookup_cache[key] = {
                    'col': disease_col,
                    'mapping': {val: idx for idx, val in enumerate(df['_norm_disease'])}
                }
    
    def predict_disease(self, symptoms_dict):
        """
        Predict disease based on symptoms
        
        Args:
            symptoms_dict: Dictionary with symptom names as keys and 1/0 as values
        
        Returns:
            Tuple of (predicted_disease, probability, top_3_predictions)
        """
        # Create feature vector using O(1) index lookup
        feature_vector = np.zeros(len(self.feature_names))
        
        for symptom, value in symptoms_dict.items():
            idx = self.feature_index.get(symptom)
            if idx is not None:
                feature_vector[idx] = value
        
        # Reshape for prediction
        feature_vector = feature_vector.reshape(1, -1)
        
        # Predict
        prediction = self.model.predict(feature_vector)[0]
        probabilities = self.model.predict_proba(feature_vector)[0]
        
        # Get disease name
        disease_name = self.label_encoder.inverse_transform([prediction])[0]
        disease_probability = probabilities[prediction]
        
        # Get top 3 predictions
        top_3_indices = np.argsort(probabilities)[-3:][::-1]
        top_3_diseases = self.label_encoder.inverse_transform(top_3_indices)
        top_3_probs = probabilities[top_3_indices]
        
        top_3_predictions = [
            {'disease': disease, 'probability': float(prob)}
            for disease, prob in zip(top_3_diseases, top_3_probs)
        ]
        
        return disease_name, float(disease_probability), top_3_predictions
    
    def calculate_severity_score(self, symptoms_dict):
        """Calculate overall severity score based on symptoms"""
        total_severity = 0
        symptom_count = 0
        
        for symptom, value in symptoms_dict.items():
            if value == 1 and symptom in self.symptom_severity:
                total_severity += self.symptom_severity[symptom]
                symptom_count += 1
        
        if symptom_count == 0:
            return 0, "Low"
        
        avg_severity = total_severity / symptom_count
        
        # Categorize severity
        if avg_severity < 3:
            severity_level = "Low"
        elif avg_severity < 5:
            severity_level = "Moderate"
        else:
            severity_level = "High"
        
        return round(avg_severity, 2), severity_level

    def _normalize_text(self, value):
        if value is None:
            return ""
        return str(value).strip().lower()

    def _resolve_column(self, df, preferred_name):
        if preferred_name in df.columns:
            return preferred_name

        preferred_lower = preferred_name.lower()
        for c in df.columns:
            if str(c).lower() == preferred_lower:
                return c
        return None

    def _find_disease_rows(self, key, disease):
        """Optimized disease lookup using cache"""
        if key not in self.recommendations_data or key not in self.lookup_cache:
            return pd.DataFrame()

        df = self.recommendations_data[key]
        cache = self.lookup_cache[key]
        target = self._normalize_text(disease)
        
        # Check cache first
        if target in cache['mapping']:
            idx = cache['mapping'][target]
            return df.iloc[[idx]]

        # Fallback to fuzzy if no exact match (less frequent now)
        choices = list(cache['mapping'].keys())
        match = difflib.get_close_matches(target, choices, n=1, cutoff=0.75)
        if match:
            idx = cache['mapping'][match[0]]
            return df.iloc[[idx]]

        return df.iloc[0:0]
    
    def get_disease_description(self, disease):
        """Get disease description"""
        result = self._find_disease_rows('description', disease)
        
        if not result.empty:
            desc_col = self._resolve_column(result, "Description")
            if desc_col is None:
                return "Description not available."
            return result.iloc[0][desc_col]
        return "Description not available."
    
    def get_medications(self, disease):
        """Get medication recommendations"""
        result = self._find_disease_rows('medications', disease)
        
        if not result.empty:
            med_col = self._resolve_column(result, "Medication")
            if med_col is None:
                return []
            medications_str = result.iloc[0][med_col]
            if pd.isna(medications_str):
                return []
            try:
                # Parse the string representation of list
                medications = ast.literal_eval(medications_str)
                return medications
            except:
                return [medications_str]
        return []
    
    def get_diet_recommendations(self, disease):
        """Get diet recommendations"""
        result = self._find_disease_rows('diets', disease)
        
        if not result.empty:
            diet_col = self._resolve_column(result, "Diet")
            if diet_col is None:
                return []
            diet_str = result.iloc[0][diet_col]
            if pd.isna(diet_str):
                return []
            try:
                diets = ast.literal_eval(diet_str)
                return diets
            except:
                return [diet_str]
        return []
    
    def get_workout_recommendations(self, disease):
        """Get workout/lifestyle recommendations"""
        result = self._find_disease_rows('workouts', disease)
        
        if not result.empty:
            workout_col = self._resolve_column(result, "workout")
            if workout_col is None:
                return []
            workouts = result[workout_col].dropna().astype(str).tolist()
            return workouts
        return []
    
    def get_precautions(self, disease):
        """Get precaution recommendations"""
        result = self._find_disease_rows('precautions', disease)
        
        if not result.empty:
            precautions = []
            for i in range(1, 5):
                col_name = f'Precaution_{i}'
                if col_name in result.columns:
                    precaution = result.iloc[0][col_name]
                    if pd.notna(precaution) and str(precaution).strip():
                        precautions.append(precaution)
            return precautions
        return []
    
    def generate_comprehensive_report(self, symptoms_dict):
        """
        Generate comprehensive health report with all recommendations
        
        Args:
            symptoms_dict: Dictionary with symptom names as keys and 1/0 as values
        
        Returns:
            Dictionary containing all recommendations
        """
        # Predict disease
        disease, probability, top_3 = self.predict_disease(symptoms_dict)
        
        # Calculate severity
        severity_score, severity_level = self.calculate_severity_score(symptoms_dict)
        
        # Get active symptoms
        active_symptoms = [s for s, v in symptoms_dict.items() if v == 1]
        
        # Generate report
        report = {
            'prediction': {
                'disease': disease,
                'confidence': probability,
                'top_3_predictions': top_3
            },
            'severity': {
                'score': severity_score,
                'level': severity_level
            },
            'symptoms': {
                'active_symptoms': active_symptoms,
                'count': len(active_symptoms)
            },
            'description': self.get_disease_description(disease),
            'medications': self.get_medications(disease),
            'diet': self.get_diet_recommendations(disease),
            'workouts': self.get_workout_recommendations(disease),
            'precautions': self.get_precautions(disease)
        }
        
        return report
    
    def get_symptom_suggestions(self, partial_symptom):
        """Get symptom suggestions based on partial input"""
        suggestions = [
            symptom for symptom in self.feature_names 
            if partial_symptom.lower() in symptom.lower()
        ]
        return suggestions[:10]  # Return top 10 matches
    
    def get_all_symptoms(self):
        """Get list of all available symptoms (cached sorted)"""
        return self._sorted_symptoms if self._sorted_symptoms else self.feature_names

def test_recommendation_engine():
    """Test the recommendation engine"""
    print("\n" + "=" * 80)
    print("TESTING RECOMMENDATION ENGINE")
    print("=" * 80)
    
    # Initialize engine
    engine = HealthRecommendationEngine()
    
    # Load model and data
    if not engine.load_model():
        print("Failed to load model. Please train the model first.")
        return
    
    if not engine.load_recommendation_data():
        print("Failed to load recommendation data.")
        return
    
    # Test with sample symptoms
    print("\nTest Case: Patient with itching, skin_rash, and nodal_skin_eruptions")
    
    test_symptoms = {
        'itching': 1,
        'skin_rash': 1,
        'nodal_skin_eruptions': 1
    }
    
    # Generate report
    report = engine.generate_comprehensive_report(test_symptoms)
    
    # Display report
    print("\n" + "-" * 80)
    print("HEALTH RECOMMENDATION REPORT")
    print("-" * 80)
    
    print("\nPREDICTION:")
    print(f"   Disease: {report['prediction']['disease']}")
    print(f"   Confidence: {report['prediction']['confidence']:.2%}")
    
    print("\nTOP 3 PREDICTIONS:")
    for i, pred in enumerate(report['prediction']['top_3_predictions'], 1):
        print(f"   {i}. {pred['disease']}: {pred['probability']:.2%}")
    
    print("\nSEVERITY:")
    print(f"   Score: {report['severity']['score']}")
    print(f"   Level: {report['severity']['level']}")
    
    print("\nDESCRIPTION:")
    print(f"   {report['description']}")
    
    print("\nMEDICATIONS:")
    for med in report['medications']:
        print(f"   - {med}")
    
    print("\nDIET RECOMMENDATIONS:")
    for diet in report['diet']:
        print(f"   - {diet}")
    
    print("\nWORKOUT/LIFESTYLE:")
    for workout in report['workouts'][:5]:  # Show first 5
        print(f"   - {workout}")
    
    print("\nPRECAUTIONS:")
    for precaution in report['precautions']:
        print(f"   - {precaution}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETED SUCCESSFULLY!")
    print("=" * 80)

if __name__ == "__main__":
    test_recommendation_engine()
