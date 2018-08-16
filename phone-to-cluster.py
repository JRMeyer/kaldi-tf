
import sys

mapping=sys.argv[1]



phoneMap={}
with open(mapping, 'r') as f:
    lines = f.readlines()
    for line in lines:
        cluster=line.split()[1]
        phone=line.split()[0]
        
        if cluster in phoneMap:
            if phone in phoneMap[cluster]:
                phoneMap[cluster][phone] = phoneMap[cluster][phone] + 1
            else:
                phoneMap[cluster][phone] = 1

        else:
            phoneMap[cluster] = {phone:1}

for item in phoneMap.items():
    print(item[0], item[1])
        
