from telethon import Button
from telethon.client.buttons import ButtonMethods


start_markup = ButtonMethods.build_reply_markup(
    [[Button.text('Погода', resize=True), Button.text('Курс'), Button.text('Новости')],
     [Button.text('Изменить город'), Button.text('Изменить время рассылки')]
     ])

cansel_markup = [Button.text('Отмена')]

change_time_markup = ButtonMethods.build_reply_markup(
    [[Button.text('8:00', resize=True), Button.text('10:00'), Button.text('12:00')],
     [Button.text('Отмена')]])

change_city_markup = ButtonMethods.build_reply_markup(
    [[Button.text('Москва', resize=True), Button.text('Санкт-Петербург')],
     [Button.text('Отмена')]])
