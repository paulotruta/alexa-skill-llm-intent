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

new:
	@echo "\n🎯 Creating a new hosted skill target\n"
	@./dev.sh new
	@echo "\n✅ Hosted skill created. To push repo code, run 'make update'"

init:
	@echo "\n🎯 Initializing hosted skill target with id $(id)\n"
	@./dev.sh init $(id)
	@echo "\n✅ Hosted skill initialized. To push repo code, run 'make update'"

update:
	@echo "\n🎯 Updating hosted skill target $(skill)\n"
	@./dev.sh update $(skill)
	@echo "\n✅ Code updated in hosted skill. Please check the status and test in the Alexa Developer Console"

list:
	./dev.sh list
