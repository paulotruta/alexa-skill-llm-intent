.DEFAULT_GOAL := release
.ONESHELL:

BUILD_DIR=build

BUILD_REPO_DIR=build/hosted
BUILD_PACKAGE_DIR=build/package


package: clean
	mkdir -p $(BUILD_DIR)
	mkdir -p $(BUILD_PACKAGE_DIR)
	zip -r $(BUILD_PACKAGE_DIR)/alexa-skill-llm-intent-release.zip lambda -x lambda/\config.example.json -x lambda/\.venv/\*  -x "**/__pycache__/**"

clean:
	rm -rf $(BUILD_PACKAGE_DIR)

dev: clean
	python -m venv .venv
	. .venv/bin/activate
	pip install -r lambda/requirements-dev.txt

# Hosted skill targets

list:
	@./dev.sh list

new:
	@echo "---"
	@echo "🎯 Creating a new hosted skill target"
	@echo "---"

	@./dev.sh new

	@echo "---"
	@echo "✅ Hosted skill created. To push repo code, run 'make update'"
	@echo "---"

import:
	@echo "---"
	@echo "🎯 Initializing hosted skill target with id $(id)"
	@echo "---"

	@./dev.sh init $(id)

	@echo "---"
	@echo "✅ Hosted skill initialized. To push repo code, run 'make update'"
	@echo "---"

update:
	@echo "---"
	@echo "🎯 Updating hosted skill target $(skill)"
	@echo "---"

	@./dev.sh update $(skill)

	@echo "---"
	@echo "✅ Hosted skill $(skill) deployed. Check completion status in the Alexa Developer Console"
	@echo "---"
config:
	@echo "---"
	@echo "🎯 Setting config file and invocation name for hosted skill target $(skill)"
	@echo "---"

	@./dev.sh config ${skill} $(file) ${invocation}

	@echo "---"
	@echo "✅ Config file and invocation name set for hosted skill target $(skill)"
	@echo "---"

dialog:
	@echo "---"
	@echo "🎯 Starting dialog for hosted skill target $(skill)"
	@echo "---"

	@./dev.sh dialog $(skill)

	@echo "---"
	@echo "✅ Dialog Session for hosted skill target $(skill) terminated"
	@echo "---"

debug:
	@echo "---"
	@echo "🎯 Debugging hosted skill target $(skill)"
	@echo "---"

	@./dev.sh debug $(skill)

	@echo "---"
	@echo "✅ Debugging session for hosted skill target $(skill) terminated"
	@echo "---"
