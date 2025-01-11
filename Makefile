.DEFAULT_GOAL := release
.ONESHELL:

BUILD_DIR=build


release: clean
	mkdir $(BUILD_DIR)
	zip -r $(BUILD_DIR)/alexa-skill-llm-intent-release.zip lambda -x lambda/\config.example.json -x lambda/\.venv/\*


clean:
	rm -rf $(BUILD_DIR)


dev: clean
	cd lambda
	python -m venv .venv
	. .venv/bin/activate
	pip install -r requirements.txt
