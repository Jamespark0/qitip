from qitip.main import init

while True:
    try:
        n: int = int(input("Input the number of quantum systems: "))
        if n >= 2:
            break
        else:
            print("Number of quantum systems has to be greater than 2 ...")
    except ValueError:
        print("Input value should be an integer greater than 1!")
    except Exception:
        raise Exception("Unexpected errors occur ...")

init(n)
