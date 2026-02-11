# Author: OScar Fonseca
# Porpouse: Pracctice teh knowledge for w1 python review and make a heart rate

"""
When you physically exercise to strengthen your heart, you
should maintain your heart rate within a range for at least 20
minutes. To find that range, subtract your age from 220. This
difference is your maximum heart rate per minute. Your heart
simply will not beat faster than this maximum (220 - age).
When exercising to strengthen your heart, you should keep your
heart rate between 65% and 85% of your heart's maximum rate.
"""

text = int(input("Enter you age:" ))
age = int(text)

max = 220 - age
fasted = max * 0.85
slowest = max * 0.65

print ("When you physically exercise to strengthen your heart, you should.") 
print (f"Keep your heart rate between 65% that it's {slowest:.0f} and 85% of your hearts maximum rate that it's {fasted:.0f}.")
print('beats per minute')

