import os
import json
import torch
import logging
from typing import List, Dict, Optional
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    AutoModelForSequenceClassification,
    pipeline
)
import numpy as np
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AIAssistant:
    """
    A comprehensive AI Assistant with multiple capabilities:
    - Text generation and chatbot functionality
    - Sentiment analysis
    - Text classification
    - Question answering
    """
    
    def __init__(self, config_path: Optional[str] = None):
        self.config = self._load_config(config_path)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        logger.info(f"Using device: {self.device}")
        
        # Initialize models
        self.chat_model = None
        self.chat_tokenizer = None
        self.sentiment_analyzer = None
        self.text_generator = None
        
        self._initialize_models()
        
    def _load_config(self, config_path: Optional[str]) -> Dict:
        """Load configuration from file or use defaults"""
        default_config = {
            "chat_model": "microsoft/DialoGPT-medium",
            "sentiment_model": "cardiffnlp/twitter-roberta-base-sentiment-latest",
            "max_length": 1000,
            "temperature": 0.7,
            "top_p": 0.9,
            "conversation_history_limit": 10
        }
        
        if config_path and os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    user_config = json.load(f)
                default_config.update(user_config)
            except Exception as e:
                logger.warning(f"Could not load config: {e}. Using defaults.")
                
        return default_config
    
    def _initialize_models(self):
        """Initialize all AI models"""
        try:
            logger.info("Loading AI models...")
            
            # Chat model for conversation
            self.chat_tokenizer = AutoTokenizer.from_pretrained(
                self.config["chat_model"], 
                padding_side='left'
            )
            if self.chat_tokenizer.pad_token is None:
                self.chat_tokenizer.pad_token = self.chat_tokenizer.eos_token
                
            self.chat_model = AutoModelForCausalLM.from_pretrained(
                self.config["chat_model"],
                torch_dtype=torch.float16 if self.device.type == "cuda" else torch.float32
            ).to(self.device)
            
            # Sentiment analyzer
            self.sentiment_analyzer = pipeline(
                "sentiment-analysis",
                model=self.config["sentiment_model"],
                device=0 if self.device.type == "cuda" else -1
            )
            
            # Text generator for creative writing
            self.text_generator = pipeline(
                "text-generation",
                model="gpt2",
                device=0 if self.device.type == "cuda" else -1
            )
            
            logger.info("All models loaded successfully!")
            
        except Exception as e:
            logger.error(f"Error initializing models: {e}")
            raise
    
    def chat(self, message: str, conversation_history: List[str] = None) -> str:
        """
        Generate a response to a chat message
        
        Args:
            message: User's input message
            conversation_history: Previous conversation context
            
        Returns:
            AI's response
        """
        try:
            if conversation_history is None:
                conversation_history = []
            
            # Prepare conversation context
            context = ""
            history_limit = self.config["conversation_history_limit"]
            recent_history = conversation_history[-history_limit:] if len(conversation_history) > history_limit else conversation_history
            
            for msg in recent_history:
                context += msg + self.chat_tokenizer.eos_token
            
            # Add current message
            context += message + self.chat_tokenizer.eos_token
            
            # Tokenize input
            inputs = self.chat_tokenizer.encode(context, return_tensors="pt").to(self.device)
            
            # Generate response
            with torch.no_grad():
                outputs = self.chat_model.generate(
                    inputs,
                    max_length=inputs.shape[1] + 100,
                    temperature=self.config["temperature"],
                    top_p=self.config["top_p"],
                    do_sample=True,
                    pad_token_id=self.chat_tokenizer.eos_token_id,
                    no_repeat_ngram_size=3
                )
            
            # Decode response
            response = self.chat_tokenizer.decode(outputs[0][inputs.shape[1]:], skip_special_tokens=True)
            return response.strip()
            
        except Exception as e:
            logger.error(f"Error in chat: {e}")
            return "I'm sorry, I encountered an error processing your message."
    
    def analyze_sentiment(self, text: str) -> Dict:
        """
        Analyze the sentiment of text
        
        Args:
            text: Input text to analyze
            
        Returns:
            Dictionary with sentiment label and confidence score
        """
        try:
            result = self.sentiment_analyzer(text)[0]
            return {
                "sentiment": result["label"],
                "confidence": round(result["score"], 3),
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.error(f"Error in sentiment analysis: {e}")
            return {"sentiment": "unknown", "confidence": 0.0, "error": str(e)}
    
    def generate_text(self, prompt: str, max_length: int = 200) -> str:
        """
        Generate creative text based on a prompt
        
        Args:
            prompt: Starting text prompt
            max_length: Maximum length of generated text
            
        Returns:
            Generated text
        """
        try:
            result = self.text_generator(
                prompt,
                max_length=max_length,
                temperature=self.config["temperature"],
                top_p=self.config["top_p"],
                do_sample=True,
                num_return_sequences=1
            )
            return result[0]["generated_text"]
            
        except Exception as e:
            logger.error(f"Error in text generation: {e}")
            return f"Error generating text: {e}"
    
    def process_batch(self, texts: List[str], operation: str) -> List[Dict]:
        """
        Process multiple texts with the specified operation
        
        Args:
            texts: List of input texts
            operation: Operation to perform ('sentiment', 'chat', 'generate')
            
        Returns:
            List of results
        """
        results = []
        for text in texts:
            if operation == "sentiment":
                results.append(self.analyze_sentiment(text))
            elif operation == "chat":
                results.append({"response": self.chat(text)})
            elif operation == "generate":
                results.append({"generated": self.generate_text(text)})
            else:
                results.append({"error": f"Unknown operation: {operation}"})
        
        return results
    
    def get_model_info(self) -> Dict:
        """Get information about loaded models"""
        return {
            "chat_model": self.config["chat_model"],
            "sentiment_model": self.config["sentiment_model"],
            "device": str(self.device),
            "models_loaded": {
                "chat": self.chat_model is not None,
                "sentiment": self.sentiment_analyzer is not None,
                "text_generator": self.text_generator is not None
            }
        }

# Example usage and testing
if __name__ == "__main__":
    print("🤖 Initializing AI Assistant...")
    
    try:
        # Create AI assistant
        ai = AIAssistant()
        
        print("✅ AI Assistant ready!")
        print(f"📊 Model info: {ai.get_model_info()}")
        
        # Interactive chat loop
        print("\n💬 Chat with the AI (type 'quit' to exit, 'sentiment: <text>' for sentiment analysis)")
        print("    Type 'generate: <prompt>' for text generation")
        
        conversation_history = []
        
        while True:
            user_input = input("\nYou: ").strip()
            
            if user_input.lower() == 'quit':
                print("👋 Goodbye!")
                break
            
            if user_input.startswith('sentiment:'):
                text = user_input[10:].strip()
                sentiment = ai.analyze_sentiment(text)
                print(f"🎭 Sentiment: {sentiment}")
                
            elif user_input.startswith('generate:'):
                prompt = user_input[9:].strip()
                generated = ai.generate_text(prompt)
                print(f"✍️  Generated: {generated}")
                
            else:
                # Regular chat
                response = ai.chat(user_input, conversation_history)
                print(f"🤖 AI: {response}")
                
                # Update conversation history
                conversation_history.extend([f"Human: {user_input}", f"AI: {response}"])
        
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Application error: {e}")