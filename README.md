# Gift Recommendation App with OpenAI & Gradio


This application uses OpenAI's language and image generation models to recommend personalized gifts and generate sample images for each suggestion. The user interface is built with [Gradio](https://gradio.app/) for a seamless and interactive experience. The project is managed using [Poetry](https://python-poetry.org/) for dependency management and packaging.


## Features


- **Personalized Gift Recommendations:** 
 Enter details such as your relationship to the recipient, their interests, location, budget, and any additional information. The app uses OpenAI's GPT model to suggest between 1 and 10 thoughtful gifts.


- **AI-Generated Gift Images:** 
 For each recommended gift, the app generates a sample image using OpenAI's DALL·E model, giving you a visual preview of the suggestion.


- **Intuitive Gradio Interface:** 
 The Gradio-powered web interface allows you to easily input preferences and view results in a chat-like format.


- **Modern Python Project Management:** 
 All dependencies and scripts are managed with Poetry for reproducibility and ease of use.


## How It Works


1. **Input Preferences:** 
  - Number of recommendations 
  - Budget 
  - Interests 
  - Relationship to recipient 
  - Location 
  - Additional information


2. **AI Processing:** 
  - The app sends your preferences to OpenAI's GPT model to generate a list of gift ideas.
  - For each gift, a prompt is sent to DALL·E to create a sample image.


3. **Output:** 
  - The app displays the recommended gifts, each with a summary, purchase links, and a generated image.


## Getting Started


1. **Clone the Repository:**
  ```bash
  git clone <your-repo-url>
  cd sampleapp_gradio
  ```


2. **Install Poetry (if not already installed):**
  ```bash
  curl -sSL https://install.python-poetry.org | python3 -
  ```


3. **Install Dependencies:**
  ```bash
  poetry install
  ```


4. **Set Up Environment Variables:**
  - Create a `.env` file in the root directory.
  - Add your OpenAI API key:
    ```
    OPENAI_API_KEY=your_openai_api_key_here
    ```


5. **Run the App:**
  ```bash
  poetry run python src/app.py
  ```


6. **Access the Interface:**
  - Open the provided local URL in your browser to use the app.


## Example


1. Select "Friend" as the relationship, "Books" as the interest, set a budget, and click "Generate".
2. The app will display a list of book-related gift ideas, each with a summary and a sample image.


## Technologies Used


- [OpenAI GPT & DALL·E](https://platform.openai.com/)
- [Gradio](https://gradio.app/)
- [Poetry](https://python-poetry.org/)
- Python


## License


This project is for educational and demonstration purposes.


---



