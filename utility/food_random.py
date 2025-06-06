import pandas as pd
import random
import sys

df = pd.read_excel('dir/food.xlsx')
ppl = 6
if len(sys.argv) > 1:
    ppl = sys.argv[1] 

food_to_order = int(ppl) - 1

headers = df.columns.tolist()

result = []
for header in headers:
    rand = df[header].tolist()
    choice = random.choice(rand)
    while True:
        if pd.isna(choice):
            choice = random.choice(rand)
        else:
            break
    result.append(choice)

if len(result) >= int(ppl):
    result = result[:food_to_order]
print(result)

