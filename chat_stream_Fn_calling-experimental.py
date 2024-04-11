import ollama
from function import forecastWeather
import json

def chat():
    """
    This function allows the user to have a conversation with an AI assistant.
    It initializes an empty list to store the chat history and prompts the user for input.
    The input is then added to the chat history and passed to the AI model for processing.
    The model's response is printed and added to the chat history.
    The conversation continues until the user decides to exit.
    """
    chat_history = []  # Initialize an empty list to store the chat history
    
    
    while True:
        usetools = """to use this tool, please input the following JSON code snippet:
        ```json
        {{
            "action": "forecastWeather",
            "action_input1": "city_name",
            "action_input2": "forecast_days" \ The number of days to forecast
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
                        ```
                        """
        input_text = input("You: ")
        fullchat = []
        
        if input_text.strip():
            chat_history.append({'role': 'user', 'content': f"""
                                USER'S INPUT
                                --------------------
                                Here is the user's input (remember to respond in json format with a single action, and NOTHING else):
                                {input_text}"""})  # Append the user's message to the chat history
                                            
            messages = [{'role': 'system', 'content': system_prompt}] + chat_history  # Add the system prompt and chat history
            
            stream = ollama.chat(
                model='openhermes-2.5-mistral-7b.Q6_K',
                messages=messages,
                stream=True,
            )
            
            print("Assistant: ", end='', flush=True)
            
            for chunk in stream:
                print(chunk['message']['content'], end='', flush=True)  # Print the model's message
                fullchat.append(chunk['message']['content'])  # Append the model's message to the chat history
            print('\n')
            fullchat = ''.join(fullchat)
            chat_history.append({'role': 'assistant', 'content': fullchat})

            try:
                fullchat = fullchat.replace("```json", "").replace("```", "").replace("{{", "").replace("}}", "")
            except:
                pass
            try:
                json_data = json.loads(fullchat)
            except json.JSONDecodeError:
                print("Error parsing JSON data.")
            else:
                with open("data.json", "w") as f:
                    json.dump(json_data, f)

            if json_data['action'] == "forecast_Weather" or json_data['action'] == "forecastWeather":
                city_name = json_data['action_input1']
                forecast_days = json_data['action_input2']
                weather_data = forecastWeather(city_name, forecast_days)
                print(f"Current temperature in {city_name}: {weather_data['current']['temp_c']}°C")
                chat_history.append({'role': 'assistant', 'content': f"Current temperature in {city_name}: {weather_data['current']['temp_c']}°C"})

chat()

