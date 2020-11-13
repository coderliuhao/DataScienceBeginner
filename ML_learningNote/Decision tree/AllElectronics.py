from sklearn.feature_extraction import DictVectorizer
import csv
from sklearn import preprocessing
from sklearn import tree
import numpy as np

all_electronic_data=open(r"D:/PycharmProjects/机器学习实战/test.csv","r")
reader=csv.reader(all_electronic_data)

dic_reader=csv.DictReader(all_electronic_data)
row=[row for row in dic_reader]

label_list=[]
for i in row:
    del i["RID"]
    label_list.append(i.pop("class_buy_computer"))

feature_col=row

vec=DictVectorizer()
dummy_X=vec.fit_transform(feature_col).toarray()
print("dummy X:"+str(dummy_X))
print(vec.get_feature_names())
print("label list:"+str(label_list))
#print(dummy_X.shape)

lb=preprocessing.LabelBinarizer()
dummy_Y=lb.fit_transform((label_list))
print("dummy Y:"+str(dummy_Y))
#print(dummy_Y.shape)

clf=tree.DecisionTreeClassifier(criterion="entropy")
clf=clf.fit(dummy_X,dummy_Y)
#print("clf :"+str(clf))

with open("D:/PycharmProjects/机器学习实战/test.dot","w") as f:
    f=tree.export_graphviz(clf,feature_names=vec.get_feature_names(),out_file=f)

row_1=dummy_X[0]
print("row1:"+str(row_1))
#print(row_1.shape)

new_rowX=row_1
new_rowX[0]=1
new_rowX[1]=0
new_rowX=new_rowX.reshape(1,10)
print("new_rowX:"+str(new_rowX))
predict_Y=clf.predict(new_rowX)
print("prediction_Y:"+str(predict_Y))