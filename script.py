from itertools import zip_longest    
def sum_of_stat(list1,list2):
        return [a+b for a,b in zip_longest(list1,list2,fillvalue=0)]

def get_stat_from_str(str):#Извлечение статистики из строки
    if str.rfind("Statistics:")!=-1:
        numb_str=str[str.rfind("Statistics:")+len("Statistics:"):len(str)]
        if numb_str.isdigit:
            stats=[int(x) for x in numb_str.split()]
            return stats
    else:
        return False

import os
class Log_file:
    def __init__(self,file_path):
        try:
                file=open(file_path,'r')
        except FileNotFoundError:
                print("Log file {:} does not found".format(file_path))
        self.stat=[]
        for line in file:
                if get_stat_from_str(line)!=False:
                    self.stat=sum_of_stat(self.stat,get_stat_from_str(line))
        self.name=os.path.splitext(os.path.basename(file_path))[0]
        file.close()
        
    def output(self,stdout):
        stdout.write("|{:^8}|".format(self.name))
        str_stat=map(str,self.stat)
        for x in str_stat:
                stdout.write(("{:>8}|".format(x)))
        stdout.write("\n")
        
def get_stat0_for_sort(Log_file):
        return (Log_file.stat)[0]
    
class Main_stat:
    def __init__(self,main_path):
        self.all_stat=[]
        for root, dirs, files in os.walk(main_path):
            for file in files:
                if file.endswith(".log"):
                    file_path=os.path.join(root, file)
                    check_for_name_coincedence=True
                    for x in self.all_stat:#Если один и тот же лог встречается больше одного раза, его статистика суммируется
                        if x.name!=((Log_file(file_path)).name):
                            check_for_name_coincedence=True
                        else:
                            check_for_name_coincedence=False
                            x.stat=sum_of_stat(x.stat,(Log_file(file_path)).stat)
                            break
                    if check_for_name_coincedence==True:
                        self.all_stat.append(Log_file(file_path))                

    def output(self):
        if self.all_stat:
            stdout=open('stdout.txt','w')
            self.all_stat=sorted(self.all_stat,key=get_stat0_for_sort,reverse=True)
            max_stat_number = max(len(log.stat) for log in self.all_stat)
            stdout.write("{:-^{i}} \n".format("",i=11*max_stat_number))
            stdout.write("|{:^8}|".format("Name"))
            for stat_number in range(max_stat_number):
                stdout.write("Stat {:<2} |".format(stat_number))
            stdout.write("\n")
            stdout.write("{:-^{i}} \n".format("",i=11*max_stat_number))
            for log in self.all_stat:
                    log.output(stdout)
            stdout.write("{:-^{i}} \n".format("",i=11*max_stat_number))
            stdout.close
        else:
            stdout=open('stdout.txt','w')
            stdout.write("Log files with statistics not found")
            stdout.close

def main(path):
    if os.path.isdir(path):
        Statistic=Main_stat(path)
        Statistic.output()
        
    else:
        print("Directory does not exists")


general_path=input()
main(general_path)
