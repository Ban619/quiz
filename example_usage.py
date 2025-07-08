#!/usr/bin/env python3
"""
Example Usage Script for AI Assistant
Demonstrates various ways to use the AI programmatically
"""

from ai_assistant import AIAssistant
from ml_demo import MLDemo
import json
from datetime import datetime

def basic_examples():
    """Basic usage examples"""
    print("🚀 Basic AI Assistant Examples")
    print("=" * 50)
    
    # Initialize AI Assistant
    print("Initializing AI Assistant...")
    ai = AIAssistant()
    
    # Example 1: Simple chat
    print("\n1. Simple Chat:")
    response = ai.chat("Hello! What can you do?")
    print(f"AI: {response}")
    
    # Example 2: Sentiment analysis
    print("\n2. Sentiment Analysis:")
    texts_to_analyze = [
        "I love this AI assistant!",
        "This is terrible and frustrating",
        "The weather is okay today",
        "Amazing work on this project!"
    ]
    
    for text in texts_to_analyze:
        sentiment = ai.analyze_sentiment(text)
        print(f"Text: '{text}'")
        print(f"Sentiment: {sentiment['sentiment']} (confidence: {sentiment['confidence']:.2f})")
        print()
    
    # Example 3: Text generation
    print("3. Text Generation:")
    prompts = [
        "The future of artificial intelligence",
        "Once upon a time in a magical forest",
        "The benefits of renewable energy"
    ]
    
    for prompt in prompts:
        generated = ai.generate_text(prompt, max_length=150)
        print(f"Prompt: '{prompt}'")
        print(f"Generated: {generated}")
        print("-" * 30)

def conversation_example():
    """Example of a multi-turn conversation"""
    print("\n🗣️ Multi-turn Conversation Example")
    print("=" * 50)
    
    ai = AIAssistant()
    conversation_history = []
    
    messages = [
        "Hi, I'm interested in learning about AI",
        "What are the main types of machine learning?",
        "Can you explain what deep learning is?",
        "How is this different from traditional programming?",
        "Thanks for the explanation!"
    ]
    
    for message in messages:
        print(f"\nUser: {message}")
        response = ai.chat(message, conversation_history)
        print(f"AI: {response}")
        
        # Update conversation history
        conversation_history.extend([
            f"Human: {message}",
            f"AI: {response}"
        ])

def batch_processing_example():
    """Example of batch processing"""
    print("\n📦 Batch Processing Example")
    print("=" * 50)
    
    ai = AIAssistant()
    
    # Batch sentiment analysis
    customer_feedback = [
        "Great service, very satisfied!",
        "Product arrived damaged",
        "Average experience, nothing special",
        "Outstanding quality and fast delivery",
        "Worst purchase ever, requesting refund"
    ]
    
    print("Analyzing customer feedback sentiment:")
    results = ai.process_batch(customer_feedback, "sentiment")
    
    for i, (text, result) in enumerate(zip(customer_feedback, results)):
        sentiment = result['sentiment']
        confidence = result['confidence']
        emoji = "😊" if sentiment == "POSITIVE" else "😞" if sentiment == "NEGATIVE" else "😐"
        print(f"{i+1}. {emoji} {text}")
        print(f"   → {sentiment} ({confidence:.2f})")

def machine_learning_example():
    """Example using the machine learning demo"""
    print("\n🔬 Machine Learning Example")
    print("=" * 50)
    
    # Run ML demo
    ml_demo = MLDemo()
    results = ml_demo.run_demo()
    
    print(f"\nTrained {results['summary']['models_trained']} models")
    print("Available models:", results['summary']['available_models'])
    
    # Make a prediction
    if 'classification_random_forest' in ml_demo.models:
        # Example prediction (you'd normally use real data)
        features = [0.5, -0.2, 1.1, 0.8, -0.5, 0.3, -0.9, 1.2, 0.1, -0.4,
                   0.7, -0.1, 0.9, -0.6, 0.2, 1.0, -0.3, 0.4, -0.8, 0.6]
        
        prediction_result = ml_demo.predict_single_sample(
            'classification_random_forest', 
            features
        )
        
        print(f"\nExample Prediction:")
        print(f"Features: {features[:5]}... (showing first 5)")
        print(f"Prediction: {prediction_result['prediction']}")
        if prediction_result['prediction_proba']:
            probs = prediction_result['prediction_proba']
            print(f"Probabilities: Class 0: {probs[0]:.3f}, Class 1: {probs[1]:.3f}")

def custom_configuration_example():
    """Example using custom configuration"""
    print("\n⚙️ Custom Configuration Example")
    print("=" * 50)
    
    # Create custom config
    custom_config = {
        "chat_model": "microsoft/DialoGPT-small",  # Faster model
        "temperature": 0.9,  # More creative
        "max_length": 500,   # Shorter responses
        "conversation_history_limit": 5  # Less context
    }
    
    # Save to temporary config file
    with open('temp_config.json', 'w') as f:
        json.dump(custom_config, f, indent=2)
    
    # Initialize AI with custom config
    ai_custom = AIAssistant(config_path='temp_config.json')
    
    print("Using custom configuration:")
    info = ai_custom.get_model_info()
    print(f"Model: {info['chat_model']}")
    print(f"Device: {info['device']}")
    
    # Test with creative prompt
    response = ai_custom.chat("Tell me a creative short story about robots")
    print(f"\nCreative response: {response}")
    
    # Clean up
    import os
    os.remove('temp_config.json')

def error_handling_example():
    """Example showing error handling"""
    print("\n🛡️ Error Handling Example")
    print("=" * 50)
    
    ai = AIAssistant()
    
    # Test with empty input
    print("1. Testing empty input:")
    empty_sentiment = ai.analyze_sentiment("")
    print(f"Result: {empty_sentiment}")
    
    # Test with very long input (should be handled gracefully)
    print("\n2. Testing very long input:")
    long_text = "This is a test. " * 1000  # Very long text
    long_sentiment = ai.analyze_sentiment(long_text)
    print(f"Result: {long_sentiment}")

def performance_monitoring_example():
    """Example showing performance monitoring"""
    print("\n📊 Performance Monitoring Example")
    print("=" * 50)
    
    ai = AIAssistant()
    
    import time
    
    # Time different operations
    operations = [
        ("Chat", lambda: ai.chat("Hello")),
        ("Sentiment", lambda: ai.analyze_sentiment("This is great!")),
        ("Generation", lambda: ai.generate_text("AI is", max_length=50))
    ]
    
    for name, operation in operations:
        start_time = time.time()
        result = operation()
        end_time = time.time()
        
        print(f"{name}: {end_time - start_time:.2f} seconds")

def main():
    """Run all examples"""
    print("🤖 AI Assistant - Example Usage Script")
    print("This script demonstrates various ways to use the AI Assistant")
    print("=" * 70)
    
    examples = [
        ("Basic Examples", basic_examples),
        ("Conversation Example", conversation_example),
        ("Batch Processing", batch_processing_example),
        ("Machine Learning", machine_learning_example),
        ("Custom Configuration", custom_configuration_example),
        ("Error Handling", error_handling_example),
        ("Performance Monitoring", performance_monitoring_example)
    ]
    
    for name, example_func in examples:
        try:
            print(f"\n{'='*20} {name} {'='*20}")
            example_func()
        except Exception as e:
            print(f"❌ Error in {name}: {e}")
        
        input("\nPress Enter to continue to next example...")
    
    print("\n🎉 All examples completed!")
    print("💡 You can modify this script to test your own use cases")

if __name__ == "__main__":
    main()