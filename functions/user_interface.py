def ask_user_choice():
    while True:
        choice_str = input("Choisissez la catégorie (de 0 à 50) : ")
        try:
            choice_int = int(choice_str)
        except ValueError:
            print("ERREUR : choisissez un nombre entre 1 et 50")
        else:
            if choice_int < 0 or choice_int > 50:
                print("ERREUR : choisissez un nombre entre 1 et 50")
            else:
                return choice_int


def print_user_choices(categories):
    sorted_categories = sorted(categories, key=lambda x: len(x[0]), reverse=True)
    max_length = len(sorted_categories[0][0])
    text = "0 : Toutes les catégories"
    for i in range(0, len(categories)):
        if i % 5 == 0:
            text += "\n"
        category = categories[i][0]
        number_of_spaces = max_length - len(category) + 3
        text += f"{i + 1} : {category}"
        for j in range(0, number_of_spaces):
            text += " "
        if i < 9:
            text += " "
    print(text)
