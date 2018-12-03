input_file = open('input12.txt','r')
# output_file = open('output.txt' , 'w')
# start_time = time.time()
size = int(input_file.readline().strip())
num_officers = int(input_file.readline().strip())
num_scooters = int(input_file.readline().strip())

position_dict = {}
'''define scotters' position by  a dict'''
for line in input_file.readlines():
    line = line.strip().split(',')
    position_x = int(line[0].strip())
    position_y = int(line[1].strip())
    print (position_x, position_y)
    if position_dict.has_key((position_x,position_y)):
        position_dict[(position_x,position_y)] = position_dict.get((position_x,position_y)) + 1
        print position_dict
    else:
        position_dict[(position_x, position_y)]  = 1
        print position_dict
print size, num_scooters, num_officers
print position_dict