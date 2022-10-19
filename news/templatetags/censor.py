from django import template
import random

register = template.Library()

sleng = ('круто','поперли')
# Регистрируем наш фильтр под именем currency, чтоб Django понимал,
# что это именно фильтр для шаблонов, а не простая функция.
@register.filter()
def mat(value):
   value2 = tuple(value.split())
   value3 = ('')
   for i in value2:
      for j in sleng:
         if j == i:
            i = i[:1]+'****'
      value3 += i + ' '
   return f'{value3}'