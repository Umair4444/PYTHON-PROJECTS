from calculator import add,minus

def main():

    add_result = add.add(2,2)
    minus_result = minus.minus(20,10)

    # assert result == 8

    print(add_result,"add result")
    print(minus_result,"minus result")

main()

# for running this file 
# python -m app.main
