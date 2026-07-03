import re
from django_hosts import patterns, host

host_patterns = patterns(
    "",
    host(re.sub(r"_", r"-", r"arches_csv"), "arches_csv.urls", name="arches_csv"),
)
