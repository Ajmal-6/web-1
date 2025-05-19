from flask import Flask, request, jsonify, render_template
import requests  # For calling external APIs
import os

app = Flask(__name__)

# --- DeepSeek API Integration ---
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Set this in your environment

def get_recipe_from_ai(ingredients):
    """Fetch recipes from DeepSeek API or use a fallback."""
    if DEEPSEEK_API_KEY:
        try:
            headers = {"Authorization": f"Bearer {DEEPSEEK_API_KEY}"}
            prompt = f"Suggest 2 detailed recipes using these ingredients: {ingredients}. Include preparation steps."
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",  # Check actual API endpoint
                headers=headers,
                json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
        
        except Exception as e:
            print("DeepSeek API Error:", e)
    
    # Fallback if API fails
    return f"""Here's a sample recipe using {ingredients}:
              
1. **Stir-Fry**:
   - Sauté {ingredients.split(',')[0]} with garlic and oil.
   - Add remaining ingredients and stir-fry for 5 mins.
   - Serve hot!

2. **Salad**:
   - Chop {ingredients} finely.
   - Toss with olive oil, lemon juice, and salt.
   - Refrigerate for 30 mins before serving."""

# --- Routes ---
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/get_recipe", methods=["POST"])
def get_recipe():
    data = request.json
    ingredients = data.get("ingredients", "")
    
    recipe = get_recipe_from_ai(ingredients)
    return jsonify({"recipe": recipe})

if __name__ == "__main__":
    app.run(debug=True)