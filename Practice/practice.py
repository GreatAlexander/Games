# Practice run to memorize Python stuff
	
#if __name__ == '__main__':

import os#8da6ce
import time

inp = input("Start \n")

start = time.clock()
delay = 3

a_tuple = ('yes', 'no', 'maybe')
a_list = ['a', 'b', 'c']
a_set = {'1', '2', '3'}

b_tuple = a_tuple[0:2]
b_list = list(a_set)
b_set = set(a_list)
empty_set = set()
a_dict = {'server': 'db.diveintopython3.org'}	# Creating a dictionary, introducing a key-value pair

a_list.append('d')
b_list.remove('2')
a_dict['database'] = 'blog'

(y,n,m) = a_tuple

print("Tuple A:", a_tuple)
print("List A:", a_list)
print("Set A:", a_set)
print("Tuple B:", b_tuple)
print("List B:", b_list)
print("Set B:", b_set)

print("Tuple A is ", type(a_tuple))

print("\nConnecting...")
time.sleep(1)
for i in range(0, delay):
	print(delay - i)
	time.sleep(1)

print("Connected to ", a_dict['server'])

r = input("\nAm I right? ")

if r == y:
	print("Thanks!")
elif r == n:
	print("Well Whateva Minga!")
else:
	print("Huh?")

stop = time.clock()

print("\nTime to run this program =", stop - start)


inp = input("\nThe End!")
