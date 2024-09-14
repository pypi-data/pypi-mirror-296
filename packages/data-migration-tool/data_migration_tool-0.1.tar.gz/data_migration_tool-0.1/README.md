# dmt (Data migration tool)

Note: has been thought for GCP / BigQuery.

## Why this tool?

Most data transformation tools (dataform, dbt) have schema-on-read features. In other words, you don't have to take
care of the schema migration. This is enough 98% of the time.

The main use case of this tool is to provide a framework to handle the remaining 2% of use cases when you want to automate the migration of your schemas:
- source tables
- big data tables

### Handle any BigQuery resource

This tool can/should only impact resources with a lifecycle (create, update, delete) that can be managed in SQL,
such as:
- views
- user defined functions (udfs)

## How to create a new BigQuery migration?

- Create a python file in a `migrations` directory
- The file should be named following the convention `XXXX_my_migration_name.py`
- Write a `migrate` and a `rollback` function

### This tool does not replace terraform

Note that you can use this tool to execute any side effect on your data and cloud resources that can be executed in
python thanks to the google cloud SDK.

That being said, we strongly recommend to manage your infrastructure resources with terraform.

## How to execute a migration?

### Executing a migration
```
PYTHONPATH=/PATH/TO/migrations dmt XXXX_my_migration_name.py
```

### Rolling back
```
PYTHONPATH=/PATH/TO/migrations dmt XXXX_my_migration_name.py --rollback
```

### Before executing
```
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Runtime relies on [application default credentials](https://cloud.google.com/docs/authentication/provide-credentials-adc).
```
gcloud auth application-default login
```

Configure the project:
```
gcloud config set project my-gcp-project

or

export GOOGLE_CLOUD_PROJECT=my-gcp-project
```

## Limitations

Ideally this tool should support:
- Resolving the linked list of migration versions at runtime to understand that one migration comes after another one
- Executing multiple migrations versions from a single execution command
- Remembering the migration version by storing it in a database
- Reading the latest known version to understand all subsequent migrations to execute + execute them
- Proposing helper functions (`rename_table`, `rename_column`, `remove_column`, `add_column`, etc.) to generate
  migration and rollback SQL code
- Automatically executing `BEGIN TRANSACTION`, `COMMIT TRANSACTION` and `ROLLBACK TRANSATION` statements before / after
  executing the migrate and rollback functions. This would open the possibility to add a `--dry-run` flag, which would
  be convenient during development cycles.

