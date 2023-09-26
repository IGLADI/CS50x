import cs50
cash = cs50.get_float("Change owed: ")
while cash < 0:
    cash = cs50.get_float("Change owed: ")
cash = round(cash * 100)
coins = 0
while cash >= 25:
    cash -= 25
    coins += 1
while cash >= 10:
    cash -= 10
    coins += 1
while cash >= 5:
    cash -= 5
    coins += 1
while cash >= 1:
    cash -= 1
    coins += 1
print(coins)
