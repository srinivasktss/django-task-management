from celery import shared_task


@shared_task
def add(x, y):
    print(f'Adding {x} and {y} = {x + y}')
    return x + y


@shared_task
def mul(x, y):
    print(f'Multiplying {x} and {y} = {x * y}')
    return x * y


@shared_task
def xsum(numbers):
    print(f'Summing {numbers}')
    return sum(numbers)