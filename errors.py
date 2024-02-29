def send_error(error):
    with open("errors.txt", "r") as f:
        ctx = f.read()
    with open("errors.txt", "w") as f:
        f.write(ctx + str(error) + "\n")
    print(error)
