from random import randint


def verify(tckn):
    response = {'status': False}
    if str(tckn).isnumeric():
        tckn_int = int(tckn)
        if len(str(tckn_int)) == 11:
            f9 = tckn_int // 100
            l2 = tckn_int % 100
            evens, odds = 0, 0
            for i in range(1, 10):
                b = f9 % 10
                if i % 2:
                    odds += b
                else:
                    evens += b
                f9 //= 10
            b10 = (odds * 7 - evens) % 10
            b11 = (odds + evens + b10) % 10
            if l2 == b10 * 10 + b11:
                response = {'status': True, 'message': f"'{tckn_int}' verified!"}
            else:
                response['error'] = f"'{tckn}' not verified!"
        else:
            response['error'] = f"'{tckn}' is not 11 digits!"
    else:
        response['error'] = f"'{tckn}' is not numerical!"
    return response


def generate():
    f9 = randint(100000000, 999999999)
    evens, odds = 0, 0
    for i in range(1, 10):
        b = f9 % 10
        if i % 2:
            odds += b
        else:
            evens += b
        f9 //= 10
    b10 = (odds * 7 - evens) % 10
    b11 = (odds + evens + b10) % 10
    return (f9 * 100) + (b10 * 10) + b11
