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

pos_math_exp = []
neg_math_exp = []


def get_type_deals(win_r):
    num = random.randrange(0, 101, 1)
    return True if num < win_r else False


def bet(val, cof):
    return val * (cof / 100.0)


def do_transaction(type_of_trans):
    win_streak = 0
    lose_streak = 0
    balance = 100
    coefficient = 30
    for transaction in type_of_trans:
        order = bet(balance, coefficient)

        if balance >= order:
            balance -= order

            if transaction:
                win_streak += 1
                lose_streak = 0
                if win_streak >= win_streak_break and coefficient + win_streak_bonus <= 100:
                    coefficient += win_streak_bonus

                order *= 1.0 + take_profit / 100.0

            else:
                lose_streak += 1
                win_streak = 0
                if lose_streak >= lose_streak_break and coefficient - lose_streak_bonus > 0:
                    coefficient -= lose_streak_bonus

                order *= 1.0 - stop_loss / 100.0

            balance += order
        else:
            print('Money is over')
            break
    return balance


if __name__ == '__main__':
    timer_start = time.perf_counter()
    for win_rate in range(20, 91, 1):
        print(f"win_rate: {win_rate}")

        for take_profit in range(11):
            for stop_loss in range(11):
                tests_result = 0
                for test in range(number_of_test):
                    type_of_transaction = [get_type_deals(win_rate) for i in range(number_of_transaction)]
                    last_value_from_transaction = do_transaction(type_of_transaction)
                    tests_result += last_value_from_transaction
                    type_of_transaction.clear()

                avg = tests_result / number_of_transaction
                if (win_rate * take_profit) - ((100 - win_rate) * stop_loss) > 0 and avg > 100:
                    pos_math_exp.append((win_rate, take_profit, stop_loss, avg))
                elif (win_rate * take_profit) - ((100 - win_rate) * stop_loss) < 0 and avg > 100:
                    neg_math_exp.append((win_rate, take_profit, stop_loss, avg))

    with open('pos_math_exp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(('Win Rate', 'Take profit', 'Stop loss', 'Avg'))
        for data in pos_math_exp:
            writer.writerow(data)

    with open('neg_math_exp.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerow(('Win Rate', 'Take profit', 'Stop loss', 'Avg'))
        for data in neg_math_exp:
            writer.writerow(data)

    timer_end = time.perf_counter()
    print(timer_end - timer_start)
