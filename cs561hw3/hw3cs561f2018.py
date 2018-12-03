import copy
import numpy as np
input_file = open('input5.txt','r')
output_file = open('output.txt','w')
size = int(input_file.readline().strip())
num_cars = int(input_file.readline().strip())
num_obstacles = int(input_file.readline().strip())
pos_start_cars = []
pos_terminal_cars = []
pos_obstacles = {}
for i in range(num_obstacles):
    pos = input_file.readline().strip().split(',')
    pos_obstacles[(int(pos[0].strip()),int(pos[1].strip()))] = 1
for i in range(num_cars):
    pos = input_file.readline().strip().split(',')
    pos_start_cars.append([int(pos[0].strip()),int(pos[1].strip())])

for i in range(num_cars):
    pos = input_file.readline().strip().split(',')
    pos_terminal_cars.append([int(pos[0].strip()),int(pos[1].strip())])

grid_value = [[-1 for x in range(size)] for y in range(size)]
grid_value_total = []
for obstacle in pos_obstacles:
    grid_value[obstacle[1]][obstacle[0]] = -101
'''
for x in range(size):
    print(grid_value[x])
'''
def pos_info(list):
    final_pos = [[-1 for x in range(2)] for y in range(4)]
    final_pos[0][0] = list[0]
    if(list[1] == 0):
         final_pos[0][1] = list[1]
    else:
        final_pos[0][1] = list[1] - 1

    final_pos[1][0] = list[0]
    if (list[1] == size -1):
        final_pos[1][1] = list[1]
    else:
        final_pos[1][1] = list[1] +1

    final_pos[2][1] = list[1]
    if (list[0] == size-1):
        final_pos[2][0] = list[0]
    else:
        final_pos[2][0] = list[0] + 1

    final_pos[3][1] = list[1]
    if (list[0] == 0):
        final_pos[3][0] = list[0]
    else:
        final_pos[3][0] = list[0] -1
    return final_pos

def compare(upper, down, right, left):
    max_number = max(upper, down, right, left)
    direction = 0
    if(max_number == left):
        direction = 2
    if(max_number == right):
        direction = 4
    if (max_number == down):
        direction = 3
    if (max_number == upper):
        direction = 1
    return([max_number, direction])

def is_done(list1, list2):
    num = 0.1/9
    for y in range(size):
        for x in range(size):
            if(abs(list1[x][y] - list2[x][y]) > num):
                return False
    return True

policies = []

for i in range(num_cars):
    ind_grid_value = copy.deepcopy(grid_value)
    ind_grid_value[pos_terminal_cars[i][1]][pos_terminal_cars[i][0]] = 99
    grid_direct = [[0 for x in range(size)] for y in range(size)]
    grid_value_total.append(ind_grid_value)
    ind_grid_value_read = copy.deepcopy(ind_grid_value)
    ind_grid_value_next = copy.deepcopy(ind_grid_value)

    while(True):
        for y in range(size):
            for x in range(size):
                if(not(y == pos_terminal_cars[i][1] and x == pos_terminal_cars[i][0])):
                    right_pos = pos_info([x, y])
                    upper = np.float64(ind_grid_value[y][x]) + 0.9 * (
                        0.7 * np.float64(ind_grid_value_read[right_pos[0][1]][right_pos[0][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[1][1]][right_pos[1][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[2][1]][right_pos[2][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[3][1]][right_pos[3][0]]))
                    down = np.float64(ind_grid_value[y][x]) + 0.9 * (
                        0.1 * np.float64(ind_grid_value_read[right_pos[0][1]][right_pos[0][0]])
                        + 0.7 * np.float64(ind_grid_value_read[right_pos[1][1]][right_pos[1][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[2][1]][right_pos[2][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[3][1]][right_pos[3][0]]))
                    right = np.float64(ind_grid_value[y][x]) + 0.9 * (
                        0.1 * np.float64(ind_grid_value_read[right_pos[0][1]][right_pos[0][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[1][1]][right_pos[1][0]])
                        + 0.7 * np.float64(ind_grid_value_read[right_pos[2][1]][right_pos[2][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[3][1]][right_pos[3][0]]))
                    left = np.float64(ind_grid_value[y][x]) + 0.9 * (
                        0.1 * np.float64(ind_grid_value_read[right_pos[0][1]][right_pos[0][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[1][1]][right_pos[1][0]])
                        + 0.1 * np.float64(ind_grid_value_read[right_pos[2][1]][right_pos[2][0]])
                        + 0.7 * np.float64(ind_grid_value_read[right_pos[3][1]][right_pos[3][0]]))

                    ind_grid_value_next[y][x] = compare(upper, down, right, left)[0]
                    grid_direct[y][x] = compare(upper, down, right, left)[1]
        if(is_done(ind_grid_value_read,ind_grid_value_next) == True):
            ind_grid_value_read = copy.deepcopy(ind_grid_value_next)
            policies.append(grid_direct)
            break
        ind_grid_value_read = copy.deepcopy(ind_grid_value_next)


    print(i+1)
    for x in range(size):
        print(ind_grid_value[x])
    for x in range(size):
        print(ind_grid_value_next[x])
    for x in range(size):
        print(grid_direct[x])
for x in range(num_cars):
    print(grid_value_total[x])

for i in range(num_cars):
    total = 0
    for j in range(10):
        reward = 0
        pos = pos_start_cars[i]
        np.random.seed(j)
        swerve = np.random.random_sample(1000000).astype(np.float64)
        #print(swerve[0].dtype)
        k = 0
        while(pos != pos_terminal_cars[i]):
            move = policies[i][pos[1]][pos[0]]
            #print("#############start")
            #print(move)
            #print(swerve[k])
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        if(move == 1): move = 3
                        elif(move == 2): move = 4
                        elif(move == 3): move = 1
                        elif(move == 4): move = 2
                    else:
                        if (move == 1): move = 4
                        elif (move == 2): move = 1
                        elif (move == 3): move = 2
                        elif (move == 4): move = 3
                else:
                    if (move == 1): move = 2
                    elif (move == 2): move = 3
                    elif (move == 3): move = 4
                    elif (move == 4): move = 1
            k += 1
            #print(move)
            #print(pos)
            #print("##############end")
            if(move == 1):
                if(pos[1] > 0):
                    pos = [pos[0], pos[1]-1]
            elif(move == 3):
                if(pos[1] < size-1):
                    pos = [pos[0], pos[1]+1]
            elif(move == 4):
                if (pos[0] < size-1):
                    pos = [pos[0] + 1, pos[1]]
            elif(move == 2):
                if (pos[0] > 0):
                    pos = [pos[0]-1 , pos[1]]
            reward += grid_value_total[i][pos[1]][pos[0]]
        #print(reward)
        total += reward
        #print("3333333333333333333")
    #print("result")
    print(int(np.floor(total/10)))
    #output_file.write(str(int(np.floor(total/10))) + '\n')



input_file.close()
output_file.close()
#print(num_cars)
#print(num_obstacles)
#print(pos_start_cars)
#print(pos_obstacles)
#print(pos_terminal_cars)




