def load_token():
    with open("./local_storage/token.txt", "r") as file:
        token = file.read()
        return token
