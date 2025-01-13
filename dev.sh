# A script to aid in the development of the project while integrating with Alexa Hosted Skills
# Usage: ./dev.sh <command>

# Exit on error
set -e

# Check if the command is provided
if [ -z "$1" ]; then
  echo "Usage: ./dev.sh <command>"
  exit 1
fi

resync_hosted_skill_repo(){
    git checkout dev
    git pull --rebase
    git merge master
    # If everything is managed via the script, then we can just push (no conflicts)
    git push --no-verify
    git checkout master
}

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
    rsync -av --exclude='build' --exclude='.git' --exclude='.ask' --exclude='skill-package/skill.json' ../../../ ./
    git add .
    git commit -a -m "Trigger init from alexa-skill-llm-intent" --no-verify && git push
    resync_hosted_skill_repo
    ;;

  update)
    echo "📤 Updating the hosted skill target repo with local repo contents"
    cd build/hosted
    # Hosted build directory can be given as an argument, otherwise its $(ls -d */ | grep -v build | head -n 1)
    HOSTED_BUILD_DIR=${2:-$(ls -d */ | grep -v build | head -n 1)}
    cd $HOSTED_BUILD_DIR
    rsync -av --exclude='build' --exclude='.git' --exclude='.ask' --exclude='skill-package/skill.json' ../../../ ./
    git add .
    git commit -a -m "Trigger update from alexa-skill-llm-intent" --no-verify && git push
    resync_hosted_skill_repo
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
