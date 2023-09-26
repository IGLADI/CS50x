def main():
    text = input("Text: ")
    letters = 0
    words = 1
    sentences = 0

    for char in text:
        if char in ['.', '!', '?']:
            sentences += 1
        elif char.isspace():
            words += 1
        elif char.isalpha():
            letters += 1

    L = (letters / words) * 100
    S = (sentences / words) * 100
    grade = 0.0588 * L - 0.296 * S - 15.8

    if grade < 1:
        print("Before Grade 1")
    elif grade >= 16:
        print("Grade 16+")
    else:
        print(f"Grade {round(grade)}")

if __name__ == "__main__":
    main()
