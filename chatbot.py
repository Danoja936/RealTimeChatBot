try:
    from google import genai
    import os
    from dotenv import load_dotenv
    has_lib = True
except ImportError:
    has_lib = False


use_ai = False
if has_lib:
    try:
        # Load variables from .env file (including GEMINI_API_KEY)
        load_dotenv()
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY not found in environment/.env file")

        client = genai.Client(api_key=api_key)
        use_ai = True
    except Exception as e:
        print(f"AI Initialization failed: {e}")

def chatbot_response(message):
    if use_ai:
        try:
            response = client.models.generate_content(
                model="gemini-2.0-flash",
                contents=f"You are a helpful, creative assistant in a real-time chat room. "
                         f"Keep your answers concise (max 2 sentences). User says: {message}"
            )
            return response.text
        except Exception as e:
            return f"AI Error: {str(e)[:50]}... (Using fallback)"

   
    message = message.lower()
    if "hello" in message:
        return "Hi! I'm the ChatBot. (AI mode is currently restricted)"
    elif "joke" in message:
        return "Why did the router go to the doctor? Because it had a bad connection!"
    return "I'm currently in basic mode. Make sure to use the Anaconda Python and have 'google-generativeai' installed."
