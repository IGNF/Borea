# Convert Micmac xml files to opk

**mm_xml_to_opk** Converts Micmac xml files into an opk file by changing column order, without changing the units, the order of the axes or any other parameters.

## Application

Call the function from a terminal in the depot directory `python borea_tools/mm_xml_to_opk.py`. To view the information on the various parameters you can do : 

```python borea_tools/mm_xml_to_opk.py -h``` 

Or if you install the package by **pip** the commande is:

```mm-xml-to-opk -h```

The parameters are:

| Symbol | Details | Default | Mandatory |
| :----: | :------ | :-----: | :-------: |
| -r | File path of the workfile | | V |
| -n | Name of worksite output file |  | V |
| -w | Conversion path e.g. "./" | "./" | X |
| -o | Type of each column in the site file. e.g. NXYZOPKC with Z origin | NXYZOPKC | X |

E.G.
```
python ./borea_tools/mm_xml_to_opk.py -r ./dataset/regex_.*.xml -n Test -o NXYZOPKC
```
or pip
```
mm-xml-to-opk -r ./dataset/regex_.*.xml -n Test -o NXYZOPKC
```

## Detail for the header of file -i and -o
`header` is used to describe the format of the opk file read. It provides information on what's in each column, and gives the data unit for Z and angles.   
Type is:
| Symbol | Details |
| :----: | :------ |
| N | name of shot |
| X | coordinate x of the shot position |
| Y | coordinate y of the shot position |
| Z | coordinate z of the shot position |
| O | omega rotation angle |
| P | phi rotation angle |
| K | kappa rotation angle |
| C | name of the camera |