# arches-csv

`arches-csv` is an Arches extension that adds a Bulk Data Manager ETL module for
loading Arches resource data from CSV files.

The extension installs as a separate CSV import module named
`Import Single CSV Plugin`. It does not replace the bundled Arches
`Import Single CSV` module.

## Requirements

- Python 3.10+
- Arches `>=7.6.17,<8.3.0`
- Django 4.2

## Installation

Install the package into the same Python environment that runs the host Arches
project:

```bash
pip install arches-csv
```

For local development, install the checkout in editable mode:

```bash
pip install -e /path/to/arches-csv
```

## Configure The Host Arches Project

Add `arches_csv` to the host project's `INSTALLED_APPS` before `arches.app`.

Example:

```python
INSTALLED_APPS = (
    # Django, Arches, and project apps...
    "arches_csv",
)

# Keep arches.app last so extension templates and static assets can override
# core Arches files when needed.
INSTALLED_APPS += ("arches.app",)
```

## Apply Migrations

Run the extension migration from the host Arches project:

```bash
python manage.py showmigrations arches_csv
python manage.py migrate arches_csv
```

The migration registers the Bulk Data Manager ETL module:

```text
name: Import Single CSV Plugin
slug: import-single-csv-plugin
component: views/components/etl_modules/import-single-csv-plugin
backend module: import_single_csv_plugin.py
class: ImportSingleCsv
```

The plugin uses a distinct module and component name so it can coexist with the
bundled Arches CSV importer:

```text
Bundled Arches module: Import Single CSV / import-single-csv
External plugin module: Import Single CSV Plugin / import-single-csv-plugin
```

## Build Frontend Assets

After installing the extension or changing hosted apps, rebuild the host
project's frontend assets:

```bash
python manage.py generate_frontend_configuration
npm install
npm run build_development
```

For production deployments, use the host project's production build command.

If the frontend has not been rebuilt, opening the plugin ETL task can fail with
a browser console error such as:

```text
Unknown component 'import-single-csv-plugin'
```

## Basic Use

1. Start the host Arches application and Celery worker.
2. Open Bulk Data Manager.
3. Select `Import Single CSV Plugin`.
4. Choose the target resource model.
5. Upload a CSV file.
6. Map CSV columns to Arches node aliases.
7. Validate the file, then run the import.

For a first smoke test, use a small CSV with simple string fields before adding
concept or resource-instance relationship columns. Relationship fields require
the referenced resources to exist in the database, and concept fields require
valid concept UUIDs or labels.

## Development

Useful local checks:

```bash
python -m py_compile \
  arches_csv/etl_modules/ext_import_single_csv.py \
  arches_csv/etl_modules/import_single_csv_plugin.py \
  arches_csv/migrations/0001_add_csv_etl_module.py

python manage.py check
npm run build_development
```

Run database-changing commands only against an approved local or test database.
