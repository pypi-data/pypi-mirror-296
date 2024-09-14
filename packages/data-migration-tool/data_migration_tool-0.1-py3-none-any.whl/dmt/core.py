import sys
import argparse
from importlib import import_module
from google.cloud.bigquery import Client


def migrate(migration_module: str, rollback: bool) -> None:
    print(f"Importing module {migration_module} (path={sys.path})")
    module = import_module(migration_module)
    print(f"Module {migration_module} imported")

    client = Client()

    if rollback:
        print("Rolling back: executing the migration 'rollback' method")
        module.rollback(client)
        print("Rollback executed successfully")
    else:
        print("Migrating: executing the migration 'migrate' method")
        module.migrate(client)
        print("Migration executed successfully")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('migration_module')
    parser.add_argument('-r', '--rollback', action='store_true')
    args = parser.parse_args()

    print(f"Executing migration tool ({args=})")
    migrate(args.migration_module, args.rollback)


if __name__ == '__main__':
    main()

