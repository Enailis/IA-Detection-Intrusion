# Sub-project 2

## Installation

Clone project:
```
git clone git@github.com:Enailis/IA-Detection-Intrusion.git
```

Install dependencies:
```
cd IA-Detection-Intrusion/sous-projet-2
pip install -r requirements.txt
```

Create a folder called `TRAIN_ENSIBS` and put every `.xml` files required for the training.

You can now execute every python while by using the command `python3 <file.py>`.

## Disclamer

This projet is suppose to get the datas pushed to ELK in [sub-project-1](../sub-project-1/README.md) but to gain some time *(because of the horrible bandwidth of our school)* we decided to serialize the datas in a pickle file.

## First data loading

You can use the file `split_data.py` to load the data from the `.xml` files and split them depending on appName.
For each appName category, the data is split into 5 sub dictionaries.

The data is then saved on `dictionnariesByAppNameSplitted.pickle`to avoid having to load the data every time.
So you only need to create the pickle file once.

This file will be used in following function to load the data.

## Data loading

### KNN

