# arches-nested-tile-csv-importer

`arches-nested-tile-csv-importer` is an Arches extension that adds a Bulk Data
Manager ETL module for loading Arches resource data from CSV files.

It goes beyond the bundled Arches `Import Single CSV` importer by adding
graph-driven CSV template downloads, nested-card mapping and staging,
parent-child tile linking, and an update-existing-resource path.

The extension installs as a separate CSV import module named
`Import Single CSV Plugin`. It does not replace the bundled Arches
`Import Single CSV` module.

## Capabilities

- Installs as a separate Bulk Data Manager ETL module with its own migration,
  backend module, and Knockout component.
- Generates CSV templates from a selected resource model graph.
- Includes a `ResourceID` control column for selecting existing resources or
  allowing the importer to create new resource identifiers.
- Uses a literal `None` placeholder convention in generated templates; cells
  with that value are skipped by the loader.
- Exposes non-semantic nested graph nodes for CSV mapping, not only top-card
  nodes.
- Stages repeated and nested-card values into multiple tile candidates when
  needed.
- Links child staging rows to parent staging rows through `parenttileid`.
- Supports an update mode that compares CSV-derived tile data against existing
  tile JSON and stages update operations.
- Recalculates tile `sortorder` after import.
- Preserves compatibility with Arches versions where `load_staging.sortorder`
  may or may not exist.

## Requirements

- Python 3.10+
- Arches `>=7.6.17,<8.3.0`
- Django 4.2

## Installation

Install the package into the same Python environment that runs the host Arches
project:

```bash
pip install arches-nested-tile-csv-importer
```

For local development, install the checkout in editable mode:

```bash
pip install -e /path/to/arches-nested-tile-csv-importer
```

## Configure The Host Arches Project

Add `arches_nested_tile_csv_importer` to the host project's `INSTALLED_APPS`
before `arches.app`.

Example:

```python
INSTALLED_APPS = (
    # Django, Arches, and project apps...
    "arches_nested_tile_csv_importer",
)

# Keep arches.app last so extension templates and static assets can override
# core Arches files when needed.
INSTALLED_APPS += ("arches.app",)
```

## Apply Migrations

Run the extension migration from the host Arches project:

```bash
python manage.py showmigrations arches_nested_tile_csv_importer
python manage.py migrate arches_nested_tile_csv_importer
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
5. Download a graph-driven CSV template or upload an existing CSV file.
6. Map CSV columns to Arches node aliases.
7. Choose whether to insert new data or use update mode for existing resources.
8. Validate the file, then run the import.

For a first smoke test, use a small CSV with simple string fields before adding
concept or resource-instance relationship columns. Relationship fields require
the referenced resources to exist in the database, and concept fields require
valid concept UUIDs or labels.

## Maintenance Notes

This extension should be treated as a customized CSV resource import subsystem,
not as a drop-in copy of the bundled Arches importer. Future Arches upgrades
should manually review behavior around template generation, nested-node mapping,
repeated-card staging, `parenttileid` linking, update mode, async/Celery loading,
and tile sort-order handling.

## Development

Useful local checks:

```bash
python -m py_compile \
  arches_nested_tile_csv_importer/etl_modules/ext_import_single_csv.py \
  arches_nested_tile_csv_importer/etl_modules/import_single_csv_plugin.py \
  arches_nested_tile_csv_importer/migrations/0001_add_csv_etl_module.py \
  arches_nested_tile_csv_importer/tasks.py

python manage.py check
npm run build_development
```

Run database-changing commands only against an approved local or test database.