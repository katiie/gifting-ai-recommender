# flake8: noqa
import os
import asyncio
import json
import logging
import gradio as gr
from openai import AsyncOpenAI
from dotenv import dotenv_values
from helpers import get_countries

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s %(name)s: %(message)s]"
)
logger = logging.getLogger(__name__)
config = dotenv_values(".env")



class AIClient:
    def __init__(self, OPENAI_API_KEY):
        self.recommendations = []
        self.initialize_prompt_details()
        self.client = AsyncOpenAI(api_key=OPENAI_API_KEY)

    def initialize_prompt_details(self):
        sample_json = {
            "gift_recommendations": [
                {
                    "name": "Wine Opender",
                    "summary": "A fancy wine opender based on the given preference",
                    "image": "sample url"
                }
            ]
        }

        self.messages = [
            {
                "role": "system",
                "content": f"Provide output in valid JSON. You knowledgeable about gifts and presents. Provide between 1 to 10 gifts recommendations and the data schema should be like this: ${json.dumps(sample_json)}.The summary should also have one or two links to buy the gifts for the provided location."
            }
        ]
        self.hobbies = [
            "Select ...",
            "Travel",
            "Food",
            "Books",
            "Movies",
            "Music",
            "Games",
            "Arts & Culture",
            "Sports & Fitness",
            "Learning & Intellectual Pursuits",
            "Outdoor & Nature",
            "Social & Community",
            "Professional & Skill-Based",
            "Other",
        ]
        self.budget_info = [
            "Select ...",
            "0-15",
            "15-20",
            "20-30",
            "30-50",
            "50-100",
            "100-200",
            "200-500",
            "500-1000",
            "1000-2000",
            "2000-5000",
            "5000 & Above"
        ]
        self.relationship = ["Select ...","Friend", "Family", "Partner", "Boss", "Colleague", "Other"]
        self.location = ["Select ..."] +get_countries()
        self.age_range = ["Select ...", "0-12", "13-19", "20-35", "35-59", "60+ years"]

    def initialize_application(self, share=False):
        with gr.Blocks() as demo:
            with gr.Row():
                # input elements
                with gr.Column():
                    with gr.Row():
                        count = gr.Slider(label="No. of recommendation", minimum=1, maximum=10, step=1, value=3)
                        age_range =  gr.Dropdown(label="Demographic",
                            choices = self.age_range,
                        )
                        budget = gr.Dropdown(label="Budget",
                            choices = self.budget_info,
                        )
                    with gr.Row():
                        hobbies = gr.Dropdown(label="Hobbies",
                        choices = self.hobbies,
                    )
                        relationship = gr.Dropdown(label="Relationship",
                            choices= self.relationship,
                        )
                        location = gr.Dropdown(label="Location",
                            choices = self.location,
                        )
                    with gr.Row():
                        additional_info = gr.TextArea(label="Additional Information",placeholder="Additional info about the person")
                    submit_btn = gr.Button("Generate")
                # ouput elements
                with gr.Column():
                    output_chatbot_component = gr.Chatbot(self.recommendations,show_copy_all_button=True, line_breaks=True,
                                                        min_height=800, autoscroll=True, editable=False, type="messages")


            submit_btn.click(fn=self.on_submit_click, inputs=[count, age_range, budget, hobbies, relationship, location, additional_info], outputs=output_chatbot_component, api_name="gift_recommendations")

        demo.launch(share=share)

    def validate_input(self, key, value):
        if not value or (isinstance(value, str) and "Select" in value):
            raise gr.Error(f"{key} is required")

    async def on_submit_click(self, *args):
        self.recommendations = []
        count, age_range, budget, hobbies, relationship, location, additional_info = args
        function_keys = ["Demographic", "Budget", "Hobbies", "Relationship", "Location"]
        for index, key in enumerate(args[1:len(function_keys)]):
            self.validate_input(function_keys[index], key)

        recommendations = await self.get_gift_ideas(count, age_range, budget, hobbies,
                                                    relationship, location, additional_info)

        if recommendations:
            for index, recommendation in enumerate(recommendations, 1):
                cm_col = []
                title, summary, image = recommendation['name'], recommendation['summary'], recommendation['image']
                content = f"{index}. {title.upper()} \r\n  {summary}"
                cm_col.append(gr.ChatMessage(
                    role="assistant",
                    content=gr.Image(value=image),
                    metadata={"title": content}))
                cm_col.append(gr.ChatMessage(role="assistant", content="\r\n"))
                self.recommendations = self.recommendations + cm_col
        return self.recommendations



    async def get_gift_ideas(self, *args):
        count, age_range, budget, hobbies, relationship, location, additional_info = args
        try:
            prompt_object = [
                {
                    "role": "user",
                    "content": f"Recommend the {count} best gift items for my {relationship}, who is {age_range} years old, enjoys {hobbies}, and lives in {location}. The budget range for the gifts should be within {budget}. Please include creative and thoughtful gift ideas tailored to them."
                }
            ]
            if additional_info:
                 prompt_object.append({
                    "role": "user",
                    "content": f"Feel free to consider other unique or personal details as well, such as {additional_info}, to make the suggestions especially meaningfu"

                })
            response = await self.client.chat.completions.create(
                model="gpt-4o-mini", messages=self.messages + prompt_object
            )
            if response and response.choices[0].finish_reason == "stop":
                initial_response = response.choices[0].message.content
                output = json.loads(initial_response)
                for _, item in enumerate(output["gift_recommendations"]):
                    prompt = f"An image of {item}"
                    response = await self.get_image(prompt)
                    item["image"] = response

                return output["gift_recommendations"]
        except Exception as e:
            logger.error(f"An error occurred, try again: {e}")
        return None

    async def get_image(self, prompt):
        try:
            response = await self.client.images.generate(
                model="dall-e-3",  # or "dall-e-2"
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            if response.data and len(response.data) > 0:
                return response.data[0].url
        except Exception as e:
            logger.error('an error occure', e)
        return

async def main():
    OPENAI_API_KEY = config.get("OPENAI_API_KEY") or os.environ.get('OPENAI_API_KEY')
    if not OPENAI_API_KEY:
        raise Exception("OPENAI_API_KEY required")
    DEMO_AS_LINE_APP = config.get("DEMO_AS_LINE_APP") or os.environ.get('DEMO_AS_LINE_APP') or True
    ai_client = AIClient(OPENAI_API_KEY)
    ai_client.initialize_application(DEMO_AS_LINE_APP)

if __name__ == "__main__":
    asyncio.run(main())
