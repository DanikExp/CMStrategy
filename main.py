import random
import csv
import time

number_of_transaction = 100
number_of_test = 100

lose_streak_break = 1
win_streak_break = 5

lose_streak_bonus = 7
win_streak_bonus = 1

type_of_transaction = []
transactions_result = []

current_value = []


def get_type_deals(win_r):
    num = random.randrange(0, 101, 1)
    if num < win_r:
        return True
    else:
        return False


def bet(val, cof):
    return val * (cof / 100.0)


timer_start = time.perf_counter()
for win_rate in range(101):
    type_of_transaction.clear()
    print(f"win_rate: {win_rate}")

    for take_profit in range(101):
        for stop_loss in range(101):
            for test in range(number_of_test):
                for i in range(number_of_transaction):
                    type_of_transaction.append((get_type_deals(win_rate)))
                win_streak = []
                lose_streak = []
                balance = 100
                coefficient = 30
                current_value.append([])

                for transaction in range(number_of_transaction):
                    order = bet(balance, coefficient)
                    current_value[test].append(balance)

                    if balance >= order:
                        balance -= order
                        if type_of_transaction[transaction]:
                            win_streak.append("+")
                            lose_streak.clear()
                            if len(win_streak) >= win_streak_break and coefficient + win_streak_bonus <= 100:
                                coefficient += win_streak_bonus

                            order *= 1.0 + take_profit / 100.0

                        else:
                            lose_streak.append("-")
                            win_streak.clear()
                            if (len(lose_streak) >= lose_streak_break) and (coefficient - lose_streak_bonus > 0):
                                coefficient -= lose_streak_bonus

                            order *= 1.0 - stop_loss / 100.0

                        balance += order
                    else:
                        print('Money is over')
                        break

                    current_value[test].append(balance)

                total = 0
                for i in range(number_of_transaction):
                    total += current_value[test][-1]

                avg = total / number_of_transaction
            transactions_result.append([win_rate, take_profit, stop_loss, avg])

with open('result.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter=';')
    writer.writerow(['Win Rate', 'Take profit', 'Stop loss', 'Avg'])
    for data in transactions_result:
        writer.writerow(data)

timer_end = time.perf_counter()

print(timer_end-timer_start)
