from telethon import Button


start_markup = [Button.text('Погода'), Button.text('Курс'), Button.text('Изменить город'), Button.text('Изменить время рассылки')]

cansel_markup = [Button.text('Отмена')]

change_time_markup = [Button.text('8:00'), Button.text('10:00'), Button.text('12:00'), Button.text('Отмена')]

change_city_markup = [Button.text('Москва'), Button.text('Санкт-Петербург'), Button.text('Отмена')]