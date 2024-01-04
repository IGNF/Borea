# Welcome to Pink Lady !!!

Pink Lady is a photogrammetric conversion and acquisition program in .OPK format. Open-source with a few tools, such as calculation of the position in the image (l,c) of a terrain point (X,Y,Z).

### Commit Message Header

```
<type>: <short summary>
  │            │
  │            └─⫸ Summary in present tense. Not capitalized. No period at the end.
  │
  └─⫸ Commit Type: build|docs|fix|refactor|test|clean|lint
```

### HTML documentation

Call the function in a terminal located in the directory of the pink_lady.py file. The command to run the function is:

```python pink_lady.py``` 

Then add the parameters:

| Symbol | Details |
| :----: | :------ |
| -f | File path of the workfile |
| -skip | Number of lines to be skipped before reading the file (optional) |
| -w | Worksite output file format ex:opk |
| -pr | Conversion path ex:test/tmp/ |
| -c | Files paths of cameras (.xml or .txt) |
| -cp | Files paths of connecting points (.mes) |
| -gcp | Files paths of ground control point (.app) |

Some settings are optional, depending on what you want to do with Pink Lady.

Html documentation in docs/_build/html/index.hmlt

### Functionality

1. Reading and writing an OPK file
2. Restructuring of read files to allow the addition of read files without modifying functions
    Structure file in reader folder: 
      - name : reader_ext.py
      - function : def read(file: str) -> Worksite:
3. Reading a camera file (XML and txt)
4. Reading connecting point (mes)
5. Reading ground control point (app)
6. Calculation of the image coordinates of gcp by the image function
