import random
rand_list = [random.randint(1 , 20 ) for _ in range(10)]

list_comprehension_below_10 = [ item for item in rand_list if item < 10]

list_comprehension_below_10_using_filter = list(filter(lambda x : x < 10 , rand_list))


print(rand_list)
print(list_comprehension_below_10)
print(list_comprehension_below_10_using_filter)
