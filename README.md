# alexa-skill-llm-intent

An Alexa Skill template that gives you a ready to use skill to start a turn conversation with an AI. Ask a question and get answered with Alexa's soothing voice, powered by ChatGPT or other llm.

## Configuration

### Setting up Environment variables

You should setup your configuration file by copying `config.example.json` to `config.json` and filling the required fields:
- `llm_url` -> an Open AI API Compatible provider api url.
- `llm_key`-> llm provider API key.
- `llm_model` -> the model name/version to use with the provider API. Set to 'webhook' to proxy request as POST to `llm_api_url`, and sending `llm_key` as the `token` key of the json body.

### Modifying Skill Package

You can modify the skill package by changing the `skill-package/interactionModels/custom/en-US.json` file. This file contains the intents, slots and utterances that the skill will use to interact with the user.

`skill-package/skill.json` contains the skill metadata, such as the name, description, and invocation name. This is not required to be changed to only run the skill in development mode, but will be necessary if you ever want to use this in a live environment as a published skill.

For more information about the `skill-package` structure, check the [ASK CLI documentation](https://developer.amazon.com/en-US/docs/alexa/smapi/skill-package-api-reference.html#skill-package-format).

## Creating an Alexa Skill

To use this template, you need to have a skill in your Alexa Developer Console. You can do this in the the Alexa Developer Console itself and upload a build package manually, or use the ASK CLI to create a new project using this repository as template.

### Using the Alexa Developer Console

1. Build the upload package by running `make build` (to later import it in the Alexa Developer Console).
5. Create a new Alexa Skill in the Alexa Developer Console.
6. Go in the Code tab of the Alexa Developer Console and click "Import Code".
7. Select the zip file with the contents of this repository.
8. Click "Save" and "Build Model". The skill should be ready to use.

For more information, check the documentation here: [Importing a Skill into the Alexa Developer Console](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-create.html#create-console).

### Using the Ask CLI

Run the following command in your terminal:

```bash
ask new --template-url https://github.com/paulotruta/alexa-skill-llm-intent.git
```

This will use the contents of this repository to create a new Alexa Skill project in your account. Fill the required information in the wizard, and the project will be created.

```
Please follow the wizard to start your Alexa skill project ->
? Choose a modeling stack for your skill:  Interaction Model
  The Interaction Model stack enables you to define the user interactions with a combination of    utterances, intents, and slots.
? Choose a method to host your skill's backend resources:  Alexa-hosted skills
  Host your skill code by Alexa (free).                                                            ? Choose the default region for your skill:  eu-west-1
? Please type in your skill name:  test import llm
? Please type in your folder name for the skill project (alphanumeric):  testimportllm
⠼ Creating your Alexa hosted skill. It will take about a minute.
```

After the project is created, you can deploy it to your Alexa Developer Console by running:

```bash
cd testimportllm
ask deploy
```

Full Documentation on the Ask CLI can be found [here](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-ask-cli.html).

## Usage

Once the skill is created, you can test it in the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) or via your Alexa device directly!

### Commands

- `Alexa, I want to ask <invokation_name> a question`
- `Alexa, ask <invokation_name> about our solar system`
- `Alexa, ask <invokation_name> to explain the NP theorem`

# Disclaimer

Use at your own risk. This is a template and should be used as a starting point for your own Alexa Skill. The code is provided as is and I am not responsible for any misuse or damages caused by this code.
