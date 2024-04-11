# Ollama Chat Assistant with WeatherAPI Integration
### Experimental
## Project Description
This project is an experimental chat application that utilizes the Ollama framework to create a conversational interface. The chat assistant is designed to autonomously consider the use of tools, such as the WeatherAPI, to provide users with weather forecasts.

## Features
- **Ollama Framework**: Leverages the Ollama framework for managing chat conversations.
- **WeatherAPI Integration**: Uses WeatherAPI to fetch weather forecasts for user-specified locations and durations.
- **JSON Interaction**: Interacts with users through JSON-formatted messages to process weather forecast requests.
- **Chat History Management**: Maintains a history of the chat conversation, which can be cleaned and parsed as needed.

## How It Works
1. Users start a chat session and input their requests in a JSON format.
2. The chat assistant processes the request, calls the `forecast_Weather` function with the provided parameters, and returns the current temperature.
3. The chat history is saved and can be used to review past interactions.

## Getting Started
To use this chat assistant, clone the repository and install the necessary dependencies. Ensure you have the `ollama` package and the `forecast_Weather` function available in your environment.

## Usage
Run the chat application and follow the on-screen prompts to input your weather forecast request in the specified JSON format.

## Contributions
Contributions are welcome! If you have suggestions for improvements or new features, feel free to fork the repository and submit a pull request.

## License
This project is open-sourced under the MIT License. See the LICENSE file for more details.
