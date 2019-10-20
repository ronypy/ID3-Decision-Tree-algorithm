import csv
import math

# from operator import add
'''
readAllSamples is a user defined function. It is used to read all the sample of CSV file. It takes filename as an argument as well as test row count to make a test set from the file. This function returns a train set and a test set.

'''


def readAllSamples(fileName, test_row_count, Del_colm):
    ff1 = csv.reader(fileName)
    b = []
    a = []
    g = []
    headers = []
    for row in ff1:
        b.append(row)
    # print(b)
    # print(len(b))

    for i in range(Del_colm, len(b[0])):
        headers.append(b[0][i])
    # print(h)
    for i in range(1, len(b)):
        g.append(b[i])
    # print(g)
    for i in range(len(g)):
        a.append(g[i][Del_colm:(len(g) - 1)])
    # print("\n",a)
    # print(len(a))
    trainSet = []
    testSet = []
    for i in range(0, (len(a) - test_row_count)):
        trainSet.append(a[i])
    for i in range((len(a) - test_row_count), len(a)):
        testSet.append(a[i])
    return trainSet, testSet, headers


f1 = open("Book1.csv", newline='')
test_row = int(input("please provide how many rows you want as test set\n"))
Del_colm = int(input(
    "is there any column you want to exclude during gain calculation? if any, please provide column number, otherwise please provide Zero(0) \n"))
train_set, test_set, headers = readAllSamples(f1, test_row, Del_colm)

'''
This is entropy function. It takes table as input and finds out entropy. 

'''


def entropy(table):
    decision_attribute = []
    for i in range(len(table)):
        decision_attribute.append(table[i][len(table[0]) - 1])

    set_decision_attribute = list(set(decision_attribute))
    decision_attribute_count = []
    for i in range(len(set_decision_attribute)):
        decision_attribute_count.append(decision_attribute.count(set_decision_attribute[i]))
    entropy = 0
    for i in range(len(set_decision_attribute)):
        if (len(set_decision_attribute)) == 1:
            entropy = 0

        else:
            entropy += (-1) * (decision_attribute_count[i] / sum(decision_attribute_count)) * math.log2(
                (decision_attribute_count[i] / sum(decision_attribute_count)))

    return entropy


'''
informationGain is an user defined function. it takes table, the attribute for which we want to find out entropy and total entropy of the table as input. It returns gain of the attribute.
'''


def informationGain(table, attribute, total_entropy):
    table_len = len(table)
    att = []
    decision_attribute = []

    for i in range(len(table)):
        decision_attribute.append(table[i][len(table[i]) - 1])
        att.append(table[i][attribute])

    set_att = list(set(att))
    att_count = []

    for i in range(0, len(set_att)):
        att_count.append(att.count(set_att[i]))

    merge_att = []
    merge_att_dec = []

    header_count = len(set_att) + 1
    header = [[] for i in range(1, header_count)]

    for j in range(len(set_att)):
        for i in range((len(att))):
            if att[i] == set_att[j]:
                merge_att.append(att[i])
                merge_att_dec.append(decision_attribute[i])

    new = [[a, merge_att_dec[ind]] for ind, a in enumerate(merge_att)]

    entropy_list_attr = []
    for j in range(len(set_att)):
        for i in range((len(new))):
            if new[i][0] == set_att[j]:
                header[j].append(new[i])

        entropy_list_attr.append(entropy(header[j]))

    entropy_att = 0
    for i in range(len(set_att)):
        entropy_att += ((att_count[i] * entropy_list_attr[i]) / sum(att_count))
    gain = total_entropy - entropy_att
    return gain


# Finding out column of maximum gain
def gainMatrix(train_set, total_entropy):
    gain = []

    for i in range(len(train_set[0]) - 1):
        gain.append(informationGain(train_set, i, total_entropy))
    max_gain_column = gain.index(max(gain))

    # print(gain)
    # print(train_set)
    return max_gain_column


# This function split data and create tree.


def splitData(train_set, max_gain_column, headers, counter):
    set_max_gain_column = []
    for i in range(len(train_set)):
        set_max_gain_column.append(train_set[i][max_gain_column])

    set_max_gain_column = list(set(set_max_gain_column))
    # print(set_max_gain_column)
    new_train_set = []
    child_root_gain = []
    child = [[] for i in range(len(set_max_gain_column))]

    for j in range(len(set_max_gain_column)):
        for i in range(len(train_set)):
            if (train_set[i][max_gain_column] == set_max_gain_column[j]):
                child[j].append(train_set[i])

        # print(child)
    # print(child)
    k = counter
    ent = []
    for i in range(len(child)):
        ent.append(entropy(child[i]))
    # print(ent)
    child, ent = zip(*sorted(zip(child, ent)))
    # print(child)
    # print(ent)
    # qq=sorted(set(child), key=child.index)
    # print(qq)
    # k=k+1
    for i in range(len(child)):
        root_child_entropy = entropy(child[i])
        max_gain_column = gainMatrix(child[i], root_child_entropy)
        if root_child_entropy == 0:
            # print("root _child node will be col", set_max_gain_column, "& element count will be", len(child[i]) )
            # max_gain_column=gainMatrix(child[i], root_child_entropy)
            # print(child[i])
            # print(max_gain_column)
            print(
                "For {} {}, decision will be {}".format(headers[k], child[i][0][k], child[i][0][len(child[i][0]) - 1]))


        else:
            k = gainMatrix(child[i], root_child_entropy)
            # print("k",k)
            print("child_root will be {} ".format(headers[max_gain_column]))
            # print(child[i])
            splitData(child[i], max_gain_column, headers, k)
            # pass
            # print(child[i])
            # for i in range(len(child[i][0][max_gain_column])):
            # splitData(child[i], max_gain_column,headers,k)

    # splitData.counter+=1
    # print(splitData.counter)
    # print(k)

    return child


total_entropy = entropy(train_set)
# print('Total entropy\n',total_entropy)
xx = gainMatrix(train_set, total_entropy)
print("root will be {}".format(headers[xx]))
counter = 0
pp = splitData(train_set, xx, headers, counter)

# the end


