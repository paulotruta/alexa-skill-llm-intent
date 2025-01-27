<p>
	<img width="256" src="./skill-package/assets/images/en-US_largeIcon.png"/>
</p>

# alexa-skill-llm-intent

[![ci](https://github.com/paulotruta/alexa-skill-llm-intent/actions/workflows/ci.yml/badge.svg)](https://github.com/paulotruta/alexa-skill-llm-intent/actions/workflows/ci.yml)

An Alexa Skill template that gives you a ready to use skill to start a turn conversation with an AI. Ask a question and get answered with Alexa's soothing voice, powered by ChatGPT or other llm.

- [alexa-skill-llm-intent](#alexa-skill-llm-intent)
  - [Configuration](#configuration)
    - [Requirements](#requirements)
    - [Setting up Environment variables](#setting-up-environment-variables)
  - [Creating an Alexa Skill](#creating-an-alexa-skill)
    - [Automated - Using the Makefile (Alexa Hosted Skills Management)](#automated---using-the-makefile-alexa-hosted-skills-management)
      - [Create a new Alexa Skill](#create-a-new-alexa-skill)
      - [Importing an existing Alexa Skill](#importing-an-existing-alexa-skill)
      - [List existing Alexa Hosted Skill targets](#list-existing-alexa-hosted-skill-targets)
      - [Setting the Skill configuration file and invocation words](#setting-the-skill-configuration-file-and-invocation-words)
      - [Updating the Skill](#updating-the-skill)
      - [Debugging Dialog Model](#debugging-dialog-model)
      - [Debugging Lambda Function](#debugging-lambda-function)
    - [Manual - Using the Alexa Developer Console](#manual---using-the-alexa-developer-console)
    - [Advanced - Using the Ask CLI](#advanced---using-the-ask-cli)
  - [Usage](#usage)
    - [Commands](#commands)
  - [Development](#development)
    - [Local Development](#local-development)
    - [Skill Package](#skill-package)
    - [Skill Lambda Function](#skill-lambda-function)
- [Contributing](#contributing)
- [Disclaimer](#disclaimer)


## Configuration

### Requirements

- [Alexa Developer Account](https://developer.amazon.com/alexa)
- [ASK CLI](https://developer.amazon.com/en-US/docs/alexa/smapi/quick-start-alexa-skills-kit-command-line-interface.html)
- [OpenAI API schema](https://github.com/openai/openai-openapi) compatible llm provider API url, key, and model name: [Open AI](https://platform.openai.com) / [Anthropic](https://www.anthropic.com/) / [OpenRouter](https://openrouter.ai/)
- Python 3.8 (optional for local development)
- [AWS Account](https://aws.amazon.com/) (optional for advanced deployment)

### Setting up Environment variables

You should setup your configuration file by copying `config.example.json` to `config.json` and filling the required fields:

- **`invocation_name`** -> The invocation name for the skill
  - *example: `gemini flash`*
- **`llm_url` ->** OpenAI OpenAPI Schema Compatible LLM API provider url
  - *example: `https://openrouter.ai/api/v1/chat/completions`*
- **`llm_model` ->** Model name/version to use with the provider API
  - *example: `google/gemini-2.0-flash-exp:free`*
- **`llm_key`->** Provider API key
  - *example: `sk-or-v1-<Secret_Code>`*



>*ℹ️ Set `llm_model` to `webhook` to proxy the alexa request as a POST call to `llm_api_url`, sending `llm_key` as the `token` key of the json body, together with useful alexa request context.*

>*⚠️ Note that the invocation name configuration value is only automatically set on deployment using the `(Automated) Makefile` method, and only for the `en-US` locale. If you are using the `(Manual) Alexa Developer Console` method, or trying to support multiple locales, you should instead set the `invocationName` value manually in the `skill-package/interactionModels/custom/<locale>.json` files.*

>*ℹ️ If you don't provide a `llm_system_prompt`, the skill will use a default system prompt, which you can see in `./lambda/lambda_function.py:37` *

## Creating an Alexa Skill

To use this template, you need to at least have an account setup in the [Alexa Developer Console](https://developer.amazon.com/alexa).

**There's three ways you can use this template in a skill:**
- **Automated ->** Using the `Makefile` to create and manage a new or imported Alexa Hosted Skill project
- **Manual ->** in the the `Alexa Developer Console` itself, by uploading a build package
- **Advanced ->** Using the `ask CLI` to create and manage a new AWS-hosted or Self-hosted skill project using this repository as template.

### Automated - Using the Makefile (Alexa Hosted Skills Management)

>*ℹ️ This is the recommended way to create a new Alexa Skill using this template. It leverages the Ask CLI to create a new project and deploy it to your Alexa Developer Console. You can have multiple targets and deploy the template to different skills.*

This method supports version control, testing, and debugging, and integrates with the Alexa Developer Console seamlessly.

>*⚠️ Make sure you have the `ask` CLI installed and configured with your Amazon Developer account before running this command. If not, install it by running `npm install -g ask-cli` and configure it by running `ask configure`.*

#### Create a new Alexa Skill

Run the following command in your terminal:

```bash
make new
```

And follow the wizard to create a new Alexa Skill project as a target, choosing the following options:

- **? Choose a modeling stack for your skill:**  `Interaction Model`
- **? Choose the programming language you will use to code your skill:**  `Python`
- **? Choose a method to host your skill's backend resources:**  `Alexa Hosted`

>*⚠️ If you don't choose the specified options on the New Skill Wizard, the process could fail as this template is made to run an Interaction Model skill in Python, while the Makefile method currently only supports Alexa Hosted skills.*

The skill will start being created:
```
🎯 Creating a new hosted skill target

Please follow the wizard to start your Alexa skill project ->
? Choose a modeling stack for your skill:  Interaction Model
  The Interaction Model stack enables you to define the user interactions with a combination of utterances, intents, and slots.
? Choose the programming language you will use to code your skill:  Python
? Choose a method to host your skill's backend resources:  Alexa-hosted skills
  Host your skill code by Alexa (free).
? Choose the default region for your skill:  eu-west-1
? Please type in your skill name:  gemini flash
? Please type in your folder name for the skill project (alphanumeric):  geminiflash
⠧ Creating your Alexa hosted skill. It will take about a minute.

(...)

Lambda code for gemini flash created at
        ./lambda

Skill schema and interactionModels for gemini flash created at
        ./skill-package

The skill has been enabled.

Hosted skill provisioning finished. Skill-Id: amzn1.ask.skill.b9198cd2-7e05-4119-bc9b-fe264d2b7fe0
Please follow the instructions at https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-ask-cli.html to learn more about the usage of "git" for Hosted skill.
🔗 Finished. Current targets:
geminiflash             perplexitysearch        testapplication

✅ Hosted skill created. To push repo code, run 'make update'
```

A new Alexa Hosted Skill target will show up in your Alexa Developer account with the provided name, but its code and configuration is from a blank "hello world" project. But it is now ready to be updated with the template code (check the `make update` command below).

>*⚠️ Due to instabilities on Amazon's infrastrucure side, sometimes this process can hang while the skill is being created. This can result in you seeing the skill in the developer console but not on your machine. Give it an hour, delete the skill and creating a new one again.*


#### Importing an existing Alexa Skill

If you already have an existing Alexa Skill and want to import this template to it (overriding any previous code, model interactions, and actions), you can run:

```bash
make init id=<skill_id>
```

This will import your skill as a Alexa Hosted Skill target, which you can then use to update the skill to use this template.

>*⚠️ Be aware that if your imported Alexa-Hosted skill contains any custom code or configurations, they will be fully overriten once you run the `make update` command after importing your skill as a target.*

#### List existing Alexa Hosted Skill targets

You can list all the existing Alexa Hosted Skill targets being managed by this project by running:

```bash
make list
```

This will return a list of `<skill_slug>` and the date they were created or imported, for example:

```
perplexitysearch -> Created on Jan 13 02:12
testapplication -> Created on Jan 13 02:45
```

>*ℹ️ These are available in the `build/hosted` folder, and are the target hosted repositories, that can individually be managed by navigating to the respective folder and using the `ask` CLI.*

#### Setting the Skill configuration file and invocation words

When your skill was created or imported, it automatically use the `config.json` in the `lambda` directory as its configuration. But you might want to set a different configuration per target hosted skill. Use the following command to set a target configuration file:

```bash
make config skill=<skill_slug> file=<config_file_path>
```

This will make a copy of this file into `/build/hosted/<skill_slug>_config.json`, which will be used by the skill when it is updated. The invocation words for the skill are set at update time using the `invokation_name` value in the `config.json` file.

>*⚠️ The config files in `/build/hosted/<skill_slug>_config.json` can also be changed manually before running `make update`.*

#### Updating the Skill

After creating a new skill or importing an existing one, you can update the skill to use this template.

You can do this by running:

```bash
make update skill=<skill_slug>
```

This will deploy the code to the Alexa Developer Console and trigger a Model and lambda function build. Once the deployment finishes, it will be ready to use.

You should also run this every time you make changes to the skill package or the lambda function code, to update the skill in the Alexa Developer Console.

>*⚠️ Currently this project only allows sync in one direction, from the local repository to the Alexa Developer Console. Any changes made in the Alexa Developer Console will be overwritten by the local repository when you run the update command.*

#### Debugging Dialog Model

You can debug the dialog model (using `ask dialog`) for a skill target project by running:

```bash
make dialog skill=<skill_slug> locale=<locale>
```

#### Debugging Lambda Function

You can debug the lambda function (using `ask run`) for a skill target project by running:

```bash
make debug skill=<skill_slug>
```

>*❌ This command is not fully tested and might not work properly at the moment. Contributions are welcome 😉*

>*⚠️ Because of Alexa hosted skills limitations, debugging using `make debug skill=<skill_slug>` (or the `ask run` CLI command) is currently only available to customers in the NA region. You will only be able to use the debugger this way if your skill is hosted in one of the US regions.*

### Manual - Using the Alexa Developer Console

>*ℹ️ This method is recommended for beginners, as it requires less configuration and manual steps. Follow this method if you are not familiar with the ASK CLI and want to use the Alexa Developer Console directly.*

1. Make sure you the `config.json` file and `invocation_name` value in `skill-package/interactionModels/custom/en-US.json` is setup correctly.
2. Build the upload package by running `make package` (to later import it in the Alexa Developer Console).
3. Create a new Alexa Skill in the Alexa Developer Console.
4. Go in the Code tab of the Alexa Developer Console and click "Import Code".
5. Select the zip file located in the `./build/package/` directory.
6. Click "Save" and "Build Model". The skill should be ready to use.

For more information, check the documentation here: [Importing a Skill into the Alexa Developer Console](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-create.html#create-console).

### Advanced - Using the Ask CLI

>*ℹ️ This method is not recommended for beginners, as it requires more manual steps and configuration and requires using an AWS account you own to host the lambda function. Only follow this method if you know what you're doing and have previous experience with Alexa Skills development using AWS.*

Choose a location for your new skill project (not this repository, as it will be cloned). Run the following command in your terminal (at your chosen location) to start a new skill project using this template:

```bash
ask new --template-url https://github.com/paulotruta/alexa-skill-llm-intent.git
```

This will use the contents of this repository to create a new Alexa Skill project in your account. Fill the required information in the wizard, and the project will be created.

After the project is created, you can deploy it to your Alexa Developer Console by running:

```bash
cd llm-intent
ask deploy
```
>*⚠️ Before running deploy, make sure you modify the `config.json` file and `invokation_name` value in `skill-package/modelInteractions/custom/en-US.json` with the required configuration for the skill to work.*

Full Documentation on the Ask CLI can be found [here](https://developer.amazon.com/en-US/docs/alexa/hosted-skills/alexa-hosted-skills-ask-cli.html).

## Usage

Once the skill is created, you can test it in the [Alexa Developer Console](https://developer.amazon.com/alexa/console/ask) or via your Alexa device directly!

### Commands

Once your skill is deployed, you can interact with it using the following commands (from the Test tab in the Alexa Developer Console or your account connected Alexa devices):

- `Alexa, I want to ask <invocation_name> a question`
- `Alexa, ask <invocation_name> about our solar system`
- `Alexa, ask <invocation_name> to explain the NP theorem`
- `Alexa, open <invocation_name>`

## Development

### Local Development

To develop the skill locally, you should activate the virtual environment and install the required dependencies. You can do this by running:

```bash
make dev
```

### Skill Package

You can modify the skill package by changing the `skill-package/interactionModels/custom/en-US.json` file. This file contains the intents, slots and utterances that the skill will use to interact with the user.

`skill-package/skill.json` contains the skill metadata, such as the name, description, and invocation name. This is not required to be changed to only run the skill in development mode, but will be necessary if you ever want to use this in a live environment as a published skill.

For more information about the `skill-package` structure, check the [Skill Package Format documentation](https://developer.amazon.com/en-US/docs/alexa/smapi/skill-package-api-reference.html#skill-package-format).

>*When using the `(Automated) Makefile` method to manage Alexa Hosted Skill targets, you can debug their dialog model by using the `make dialog skill=<skill_slug>` command, which will open the dialog model test CLI for that specific skill.*

### Skill Lambda Function

The skill code is a python lambda function and is located in the `lambda/` folder. The main file is `lambda_function.py`, which contains the Lambda handlerfor the supported intents, and is the entrypoint for the rest of the code.

>*ℹ️ When using the `(Automated) Makefile` method to manage Alexa Hosted Skill targets, you can debug the lambda function by using the `make debug skill=<skill_slug>` command, which enables you to test your skill code locally against your skill invocations by routing requests to your developer machine. This enables you to verify changes quickly to skill code as you can test without needing to deploy skill code to Lambda.*

>*⚠️ Because of Alexa hosted skills limitations, debugging using `make debug skill=<skill_slug>` (or the `ask run` CLI command) is currently only available to customers in the NA region. You will only be able to use the debugger this way if your skill is hosted in one of the US regions.*

# Contributing

Feel free to contribute to this project by opening issues or pull requests. I'm open to suggestions to improve the code, especially to fix any bugs. A good place to start is checking if there are any issues with the label `good first issue` or `help wanted`.

# Disclaimer

Use at your own risk. This is a template and should be used as a starting point for your own Alexa Skill. The code is provided as is and I am not responsible for any misuse or damages caused by this code.
