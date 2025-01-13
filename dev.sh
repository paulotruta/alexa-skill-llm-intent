# A script to aid in the development of the project while integrating with Alexa Hosted Skills
# Usage: ./dev.sh <command>

# Exit on error
set -e

# Check if the command is provided
if [ -z "$1" ]; then
  echo "Usage: ./dev.sh <command>"
  exit 1
fi

# Check if the command is valid, commands can be:
# - init: Initialize the project with an existing skill id
# - update: Update the skill hosted repo with the code from the local repo
# - deploy: Update the model and Deploy the code from the skill hosted repo

COMMAND=$1

case $COMMAND in
  new)
    echo "🎯 Creating a new hosted skill target"
    mkdir -p build
    mkdir -p build/hosted
    cd build/hosted
    ask new
    cd $(ls -d */ | grep -v build | head -n 1)
    pwd
    ;;

  init)
    if [ -z "$2" ]; then
      echo "Usage: ./dev.sh init <skill-id>"
      exit 1
    fi
    SKILL_ID=$2
    echo "Initializing project with skill id: $SKILL_ID"
    mkdir -p build
    mkdir -p build/hosted
    cd build/hosted
    pwd
    ask init --hosted-skill-id $SKILL_ID
    cd $(ls -d */ | grep -v build | head -n 1)
    pwd
    rsync -av --exclude='build' --exclude='.git' --exclude='.ask' ../../../ ./
    git commit -a -m "Trigger init from alexa-skill-llm-intent" --no-verify && git push
    ;;

  update)
    echo "📤 Updating the hosted skill target repo with local repo contents"
    # Hosted build directory can be given as an argument, otherwise its $(ls -d */ | grep -v build | head -n 1)
    HOSTED_BUILD_DIR=${2:-$(ls -d */ | grep -v build | head -n 1)}
    rsync -av --exclude='build' --exclude='.git' --exclude='.ask' ./ build/hosted/$HOSTED_BUILD_DIR/
    cd build/hosted/$HOSTED_BUILD_DIR
    git commit -a -m "Trigger update from alexa-skill-llm-intent" --no-verify && git push

    # ask smapi update-skill-manifest --skill-id $SKILL_ID --manifest file://skill.json
    # ask smapi update-interaction-model --skill-id $SKILL_ID --locale en-US --interaction-model file://models/en-US.json
    ;;

  deploy)
    echo "Deploying the code from the skill hosted repo"
    ask deploy
    ;;

  *)
    echo "Invalid command: $COMMAND"
    echo "Usage: ./dev.sh <command>"
    echo "Commands can be: init, update, deploy"
    exit 1
    ;;
esac
