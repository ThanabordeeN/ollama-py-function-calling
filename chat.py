import json
import ollama
from function import forecast_Weather
class Chat:
    def __init__(self):
        self.chat_history = []

    def clean_chat(self, fullchat):
        fullchat = fullchat.replace("```json", "").replace("```", "").replace("{{", "").replace("}}", "")
        return fullchat

    def parse_chat(self, fullchat):
        try:
            json_data = json.loads(fullchat)
            return json_data
        except json.JSONDecodeError:
            print("Error parsing JSON data.")
            return None

    def save_chat(self, json_data):
        with open("data.json", "w") as f:
            json.dump(json_data, f)

    def process_chat(self, json_data):
        forecastWeather = forecast_Weather
        if json_data and json_data['action'] in ["forecast_Weather", "forecastWeather"]:
            city_name = json_data['action_input1']
            forecast_days = json_data['action_input2']
            weather_data = forecastWeather(city= city_name,days=forecast_days)
            print(f"Current temperature in {city_name}: {weather_data['current']['temp_c']}°C")
            self.chat_history.append({'role': 'assistant', 'content': f"Current temperature in {city_name}: {weather_data['current']['temp_c']}°C"})
        elif json_data and json_data['action'] == "Final Answer": 
            print("Assistant : ",json_data['action_input'])
        else:
            print("Assistant : please try again")


    def chat(self):
        while True:
            usetools = """to use this tool, please input the following JSON code snippet:
            ```json
            {{
                "action": "forecastWeather",
                "action_input1": "city_name",
                "action_input2": "forecast_days"
            }}
            ```
            for example:
            ```json
            {{
                "action": "forecastWeather",
                "action_input1": "London",
                "action_input2": "1"
            }}
            ```
            """
            tools = f"""Forecast Weather {usetools}"""

            tool_names = ["forecast_Weather"]
            system_prompt = f"""SYSTEM
                            Assistant is a large language model trained.
                            Assistant is designed to be able to assist with a wide range of tasks, from answering simple questions to providing in-depth explanations and discussions on a wide range of topics. As a language model, Assistant is able to generate human-like text based on the input it receives, allowing it to engage in natural-sounding conversations and provide responses that are coherent and relevant to the topic at hand.
                            Assistant is constantly learning and improving, and its capabilities are constantly evolving. It is able to process and understand large amounts of text, and can use this knowledge to provide accurate and informative responses to a wide range of questions. Additionally, Assistant is able to generate its own text based on the input it receives, allowing it to engage in discussions and provide explanations and descriptions on a wide range of topics.
                            Overall, Assistant is a powerful system that can help with a wide range of tasks and provide valuable insights and information on a wide range of topics. Whether you need help with a specific question or just want to have a conversation about a particular topic, Assistant is here to assist.

                            TOOLS
                            ------
                            Assistant can ask the user to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:
                            {tools}
                            RESPONSE FORMAT INSTRUCTIONS
                            ----------------------------
                            When responding , MUST output a response in one of two formats:
                            **Option 1:**
                            Use this if you want the human to use a tool.
                            formatted in the following schema:
                            ```json
                            {{

                                "action": string, \ The action to take. Must be one of {tool_names}

                                "action_input": string \ The input to the action

                            }}

                            ```
                            **Option #2:**
                            Use this if you want to respond directly to the human. formatted in the following schema:

                            {{

                                "action": "Final Answer",

                                "action_input": string \ You should put what you want to return to use here

                            }}
                            """
            input_text = input("You: ")
            if input_text.strip():
                self.chat_history.append({'role': 'user', 'content': f"""
                                    USER'S INPUT
                                    --------------------
                                    Here is the user's input (remember to respond in json format with a single action, and NOTHING else):
                                    {input_text}"""})  # Append the user's message to the chat history
                                                
                messages = [{'role': 'system', 'content': system_prompt}] + self.chat_history  # Add the system prompt and chat history
                
                result = ollama.chat(
                    model='openhermes-2.5-mistral-7b.Q5_0',
                    messages=messages,
                    stream=False,
                )
            fullchat = result['message']['content']        
            fullchat = self.clean_chat(fullchat)
            json_data = self.parse_chat(fullchat)
            self.save_chat(json_data)
            self.process_chat(json_data)

chat = Chat()
chat.chat()