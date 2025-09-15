# run translate.py in path   of the bash script

# 1. get the path of the bash script
# 2. get the path of the python script
# 3. run the python script in the path of the bash script
path=$(cd `dirname $0`; pwd)
echo $path

pwd
python_path=$path/translate.py
# Create and activate virtual environment
venv_path=$path/trans_env
requirements_path=$path/trans_requirements.txt

# Create virtual environment if it doesn't exist
if [ ! -d "$venv_path" ]; then
    echo "Creating virtual environment at $venv_path"
    python3 -m venv $venv_path > /dev/null
fi

# Install requirements if requirements file exists
if [ -f "$requirements_path" ]; then
    echo "Installing requirements from $requirements_path"
    $venv_path/bin/pip install -r $requirements_path > /dev/null
fi

# Use the virtual environment python
python_path_venv=$venv_path/bin/python3

echo $python_path

$python_path_venv $python_path
