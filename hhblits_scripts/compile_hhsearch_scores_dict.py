import pickle 

scores_dir = '../data/SCOPe/contrib_hhblits/'
fns = ['hhblits_all_th95_query_fast_chunk'+str(i)+'.scores.ffdata' for i in range(10)]

data = {}
current_entry = {}
i=0

for fn in fns:
    scores_path = scores_dir + fn
    with open(scores_path, 'r') as file:
        for line in file:
            i+=1
            # if i>60000:
            #     break
            line = line.strip().replace('\x00','')
            if line.startswith("NAME"):
                if current_entry:
                    data[current_entry['FILE']] = current_entry
                    current_entry = {}
            elif line:
                key, value = line.split(maxsplit=1)
                try:
                    if key !='FILE':
                        value = value.split()[6]
                except:
                    pass
                current_entry[key] = value
        

with open('../data/SCOPe/contrib_hhblits/scope_th95_hhsearch_probs_dct.pk', 'wb') as file:
    pickle.dump(data, file)