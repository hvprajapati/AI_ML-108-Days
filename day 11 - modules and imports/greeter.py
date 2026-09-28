
def greet(name):
    return f"Hello, {name}!"

print("Module loaded. __name__ =", __name__)

if __name__ == "__main__":
    # This code runs ONLY when the file is run directly
    print(greet("Tester"))
