def ask_user_status():
    response = input("How are you? : ").strip().lower()

    if response == "ok":
        print("Excellent!")
    else:
        print("Oh no.")