import intlists
import twosmdef
my_file = "result.txt"
file = open(my_file, 'w')
file.write(str(twosmdef.find_two_smallest(intlists.list_a)))
file.write(str(twosmdef.find_two_smallest(intlists.list_b)))
file.write(str(twosmdef.find_two_smallest(intlists.list_c)))
file.close()
