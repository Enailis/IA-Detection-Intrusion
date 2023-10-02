def get_dictionnaries():
    import os
    import xmltodict as xtd

    directory = "TRAIN_ENSIBS"
    dictionnaries = []

    print("Indexing files...")

    for filename in os.listdir(directory):
        file = os.path.join(directory, filename)
        if os.path.isfile(file):
            print("╰─ " + file)
            with open(file, 'r') as f:
                dictionnaries.append(xtd.parse(f.read()))
    
    return dictionnaries


if __name__ == "__main__":
    dictionnaries = get_dictionnaries()
