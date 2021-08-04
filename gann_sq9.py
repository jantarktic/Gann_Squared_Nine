import math

def initializeGannSquareNine(price):

    gann_square_nine_levels = []

    square = math.sqrt(price)
    
    a = ((square*180.0)-225.0)/360.0
    
    b = (a - math.trunc(a))*360
    
    base = (math.floor(square)-1.0) * (math.floor(square)-1.0)

    base_1 = math.sqrt(base)

    base_2 = base_1 + 1.0

    base_3 = base_1 + 2.0

    if gann_square_nine_levels is not None:
        gann_square_nine_levels.clear()
    else:
        pass

    angle = 0.125
    i = 0

    while i < 8:
        level = (base_1 + angle) * (base_1 + angle)
        gann_square_nine_levels.append(level)
        angle += 0.125
        i += 1

    angle = 0.125
    i = 0

    while i < 8:
        level = (base_2 + angle) * (base_2 + angle)
        gann_square_nine_levels.append(level)
        angle += 0.125
        i += 1

    angle = 0.125
    i = 0

    while i < 8:
        level = (base_3 + angle) * (base_3 + angle)
        gann_square_nine_levels.append(level)
        angle += 0.125
        i += 1

    gann_square_nine_levels.sort()
    message = []

    for num in gann_square_nine_levels:
        message.append(num)

    print('Gann initialize. Square 9 levels are: ', message)
    print('The total amount of numbers are: ', len(message))
    return message
#Enter any number to return its Gann values.
initializeGannSquareNine(4400)