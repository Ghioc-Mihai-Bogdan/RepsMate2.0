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

openai.api_key = api_key

# HR Agent system message
HR_SYSTEM_MESSAGE = """You are an HR assistant for a company. Your role is to:
1. Answer questions about company policies, benefits, and procedures
2. Provide guidance on HR-related matters
3. Help with onboarding and employee relations
4. Maintain a professional and helpful tone
5. Respect confidentiality and privacy
6. Direct complex issues to human HR staff when necessary

Remember to be clear, concise, and professional in your responses."""

class HRAgent:
    def __init__(self):
        self.chat_history = []
        self.max_retries = 3
        self.retry_delay = 2  # seconds
    
    def get_response(self, user_input):
        retries = 0
        while retries < self.max_retries:
            try:
                # Prepare messages for the API call
                messages = [
                    {"role": "system", "content": HR_SYSTEM_MESSAGE},
                    *self.chat_history,
                    {"role": "user", "content": user_input}
                ]
                
                # Call OpenAI API
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=messages,
                    temperature=0.7,
                    max_tokens=500
                )
                
                # Extract the response
                assistant_response = response.choices[0].message.content
                
                # Update chat history
                self.chat_history.append({"role": "user", "content": user_input})
                self.chat_history.append({"role": "assistant", "content": assistant_response})
                
                return assistant_response

            except openai.RateLimitError as e:
                retries += 1
                if retries < self.max_retries:
                    time.sleep(self.retry_delay * retries)  # Exponential backoff
                    continue
                return "Error 429: Rate limit exceeded. Please wait a moment before trying again."
            
            except openai.AuthenticationError as e:
                return "Error: Invalid API key. Please check your OpenAI API key configuration."
            
            except openai.APIConnectionError as e:
                return "Error: Could not connect to OpenAI API. Please check your internet connection."
            
            except openai.APIError as e:
                return f"Error: OpenAI API error occurred. Details: {str(e)}"
            
            except Exception as e:
                return f"Unexpected error occurred: {str(e)}"
    
    def clear_history(self):
        """Clear the chat history"""
        self.chat_history = [] 