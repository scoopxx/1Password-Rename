import subprocess
import tldextract
import argparse
import re
import shlex
import json


def run_command(cmd):
    try:
        return subprocess.run(
            shlex.split(cmd), check=True, capture_output=True, text=True
        ).stdout
    except subprocess.CalledProcessError as e:
        # print(e)
        raise


def gen_title(url: str):
    url1 = re.sub(r"\s*\([^)]*\)", "", url)
    url1 = url1.strip().lstrip()
    extraction = tldextract.extract(url1)
    is_url = bool(extraction.domain and extraction.suffix)
    if not is_url:
        return False
    domain = extraction.domain
    domain = domain[0].upper() + domain[1:]
    return domain

def update(item, new_title):
    """Update item's title in 1Password."""
    print(f'Prev title: {item["title"]}, Proposed title: {new_title}')
    if not dry_run:
        run_command(f"op item edit {item["id"]} title='{new_title}'")
        print(f'Done for item: {item["id"]}')
    return


def run(items: list):
    for new_item in items:
        if "trashed" in new_item:
            continue

        if not "urls" in new_item:
            continue

        prev_title = new_item["title"]
        new_title = gen_title(prev_title)
        if new_title:
            update(new_item, new_title)
        else:
            print(f'Skipping item: {new_item['title']}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rename login titles from your 1Password vault"
    )
    parser.add_argument(
        "-d",
        "--dry-run",
        action="store_true",
        help="Output the proposed name without actually updating the item",
    )
    parser.add_argument(
        "--vault",
        metavar="[vault id]",
        help="Only search for duplicates in the specified vault",
    )
    parser.add_argument(
        "--tag",
        metavar="[tag id]",
        action="append",
        help="Only search for duplicates with the specified tags",
    )

    args = parser.parse_args()
    dry_run = args.dry_run

    cmd = "op item list --categories Login --format=json"
    if args.vault:
        cmd += f" --vault {args.vault}"
    if args.tag:
        cmd += f' --tags {",".join(args.tag)}'
    items = json.loads(run_command(cmd))

    run(items)
    print("Finished.")
