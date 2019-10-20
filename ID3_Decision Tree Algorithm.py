import csv
import math
#from operator import add
'''
readAllSamples is a user defined function. It is used to read all the sample of CSV file. It takes filename as an argument as well as test row count to make a test set from the file. This function returns a train set and a test set.

'''
def readAllSamples(fileName,test_row_count,Del_colm):
    
    ff1=csv.reader(fileName)
    b=[]
    a=[]
    g=[]
    for row in ff1:
        b.append(row)
    #print(b)
    #print(len(b))
    for i in range(1,len(b)):
      g.append(b[i])
    for i in range(len(g)):
      a.append(g[i][Del_colm:(len(g)-1)])
    #print("\n",a)
    #print(len(a))
    trainSet=[]
    testSet=[]
    for i in range(0,(len(a)-test_row_count)):
      trainSet.append(a[i])
    for i in range((len(a)-test_row_count), len(a)):
      testSet.append(a[i])
    return trainSet,testSet

'''
This is the end of readAllSamples function.
'''

f1=open("Book1.csv",newline='')
test_row=int(input("please provide how many rows you want as test set\n"))
Del_colm=int(input("is there any column you want to exclude during gain calculation? if any, please provide column number, otherwise please provide Zero(0) \n"))
train_set,test_set=readAllSamples(f1,test_row,Del_colm)
#print(train_set)
#print(test_set)

'''
This is entropy function. It takes table as input and finds out entropy. 

'''
def entropy(table):
    decision_attribute=[]
    for i in range(len(table)):
        decision_attribute.append(table[i][len(table[0])-1])
    
    set_decision_attribute=list(set(decision_attribute))
    #print('set_decision_attribute', set_decision_attribute)
    decision_attribute_count=[]
    for i in range(len(set_decision_attribute)):
      decision_attribute_count.append(decision_attribute.count(set_decision_attribute[i]))
    entropy=0
    for i in range(len(set_decision_attribute)):
      if (len(set_decision_attribute))==1:
        entropy=0
        
      #if len(decision_attribute_count)==1:
        #entropy=0
        #break
      else:
        entropy += (-1)*(decision_attribute_count[i]/sum(decision_attribute_count))* math.log2((decision_attribute_count[i]/sum(decision_attribute_count)))

    #print("entropy",entropy)
    return entropy
'''
a=[['Overcast', 'Hot', 'High', 'Weak', 'Yes'], ['Overcast', 'Cool', 'Normal', 'Strong', 'Yes'], ['Overcast', 'Mild', 'High', 'Strong', 'Yes'], ['Overcast', 'Hot', 'Normal', 'Weak', 'Yes']]
sample=entropy(a)
print(sample)
b=[['Sunny', 'Hot', 'High', 'Weak', 'No'], ['Sunny', 'Hot', 'High', 'Strong', 'No'], ['Sunny', 'Mild', 'High', 'Weak', 'No'], ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],['Sunny', 'Mild', 'Normal', 'Strong', 'Yes']]
sample1=entropy(b)
print("sample1" ,sample1)
'''
total_entropy=entropy(train_set)
print('Total entropy\n',total_entropy)


'''
informationGain is an user defined function. it takes table, the attribute for which we want to find out entropy and total entropy of the table as input. It returns gain of the attribute.
'''

def informationGain(table, attribute, total_entropy):

  #print(table)
  table_len=len(table)
  #print(table_len)
  att=[]
  decision_attribute=[]
  for i in range(len(table)):
        decision_attribute.append(table[i][len(table[0])-1])
        att.append(table[i][attribute])
  #print('att',att)
  #print(decision_attribute)
  set_att=list(set(att))
  att_count=[]


  for i in range(0,len(set_att)):
      att_count.append(att.count(set_att[i])) 
  #print("att_count",att_count)
  merge_att=[]
  merge_att_dec=[]

  header_count = len(set_att)+1
  header = [[] for i in range(1, header_count)]
  #print(header)

  for j in range(len(set_att)):
      for i in range((len(att))):
            if att[i]==set_att[j]:
              merge_att.append(att[i])
              merge_att_dec.append(decision_attribute[i])
  #print(merge_att_dec)
  #print(merge_att)
  new=[[a,merge_att_dec[ind]] for ind, a in enumerate(merge_att)]
  #print(new)
  entropy_list_attr=[]
  for j in range(len(set_att)):
    for i in range((len(new))):
      if new[i][0]==set_att[j]:
        header[j].append(new[i])
        #print(header)
    entropy_list_attr.append(entropy(header[j]))
    #print(entropy_list_attr)

  #print(entropy_list_attr)
  #print(set_att)
  entropy_att=0
  for i in range(len(set_att)):
    entropy_att +=((att_count[i]*entropy_list_attr[i])/sum(att_count))
  gain=total_entropy-entropy_att
  #print(gain)
  #print(entropy_att)
  return gain

# Finding out gain
gain=[]
for i in range((len(train_set[0])-1)):
  gain.append(informationGain(train_set,i,total_entropy))
max_gain_column=gain.index(max(gain))


print("gain of the training sets are", gain)
#print(max_gain_column)
print("root will be column number-->",max_gain_column+1)


  
def splitData(train_set, max_gain_column):  
  set_max_gain_column=[]
  for i in range(len(train_set)):
    set_max_gain_column.append(train_set[i][max_gain_column])
  set_max_gain_column=list(set(set_max_gain_column))  
  #print(set_max_gain_column)
  new_train_set=[]
  child_root_gain=[]
  child = [[] for i in range(1, len(set_max_gain_column)+1)]
  for j in range(len(set_max_gain_column)):
    for i in range(len(train_set)):
      if (train_set[i][max_gain_column]==set_max_gain_column[j]):
        child[j].append(train_set[i])
        #print(child[j])
    #print(child)
  return child

def treeBuild(train_set,max_gain_column):
  root_child=[]
  root_child=splitData(train_set,max_gain_column)
  root_child_entropy=[]
  root_child_gain=[]
  test=[]
  test2=[]
  #print(root_child)
  for i in range(len(root_child)):
    root_child_entropy.append(entropy(root_child[i]))
    if root_child_entropy[i]==0:
      print('First root_child for',root_child[i][1][max_gain_column], "is -->",root_child[i][1][-1],len(root_child[i]))
      
    else:
      for j in range(len(root_child[i])-1):
        root_child_gain.append(informationGain(root_child[i],j,root_child_entropy[i]))
      #test2.append(root_child_gain[j])
      test.append(root_child[i])
        #print("root_child_gain",root_child_gain)

  #print(root_child_gain)
  #print(test)
  #print(test2)
  def to_matrix(root_child_gain, n):
    return [root_child_gain[i:i+n] for i in range(0, len(root_child_gain), n)]

  for i in range(len(root_child)):
    if len(root_child_gain) > len(root_child):
      test2= to_matrix(root_child_gain,len(test[0][:-1]))
    else:
      pass
  #print(test2)
  print("Second root_child will be coulmn number-->", (test2[0].index(max(test2[0]))+1))
  while len(test2)!=1:
    print("Third root_child will be coulmn number-->", (test2[1].index(max(test2[1]))+1))
    break
  return test,test2

a,b=treeBuild(train_set,max_gain_column)
#print("aqkdhckw",a)
#print("bwrefwre",b)
#c=[]
#for i in range(len(a)):
  #c.append(treeBuild(a[i],b[i].index(max(b[i]))))
  #print(c)
d=treeBuild(a[0],b[0].index(max(b[0])))
e=treeBuild(a[1],b[1].index(max(b[1])))
print(d)
print(e)
'''
a=[['Rain', 'Mild', 'High', 'Weak', 'Yes'], ['Rain', 'Cool', 'Normal', 'Weak', 'Yes'], ['Rain', 'Cool', 'Normal', 'Strong', 'No'], ['Rain', 'Mild', 'Normal', 'Weak', 'Yes'], ['Rain', 'Mild', 'High', 'Strong', 'No']]
sample=entropy(a)
test=[]
for i in range(len(a[1])-1):
  test.append(informationGain(a,i,sample))
#print(sample)
#print("test", test)
b=[['Sunny', 'Hot', 'High', 'Weak', 'No'], ['Sunny', 'Hot', 'High', 'Strong', 'No'], ['Sunny', 'Mild', 'High', 'Weak', 'No'], ['Sunny', 'Cool', 'Normal', 'Weak', 'Yes'],['Sunny', 'Mild', 'Normal', 'Strong', 'Yes']]
sample1=entropy(b)
test1=[]
for i in range(len(b[1])-1):
  test1.append(informationGain(b,i,sample1))
  print("test1", test1)
print("sample1" ,sample1)
#print("test", test1)

'''

    

#print(root_child_entropy)

#Implementing decision tree algorithm ID3 using the above functions.

'''
class Node:

    def __init__(self):
        self.children=[]
        self.name=""


    def rename(self,a):
        self.name=a

    def addChildren(self,a):
        self.children = self.children + [a]

def preOrderTraversal(a):
    print(a.name)
    for c in a.children:
        preOrderTraversal(c)

root=Node()
root.rename(train_set[0][max_gain_column])

n1 = Node()
#n1.rename(root_child[i][1][-1])

n11 = Node()
n11.rename("N11")
n12 = Node()
n12.rename("N12")
n13 = Node()
n13.rename("N13")
n1.addChildren(n11)
n1.addChildren(n12)
n1.addChildren(n13)


n2 = Node()
n2.rename("N2")

root.addChildren(n1)
root.addChildren(n2)

preOrderTraversal(root)

'''








'''
def Information_gain(train_set,total_entropy):
  attribute_1=[]
  attribute_2=[]
  attribute_3=[]
  attribute_4=[]
  attribute_5=[]
  decision_attribute=[]
  for i in range(len(train_set)):
        attribute_1.append(train_set[i][1:6:4])
        attribute_2.append(train_set[i][2:6:3])
        attribute_3.append(train_set[i][3:6:2])
        attribute_4.append(train_set[i][4:6:1])
        #attribute_5.append(train_set[i][5:6])
        #decision_attribute.append(train_set[i][len(train_set[0])-1])
  print(attribute_1)
  print(attribute_2)
  #print(attribute_3)
  #print(attribute_4)
  #print(attribute_5)
  sub_attribute_1=[]

  for i in range(len(attribute_1)):
    if attribute_1[i][0]=="Sunny":
      sub_attribute_1.append(attribute_1[i])

  print(sub_attribute_1)
  entropy_sub_attribute_1=entropy(sub_attribute_1)
  print(entropy_sub_attribute_1)

gain=Information_gain(train_set,total_entropy) 
'''
  


  