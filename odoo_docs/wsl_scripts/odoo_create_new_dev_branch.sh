#!/bin/bash


# Check if there are staged or unstaged changes in the Git repository
if [[ -n $(git status --porcelain) ]]; then
    echo "You have staged or unstaged changes in the repository. Please commit or stash them before proceeding."
    exit 1
fi


if [ "$#" -ne 3 ]; then
    echo -e "\nUsage: $0 <existing_db> <existing_branch> <dev_branch>"
    exit 1
fi
db_host=localhost
db_port=5432
db_user=odoo
db_passwd=odoo
# Assigning arguments to variables
existing_db="$1"
export PGPASSWORD="$db_passwd"
# check if there is a database with the provided name
if ! psql -h "$db_host" -p "$db_port" -U "$db_user" -d postgres -Atc "SELECT datname FROM pg_database WHERE datistemplate = false;" | grep -Fxq "$existing_db"; then
    echo "Database $existing_db does not exist. Please provide a valid database name."
    exit 1
fi
existing_branch="$2"
dev_branch="$3"
# check if the branch already exists and exit the script if it does
if git show-ref --verify --quiet "refs/heads/$dev_branch"; then
    echo "Branch $dev_branch already exists. Please provide a new branch name."
    exit 1
fi

dev_db="${dev_branch}"
# Check if there is already a database with the dev_branch name
if psql -h "$db_host" -p "$db_port" -U "$db_user" -lqt | cut -d \| -f 1 | grep -qw "$dev_db"; then
    echo "Database $dev_db already exists. Please provide a different branch name."
    exit 1
fi


git fetch --all
# Checkout to the specified branch before creating a new one
git checkout "$existing_branch"
# pull latest changes from the branch
git pull origin "$existing_branch" >/dev/null 




# Create a new database with the provided name and set the owner to 'odoo'
createdb -h "$db_host" -p "$db_port" -U "$db_user" --owner=${db_user} "$dev_db" >/dev/null 

# Dump the data from the original database and restore it to the new database
pg_dump -h "$db_host" -p "$db_port" -U "$db_user" "${existing_db}" | psql -h "$db_host" -p "$db_port" -U "$db_user" -d "${dev_db}" >/dev/null 

git checkout -b "$dev_branch" 
# if branch already exists create new branch with timestamp appended



cp -r ~/.local/share/Odoo/filestore/"${existing_db}" ~/.local/share/Odoo/filestore/"$dev_db"

# Exit from 'odoo' user

echo "==================== Success ====================== "
