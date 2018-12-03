import time
input_file = open('input13.txt','r')
output_file = open('output.txt' , 'w')
start_time = time.time()
size = int(input_file.readline().strip())
num_officers = int(input_file.readline().strip())
num_scooters = int(input_file.readline().strip())

position_dict = { }
'''define scotters' position by  a dict'''
for line in input_file.readlines():
    line = line.strip().split(',')
    position_x = int(line[0].strip())
    position_y = int(line[1].strip())
    if position_dict.has_key((position_x,position_y)):
        position_dict[(position_x,position_y)] = position_dict.get((position_x,position_y)) + 1
    else:
        position_dict[(position_x, position_y)]  = 1
print position_dict

max_colValue = []
for x in range(size):
    list = []
    for y in range(size):
        if  position_dict.has_key((x,y)):
            list.append(position_dict.get((x,y)))
        else:
            list.append(0)
    max_colValue.append(max(list))
print max_colValue

row_list = []
for x in range(size):
    dict = {}
    for y in range(size):
        if  position_dict.has_key((x,y)):
            dict[(x, y)] = position_dict.get((x,y))
        else:
            dict[(x, y)] = 0
    row_list.append(sorted([(value, key) for (key, value) in dict.items()],reverse=True))

def queen_rule(list, point):
    if len(list) == 0: return True
    x_dict = {}
    y_dict = {}
    diag1_dict = {}
    diag2_dict = {}
    for i in range(len(list)):
        x_dict[list[i][0]] = 1
        y_dict[list[i][1]] = 1
        diag1_dict[list[i][0] - list[i][1]] = 1
        diag2_dict[list[i][1] + list[i][0]] = 1
    if x_dict.has_key(point[0]): return False
    if y_dict.has_key(point[1]): return False
    if diag1_dict.has_key(point[0] - point[1]): return False
    if diag2_dict.has_key(point[0] + point[1]): return False
    return True

def goodToGo(queen_list, current_score):

    start = queen_list[-1][0]
    score = current_score
    num_needed = num_officers - len(queen_list)
    rest_list = max_colValue[start+1:]
    if len(rest_list) < num_needed: return False
    max_list = sorted(rest_list, reverse=True)
    if len(max_list) !=0:
         for i in range(num_needed):
             score += max_list[i]
    if score <= max(current_scoreList):
        return False
    return True

all_list = []

current_scoreList = [max(max_colValue)]

def dfs_nQueen(x_start, size, num_officers, queen_list, all_list, current_score):
    if len(queen_list) != 0:
        if goodToGo(queen_list, current_score) == False:
            return
    if len(queen_list) == num_officers:
        current_scoreList.append(current_score)
        return

    for x in range(x_start, size):
        for point in row_list[x]:
            y = point[1][1]
            if len(queen_list) == 0 and x == size - num_officers + 1: return

            if queen_rule(queen_list,(x,y)) == True:
                queen_list.append((x,y))
                if position_dict.has_key((x,y)):
                    current_score += position_dict.get((x,y))
                #print goodToGo(queen_list)
                dfs_nQueen(x_start + 1, size, num_officers, queen_list, all_list, current_score)
                if position_dict.has_key((x, y)):
                    current_score -= position_dict.get((x,y))
                queen_list.pop()



'''
def dfs_nQueen(x_start, size, num_officers, queen_list, all_list, current_score):
    if len(queen_list) != 0:
        if goodToGo(queen_list, current_score) == False:
            return
    if len(queen_list) == num_officers:
        current_scoreList.append(current_score)
        return

    for x in range(x_start, size):
        for y in range(size):
            if len(queen_list) == 0 and x == size - num_officers + 1: return

            if queen_rule(queen_list,(x,y)) == True:
                queen_list.append((x,y))
                if position_dict.has_key((x,y)):
                    current_score += position_dict.get((x,y))
                #print goodToGo(queen_list)
                dfs_nQueen(x_start + 1, size, num_officers, queen_list, all_list, current_score)
                if position_dict.has_key((x, y)):
                    current_score -= position_dict.get((x,y))
                queen_list.pop()
'''



dfs_nQueen( 0, size, num_officers, [], all_list, 0)

print max(current_scoreList)
output_file.write(str(max(current_scoreList)))

input_file.close()
output_file.close()
end_time  = time.time()
print end_time - start_time

