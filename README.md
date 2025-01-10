# alexa-skill-llm-intent

An Alexa Skill template that gives you a ready to use skill to start a turn conversation with an AI. Ask a question and get answered with Alexa's soothing voice, powered by ChatGPT or other llm.

## Setup

1. Copy `config.example.json` to `config.json`
2. Set `llm_url` value in `config.json` to an Open AI API Compatible provider api url.
3. Set `llm_key` in `config.json` to your llm provider API key
3. Set `llm_model` to a provider compatible `model` argument (or 'webhook' to proxy request as POST to `llm_api_url`), in `config.json`.
4. Zip this repository (to later import it in the Alexa Developer Console).
5. Create a new Alexa Skill in the Alexa Developer Console.
6. Go in the Code tab of the Alexa Developer Console and click "Import Code".
7. Select the zip file with the contents of this repository.
8. Click "Save" and "Build Model".
9. Go in the Test tab of the Alexa Developer Console and test! You can also use your alexa devices if they are connected to the same account!

## Usage

### Commands

- `Alexa, I want to ask <invokation_name> a question`
- `Alexa, ask <invokation_name> about our solar system`
- `Alexa, ask <invokation_name> to explain the NP theorem`

# Disclaimer

Use at your own risk. This is a template and should be used as a starting point for your own Alexa Skill. The code is provided as is and I am not responsible for any misuse or damages caused by this code.