
log_file = "d:\Python\plane_20180122.log"
#log file location:d:\Python\plane_20180122.log
#log_file = raw_input("pls input plane log file:")
#print "your input plane log file is:"+log_file

search_index = raw_input("pls input search index:")

import re

#search_index format reg.
search_index_reg='^(([0]?)|([1-9]+[0-9]*))$'
while 1:
    if search_index == '':
        search_index = raw_input("search index can't be empty, pls re-input search index:")
    elif re.search(search_index_reg,search_index):
        print "your input searched index is:"+search_index
        break
    else:
        search_index = raw_input("incorrect format, pls re-input search index:")

#Set search row num value
search_row_num = int(search_index)+1

#Before read the log file, check the log file's total records number, if total records < search_row_num, can't find the searched row.
total_records_of_log_file = 0
thefile = open(log_file,'rb')
while True:
    buffer = thefile.read(1024 * 8192)
    if not buffer:
        break
    total_records_of_log_file += buffer.count('\n')  
thefile.close()
print "total_records_of_log_file=",total_records_of_log_file

if search_row_num > total_records_of_log_file:
    print "Can't find ", search_index
    exit(0)
else:
    print "searched row number less than file's total records number, will open the log file and search..."


#Row number of the log file.
row_num = 0

#The first column's format reg.
column_1_reg = '^[a-zA-Z0-9]+$'

#Except the first column, other's column's format reg.
column_others_reg = '^(([0]?)|([-]?[1-9]+[0-9]*))$'

#Break flag
break_flag = "NO"

#Current row list
current_row_list = []

#Previous row list
previous_row_list = []

#Current row x y z and x' y' z'
current_row_x = 0
current_row_y = 0
current_row_z = 0
current_row_offset_x = 0
current_row_offset_y = 0
current_row_offset_z = 0


#Previous x y z and x' y' z'
previous_row_x = 0
previous_row_y = 0
previous_row_z = 0
previous_row_offset_x = 0
previous_row_offset_y = 0
previous_row_offset_z = 0


#Start read the log file, check the column's format.
#for line in open(log_file,'r'):
fo = open(log_file,'r')
for line in fo:

    row_num = row_num + 1
    print "row number is: ", row_num
    
    #print line
    current_row_list = line.split(' ')
    previous_row_list = current_row_list
    #print list_line
    #print list_line[0]

    #Get the column's number for each row.
    list_line_size = len(current_row_list)
    print "row ",row_num, ", column's number is: ", list_line_size


    #Check the column's number for each row.
    if row_num == 1:
        if list_line_size != 4:
            print "the first row, column's number is error."
            break_flag = "YES"
            #break
        else:
            print "the first row, column's number is correct."
    else:
        if list_line_size != 7:
            print "for row ", row_num, " , column's number is error."
            break_flag = "YES"
            #break
        else:
            print "for row ", row_num, " , column's number is correct."

    #Check whether need break current loop or not, after checked the column's number of current row, if no need break the loop.
    if break_flag == "NO":

        #Check the column's format for each row.
        for i in range(list_line_size):
            if i == 0:#For the first column format checking
                if re.search(column_1_reg,current_row_list[i]):
                    print 'for row ',row_num, ' column ', i, ' format checked ok!'
                else:
                    print 'for row ',row_num, ' column ', i, ' format checked ERROR!'
                    break_flag = "YES"
                    #break
            else:#For others column format checking
                if re.search(column_others_reg,current_row_list[i]):
                    print 'for row ',row_num, ' column ', i, ' format checked ok!'
                else:
                    print 'for row ',row_num, ' column ', i, ' format checked ERROR!'
                    break_flag = "YES"
                    #break
    else:
        pass
    

    #Check whether need break current loop or not, after checked the column's format of current row, if no need break the loop.
    if break_flag == "NO":
        
        #Check current row XYZ whether match with previous row XYZ+X'Y'Z' or not.
        if row_num == 1:#For the first row, no need check X Y Z matched or not.
            current_row_offset_x = 0
            current_row_offset_y = 0
            current_row_offset_z = 0
        elif row_num == 2:#For second row, set previous row's X' Y' Z' =(0,0,0)
            previous_row_offset_x = 0
            previous_row_offset_y = 0
            previous_row_offset_z = 0
        else:#For others rows, set previous row's X' Y' Z' = previous column 4,5,6
            previous_row_offset_x = int(previous_row_list[4])
            previous_row_offset_y = int(previous_row_list[5])
            previous_row_offset_z = int(previous_row_list[6])

        #Set current row X Y Z
        current_row_x = int(current_row_list[1])
        current_row_y = int(current_row_list[2])
        current_row_z = int(current_row_list[3])
        if row_num != 1:
            current_row_offset_x = int(current_row_list[4])
            current_row_offset_y = int(current_row_list[5])
            current_row_offset_z = int(current_row_list[6])
        else:
            current_row_offset_x = 0
            current_row_offset_y = 0
            current_row_offset_z = 0

        #Set previous X Y Z
        previous_row_x = int(previous_row_list[1])
        previous_row_y = int(previous_row_list[2])
        previous_row_z = int(previous_row_list[3])

        #Caculator XYZ=(previous)XYZ + (previous)X'Y'Z'
        temp_x = previous_row_x + previous_row_offset_x
        temp_y = previous_row_y + previous_row_offset_y
        temp_z = previous_row_z + previous_row_offset_z

        #Current row xyz not matched with previous, break the loop.
        if (temp_x != current_row_x) or (temp_y != current_row_y) or (temp_z != current_row_z):
            print "error, current row not matched with previous row!"
            break_flag == "YES"
            #break
        else:
            print "ok, current row not matched with previous row."
    else:
        pass


    #After above checking, need break current loop.
    if break_flag == "YES":
        if search_row_num >= row_num:
            print "Error: ", search_index
            break
        elif search_row_num < row_num:
            print current_row_list[0]," ",search_index," ",current_row_x + current_row_offset_x, " ",current_row_y + current_row_offset_y, " ",current_row_z + current_row_offset_z
        else:
            pass
    else:# No need break current loop.
        if search_row_num == row_num:#Get the searched row, can exit the loop now.
            print current_row_list[0]," ",search_index," ",current_row_x + current_row_offset_x, " ",current_row_y + current_row_offset_y, " ",current_row_z + current_row_offset_z
            break
        elif search_row_num > row_num:#If still not searched the target row, continue read the log file.
            continue
        else:
            pass

#Close the file
fo.close()

