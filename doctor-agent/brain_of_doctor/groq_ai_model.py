import os
import base64
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the Groq API key from environment variables
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment variables. Please set it in your .env file.")

image_path = 'images/acne.jpg'

def encode_image(image_path=image_path):
    """
    Encode an image file to base64.
    
    Args:
        image_path (str): Path to the image file.
    
    Returns:
        str: Base64-encoded string of the image.
    
    Raises:
        FileNotFoundError: If the image file does not exist.
    """

    try:
        with open(image_path, 'rb') as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode('utf-8')
        return encoded_image
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found at: {image_path}")


def analyse_image_with_query(query,model,encoded_image):
    """
    Analyze an image with a query using the Groq API.
    
    Args:
        query (str): The query to send with the image.
        model (str): The model to use for analysis.
        encoded_image (str): Base64-encoded image string.
    
    Returns:
        str: Response from the Groq API.
    
    Raises:
        Exception: If the API request fails.
    """
    try:
        client = Groq(api_key=GROQ_API_KEY)
        
        messages = [
            {
                'role': 'user',
                'content': [
                    {'type': 'text', 'text': query},
                    {'type': 'image_url', 'image_url': {'url': f"data:image/jpeg;base64,{encoded_image}"}}
                ]
            }
        ]

        chat_completion = client.chat.completions.create(
            messages=messages,
            model=model
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        raise Exception(f"Error during API request: {str(e)}")

if __name__ == '__main__':
    try:
        query = "What is wrong with me?"
        model = "meta-llama/llama-4-scout-17b-16e-instruct"
        encoded_image = encode_image()
        response = analyse_image_with_query(query=query, model=model, encoded_image=encoded_image)
        print("Response from Groq API:")
        print(response)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
