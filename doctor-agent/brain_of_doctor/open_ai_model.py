import os
import base64
from dotenv import load_dotenv
from agents import (
    Agent,
    Runner,
    AsyncOpenAI,
    OpenAIChatCompletionsModel,
    RunConfig
)

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in your .env file.")

# Setup Gemini-compatible client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.5-pro",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    tracing_disabled=True
)

image_path='images/acne.jpg'
# Function to encode image to base64
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

# Define the Agent

def analyse_image_with_query(query,model,encoded_image):

    # Vision-compatible input using OpenAI's "image_url" format
    try:
        doctor = Agent(
            name="Doctor Agent",
            instructions="""
                You are a professional Doctor. Analyze images and give accurate 
                diagnosis and treatment advice based on visual input. Respond only with 
                medically accurate and ethical suggestions.
            """,
            model=model
        )

        image = f"data:image/jpeg;base64,{encoded_image}"
        message = query + image
        # print("message",message)
        # Run the agent synchronously
        response = Runner.run_sync(
            starting_agent=doctor,
            input=message,
            run_config=config,

        )    
        return response.final_output
    except Exception as e:
        raise Exception(f"Error during API request: {str(e)}")
    

if __name__ == '__main__':
    try:
        # query = "What is wrong with me?"
        query = "How do i get better?"
        model=model
        encoded_image = encode_image()
        response = analyse_image_with_query(query=query, model=model, encoded_image=encoded_image)
        # Output the result

        print("\n💬 Diagnosis and Treatment:")
        print(response)

    except Exception as e:
        print(f"An error occurred: {str(e)}")
