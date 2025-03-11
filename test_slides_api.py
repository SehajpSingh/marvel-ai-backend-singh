
import requests
import json
import time

# Base URL - modify if you're hosting on a different port
BASE_URL = "http://0.0.0.0:8000"

# API Key
API_KEY = "dev"

# Headers for API requests
headers = {
    "Content-Type": "application/json",
    "x-api-key": API_KEY
}

def test_generate_outline():
    """Generate an outline and return the presentation ID"""
    url = f"{BASE_URL}/generate-outline"
    
    # Example payload based on the expected format
    payload = {
        "user": {
            "id": "12345",
            "fullName": "Test User",
            "email": "test@example.com"
        },
        "type": "tool",
        "tool_data": {
            "tool_id": "presentation-generator",
            "inputs": [
                {
                    "name": "grade_level",
                    "value": "5"
                },
                {
                    "name": "topic", 
                    "value": "History of Science"
                },
                {
                    "name": "n_slides",
                    "value": "10"
                },
                {
                    "name": "objectives",
                    "value": "Explain major scientific milestones;Understand the impact of technology"
                },
                {
                    "name": "lang",
                    "value": "English"
                }
            ]
        }
    }
    
    # Send request
    print("Generating outline...")
    response = requests.post(url, json=payload, headers=headers)
    
    # Check response
    if response.status_code == 200:
        response_data = response.json()
        print("Outline generated successfully!")
        print("Response:", json.dumps(response_data, indent=2))
        
        # Extract presentation_id from the response
        presentation_id = response_data.get("data", {}).get("presentation_id")
        if presentation_id:
            print(f"Presentation ID: {presentation_id}")
            return presentation_id
        else:
            print("Error: Could not find presentation_id in response")
            print("Full response:", response_data)
            return None
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def test_generate_slides(presentation_id=None):
    """Generate slides using the presentation ID"""
    if not presentation_id:
        print("No presentation ID provided. Using previously provided ID...")
        presentation_id = "a43389c8-e30f-44c4-bdbb-1c176e48576e"
    
    url = f"{BASE_URL}/generate-slides/{presentation_id}"
    
    # Send request
    print(f"Generating slides for presentation {presentation_id}...")
    response = requests.post(url, headers=headers)
    
    # Check response
    if response.status_code == 200:
        response_data = response.json()
        print("Slides generated successfully!")
        print("Response:", json.dumps(response_data, indent=2))
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        
        if response.status_code == 404:
            print("\nDEBUG: 404 error suggests the presentation ID is not found in cache.")
            print("This could be because:")
            print("1. The outline generation process didn't store data properly")
            print("2. The cache entry has expired")
            print("3. There's a typo in the presentation ID")
            print("\nTry generating a new outline first, then immediately use the new ID.")

if __name__ == "__main__":
    choice = input("Do you want to (1) generate a new outline or (2) use existing ID? Enter 1 or 2: ")
    
    if choice == "1":
        # First generate an outline to get a presentation ID
        presentation_id = test_generate_outline()
        
        if presentation_id:
            # Wait a moment to ensure the outline is processed
            print("Waiting for outline processing...")
            time.sleep(2)
            
            # Then generate slides using that ID
            test_generate_slides(presentation_id)
    else:
        # Use existing ID
        test_generate_slides()
