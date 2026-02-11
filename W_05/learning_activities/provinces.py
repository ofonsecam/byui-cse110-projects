"""
Purpose: Read a list of provinces, modify it, and count specific occurrences.
Author: Your Name
"""

def main():
    # Leer el archivo y convertirlo en lista
    provinces_list = read_list("provinces.txt")

    # Imprimir lista original (opcional, según tu requerimiento)
    print("Original List:")
    print(provinces_list)

    # Modificaciones requeridas
    if len(provinces_list) > 0:
        provinces_list.pop(0)    # Eliminar el primero
        provinces_list.pop()       # Eliminar el último

    # Reemplazar AB por Alberta y contar
    for i in range(len(provinces_list)):
        if provinces_list[i] == "AB":
            provinces_list[i] = "Alberta"

    # Contar e imprimir
    count = provinces_list.count("Alberta")
    print(f"\nAlberta appears {count} times.")

    # Guardar la lista modificada en provinces_clean.txt
    with open("provinces_clean.txt", "w", encoding="utf-8") as out_file:
        for province in provinces_list:
            out_file.write(province + "\n")
    print("Resultados guardados en provinces_clean.txt")

def read_list(filename):
    """Lee el archivo línea por línea y devuelve una lista limpia."""
    text_list = []
    with open(filename, "rt") as text_file:
        for line in text_file:
            clean_line = line.strip()
            text_list.append(clean_line)
    return text_list

# Llamar a la función principal
if __name__ == "__main__":
    main()