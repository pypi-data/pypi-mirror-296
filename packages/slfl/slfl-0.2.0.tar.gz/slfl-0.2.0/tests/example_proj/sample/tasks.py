import math
from slfl import task


@task()
def side_account_balance() -> int:
    print(
        """
        1. Go to https://<bank url>
        2. Read PLN balance on the side account and paste below.
        """
    )
    input_str = input("> ")

    return int(input_str)


@task(
    depends_on=["side_account_balance"],
)
def amount_transfered_to_main(side_account_balance: int) -> int:
    fee = 1.5
    left_for_later = 100
    to_transfer = side_account_balance - left_for_later - math.ceil(fee)
    print(
        f"""
        1. Go to https://<bank url>
        2. Transfer {to_transfer} USD to the main account.
        3. Press enter.
        """
    )
    input("> ")

    return to_transfer


@task(depends_on=["amount_transfered_to_main"])
def transfer_to_savings(amount_transfered_to_main: int) -> bool:
    left_for_later = 200
    to_transfer = amount_transfered_to_main - left_for_later
    print(
        f"""
        1. Go to https://<bank url>
        2. Transfer {to_transfer} USD from the main account to the savings account.
        3. Press enter.
        """
    )
    input("> ")
    return True
