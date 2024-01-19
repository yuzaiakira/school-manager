from payments.models import UserPaymentModel, UserPriceModel


def check_part_of_installment(user_price: UserPriceModel) -> int:
    """
    This function check user installment if the user have installment.

    Parameters:
    user_price (UserPriceModel): get UserPriceModel to find of installments part.

    Returns:
    int: part of installment for user.
    """


    if user_price.Installment:
        return user_price.total_price.part
    else:
        return 0



def get_total_price(user_payment: UserPaymentModel) -> int:
    """
    This function get total of price user.

    Parameters:
    user_payment (UserPaymentModel): get UserPaymentModel to Computing all user payment in UserPriceModel.

    Returns:
    int: user total price.
    """

    total_price = 0

    for pay in user_payment:
        total_price += abs(pay.price)

    return total_price


def total_price(user_price_model: UserPriceModel) -> int:
    """
    This function get total of price user.

    Parameters:
    user_price_model (UserPriceModel): get UserPriceModel to Computing all user payment in UserPriceModel.

    Returns:
    int: user total price.
    """

    total = 0
    user_price = UserPaymentModel.objects.filter(total=user_price_model)

    if user_price:
        for pay in user_price:
            total += abs(pay.price)

    return total


def price_peer_part(user_price: UserPriceModel) -> int:
    """
    To calculate user payments price per Installment

    Parameters:
    user_payment (UserPaymentModel): get UserPaymentModel to Computing all user payment in UserPriceModel

    Returns:
    int: the cost that the user should payment.
    """
    total = total_price(user_price)
    if total < user_price.total_price.price:
        if user_price.Installment:
            if UserPaymentModel.objects.filter(total=user_price).count() + 1 < user_price.total_price.part:
                return user_price.total_price.price // user_price.total_price.part

            if UserPaymentModel.objects.filter(total=user_price).count() + 1 == user_price.total_price.part:
                return user_price.total_price.price - total

        else:
            return user_price.total_price.price

    return 0
