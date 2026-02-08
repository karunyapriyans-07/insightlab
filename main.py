import os
from google import genai
from google.genai import types
from PIL import Image

# 1. Setup Client (Requires GEMINI_API_KEY environment variable)
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
MODEL_ID = "gemini-3-pro-preview"

# 2. Define a "Tool" function (Function Calling)
# This simulates looking up scientific data.
def get_scientific_context(concept: str):
    """Looks up scientific context for a given concept."""
    knowledge_base = {
        "exponential growth": "Exponential growth occurs when the growth rate of a value is proportional to its current value.",
        "plateau": "A plateau in a graph indicates a period of stability where no net change is occurring.",
        "enzyme activity": "Enzyme activity is affected by pH and temperature, usually showing a bell-curve shape."
    }
    return knowledge_base.get(concept.lower(), "Concept not found in database.")

# 3. Main Analysis Function
def analyze_chart(image_path: str):
    image = Image.open(image_path)
    
    # Define the prompt
    prompt = """
    Analyze this scientific chart. 
    1. Describe the main trends (e.g., rising, falling, plateau).
    2. Identify the core scientific concept being demonstrated.
    3. Use the get_scientific_context tool to explain that concept.
    """

    # 4. Configure Gemini 3 with Tools
    config = types.GenerateContentConfig(
        tools=[get_scientific_context],
        thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH)
    )

    # 5. Generate Response
    response = client.models.generate_content(
        model=MODEL_ID,
        contents=[prompt, image],
        config=config
    )

    # 6. Handle Function Calls automatically
    if response.candidates[0].content.parts[0].function_call:
        # In a real app, you'd execute the tool here.
        # The GenAI SDK handles this automatically in newer versions.
        print("Analysis:", response.text)
    else:
        print("Analysis:", response.text)

# Run the project
if __name__ == "__main__":
    # Ensure you have a 'chart.png' in the same directory
    # analyze_chart("chart.png") 
    print("Project structure ready.")
