# run translate.py in path   of the bash script

# 1. get the path of the bash script
# 2. get the path of the python script
# 3. run the python script in the path of the bash script
path=$(cd `dirname $0`; pwd)
echo $path

pwd
python_path=$path/translate.py



python $python_path
