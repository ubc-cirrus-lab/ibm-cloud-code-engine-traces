# check that the data directory exists and has all the required pickle files
if [ ! -d "data" ]; then
    echo "Data directory does not exist. Make sure to run 'decompress.sh' first."
    exit 1
fi
# check if there are 11 distinct pickle files in the data directory
num_files=$(ls data/*.pickle 2> /dev/null | wc -l)
if [ "$num_files" -ne 11 ]; then
    echo "Data directory must contain exactly 11 pickle files (1 app config and 10 weeks). Found $num_files files. Make sure to run 'decompress.sh' first."
    exit 1
fi

# create a python3 virtual environment if does not exist in this directory
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# activate the virtual environment
source venv/bin/activate

# install required packages
pip3 install -r requirements.txt