
"""
Personal Information Manager

"""

SAVE_FILE = "pim_saved.txt"   


def input_nonempty(prompt):
    """Ask until user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value != "":
            return value
        print("Input cannot be empty. Try again.")


def input_age(prompt):
    """Ask until user enters a valid non-negative integer for age."""
    while True:
        s = input(prompt).strip()
        try:
            age = int(s)           
            if age < 0:
                print("Age cannot be negative. Try again.")
                continue
            return age
        except ValueError:
            print("Please enter a whole number for age (e.g. 25).")


def parse_hobbies(hobby_string):
    """Turn a comma-separated string into a list of hobby strings."""
    parts = hobby_string.split(",")
    cleaned = []
    for p in parts:
        p2 = p.strip()
        if p2 != "":
            cleaned.append(p2)
    return cleaned


def display_person(person):
    """Nice formatted output for the person's info."""
    name = person.get("name", "Unknown")
    age = person.get("age", "Unknown")
    city = person.get("city", "Unknown")
    hobbies = person.get("hobbies", [])
    if hobbies:
        hobbies_text = ", ".join(hobbies)    
    else:
        hobbies_text = "No hobbies listed"

    print("\n--- Personal Information ---")
    print(f"Name   : {name}")
    print(f"Age    : {age} years")
    print(f"City   : {city}")
    print(f"Hobbies: {hobbies_text}")
    print("----------------------------\n")


def save_plain_text(person):
    """Save the person's info to a plain text file (simple persistence)."""
    try:
        f = open(SAVE_FILE, "w", encoding="utf-8")
        f.write("Name: " + person.get("name", "") + "\n")
        f.write("Age: " + str(person.get("age", "")) + "\n")
        f.write("City: " + person.get("city", "") + "\n")
        f.write("Hobbies: " + (", ".join(person.get("hobbies", []))) + "\n")
        f.close()
        print("Saved info to", SAVE_FILE)
    except Exception as e:
        # Demonstrates simple error reporting (understanding errors)
        print("Could not save file — error:", e)


def load_plain_text():
    """Try to load previously saved plain-text info (very simple)."""
    try:
        f = open(SAVE_FILE, "r", encoding="utf-8")
    except Exception:
        return None

    person = {}
    for line in f:
        line = line.strip()
        if line.startswith("Name:"):
            person["name"] = line[len("Name:"):].strip()
        elif line.startswith("Age:"):
            s = line[len("Age:"):].strip()
            try:
                person["age"] = int(s)
            except Exception:
                person["age"] = s
        elif line.startswith("City:"):
            person["city"] = line[len("City:"):].strip()
        elif line.startswith("Hobbies:"):
            raw = line[len("Hobbies:"):].strip()
            person["hobbies"] = parse_hobbies(raw) if raw else []
    f.close()
    return person


def main():
    print("Welcome! Simple Personal Information Manager\n")

    prev = load_plain_text()
    if prev:
        print("Found saved data:")
        display_person(prev)
        ans = input("Use (u), edit (e) or enter new (n)? [u/e/n]: ").strip().lower()
        if ans == "u":
            print("Using saved data. Goodbye!")
            return
        elif ans == "e":
            person = prev.copy()
            # edit: press Enter to keep current value
            name_in = input(f"Name [{person.get('name','')}]: ").strip()
            if name_in:
                person["name"] = name_in
            age_in = input(f"Age [{person.get('age','')}]: ").strip()
            if age_in:
                try:
                    person["age"] = int(age_in)
                except Exception:
                    print("Invalid age input; keeping previous.")
            city_in = input(f"City [{person.get('city','')}]: ").strip()
            if city_in:
                person["city"] = city_in
            hobbies_in = input(f"Hobbies (comma-separated) [{', '.join(person.get('hobbies', []))}]: ").strip()
            if hobbies_in:
                person["hobbies"] = parse_hobbies(hobbies_in)
        else:
            person = {}
    else:
        person = {}

    if "name" not in person:
        person["name"] = input_nonempty("Enter your name: ")
    if "age" not in person:
        person["age"] = input_age("Enter your age (whole years): ")
    if "city" not in person:
        person["city"] = input_nonempty("Enter your city: ")
    if "hobbies" not in person:
        raw = input("Enter hobbies (comma-separated), or leave blank: ").strip()
        person["hobbies"] = parse_hobbies(raw) if raw else []

    display_person(person)

    save_q = input("Save this to disk? (y/N): ").strip().lower()
    if save_q == "y":
        save_plain_text(person)
    else:
        print("Not saved. Exiting.")


if __name__ == "__main__":
    main()
