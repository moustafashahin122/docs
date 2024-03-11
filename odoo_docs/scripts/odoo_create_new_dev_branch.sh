#!/bin/bash

# Check if the correct number of arguments are provided
if [ "$#" -ne 2 ]; then
    echo -e "\nUsage: $0 <database_name_to_backup> <git_branch>"
    exit 1
fi

# Assigning arguments to variables
db_name="$1"
git_branch="$2"
backup_db_name="${git_branch}"

# Drop the existing backup database if it exists
dropdb "$backup_db_name" >/dev/null 

# Create a new database with the provided name and set the owner to 'odoo'
createdb --owner=metrics "$backup_db_name" >/dev/null 

# Dump the data from the original database and restore it to the new database
pg_dump "$db_name" | psql -d "$backup_db_name" >/dev/null 

git checkout -b "$git_branch"

cp -r ~/.local/share/Odoo/filestore/"$db_name" ~/.local/share/Odoo/filestore/"$backup_db_name"

# Exit from 'odoo' user

echo "==================== Success ====================== "
