#!/usr/bin/env python3

import csv
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

manifest = Path(sys.argv[1])
outdir = Path(sys.argv[2])

outdir.mkdir(parents=True, exist_ok=True)

BASE_URL = (
    "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
)

formats = {
    "fasta": "fasta",
    "gbff": "gbwithparts",
}

def download(accession, rettype, destination):
    params = urllib.parse.urlencode({
        "db": "nuccore",
        "id": accession,
        "rettype": rettype,
        "retmode": "text",
    })

    url = f"{BASE_URL}?{params}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "PhyloClockLab/1.0 Carsonella-replication"
        }
    )

    with urllib.request.urlopen(request, timeout=60) as response:
        content = response.read()

    if len(content) == 0:
        raise RuntimeError("NCBI returned an empty file")

    destination.write_bytes(content)


with manifest.open() as handle:
    reader = csv.DictReader(handle, delimiter="\t")

    rows = list(reader)

print(f"Taxa in manifest: {len(rows)}")
print(f"Output directory: {outdir}")
print()

failures = []

for number, row in enumerate(rows, start=1):

    sample_id = row["sample_id"]
    accession = row["ncbi_accession_version"]

    print(
        f"[{number:02d}/{len(rows)}] "
        f"{sample_id}  {accession}"
    )

    for extension, rettype in formats.items():

        destination = outdir / f"{sample_id}_{accession}.{extension}"

        if destination.exists() and destination.stat().st_size > 0:
            print(f"    {extension}: already exists — skipping")
            continue

        try:
            download(accession, rettype, destination)

            print(
                f"    {extension}: downloaded "
                f"({destination.stat().st_size:,} bytes)"
            )

        except Exception as error:
            failures.append(
                (sample_id, accession, extension, str(error))
            )

            print(
                f"    {extension}: FAILED — "
                f"{type(error).__name__}: {error}"
            )

        # Respect NCBI request limits
        time.sleep(0.4)

print()
print("Download summary")
print("----------------")

if failures:
    print(f"Failures: {len(failures)}")

    for failure in failures:
        print("\t".join(failure))

    sys.exit(1)

else:
    print("PASS: all requested files downloaded successfully")
