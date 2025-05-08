#!/bin/bash
#set -x #debug enable/disable

# Check if user has bash
[ ${BASH_VERSION%%.*} -ge 3 ] || { echo "Need bash =>v3"; exit 1; }

# Define programms array based on user OS
declare -a programs=("python3" "pip3" "unzip" "curl")
declare -a not_installed_programs=()

# Find the programs which the user has not installed
for i in "${programs[@]}"; do
    [ $(command -v $i) ] || not_installed_programs+=("$i")
done

# Tell user to install the programs they need
[ "${#not_installed_programs[@]}" -ne 0 ] && { echo "Missing ${not_installed_programs[@]}"; exit 2; }

# Assume programs have been installed.
declare -r prog_name="alien-invasion"
declare -r git_rep="https://codeload.github.com/SurenMar/${prog_name}/zip/refs/heads/main"

# Get files from repo and store in zip file
curl -s -o "${prog_name}.zip" "$git_rep"

[ $? -ne 0 ] && { echo "Error: Could not download files"; exit 3; }

# Check if downloaded files are corrupted
unzip -t -qq "${prog_name}.zip" && { unzip -qq "${prog_name}.zip"; } \
				|| { echo "Some files are corrupted! Exiting..."; exit 4; }

# Clean up directory
rm "${prog_name}.zip" && mv "${prog_name}-main" $prog_name

# Install pygame if user does not have it installed
pip3 -q install pygame
[ $? -ne 0 ] && { echo "Unable to install required libraries. Exiting..."; exit 5; }

chmod +x "$prog_name"/run.sh

echo -e "You're all set,\nsimply type ./run.sh in the termal and enjoy the game!"

exit 0
