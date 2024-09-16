import pandas as pd
from datetime import datetime
from datetime import date
from dateutil.relativedelta import relativedelta
import numpy as np
import numba as nb
from tqdm import tqdm
# from numba import njit, jit, cuda
import time 


newPandasDataFrame = pd.DataFrame()
now = date.today()

#for fix BUG: df.loc astype type change on specific row not working #59732
pd.options.future.infer_string = True


#Remove symbols and return alphanumerics
def alphanum(element):
    return "".join(filter(str.isalnum, element))
#Remove symbols & characters and return numbers only
def numbers(element):
    return "".join(filter(str.isnumeric, element))


#birthplace_identifier function
def birthplace_identifier(birthplace_two_digit):

    birthplace = birthplace_two_digit[0:1]
    birthplace=birthplace.upper()

    if birthplace == "А":
        birthplace = "Архангай"
    elif birthplace == "Б":
        birthplace = "Баян-Өлгий"
    elif birthplace == "В":
        birthplace = "Баянхонгор"
    elif birthplace == "Г":
        birthplace = "Булган"
    elif birthplace == "Д":
        birthplace = "Говь-Алтай"
    elif birthplace == "Е":
        birthplace = "Дорноговь"
    elif birthplace == "Ж":
        birthplace = "Дорнод"
    elif birthplace == "З":
        birthplace = "Дундговь"
    elif birthplace == "И":
        birthplace = "Завхан"
    elif birthplace == "Й":
        birthplace = "Өвөрхангай"
    elif birthplace == "К":
        birthplace = "Өмнөговь"
    elif birthplace == "Л":
        birthplace = "Сүхбаатар"
    elif birthplace == "М":
        birthplace = "Сэлэнгэ"
    elif birthplace == "Н":
        birthplace = "Төв"
    elif birthplace == "О":
        birthplace = "Увс"
    elif birthplace == "П":
        birthplace = "Ховд"
    elif birthplace == "Р":
        birthplace = "Хөвсгөл"
    elif birthplace == "С":
        birthplace = "Хэнтий"
    elif birthplace == "Т":
        birthplace = "Дархан-Уул"
    elif birthplace == "Ф":
        birthplace = "Орхон"
    elif birthplace == "Х":
        birthplace = "Говьсүмбэр"
    elif birthplace == "Ш":
        birthplace = "Эрдэнэт"
    elif birthplace == "У" or birthplace == "Ч":
        birthplace = "Улаанбаатар"
    else :
        birthplace = birthplace_two_digit
    
    return birthplace


# @nb.njit((nb.float64[:], nb.float64[:], nb.float64[:]))
def looper(birthYearColumn,birthMonthColumn,birthDayColumn, reg_number_cut, genderColumn):
    birthColumn = [0] * birthYearColumn.shape[0]
    ageColumn = [0] * birthYearColumn.shape[0]
    genderExtractedColumn = [0] * birthYearColumn.shape[0]

    for i in tqdm(range(birthYearColumn.shape[0]), desc = 'parsing birthday and age'):
        #print('input: ', reg_number_cut)

        if len(str(reg_number_cut[i])) < 5:
            birthYearColumn[i] = 1000
            birthMonthColumn[i] = 1
            birthDayColumn[i] = 1
        elif (birthMonthColumn[i]==2 and birthDayColumn[i]>29) or (birthMonthColumn[i] == 4 and birthDayColumn[i]>30) or (birthMonthColumn[i] == 6 and birthDayColumn[i]>30) or (birthMonthColumn[i] == 9 and birthDayColumn[i]>30) or (birthMonthColumn[i] == 11 and birthDayColumn[i]>30):
            #print('wrong datetime 1')
            birthYearColumn[i] = 1100
            birthMonthColumn[i] = 1
            birthDayColumn[i] = 1
        elif (birthYearColumn[i])>40 and birthMonthColumn[i]<13 and birthDayColumn[i]<32:
            birthYearColumn[i] = 1900 + birthYearColumn[i]
            birthMonthColumn[i] = birthMonthColumn[i]
            birthDayColumn[i] = birthDayColumn[i]
        elif (birthYearColumn[i])<30 and (birthMonthColumn[i]<33 and birthMonthColumn[i]>20) and birthDayColumn[i]<32:
            birthYearColumn[i] = 2000 + birthYearColumn[i]
            birthMonthColumn[i] = abs(birthMonthColumn[i] - 20)
            birthDayColumn[i] = birthDayColumn[i]
        else:
            #print('wrong datetime 2 - else')
            birthYearColumn[i] = 1200
            birthMonthColumn[i] = 1
            birthDayColumn[i] = 1
        
        #month date fixer
        if birthMonthColumn[i]>12 or birthMonthColumn[i]<1:
            birthMonthColumn[i]=1
        if birthDayColumn[i]>31 or birthDayColumn[i]<1:
            birthDayColumn[i]=1
        #print('                         : ', i)

        #birthdate calculator
        birthYear = int(birthYearColumn[i])
        birthMonth = int(birthMonthColumn[i])
        birthDay = int(birthDayColumn[i])
        
        birthYear = str(birthYear)
        birthMonth = str(birthMonth)
        birthDay = str(birthDay)

        date_str  = birthYear + "-" + birthMonth + "-" + birthDay
        #print("birth_date: ", date_str)
        date_format = '%Y-%m-%d'
        date_obj = datetime.strptime(date_str, date_format)
        age = relativedelta(now, date_obj).years

        birthColumn[i] = date_obj
        ageColumn[i] = age
        # print("\n\reg_number_cut[i]: ", reg_number_cut[i], '\n')
        # print("\n\ngenderColumn[i]: ", genderColumn[i], '\n\n')

        if genderColumn[i] % 2 == 0:
            genderExtractedColumn[i] = "female"
        else:
             genderExtractedColumn[i] = "male"

    #print(birthYearColumn,birthMonthColumn,birthDayColumn, birthColumn, ageColumn)
    print("loop done")
    return birthYearColumn,birthMonthColumn,birthDayColumn, birthColumn, ageColumn, genderExtractedColumn
    


#mongol_register_parser function------------------------------------------------------------
# @njit
def mongol_register_parser(your_csv_file_name, register_number_column):
    # register number fixer


    df = pd.read_csv(your_csv_file_name) #, low_memory=False


    #cut 500 samples for test
    #df = df.sample(n=min(50, len(df)), replace=True, random_state=42)
    # #to csv
    # df.to_csv('fiveHundred.csv', index=False)


    print('\n-----', your_csv_file_name,' file loaded. total row count: ', len(df))
    df.head(3)

    # Convert the 'register_number_column' column to numeric type; set non-numeric values to NaN
    df[register_number_column] = df[register_number_column].astype('str')

    #Remove symbols and return alphanumerics
    df.loc[:,register_number_column] = [alphanum(x) for x in df[register_number_column]]
    #Remove symbols & characters and return numbers only
    # df.loc[:,register_number_column] = [numbers(x) for x in df[register_number_column]]


    empty_rows = df[df[register_number_column].isna() | (df[register_number_column] == '')]
    print('\nbefore fill: empty rows in register_number_column:  ', len(empty_rows))


    # Fill the empty rows in register_number_column column with 'aa33333333'
    df[register_number_column] = df[register_number_column].fillna('aa3311111').replace('', 'aa3311111')

    # Optionally display print() the rows with empty register_number_column column
    empty_rows = df[df[register_number_column].isna() | (df[register_number_column] == '')]
    print('\nafter fill: empty rows in register_number_column:  ', len(empty_rows))
    

    df['reg_number_cut'] = df[register_number_column].str[2:9]


    #Remove symbols & characters and return numbers only
    df.loc[:,"reg_number_cut"] = [numbers(x) for x in df["reg_number_cut"]]

    # Fill the empty rows in register_number_column column with '3311111'
    df["reg_number_cut"] = df["reg_number_cut"].fillna('3311111').replace('', '3311111')


    df['birthYear'] = df["reg_number_cut"].str[0:2]
    df['birthMonth'] = df["reg_number_cut"].str[2:4]
    df['birthDay'] = df["reg_number_cut"].str[4:6]
    #genderColumn
    df['genderColumn'] = df["reg_number_cut"].str[6:7]
    print('\n--gender:', df['genderColumn'])
    


    # error here?
    df['reg_number_cut'] = pd.to_numeric(df['reg_number_cut'])
    # error here?
    df['birthYear'] = pd.to_numeric(df['birthYear'])
    df['birthMonth'] = pd.to_numeric(df['birthMonth'])
    df['birthDay'] = pd.to_numeric(df['birthDay'])
    df['genderColumn'] = pd.to_numeric(df['genderColumn'])

    #print test
    print("\n************reg_number_cut ", df['reg_number_cut'].dtype)
    print("************", df['reg_number_cut'])
    print("************reg_number_cut isnull(): ",df['reg_number_cut'].isnull().sum())
    print("************reg_number_cut isna(): ",df['reg_number_cut'].isna().sum().sum())

    print("\n************birthYear ", df['birthYear'].dtype)
    print("************", df['birthYear'])
    print("************birthYear isnull(): ",df['birthYear'].isnull().sum())
    print("************birthYear isna(): ",df['birthYear'].isna().sum().sum())
    print('\n')

    #prepare empty columns
    df["birthColumn"] = ""
    df["ageColumn"] = ""

    #main loop df-g numpy bolgood column aar ni oruulj irj bn
    birthYearColumn,birthMonthColumn,birthDayColumn, birthColumn, ageColumn, genderExtractedColumn = looper(df.birthYear.to_numpy(), df.birthMonth.to_numpy(), df.birthDay.to_numpy(), df.reg_number_cut.to_numpy(), df.genderColumn.to_numpy())

    #birthplace_identifier function
    df["birthplace"]=df[register_number_column].str[0:2]
    birthPlaceColumn = df["birthplace"]

    for index in tqdm(range(birthPlaceColumn.shape[0]), desc = 'parsing birth place'):
        birthPlaceColumn[index] = birthplace_identifier(birthPlaceColumn[index])



    # assign to dataframe
    df['birthYear'] = birthYearColumn
    df['birthMonthColumn'] = birthMonthColumn
    df['birthDayColumn'] = birthDayColumn
    df['birthColumn'] = birthColumn
    df['ageColumn'] = ageColumn
    df['genderExtractedColumn'] = genderExtractedColumn
    df['birthplace'] = birthPlaceColumn

    print("\nsaving age_added.csv to disk .........")
    df.to_csv('age_added.csv', encoding='utf-8', index=False, header=True)
    print("age_added.csv file saved to disk!\nparser Done!")
    
    #return newPandasDataFrame
    return df



#-----------------------------------for single register number---------------------------
def single_register_parser(text):

    birthplace_two_digit = text[0:2]
    birthYear = text[2:4]
    birthMonth = text[4:6]
    birthDay = text[6:8]
    gender = text[8:9]

    birthYear=int(birthYear)
    birthMonth=int(birthMonth)
    birthDay=int(birthDay)
    gender=int(gender)

    #birthplace_identifier function
    birthplace = birthplace_identifier(birthplace_two_digit)

    if len(str(text)) < 5:
        birthYear = 1000
        birthMonth = 1
        birthDay = 1
    elif (birthMonth==2 and birthDay>29) or (birthMonth == 4 and birthDay>30) or (birthMonth == 6 and birthDay>30) or (birthMonth == 9 and birthDay>30) or (birthMonth == 11 and birthDay>30):
        #print('wrong datetime 1')
        birthYear = 1100
        birthMonth = 1
        birthDay = 1
    elif birthYear>40 and birthMonth<13 and birthDay<32:
        birthYear = 1900 + birthYear
        birthMonth = birthMonth
        birthDay = birthDay
    elif birthYear<30 and (birthMonth<33 and birthMonth>20) and birthDay<32:
        birthYear = 2000 + birthYear
        birthMonth = abs(birthMonth - 20)
        birthDay = birthDay
    else:
        #print('wrong datetime 2 - else')
        birthYear = 1200
        birthMonth = 1
        birthDay = 1
    
    #month date fixer
    if birthMonth>12 or birthMonth<1:
        birthMonth=1
    if birthDay>31 or birthDay<1:
        birthDay=1
    #print('                         : ', i)

    #birthdate calculator
    birthYear = int(birthYear)
    birthMonth = int(birthMonth)
    birthDay = int(birthDay)
    
    birthYear = str(birthYear)
    birthMonth = str(birthMonth)
    birthDay = str(birthDay)

    date_str  = birthYear + "-" + birthMonth + "-" + birthDay
    #print("birth_date: ", date_str)
    date_format = '%Y-%m-%d'
    birthdate = datetime.strptime(date_str, date_format)
    age = relativedelta(now, birthdate).years


    if gender % 2 == 0:
        gender = "female"
    else:
        gender = "male"

    #print(birthYearColumn,birthMonthColumn,birthDayColumn, birthColumn, ageColumn)
    print("single register number extractor - done\n", "input: ", text, "\nbirthplace:",birthplace, "\nbirthYear:", birthYear, "\nbirthMonth:", birthMonth, "\nbirthDay:", birthDay, "\nbirthdate:", birthdate, "\nage:", age, "\ngender:", gender)

    return birthplace, birthYear,birthMonth,birthDay, birthdate, age, gender
    

## test for mongol_register_parser function ----------------------------
# #loop_mode on cpu or gpu
# loop_mode="cpu"

your_csv_file_name='ordered_merged_result.csv'
register_number_column = "reg_number"
#df = mongol_register_parser(your_csv_file_name, register_number_column)


## test for single_register_parser function ----------------------------
text = "уд01240585"
#birthplace, birthYear,birthMonth,birthDay, birthdate, age, gender = single_register_parser(text)



