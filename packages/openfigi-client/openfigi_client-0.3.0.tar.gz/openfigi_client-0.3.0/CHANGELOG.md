## v0.3.0 (2024-09-18)

### ✨ Features

- implement async client

### 🐛🚑️ Fixes

- use msgspec for json decoding

### ♻️  Refactorings

- switch client to httpx

### 💚👷 CI & Build

- use uv venv
- add ls

### 🔧🔨📦️ Configuration, Scripts, Packages

- remove project url
- move ruff unfixable

### 🧑‍💻 Developer Experience

- switch to uv

## v0.2.5 (2024-09-17)

### ♻️  Refactorings

- make modules private

## v0.2.4 (2024-09-17)

### 🐛🚑️ Fixes

- some readme fixes

### 💚👷 CI & Build

- rename repo url
- move clone path to test job

## v0.2.3 (2024-05-09)

### 🐛🚑️ Fixes

- put validation back on init

## v0.2.2 (2024-05-09)

### 🐛🚑️ Fixes

- comparison

## v0.2.1 (2024-05-09)

### 🐛🚑️ Fixes

- don't try to create enum in validation and add test

### ⏪️ Reversions

- "🐛 fix: don't try to create enum in validation and add test"

### 📄 License

- update license

## v0.2.0 (2024-05-09)

### ✨ Features

- switch to msgspec

### 🎨🏗️ Style & Architecture

- switch to google docstring

### 🔧🔨📦️ Configuration, Scripts, Packages

- **ruff**: select all codes

## v0.1.13 (2024-05-08)

### ⚡️ Performance

- add timeout and logging

### 📌➕⬇️ ➖⬆️  Dependencies

- ipython dev dependency

### 🦺 Validation

- use IdType enum for validating input

## v0.1.12 (2024-05-07)

### 🐛🚑️ Fixes

- try publish with ci token

### 💚👷 CI & Build

- log output first
- capture 21
- redirect output
- capture exit code differently
- use variables

## v0.1.11 (2024-05-07)

### 🐛🚑️ Fixes

- don't overwrite before_script

## v0.1.10 (2024-05-07)

### 🐛🚑️ Fixes

- proper check for unset
- set clone path

## v0.1.9 (2024-05-07)

### 🐛🚑️ Fixes

- echo exit code

## v0.1.8 (2024-05-07)

### 🐛🚑️ Fixes

- unset e after bump
- fail if repo url is not set

## v0.1.7 (2024-05-07)

### 🐛🚑️ Fixes

- don't fail on non-zero

## v0.1.6 (2024-05-07)

### 🐛🚑️ Fixes

- set correct exit code

## v0.1.5 (2024-05-07)

### 🐛🚑️ Fixes

- comment
- var exports

## v0.1.4 (2024-05-07)

### 🐛🚑️ Fixes

- exit code
- checking exit code
- check bump exit code

### ⏪️ Reversions

- "🐛 fix: try to set local url"

### 💚👷 CI & Build

- try with env vars

## v0.1.3 (2024-05-07)

### 🐛🚑️ Fixes

- try to set local url

## v0.1.2 (2024-05-07)

### 🐛🚑️ Fixes

- also run on tags

## v0.1.1 (2024-05-07)

### 🐛🚑️ Fixes

- set credentials
- set name to token
- push tags too
- use right index url

### 💚👷 CI & Build

- use bot token
- specify what to push
- use python3.12 image
- always run on main
- don't run on empty branch
- configure git creds
- bump only when no tag
- install dev deps
- add pipeline
- add pipeline

### 📝💡 Documentation

- fix readme
