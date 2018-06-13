
try:
    with open('e_pass.txt', 'r') as f:
        email, password = f.readline().split(',')
except:
    email = input('Введите логин: ')
    password = input('Введите пароль: ')
    with open('e_pass.txt', 'w') as f:
        f.write(email + ',' + password)


h_farm = 3

min_glory_points_to_buy = 1000
max_stone_cost = 400
max_instrument_cost = 400
