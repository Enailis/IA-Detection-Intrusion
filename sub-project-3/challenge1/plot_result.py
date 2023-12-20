from matplotlib import pyplot as plt


def plot_result(predictions, name: str, title: str):
    print("[+] Plotting the pie chart of Attack vs Normal")

    normal_count = list(predictions).count(0)
    attack_count = list(predictions).count(1)
    labels = f'Normal: {normal_count}', f'Attack: {attack_count}'
    sizes = [normal_count, attack_count]
    print(f'Normal : {normal_count}')
    print(f'Attack : {attack_count}')
    explode = (0, 0.1)

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')
    plt.title(title)
    plt.savefig(name)
