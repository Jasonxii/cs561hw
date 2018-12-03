import time
start = time.clock()
input_file = open('input10.txt','r')
output_file = open('output.txt','w')
start_time = time.time()
num_beds = int(input_file.readline().strip())
num_space = int(input_file.readline().strip())
num_LAHSA_chosen = int(input_file.readline().strip())
applicants_LAHSA_chosen = {}
for i in range(num_LAHSA_chosen):
    line = str(input_file.readline().strip())
    applicants_LAHSA_chosen[line] = line[13:]
num_SPLA_chosen = int(input_file.readline().strip())
applicants_SPLA_chosen = {}
for i in range(num_SPLA_chosen):
    line = str(input_file.readline().strip())
    applicants_SPLA_chosen[line] = line[13:]
num_total = int(input_file.readline().strip())

def is_Free(ID):
    if (applicants_LAHSA_chosen.has_key(ID)): return False
    if(applicants_SPLA_chosen.has_key(ID)): return False
    return True

applicants_total = {}
applicants_LAHSA_qualified = {}
applicants_SPLA_qualified = {}
applicants_SPLA_qualified_list = []
applicants_LAHSA_qualified_list = []


def isQualified_LAHSA(record):
    if(record[5] != 'F'): return False
    if(int(record[6:9]) <= 17 ): return False
    if(record[9] != 'N'): return False
    return True

def isQualified_SPLA(record):
    if (record[10] != 'N'): return False
    if (record[11] != 'Y'): return False
    if (record[12] != 'Y'): return False
    return True



def efficient(record):
    num_days = 0
    for i in range(7):
        if(int(record[13 + i]) == 1): num_days += 1
    return num_days


for i in range(num_total):
    record = str(input_file.readline().strip())
    applicants_total[record[:5]] = record[13:]
    if(is_Free(record[:5]) == True):
        if(isQualified_LAHSA(record)):
            applicants_LAHSA_qualified[record[:5]] = efficient(record)
            applicants_LAHSA_qualified_list.append(record[:5])
        if(isQualified_SPLA(record)):
            applicants_SPLA_qualified[record[:5]] = efficient(record)
            applicants_SPLA_qualified_list.append(record[:5])


for record in applicants_LAHSA_chosen:
    applicants_LAHSA_chosen[record] = applicants_total.get(record)

for record in applicants_SPLA_chosen:
    applicants_SPLA_chosen[record] = applicants_total.get(record)


date_LAHSA = {}
for ID in applicants_LAHSA_chosen:
    for i in range(7):
        if (int(applicants_LAHSA_chosen.get(ID)[i]) == 1):
            if (date_LAHSA.has_key(1 + i)):
                date_LAHSA[1 + i] = date_LAHSA.get(1 + i) + 1
            else:
                date_LAHSA[1 + i] = 1

def isDate_LAHSA(LAHSA_path, record):
    local_date_LAHSA = date_LAHSA.copy()
    LAHSA_path.append(record)
    for records in LAHSA_path:
        for i in range(7):
            if(int(applicants_total[records][i]) == 1 ):
                if(local_date_LAHSA.has_key(1 + i)):
                    if(local_date_LAHSA[1 + i] == num_beds): return False
                    else:
                        local_date_LAHSA[1 + i] = local_date_LAHSA[1 + i] + 1
                else: local_date_LAHSA[1 + i] =  1
    return True

date_SPLA = {}
for ID in applicants_SPLA_chosen:
    for i in range(7):
        if (int(applicants_SPLA_chosen[ID][i]) == 1):
            if (date_SPLA.has_key(1 + i)):
                date_SPLA[1 + i] = date_SPLA[1 + i] + 1
            else:
                date_SPLA[1 + i] = 1


def isDate_SPLA(SPLA_path, record):
    local_date_SPLA = date_SPLA.copy()
    SPLA_path.append(record)
    for records in SPLA_path:
        for i in range(7):
            if(int(applicants_total[records][i]) == 1 ):
                if(local_date_SPLA.has_key(1 + i)):
                    if(local_date_SPLA[1 + i] == num_space): return False
                    else:
                     local_date_SPLA[1 + i] = local_date_SPLA[1 + i] + 1
                else: local_date_SPLA[1 + i] =  1
    return True

SPLA_score = 0
LAHSA_score = 0
def maximax(Depth, ID, SPLA_path, LAHSA_path, S_turn):
    global SPLA_score,LAHSA_score
    if Depth == 2*max(len(applicants_SPLA_qualified_list),len(applicants_LAHSA_qualified_list)):
        return [SPLA_score, LAHSA_score]
    if S_turn == True:
        if (ID != -1):
            SPLA_path.append(ID)
            SPLA_score += applicants_SPLA_qualified[ID]
        temp_LAHSA = []
        for ID_LAHSA in applicants_LAHSA_qualified_list:
            if((not ID_LAHSA in SPLA_path)and (not ID_LAHSA in LAHSA_path) and isDate_LAHSA(list(LAHSA_path), ID_LAHSA) == True):
                temp_LAHSA.append(ID_LAHSA)
        if(len(temp_LAHSA)!=0):
            LAHSA_max = [0, 0]
            for i in temp_LAHSA:
                LAHSA_have = maximax(Depth+1, i, SPLA_path, LAHSA_path, False)
                if (LAHSA_have[1] > LAHSA_max[1]):
                    LAHSA_max = list(LAHSA_have)
                LAHSA_path.pop()
                LAHSA_score -= applicants_LAHSA_qualified[i]
            return LAHSA_max
        else:
            return maximax(Depth + 1, -1, SPLA_path, LAHSA_path, False)
    else:
        if (ID != -1):
            LAHSA_path.append(ID)
            LAHSA_score += applicants_LAHSA_qualified[ID]
        temp_SPLA = []
        for ID_SPLA in applicants_SPLA_qualified_list:
            if((not ID_SPLA in SPLA_path)and (not ID_SPLA in LAHSA_path) and isDate_SPLA(list(SPLA_path), ID_SPLA) == True):
                temp_SPLA.append(ID_SPLA)
        if (len(temp_SPLA)!=0):
            SPLA_max = [0, 0]
            for i in temp_SPLA:
                SPLA_have = maximax(Depth + 1, i, SPLA_path, LAHSA_path, True)
                if(SPLA_have[0] > SPLA_max[0]):
                    SPLA_max = list(SPLA_have)
                SPLA_path.pop()
                SPLA_score -= applicants_SPLA_qualified[i]
            return SPLA_max
        else:
            return maximax(Depth+1, -1, SPLA_path, LAHSA_path, True)

best_scores = [0, 0]
first_choice_ID = ""
for ID_SPLA in applicants_SPLA_qualified_list:
    SPLA_score = 0
    LAHSA_score = 0
    back_score = maximax(0, ID_SPLA, [], [], True)
    if back_score[0] > best_scores[0]:
        best_scores = back_score
        first_choice_ID = ID_SPLA
print first_choice_ID
print best_scores
output_file.write(first_choice_ID)

end = time.clock()
print(end-start)
input_file.close()
output_file.close()