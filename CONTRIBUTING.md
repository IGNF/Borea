# Contributor information to Pink Lady

### Commit Message Header

```
<type>: <short summary>
  │            │
  │            └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|ci|docs|feat|fix|refactor|test
```
Must be one of the following:

  * build: Changes that affect the build system or external dependencies (e.g. scopes: gulp, broccoli, npm)
  * ci: Changes to our CI configuration files and scripts (e.g. CircleCi, SauceLabs)
  * docs: Documentation only changes
  * feat: A new feature
  * fix: A bug fix
  * refactor: A code change that neither fixes a bug nor adds a feature
  * test: Adding missing tests or correcting existing tests

Based on: https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit

### Structure of format reading/writing functions

Restructuring of read files to allow the addition of read files without modifying functions.  
Same thing with write files.
- Structure file in reader folder:
    - name : reader_{ext}.py
    - function : def read(file: str, line: list, header: list, work: Worksite) -> Worksite:
- Structure file in writer folder: 
    - name : writer_{ext}.py
    - function : def write(path_folder: str, work: Worksite) -> converted file:

### More information

Html documentation python in docs/_build/html/index.hmlt  
Markdown documentation function in docs/functions/  
Diagram of code structure Pink Lady in docs/diagram/

![logo ign](docs/logo/logo_ign.png) ![logo fr](docs/logo/Republique_Francaise_Logo.png)