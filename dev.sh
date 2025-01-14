# A script to aid in the development of the project while integrating with Alexa Hosted Skills
# Usage: ./dev.sh <command>

# Exit on error
set -e

# Check if the command is provided
if [ -z "$1" ]; then
  echo "Usage: ./dev.sh <command>"
  exit 1
fi

# Cheeck if the ask-cli is installed
if ! command -v ask &> /dev/null
then
    echo "❌ ask-cli could not be found. Please install ask-cli before running this script"
    exit
fi

update_hosted_skill_repo(){
    rsync -av --delete ../../../lambda ./
    rsync -av --delete ../../../skill-package/interactionModels ./skill-package
    rsync -av --delete ../../../skill-package/assets ./skill-package
}

resync_hosted_skill_repo(){
    git checkout dev
    git pull --rebase
    git merge master
    # If everything is managed via the script, then we can just push (no conflicts)
    git push --no-verify
    git checkout master
}

# Check if the command is valid, commands can be:
# -> new: Create a new blank target skill project as an Alexa hosted skill (requires configured ask-cli)
# -> init <skill_id>: Initialize a target skill project with an existing skill id (Must be a custom alexa hosted skill)
# -> list: List all the available target skill projects
# -> update <skill_slug>: Update the skill hosted repo with the code from the local repo (deploy)
# -> config <config_file_path>: Configure the target skill to be deployed using a copy of the provided config file
# -> dialog <skill_slug> <locale>: Debug the dialog model for the target skill
# -> debug <skill_slug>: Debug the code for the skill hosted repo

COMMAND=$1

case $COMMAND in
  new)

    mkdir -p build
    mkdir -p build/hosted
    cd build/hosted

    ask new

    echo "🔗 Finished. Current targets:"
    ls
    ;;

  init)

    if [ -z "$2" ]; then
      echo "Usage: ./dev.sh init <skill-id>"
      exit 1
    fi
    SKILL_ID=$2

    mkdir -p build
    mkdir -p build/hosted
    cd build/hosted
    pwd
    ask init --hosted-skill-id $SKILL_ID

    echo "🔗 Finished. Current targets:"
    ls
    ;;

  update)
    cd build/hosted
    # Hosted build directory can be given as an argument, otherwise its $(ls -d */ | grep -v build | head -n 1)
    HOSTED_BUILD_DIR=${2:-$(ls -d */ | grep -v build | head -n 1)}
    cd $HOSTED_BUILD_DIR
    echo "Updating hosted skill target repo: $HOSTED_BUILD_DIR"

    update_hosted_skill_repo > /dev/null 2>&1

    # Copy over the config file if it exists in ../<$HOSTED_BUILD_DIR>_config.json
    if [ -f "../${HOSTED_BUILD_DIR}_config.json" ]; then
      cp "../${HOSTED_BUILD_DIR}_config.json" "./lambda/config.json"
    else
      # Create one from the default config
      cp "./lambda/config.json" "../${HOSTED_BUILD_DIR}_config.json"
    fi

    # Copy over the invocation name if it exists as "invocation_name" in ../<$HOSTED_BUILD_DIR>_config.json
    INVOCATION_NAME=$(cat "../${HOSTED_BUILD_DIR}_config.json" | jq -r '.invocation_name')
    if [ -z "$INVOCATION_NAME" ]; then
      echo "Invocation name not found in the config file. Skipping invocation name update"
    else
      echo "Updating invocation name to $INVOCATION_NAME"
      sed -i "s/\"invocationName\": \"[^\"]*\"/\"invocationName\": \"$INVOCATION_NAME\"/g" "./skill-package/interactionModels/custom/en-US.json"
    fi

    git add .
    git commit -a -m "Trigger update from alexa-skill-llm-intent" --no-verify && git push

    resync_hosted_skill_repo
    echo "🔗 Finished updating $HOSTED_BUILD_DIR. "
    ;;

  list)
    echo "🔗 Available Targets:"
    cd build/hosted
    ls -ld */ | awk '{sub(/\/$/, "", $9); print $9 " -> Created on " $6 " " $7 " " $8}'
    ;;

  config)
    echo "🔗 Setting config file and invokation naem for hosted skill"
    SKILL_SLUG=${2}
    CONFIG_FILE=${3}

    # Check if the config file exists in the provided path
    if [ -f "$CONFIG_FILE" ]; then
      cp "$CONFIG_FILE" "./build/hosted/${SKILL_SLUG}_config.json"
    else
      echo "Config file not found. Please provide the config file path"
      exit 1
    fi

    echo "🔗 Finished setting config file and invocation name for $SKILL_SLUG. Run 'make update skill=$SKILL_SLUG' to apply changes."
    ;;

  dialog)
    echo "Debugging the dialog model from the skill hosted repo"
    HOSTED_BUILD_DIRNAME=${2}
    DIALOG_LOCALE=${3:-en-US}
    cd build/hosted/$HOSTED_BUILD_DIRNAME
    pwd
    ask dialog --locale $DIALOG_LOCALE
    ;;

  debug)
    echo "Debugging the code from the skill hosted repo"
    HOSTED_BUILD_DIRNAME=${2}
    echo $HOSTED_BUILD_DIRNAME
    cd build/hosted/$HOSTED_BUILD_DIRNAME
    pwd
    ask run
    ;;

  *)
    echo "Invalid command: $COMMAND"
    echo "Usage: ./dev.sh <command>"
    echo "Commands can be: new, init, update, deploy"
    exit 1
    ;;
esac
