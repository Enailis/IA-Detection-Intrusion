from matplotlib import pyplot as plt


def plot_result(predictions, name: str, title: str):
    # Plot the pie chart of Attack vs Normal
    print("[+] Plotting the pie chart of Attack vs Normal")

    labels = 'Normal', 'Attack'
    sizes = [list(predictions).count(0), list(predictions).count(1)]
    print(f'Normal : {list(predictions).count(0)}')
    print(f'Attack : {list(predictions).count(1)}')
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title(title)
    plt.savefig(name)