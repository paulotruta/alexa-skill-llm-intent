# A script to aid in the development of the project while integrating with Alexa Hosted Skills
# Usage: ./dev.sh <command>

# Exit on error
set -e

# Check if the command is provided
if [ -z "$1" ]; then
  echo "Usage: ./dev.sh <command>"
  exit 1
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
# - init: Initialize the project with an existing skill id
# - update: Update the skill hosted repo with the code from the local repo
# - deploy: Update the model and Deploy the code from the skill hosted repo

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

  deploy)
    echo "Deploying the code from the skill hosted repo"
    ask deploy
    ;;

  *)
    echo "Invalid command: $COMMAND"
    echo "Usage: ./dev.sh <command>"
    echo "Commands can be: new, init, update, deploy"
    exit 1
    ;;
esac
