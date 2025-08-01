# flake8: noqa
import os
import json
import logging
import gradio as gr
from openai import OpenAI
from dotenv import dotenv_values


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
        self.client = OpenAI(api_key=OPENAI_API_KEY)

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
                "content": f"Provide output in valid JSON. You are world traveller knowledgeable about gifts and presents. Provide between 1 to 10 gifts recommendations and the data schema should be like this: ${json.dumps(sample_json)}. summary should also have one or two links to buy the gifts for the provided location."
            }
        ]


    def initialize_application(self, share= False):
        with gr.Blocks() as demo:
            with gr.Row():
                # input elements
                with gr.Column():
                    with gr.Row():
                        recommendation_count = gr.Slider(label="No. of recommendation", minimum=0, maximum=10, step=1, value=3)
                        budget = gr.Slider(label="Budget", minimum=0, maximum=5000, step=10, value=100)
                    with gr.Row():
                        interests = gr.Dropdown(label="Interest",
                        choices=[
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
                        ],
                        value="Travel",
                    )
                        relationship = gr.Dropdown(label="Relationship",
                            choices=["Friend", "Family", "Partner", "Boss", "Colleague", "Other"],
                            value="Friend",
                        )
                        location = gr.Dropdown(label="Location",
                            choices=["England", "Canada", "Nigeria", "Ghana", "Other"],
                            value="England",
                        )
                    with gr.Row():
                        additional_info = gr.Textbox(label="Additional Information",placeholder="Additional info about the person")
                    submit_btn = gr.Button("Generate")
                # ouput elements
                with gr.Column():
                    output_chatbot_component = gr.Chatbot(self.recommendations,show_copy_all_button=True, line_breaks=True,
                                                        min_height=800, autoscroll=True, editable=False, type="messages")


            submit_btn.click(fn=self.on_submit_click, inputs=[recommendation_count,interests, relationship, budget, location, additional_info], outputs=output_chatbot_component, api_name="gift_recommendations")

        demo.launch(share)

    def on_submit_click(self, *args):
        self.recommendations = []
        count,interests, relationship, budget, location, additional_info = args
        recommendations = self.get_gift_ideas(count,relationship, budget, location, interests, additional_info)

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



    def get_gift_ideas(self, *args):
        count, relationship, budget, location, interests, additional_info = args
        try:
            prompt_object = [
                {
                    "role": "user",
                    "content": f"I am looking for {count} gift ideas. The person in question is {relationship}, has the following {interests} and resides in {location}. Any gift listed should be less than or equal to {budget}. Additional details: {additional_info}.",
                }
            ]
            response = self.client.chat.completions.create(
                model="gpt-4o-mini", messages=self.messages + prompt_object
            )

            if response and response.choices[0].finish_reason == "stop":
                initial_response = response.choices[0].message.content
                output = json.loads(initial_response)
                for _, item in enumerate(output["gift_recommendations"]):
                    prompt = f"An image of {item}"
                    response = self.get_image(prompt)
                    item["image"] = response

                return output["gift_recommendations"]
        except Exception as e:
            logger.error(f"An error occurred, try again: {e}")
        return None

    def get_image(self, prompt):
        try:
            response = self.client.images.generate(
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
        return None


if __name__ == "__main__":
    ai_client = AIClient(config["OPENAI_API_KEY"])
    ai_client.initialize_application(share=False)
