.DEFAULT_GOAL := release
.ONESHELL:

BUILD_DIR=build

BUILD_REPO_DIR=build/hosted
BUILD_REPO_DIR=build/package


release: clean
	mkdir -p $(BUILD_DIR)
	mkdir -p $(build_package_dir)
	zip -r $(build_package_dir)/alexa-skill-llm-intent-release.zip lambda -x lambda/\config.example.json -x lambda/\.venv/\*  -x "**/__pycache__/**"

import-package:
	ask smapi import-skill-package -s $(id) -f ./$(BUILD_DIR)/alexa-skill-llm-intent-release.zip

clean:
	rm -rf $(build_package_dir)

dev: clean
	python -m venv .venv
	. .venv/bin/activate
	pip install -r lambda/requirements-dev.txt

new:
	./dev.sh new
	# mkdir -p $(BUILD_DIR)
	# mkdir -p $(BUILD_REPO_DIR)
	# cd $(BUILD_REPO_DIR) && ask new && cd $(ls -d */ | grep -v build | head -n 1) && cp -r ../../* ./ && git commit -a -m "Trigger init from alexa-skill-llm-intent" && git push
	@echo "\n✅ Code initialized in hosted skill. Please manage the changes in ./$(BUILD_REPO_DIR), or deploy with 'make deploy'"

init:
	./dev.sh init $(id)
	# mkdir -p $(BUILD_DIR)
	# mkdir -p $(BUILD_REPO_DIR)
	# cd $(BUILD_REPO_DIR) && ask init --hosted-skill-id $(id) && cd $(ls -d */ | grep -v build | head -n 1) && cp -r ../../* ./ && git commit -a -m "Trigger init from alexa-skill-llm-intent" && git push


model:
	cd $(BUILD_REPO_DIR) && ask smapi update-model -s $(id) -l en-US -f ./skill-package/interactionModels/custom/en-US.json

update:
	./dev.sh update
	# mkdir -p $(BUILD_DIR)
	# mkdir -p $(BUILD_REPO_DIR)
	# pwd && cd $(BUILD_REPO_DIR) && cd $(ls -d */ | grep -v build | head -n 1) && cp -r ../../* ./
	@echo "\n✅ Code updated in hosted skill. Please manage the changes in ./$(build_repo_dir), or deploy with 'make deploy'"

make deploy:
	cd $(BUILD_REPO_DIR) && cd $(ls -d */ | grep -v build | head -n 1) && git commit -a -m "Trigger deploy from alexa-skill-llm-intent" && git push
	@echo "\n✅ Code deployed started for hosted skill. Please check the status in the Alexa Developer Console"
