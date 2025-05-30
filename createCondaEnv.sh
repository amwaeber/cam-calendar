#!/bin/bash
# => Environment anderror handling setup
set -e
# Function for returning to the caller directory
retCallerDir() {
  popd > /dev/null
}
# Switch to script directory while keeping caller directory in the stack
readonly CURRENT_DIR_PATH=$(dirname "$(readlink -f "$0")")
pushd ${CURRENT_DIR_PATH} > /dev/null
# Return to caller directory on error condition
trap  'retCallerDir' ERR
# <==============================

# => Install conda environment
readonly CONDA_PATH="${CURRENT_DIR_PATH}/.condaenv"
# Deactivate any active conda environment
if [[ $(python3 -c "import sys; sys.exit('conda' in sys.version)") ]]; then
  conda deactivate
fi

# Install miniconda
cd /tmp
wget https://repo.anaconda.com/miniconda/Miniconda3-py312_25.1.1-2-Linux-x86_64.sh
chmod +x Miniconda3-py312_25.1.1-2-Linux-x86_64.sh
./Miniconda3-py312_25.1.1-2-Linux-x86_64.sh -b -f -p "${CONDA_PATH}"
rm -rf ./Miniconda3-py312_25.1.1-2-Linux-x86_64.sh
cd "${CURRENT_DIR_PATH}"

"${CONDA_PATH}"/bin/pip3 install -r requirements.txt
# <==============================

# ('cd' back to caller directory)
retCallerDir