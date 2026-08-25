#!/usr/bin/env python3

import csv
import re
import sys
import time
import urllib.parse
import urllib.request

manifest = sys.argv[1]

print(
    "sample_id\trequested_accession\t"
    "ncbi_accession_version\tstatus"
)

with open(manifest, newline="") as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    for row in reader:
        sample_id = row["sample_id"]
        requested = row["accession"]

        params = urllib.parse.urlencode({
            "db": "nuccore",
            "id": requested,
            "rettype": "gb",
            "retmode": "text",
        })

        url = (
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"
            f"efetch.fcgi?{params}"
        )

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "PhyloClockLab-accession-validation/1.0"}
        )

        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                text = response.read().decode("utf-8")

            match = re.search(r"^VERSION\s+(\S+)", text, re.MULTILINE)

            if not match:
                version = "NA"
                status = "FAILED"
            else:
                version = match.group(1)

                requested_base = requested.split(".")[0]
                returned_base = version.split(".")[0]

                if requested_base == returned_base:
                    status = "OK"
                else:
                    status = "MISMATCH"

        except Exception as error:
            version = "NA"
            status = f"ERROR:{type(error).__name__}"

        print(
            f"{sample_id}\t{requested}\t"
            f"{version}\t{status}"
        )

        # Stay comfortably below NCBI's unauthenticated request rate
        time.sleep(0.4)
