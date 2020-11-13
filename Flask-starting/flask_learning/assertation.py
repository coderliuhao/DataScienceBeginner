def num_divide(num1,num2):

    assert isinstance(num1,int)
    assert isinstance(num2,int)

    print(num1/num2)

def multiple(a,b):
    assert a != 0
    assert isinstance(a,float)
    assert isinstance(b,float)

    return a*b

if __name__ == "__main__":
    multiple(64.0,"a")

