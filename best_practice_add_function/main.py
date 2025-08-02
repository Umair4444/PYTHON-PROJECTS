from calculator.add import add
from calculator.minus import minus 

def main():

    # add_result = add(2,2)
    # minus_result = minus(20,10)
    add_result = add(2,3)
    minus_result = minus(12,3)

    # assert result == 8

    print(add_result,"add result")
    print(minus_result,"minus result")

if __name__ == "__main__":
    main()
