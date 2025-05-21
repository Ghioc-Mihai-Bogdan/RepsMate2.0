import openai
from dotenv import load_dotenv
import os
import time

# Load environment variables
load_dotenv()

# Configure OpenAI
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("""
    OpenAI API key not found! Please follow these steps:
    1. Create a .env file in your project directory
    2. Add your OpenAI API key like this: OPENAI_API_KEY=your_api_key_here
    3. Get your API key from: https://platform.openai.com/api-keys
    """)

# Initialize OpenAI client
client = openai.OpenAI(api_key=api_key)

# CFO Agent system message
CFO_SYSTEM_MESSAGE = """You are a CFO assistant for a company. Your role is to:
1. Answer questions about financial matters, budgets, and financial planning
2. Provide guidance on financial strategies and investments
3. Help with financial reporting and analysis
4. Maintain a professional and analytical tone
5. Respect confidentiality of financial data
6. Direct complex financial issues to human CFO staff when necessary

Remember to be clear, precise, and professional in your responses."""

class CFOAgent:
    def __init__(self):
        self.chat_history = []
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def get_response(self, message_content, recent_messages=None):
        """Get response from the CFO agent"""
        try:
            # Prepare the input for the responses API
            input_content = []
            
            # Add system message
            input_content.append({
                "type": "text",
                "text": CFO_SYSTEM_MESSAGE
            })
            
            # Add recent messages if provided
            if recent_messages:
                for msg in recent_messages:
                    if msg["role"] == "user":
                        input_content.append({
                            "type": "text",
                            "text": msg["content"]
                        })
            
            # Add the current message content
            input_content.extend(message_content)
            
            # Get response from OpenAI using responses API
            response = client.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {
                        "role": "user",
                        "content": input_content
                    }
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            # Extract and store the response
            assistant_response = response.choices[0].message.content
            
            # Store the conversation
            self.chat_history.append({"role": "user", "content": message_content})
            self.chat_history.append({"role": "assistant", "content": assistant_response})
            
            return assistant_response
            
        except Exception as e:
            return f"Error: {str(e)}"
    
    def clear_history(self):
        """Clear the chat history"""
        self.chat_history = [] 