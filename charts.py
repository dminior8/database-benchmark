from matplotlib import pyplot as plt


def save_chart(title, data_rows, operation_index=1):
    """
    Rysuje porównanie jednej operacji (wybór przez operation_index)
    dla wszystkich wierszy w data_rows.

    - title:        np. "CREATE"
    - data_rows:    [[X, y1, y2, y3, y4, label, color], ...]
    - operation_index:  1=create, 2=read, 3=update, 4=delete
    """
    fig, ax = plt.subplots()

    for row in data_rows:
        x = row[0]
        y = row[operation_index]
        label = row[5]
        color = row[6]
        ax.plot(
            x, y,
            label=label,
            color=color,
            linewidth=2,
            marker='o',
            markersize=6,
            markerfacecolor=color
        )

    # Dodajemy osie w zerze
    ax.axhline(0, color='grey', linestyle='--', linewidth=0.5)  # pozioma linia y=0
    ax.axvline(0, color='grey', linestyle='--', linewidth=0.5)  # pionowa linia x=0

    # Włączamy siatkę w tle i ustawiamy, by była pod wykresem
    ax.grid(True, which='major', linestyle='--', linewidth=0.5)  # siatka dla głównych i pomocniczych ticków
    ax.set_axisbelow(True)  # rysuje grid pod innymi elementami wykresu

    ax.set_title(f"Wykres dla operacji {title}")
    ax.set_xlabel("Liczba rekordów")
    ax.set_ylabel("Czas (s)")
    ax.legend(loc="upper left")

    fig.savefig(f"Wykres_{title}_no_cass.png")
    plt.close(fig)
