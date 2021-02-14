# import os
# from PIL import Image

# for file in os.listdir():
# 	name, ext = os.path.splitext(file)
# 	if name.startswith('bg'):
# 		img = Image.open(file).resize((500,500))
# 		img.save(f'{name}s.png')

def subsetproduct(lst, k):
  count = 0
  n = len(lst)
  for i in range(0,n):
    if lst[i] <= k:
      count += 1
    prod = lst[i]
    for j in range(i+1, n):
      prod = prod * lst[j]
      
      if prod <= k:
        count += 1
      else:
        break
        
  return count

lst = [1,2,3,4,5,6]
k = 20
print(subsetproduct(lst, k))
