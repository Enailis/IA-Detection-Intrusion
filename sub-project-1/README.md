# Sub-project 1

## Installation

Clone project:
```
git clone git@github.com:Enailis/IA-Detection-Intrusion.git
```

Install dependencies:
```
cd IA-Detection-Intrusion/sub-project-1
pip install -r requirements.txt
```

Configure the `.env-example` with included datas and rename it with `.env`.

Create a folder called `TRAIN_ENSIBS` and put every `.xml` files required for the training.

You can now execute every python while by using the command `python3 <file.py>`.

## Disclamer

The file `import_data.py` must not be launched. It is used to import data from `.xml` files to ElasticSearch but this step has already been done.

## Explaination

### [`import_data.py`](./import_datas.py)

This file is used to import data from `.xml` files to ElasticSearch. The function `get_dictionnaries` uses `lxml` lib to extract information from the `.xml` files to put them in a dictionnary before importing it to ElasticSearch.
