import pandas as pd
import re
#To display all rows and columns without truncating
pd.set_option("max_rows", None)
pd.set_option("max_columns", None)
# getting the student list
stuList = pd.read_excel('MINI-2\SOURCE-FILE.xlsx')
stuList.head()
stuList["Student Name"] = stuList["Student Name"].str.replace('.','')
stuList["Student Name"] = stuList["Student Name"].str.replace('  ',' ')
stuList["Student Name"] = stuList["Student Name"].str.strip()
stuDict = dict(zip(stuList['Roll No.'].astype(str), stuList['Student Name']))
# getting the saved data from file 1
df1 = pd.read_table('MINI-2\meeting_saved_chat.txt', sep=":", names=('Hour', 'Min', 'Details', 'Roll'))
df1.head(7)
# getting the saved data from file 2
df2 = pd.read_table('MINI-2\chat.txt', sep=":", names=('Hour', 'Min', 'Details', 'Roll'))
df2.head(7)
df2.Roll = df2.Roll.astype(str)
#data.Details = data.Details.apply(lambda x: x.replace("_", " "))
#data.Details.apply(lambda x: [int(i) for i in x.split() if i.isdigit()])
#data["Roll_extracted"] = data.Details.apply(lambda x: re.findall('[0-9]+', x))
#data["name"] = data.Details.apply(lambda x: re.findall('[a-z]+', x))pattern = "From (.*?) to"
df1["Details"] = df1.Details.apply(lambda x: re.search(pattern, x).group(1))
df1[100:107]
pattern = "From (.*?)"
df2["Details"] = df2.Details.apply(lambda x: re.search('From(.*)', x).group(1))
df2.head(7)
frames = [df1, df2]
df = pd.concat(frames)
print("Size of first dataset:",df1.shape)
print("Size of second dataset:",df2.shape)
print("Size after combining them:",df.shape)
df.reset_index(drop=True, inplace=True)
df.drop(columns=['Hour','Min'],inplace=True)
df["Roll_extracted"] = df['Details'].apply(lambda x: re.findall('[0-9]+', x))
df.Roll_extracted = df.Roll_extracted.apply(lambda x: " ".join(x))
df.head()
#df[df['Roll_extracted'].str.len()<7]
#data['Roll_extracted'].apply(lambda x: x[0:7])
#df['Roll_extracted']=df['Roll_extracted'].astype(int, errors='raise')
df["Name"] = df.Details.map(lambda x: re.findall(('[a-zA-Z]+'), x))
df.Name = df.Name.apply(lambda x: " ".join(x))
df.head()
df.drop(columns = "Details", inplace=True)
df.Roll = df.Roll.str.strip()
df.Roll_extracted = df.Roll_extracted.str.strip()
df.Name = df.Name.str.strip()
# removing chat rolls having length more than 8
rule = df['Roll'].str.len()>8
df.drop(df[rule].index, inplace=True)
# removing students with no name and no roll number
rule = (df['Roll_extracted'].str.len() == 0) & (df['Name'] == 'KIIT')
df.drop(df[rule].index, inplace=True)
df.head()
df.shape
df['Attn'] = "ABS"
for ind in df.index:
    if df['Roll'][ind] == df['Roll_extracted'][ind] or df['Roll'][ind][-3:] == df['Roll_extracted'][ind]:
        df['Attn'][ind] = 'PRES'

    if df['Attn'][ind] == 'ABS' and stuDict[df['Roll'][ind]] == df['Name'][ind].upper():
        df['Attn'][ind] = 'PRES'
CList = list(stuDict.keys())
Pres = list(df['Roll'])
# making absent list
Abs = pd.DataFrame(df(CList,Pres))
Abs.columns = ['Absentees Roll']
Abs.sort_values("Absentees Roll", inplace=True)
Abs.reset_index(drop=True, inplace=True)

