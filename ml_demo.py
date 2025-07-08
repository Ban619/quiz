#!/usr/bin/env python3
"""
Machine Learning Demo
Demonstrates basic AI/ML capabilities using scikit-learn
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification, make_regression, load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler
import json
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

class MLDemo:
    """
    A class to demonstrate various machine learning capabilities
    """
    
    def __init__(self):
        self.models = {}
        self.results = {}
        
    def create_sample_data(self):
        """Create sample datasets for demonstration"""
        print("🔬 Creating sample datasets...")
        
        # Classification dataset
        X_class, y_class = make_classification(
            n_samples=1000, 
            n_features=20, 
            n_informative=10,
            n_redundant=10,
            n_clusters_per_class=1,
            random_state=42
        )
        
        # Regression dataset
        X_reg, y_reg = make_regression(
            n_samples=1000,
            n_features=10,
            noise=0.1,
            random_state=42
        )
        
        # Real dataset - Iris
        iris = load_iris()
        X_iris, y_iris = iris.data, iris.target
        
        return {
            'classification': (X_class, y_class),
            'regression': (X_reg, y_reg),
            'iris': (X_iris, y_iris)
        }
    
    def train_classification_model(self, X, y, model_type='random_forest'):
        """Train a classification model"""
        print(f"🎯 Training {model_type} classification model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Choose model
        if model_type == 'random_forest':
            model = RandomForestClassifier(n_estimators=100, random_state=42)
        else:
            model = LogisticRegression(random_state=42, max_iter=1000)
        
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, y_pred)
        
        results = {
            'model_type': model_type,
            'task': 'classification',
            'accuracy': float(accuracy),
            'n_samples': len(X),
            'n_features': X.shape[1],
            'timestamp': datetime.now().isoformat()
        }
        
        self.models[f'classification_{model_type}'] = {
            'model': model,
            'scaler': scaler,
            'results': results
        }
        
        return results
    
    def train_regression_model(self, X, y, model_type='random_forest'):
        """Train a regression model"""
        print(f"📈 Training {model_type} regression model...")
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        
        # Scale features
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Choose model
        if model_type == 'random_forest':
            model = RandomForestRegressor(n_estimators=100, random_state=42)
        else:
            model = LinearRegression()
        
        # Train model
        model.fit(X_train_scaled, y_train)
        
        # Make predictions
        y_pred = model.predict(X_test_scaled)
        
        # Calculate metrics
        mse = mean_squared_error(y_test, y_pred)
        r2 = r2_score(y_test, y_pred)
        
        results = {
            'model_type': model_type,
            'task': 'regression',
            'mse': float(mse),
            'r2_score': float(r2),
            'n_samples': len(X),
            'n_features': X.shape[1],
            'timestamp': datetime.now().isoformat()
        }
        
        self.models[f'regression_{model_type}'] = {
            'model': model,
            'scaler': scaler,
            'results': results
        }
        
        return results
    
    def predict_single_sample(self, model_name, features):
        """Make a prediction on a single sample"""
        if model_name not in self.models:
            return {"error": f"Model {model_name} not found"}
        
        model_info = self.models[model_name]
        model = model_info['model']
        scaler = model_info['scaler']
        
        # Scale features
        features_scaled = scaler.transform([features])
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get probability for classification models
        prediction_proba = None
        if hasattr(model, 'predict_proba'):
            prediction_proba = model.predict_proba(features_scaled)[0].tolist()
        
        return {
            'prediction': float(prediction),
            'prediction_proba': prediction_proba,
            'model': model_name,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_demo(self):
        """Run the complete ML demonstration"""
        print("🤖 Starting Machine Learning Demo")
        print("=" * 50)
        
        # Create datasets
        datasets = self.create_sample_data()
        
        all_results = []
        
        # Train classification models
        for model_type in ['random_forest', 'logistic']:
            X_class, y_class = datasets['classification']
            result = self.train_classification_model(X_class, y_class, model_type)
            all_results.append(result)
            print(f"✅ {model_type} Classification Accuracy: {result['accuracy']:.3f}")
        
        # Train regression models  
        for model_type in ['random_forest', 'linear']:
            X_reg, y_reg = datasets['regression']
            result = self.train_regression_model(X_reg, y_reg, model_type)
            all_results.append(result)
            print(f"✅ {model_type} Regression R²: {result['r2_score']:.3f}")
        
        # Train on Iris dataset
        X_iris, y_iris = datasets['iris']
        iris_result = self.train_classification_model(X_iris, y_iris, 'random_forest')
        all_results.append(iris_result)
        print(f"✅ Iris Classification Accuracy: {iris_result['accuracy']:.3f}")
        
        # Save results
        self.results = {
            'summary': {
                'models_trained': len(all_results),
                'timestamp': datetime.now().isoformat(),
                'available_models': list(self.models.keys())
            },
            'detailed_results': all_results
        }
        
        return self.results
    
    def save_results(self, filename='ml_results.json'):
        """Save results to a JSON file"""
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"💾 Results saved to {filename}")
    
    def interactive_prediction(self):
        """Interactive prediction interface"""
        print("\n🎮 Interactive Prediction Mode")
        print("Available models:", list(self.models.keys()))
        
        while True:
            model_name = input("\nEnter model name (or 'quit' to exit): ").strip()
            
            if model_name.lower() == 'quit':
                break
                
            if model_name not in self.models:
                print("❌ Model not found!")
                continue
            
            model_info = self.models[model_name]
            n_features = model_info['results']['n_features']
            
            print(f"Enter {n_features} features (space-separated):")
            try:
                features_input = input().strip()
                features = [float(x) for x in features_input.split()]
                
                if len(features) != n_features:
                    print(f"❌ Expected {n_features} features, got {len(features)}")
                    continue
                
                result = self.predict_single_sample(model_name, features)
                
                if 'error' in result:
                    print(f"❌ {result['error']}")
                else:
                    print(f"🎯 Prediction: {result['prediction']:.3f}")
                    if result['prediction_proba']:
                        print(f"📊 Probabilities: {[f'{p:.3f}' for p in result['prediction_proba']]}")
                        
            except ValueError:
                print("❌ Invalid input! Please enter numeric values.")
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function to run the ML demo"""
    print("🚀 AI/ML Demonstration Script")
    print("This script demonstrates various machine learning capabilities")
    print("=" * 60)
    
    # Create and run demo
    demo = MLDemo()
    results = demo.run_demo()
    
    print("\n📊 Demo Summary:")
    print(f"Models trained: {results['summary']['models_trained']}")
    print(f"Available models: {len(results['summary']['available_models'])}")
    
    # Save results
    demo.save_results()
    
    # Interactive mode
    print("\n" + "=" * 60)
    response = input("Would you like to try interactive prediction? (y/n): ").strip().lower()
    if response == 'y':
        demo.interactive_prediction()
    
    print("\n🎉 Demo completed successfully!")
    print("💡 You can import this module and use the MLDemo class in your own projects")

if __name__ == "__main__":
    main()