from src.qitip.qitip import Qitip


def init(n: int) -> Qitip:
    return Qitip(n=n)


if __name__ == "__main__":
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
