"""
Сервисные функции для работы с Stripe API
"""

import stripe
from django.conf import settings
from decimal import Decimal
import logging

logger = logging.getLogger(__name__)

# Настройка Stripe
stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(course_title, course_description):
    """
    Создает продукт в Stripe

    Args:
        course_title (str): Название курса
        course_description (str): Описание курса

    Returns:
        dict: Данные созданного продукта
    """
    try:
        product = stripe.Product.create(
            name=course_title, description=course_description, type="service"
        )
        logger.info(f"Создан продукт в Stripe: {product.id}")
        return product
    except stripe.error.StripeError as e:
        logger.error(f"Ошибка создания продукта в Stripe: {e}")
        raise


def create_stripe_price(product_id, amount):
    """
    Создает цену для продукта в Stripe

    Args:
        product_id (str): ID продукта в Stripe
        amount (Decimal): Сумма в рублях

    Returns:
        dict: Данные созданной цены
    """
    try:
        # Конвертируем рубли в копейки для Stripe
        amount_cents = int(amount * 100)

        price = stripe.Price.create(
            product=product_id,
            unit_amount=amount_cents,
            currency="rub",
        )
        logger.info(f"Создана цена в Stripe: {price.id}")
        return price
    except stripe.error.StripeError as e:
        logger.error(f"Ошибка создания цены в Stripe: {e}")
        raise


def create_stripe_checkout_session(
    price_id, success_url, cancel_url, customer_email=None
):
    """
    Создает сессию для оплаты в Stripe

    Args:
        price_id (str): ID цены в Stripe
        success_url (str): URL для перенаправления после успешной оплаты
        cancel_url (str): URL для перенаправления при отмене оплаты
        customer_email (str, optional): Email покупателя

    Returns:
        dict: Данные созданной сессии
    """
    try:
        session_data = {
            "payment_method_types": ["card"],
            "line_items": [
                {
                    "price": price_id,
                    "quantity": 1,
                }
            ],
            "mode": "payment",
            "success_url": success_url,
            "cancel_url": cancel_url,
        }

        if customer_email:
            session_data["customer_email"] = customer_email

        session = stripe.checkout.Session.create(**session_data)
        logger.info(f"Создана сессия оплаты в Stripe: {session.id}")
        return session
    except stripe.error.StripeError as e:
        logger.error(f"Ошибка создания сессии оплаты в Stripe: {e}")
        raise


def retrieve_stripe_session(session_id):
    """
    Получает информацию о сессии оплаты из Stripe

    Args:
        session_id (str): ID сессии в Stripe

    Returns:
        dict: Данные сессии
    """
    try:
        session = stripe.checkout.Session.retrieve(session_id)
        logger.info(f"Получена информация о сессии: {session_id}")
        return session
    except stripe.error.StripeError as e:
        logger.error(f"Ошибка получения сессии из Stripe: {e}")
        raise


def get_payment_status(session_id):
    """
    Получает статус платежа по ID сессии

    Args:
        session_id (str): ID сессии в Stripe

    Returns:
        str: Статус платежа ('pending', 'paid', 'cancelled', 'failed')
    """
    try:
        session = retrieve_stripe_session(session_id)

        if session.payment_status == "paid":
            return "paid"
        elif session.payment_status == "unpaid":
            return "pending"
        else:
            return "failed"
    except Exception as e:
        logger.error(f"Ошибка получения статуса платежа: {e}")
        return "failed"


def create_payment_flow(course, user, success_url, cancel_url):
    """
    Создает полный процесс оплаты для курса

    Args:
        course: Объект курса
        user: Объект пользователя
        success_url (str): URL для перенаправления после успешной оплаты
        cancel_url (str): URL для перенаправления при отмене оплаты

    Returns:
        dict: Данные для создания платежа
    """
    try:
        # 1. Создаем продукт в Stripe
        product = create_stripe_product(
            course_title=course.title,
            course_description=course.description or f"Курс: {course.title}",
        )

        # 2. Создаем цену в Stripe
        price = create_stripe_price(product_id=product.id, amount=course.price)

        # 3. Создаем сессию оплаты
        session = create_stripe_checkout_session(
            price_id=price.id,
            success_url=success_url,
            cancel_url=cancel_url,
            customer_email=user.email,
        )

        return {
            "product_id": product.id,
            "price_id": price.id,
            "session_id": session.id,
            "payment_url": session.url,
            "amount": course.price,
        }
    except Exception as e:
        logger.error(f"Ошибка создания процесса оплаты: {e}")
        raise
