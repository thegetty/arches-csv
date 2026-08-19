import re
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(re.sub(r"_", r"-", r"arches_nested_tile_csv_importer"), "arches_nested_tile_csv_importer.urls", name="arches_nested_tile_csv_importer"),
)
