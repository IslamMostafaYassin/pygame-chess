path = "text.txt"
with open(path, "r") as file:
    text = file.read()
    for letter in text:
        if letter == "\n":
            break
        print(letter, end="")
