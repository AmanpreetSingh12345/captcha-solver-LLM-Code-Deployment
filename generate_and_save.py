import requests
import json

# Read your request data from the file
with open("request.json", "r") as f:
    payload = json.load(f)

# Send POST request to FastAPI endpoint
response = requests.post(
    "http://127.0.0.1:8000/api/llm-build",
    headers={"Content-Type": "application/json"},
    json=payload
)

if response.status_code == 200:
    data = response.json()
    # Get FULL generated code if your API returns it (here it may be truncated)
    code = data.get("generated_code", "")
    print("Generated code preview:")
    print(code[:700])  # Print first 700 chars, adjust as needed


    # Save the preview to a file
    with open("app.py", "w") as f:
        f.write(code)
    print("Saved generated code preview to app.py")
else:
    print("Error:", response.status_code, response.text)
