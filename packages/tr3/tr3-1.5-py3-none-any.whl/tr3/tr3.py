def approx_pi() -> float:
    return 22 / 7


def is_perfect_number(number: int) -> bool:
    sum_divisors = 0
    for i in range(1, number):
        if number % i == 0:
            sum_divisors += i
    return sum_divisors == number


def is_divisible_by_3(number: int) -> bool:
    return number % 3 == 0


if __name__ == "__main__":
    for i in range(10):
        if is_divisible_by_3(i):
            print(i)
