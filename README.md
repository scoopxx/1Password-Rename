# 1Password Rename

Script for myself to rename 1password login entries in batch.

After importing passwords from chrome password manager into 1password,
the default title is named as the original URL like
`accounts.google.com`, `appleid.apple.com`.
The script wil rename the title to its main domain. For example,

- `accounts.google.com` -> `Google`
- `appleid.apple.com` -> `Apple`

The idea is based on the deletion script originally made by [ben-hampson](https://github.com/ben-hampson/1Password-Deduplicator/tree/master).

## Setup

```
# Install the 1Password CLI if you don't already have it
brew install --cask 1password/tap/1password-cli

# Download and setup
pip install -r requirements.txt

# Run it
python -m 1password_rename
```

## Options

```
--dry-run          - Tells you which items it would delete but doesn't delete them.
--tag <tag>        - Only looks for items with the given tag. (untested)
--vault <vault>    - Only looks for items in the given vault. (untested)
```
