# *-* coding: iso-8859-1 *-*

import datetime
import os
import csv
import pprint
import re
import sys
import copy
import random
import time
import math
import lib.easygui as easygui
import lib.fibonacci as fibonacci

'''
Welcome in PythonVocable!\n
This tool has been designed to allow people to enhance their vocabulary a foreign Language using the FlashCards and the LEITNER Method
Creator: Kevin DUIGOU. Release: 19 November 2012. Version: 2.0

### Flash Card Methods
A flashcard or flash card is a set of cards bearing information,
as words or numbers, on either or both sides, used in classroom drills or in private study. 
One writes a question on a card and an answer overleaf. 
Flashcards can bear vocabulary, historical dates, 
formulas or any subject matter that can be learned via a question and answer format. 
Flashcards are widely used as a learning drill to aid memorization by way of spaced repetition.

### Leitner Methods
The Leitner system is a widely used method to efficiently use flashcards that was proposed 
by the German science journalist Sebastian Leitner in the 1970s. 
It is a simple implementation of the principle of spaced repetition, 
where cards are reviewed at increasing interval.

In this method flashcards are sorted into groups according to how well you know each one
in the Leitner's learning box. This is how it works: you try to recall the solution written on a flashcard.
If you succeed, you send the card to the next group. 
But if you fail, you send it back to the first group. 
Each succeeding group has a longer period of time before you are required to revisit the cards.
'''
class dictionary ():
    '''
    A Dictionary is an OBJECT which allows to store Words and their associations or definitions.
    For each words their is also some Stat which allow knowing how the word is known by the User
    '''
    def __init__(self):
        '''
        Iniatilsation of the OBJECT
        '''
        self.__content={}
        '''
        Column associated to a word:
        Word: The word himself
        Definition/Translation/Association: Definition, Translation orAssociation
        Group: Number of time where the Word has been given good without Errors
        Last Interogation Date: The Date of the Last Interogation
        Number of Days since the last interogation: Number of Days since the Last interogation
        '''
        self.__column=["Word","Definition/Translation/Association","Group","Last Interogation Date",
        "Number of Days since the last interogation","Number of Days before the next interogation"]
        
        self.__uploaded_dictionary_file_path=""
        
    def get_content(self):
        '''
        Return a Dictionary which is the Content of the Dictionary
        '''
        return self.__content

    def add_word(self):
        '''
        Method which Allow adding a word in the dictionary by a GUI
        '''
        word_input=easygui.multenterbox(msg='Add Word', title='Add Word',fields=('Word',"Definition/Translation/Association"), values=("Bonjour","Guten Tag"))
        
        if not word_input==None:
            word=word_input[0]
            translation=word_input[1]
            Group=0
            Last_Interogation_Date=None
            Time_since_the_last_interogation=None
            Time_before_the_next_interogation=0

            self.__content[word]={"Word":word,"Definition/Translation/Association":translation,"Group":Group,
                                  "Last Interogation Date":Last_Interogation_Date,
                                  "Number of Days since the last interogation":Time_since_the_last_interogation,
                                  "Number of Days before the next interogation":Time_before_the_next_interogation}
            self.save(self.__uploaded_dictionary_file_path)
            msg   = "We have add the word: "+word+" (Translation: "+translation+") in the dictionry"
            choices = ["Add Word Again","Main Menu","Cancel"]
            reply=easygui.buttonbox(msg,choices=choices)
        else:
            reply="Main Menu"
        if reply=="Add Word Again":
            self.add_word()
        elif reply=="Cancel":
            del  self.__content[word]
        else :
            pass


    def del_word(self):
        choices_list=[]
        for word in self.__content.keys():
            choices_list.append(word)
        if len(choices_list)> 0:
            word_to_delete=easygui.multchoicebox(msg='Pick all the item that you want to delete', title='Delete Words', choices=choices_list)
        if not word_to_delete==None:
            if len(word_to_delete)>0:
                for word in word_to_delete:
                    del self.__content[word]

    def modify_word(self,word_to_change=None):
        
        if word_to_change==None:
            choices_list=[]
            for word in self.__content.keys():
                choices_list.append(word)
            if len(choices_list)>0:
                word_to_change=easygui.choicebox(msg='Pick the item that you want to change', title='Change a Word', choices=choices_list)
        
        if not word_to_change==None:
            previous_translation=self.__content[word_to_change]["Definition/Translation/Association"]
            previous_group=str(self.__content[word_to_change]["Group"])
            input_modif=easygui.multenterbox(msg='Enter the new definition for the word: '+word_to_change,fields=("Word","Translation","Group"),values=(word_to_change,str(previous_translation),previous_group))
            if not input_modif==None:
                if input_modif[0]==word_to_change:
                    self.__content[word_to_change]["Definition/Translation/Association"]=input_modif[1]
                    self.__content[word_to_change]["Group"]=int(input_modif[2])
                else :
                    del self.__content[word_to_change]
                    word=input_modif[0]
                    translation=input_modif[1]
                    """Group=int(input_modif[2])"""
                    Group=0
                    Last_Interogation_Date=None
                    Time_since_the_last_interogation=None
                    Time_before_the_next_interogation=0

                    self.__content[word]={"Word":word,"Definition/Translation/Association":translation,"Group":Group,
                                          "Last Interogation Date":Last_Interogation_Date,
                                          "Number of Days since the last interogation":Time_since_the_last_interogation,
                                          "Number of Days before the next interogation":Time_before_the_next_interogation}

    def upload_dictionary(self,file_path):
        '''
        Method which Allow to Upload Data from file (path of the file egal to file_path)
        '''
        self.__uploaded_dictionary_file_path=file_path
        
        '''
        iso-8859-1 must be used to read the file to allow reading of special charecters
        '''
        file=open(self.__uploaded_dictionary_file_path,mode="r",encoding="iso-8859-1")
        csv_file=csv.reader(file,delimiter=";")
        line=0
        col_dict={}
        pattern_date=re.compile("([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})")
        for row in csv_file:
            #print (row)
            if line==0:
                '''
                The first LINE is the Header Line which must be the Same for each File
                '''
                for pos,elt in enumerate(row):
                    col_dict[elt]=pos
                line+=1
            else:
                if not row[col_dict["Word"]]=="":
                    self.__content[row[col_dict["Word"]]]={}
                    for col in self.__column:
                        self.__content[row[col_dict["Word"]]][col]=row[col_dict[col]]

                    for col, pos in col_dict.items():
                        '''
                        Special Treatment for each Column
                        '''
                        if col=="Last Interogation Date":
                            if not row[col_dict[col]]=="":
                                pattern_date.search(row[col_dict[col]])
                                year=int(pattern_date.search(row[col_dict[col]]).group(1))
                                month=int(pattern_date.search(row[col_dict[col]]).group(2))
                                day=int(pattern_date.search(row[col_dict[col]]).group(3))
                                hour=int(pattern_date.search(row[col_dict[col]]).group(4))
                                minute=int(pattern_date.search(row[col_dict[col]]).group(5))
                                second=int(pattern_date.search(row[col_dict[col]]).group(6))
                                Last_Interogation_Date=datetime.datetime(year,month,day,hour,minute,second)
                                self.__content[row[col_dict["Word"]]][col]=Last_Interogation_Date
                            else:
                                self.__content[row[col_dict["Word"]]][col]=None
                        
                        elif col=="Group":
                            if row[col_dict[col]]=="":
                                self.__content[row[col_dict["Word"]]][col]=0
                            else:
                                self.__content[row[col_dict["Word"]]][col]=int(row[col_dict[col]])
                        elif col=="Number of Days before the next interogation":
                            if row[col_dict[col]]=="":
                                self.__content[row[col_dict["Word"]]][col]=0
                            else:
                                self.__content[row[col_dict["Word"]]][col]=int(row[col_dict[col]])
                        
                
                    if self.__content[row[col_dict["Word"]]]["Last Interogation Date"]==None:
                        self.__content[row[col_dict["Word"]]]["Number of Days since the last interogation"]=None
                    else:
                        delta_time=datetime.datetime.now()-self.__content[row[col_dict["Word"]]]["Last Interogation Date"]
                        self.__content[row[col_dict["Word"]]]["Number of Days since the last interogation"]=delta_time.days
                    
                    line+=1
        file.close()
    def save(self,dictionary_file_path,option=None):
        '''
        This function allows saving a dictionary and the modification associated
        '''
        if option=="Quizlet":
            column=["Word","Definition/Translation/Association"]
        else:
            column=copy.copy(self.__column)

        self.__uploaded_dictionary_file_path=dictionary_file_path
        path=os.path.split(dictionary_file_path)[0]
        if not os.path.isdir(path):
            os.makedirs(path)
        
        file=open(dictionary_file_path,mode="w",encoding="iso-8859-1")
        
        if option=="Quizlet":
            pass
        else :

            file.write(";".join(column))
            file.write("\n")
        
        
        for value in self.__content.values():
            line=[]
            for col in column :
                if col=="Number of Days since the last interogation" and not value["Last Interogation Date"]==None:
                    delta_time=datetime.datetime.now()-value["Last Interogation Date"]
                    line.append(str(delta_time.days))
                elif col=="Last Interogation Date" and not value["Last Interogation Date"]==None:
                    line.append(str(value[col].isoformat()))
                elif col=="Number of Days before the next interogation" and not value["Number of Days since the last interogation"]==None:
                    if fibonacci.fib(int(value["Group"]))-int(value["Number of Days since the last interogation"]) <=0:
                        line.append("0")
                    else:
                        line.append(str(fibonacci.fib(int(value["Group"]))-int(value["Number of Days since the last interogation"])))
                elif value[col]==None:
                    line.append("")
                else:
                    line.append(str(value[col]))
            
            if not value["Word"]=="":
                 line.append("\n")
                 file.write(";".join(line))
        file.close()
        
    def please_translate(self,french_word,mode=""):

        translation_in=easygui.enterbox(msg=french_word,title="Flash Card Recto")
        if translation_in==None or translation_in=="-q":
            return None
        substitution_list=[",","(",")"," ",";","¨"]
        correct_pattern_str=copy.copy(self.__content[french_word]["Definition/Translation/Association"])
        
        for substitution in substitution_list:
            correct_pattern_str=correct_pattern_str.replace(substitution,".*")
        
        correct_pattern=re.compile(correct_pattern_str,re.IGNORECASE)

        if correct_pattern.search(translation_in) is not None:
            choices = ["Continue","Modify the word"]
            reply=easygui.buttonbox(msg="Good Answer",title="Good Answer",choices=choices)
            
            if reply=="Modify the word":
                self.modify_word(french_word)
                return None

            self.__content[french_word]["Group"]+=1
            self.__content[french_word]["Last Interogation Date"]=datetime.datetime.now()
            self.__content[french_word]["Number of Days since the last interogation"]=0
            value=copy.copy(self.__content[french_word])
            self.__content[french_word]["Number of Days before the next interogation"]=fibonacci.fib(int(value["Group"])-int(value["Number of Days since the last interogation"]))
            
            self.save(self.__uploaded_dictionary_file_path)
            return 1
        else:
            last_group=self.__content[french_word]["Group"]
            if self.__content[french_word]["Group"]==0:
                pass
            elif self.__content[french_word]["Group"]==1:
                self.__content[french_word]["Group"]=0
            else:
                self.__content[french_word]["Group"]-=2

            self.__content[french_word]["Last Interogation Date"]=datetime.datetime.now()
            self.save(self.__uploaded_dictionary_file_path)

            request_index=0
            while correct_pattern.search(translation_in) is None:
                translation_in=easygui.enterbox(
                    msg="Correct Anwswer for\n-->"
                    +french_word+"\n           is\n-->"
                    +self.__content[french_word]["Definition/Translation/Association"]+
                    "\n------------------------------\nYour Anwswer was\n-->"+translation_in+
                    "\n------------------------------\nWrite the GOOD Answer or 'iwr' (I was right) or 'c' (continue)",
                    title="Wrong Answer")
                request_index+=1
                if translation_in==None or translation_in=="-q":
                    return None
                if (translation_in=="I was right" or translation_in=="iwr") and request_index==1:
                    self.__content[french_word]["Group"]==last_group+1
                    self.__content[french_word]["Last Interogation Date"]=datetime.datetime.now()
                    self.__content[french_word]["Number of Days since the last interogation"]=0
                    value=copy.copy(self.__content[french_word])
                    self.__content[french_word]["Number of Days before the next interogation"]=fibonacci.fib(int(value["Group"])-int(value["Number of Days since the last interogation"]))
                    self.save(self.__uploaded_dictionary_file_path)
                    return 1 
                if translation_in=="c":
                    translation_in=self.__content[french_word]["Definition/Translation/Association"]
                    return 0
            
            choices = ["Continue","Modify the word"]
            reply=easygui.buttonbox(msg="Good Answer",title="Flash Card Recto",choices=choices)
            
            if reply=="Modify the word":
                self.modify_word(french_word)
                return None
            return 0
        
    def create_new_interogation (self,list,number_of_word_to_learn,day_in_advance,mode=""):
        '''
        Create an interogation of words
        '''
        
        total_point=0
        number_of_word=0
        vocabulary_list=list
        
        if len(list)==0 or mode=="marathon":
            for word,value in self.__content.items():
                if len(vocabulary_list)<number_of_word_to_learn:
                    if word in vocabulary_list:
                        pass
                    elif value["Group"]==0:
                        vocabulary_list.append(word)
                    elif fibonacci.fib(int(value["Group"]))-int(value["Number of Days since the last interogation"])-int(day_in_advance)<=0:
                        vocabulary_list.append(word)
                else :
                    break;
    
        
        unknown_vocabulary=[]
        known_vocabulary=[]
        

        random.shuffle(vocabulary_list)
        #pprint.pprint(vocabulary_list)
        for french_word in vocabulary_list:
        
            value=self.__content[french_word]

            number_of_word+=1
            point=self.please_translate(french_word,mode)
            if point==None:
                return;
            elif point==0:
                unknown_vocabulary.append(french_word)
            else:
                known_vocabulary.append(french_word)
            total_point+=point
      
        self.save(self.__uploaded_dictionary_file_path)
        if len(unknown_vocabulary)==0 and len(known_vocabulary)==0:
            easygui.msgbox(msg="No new Vocabulary for today",title="Learn")
            return ;
        
        if not total_point==number_of_word:
            self.create_new_interogation(unknown_vocabulary,number_of_word_to_learn=number_of_word_to_learn,day_in_advance=day_in_advance,mode=mode)
        
    def stat_display (self):
        number_total_of_word=len(self.__content.keys())
        Group_stat={}
        Group_list=[]
        time_before_interogation={}
        time_before_interogation_list=[]


        average_group=0

        text_to_display="##########   STAT   ##########\n"
        text_to_display+="Number of Word in the Dictionary: "+str(number_total_of_word)+"\n"

        for french_word, word_value in self.__content.items():
            Group=int(word_value["Group"])
            average_group+=Group
            if not int(word_value["Group"])==0:
                days_before_interogation=fibonacci.fib(int(word_value["Group"]))-int(word_value["Number of Days since the last interogation"])
            else :
                days_before_interogation=0
            if days_before_interogation<0:
                days_before_interogation=0

            days_before_interogation_list=[]

            if not Group in Group_stat.keys():
                Group_stat[Group]=1
                Group_list.append(Group)
            else:
                Group_stat[Group]+=1
            if not days_before_interogation in time_before_interogation.keys():
                time_before_interogation[days_before_interogation]=1
                time_before_interogation_list.append(days_before_interogation)
            else:
                time_before_interogation[days_before_interogation]+=1
        
        if not number_total_of_word==0:
            average_group=average_group/number_total_of_word
            text_to_display+="Average Group: "+str(average_group)+"\n"
        

        text_to_display+="_____________________________________________\n"
        

        time_before_interogation_list.sort()
        Group_list.sort()


        for Group in Group_list:
            number_of_word=Group_stat[Group]
            text_to_display+="Per Cent of Word in Group "+str(Group)+": "+str(number_of_word*100/number_total_of_word)+"("+str(number_of_word)+" Words)"+"\n"
        text_to_display+="_____________________________________________\n"

        text_to_display+="_____________________________________________\n"
        
        for number_of_days in time_before_interogation_list:
            number_of_word=time_before_interogation[number_of_days]
            text_to_display+=str(number_of_word)+" more Words will be present in the interogation set in "+str(number_of_days)+" Days\n"
        text_to_display+="_____________________________________________\n"

        text_to_display+="##########   END STAT   ##########\n"
        easygui.textbox(title='Statistic', text=text_to_display, codebox=0)
    
    def help(self):
        text_to_display='''Welcome in PythonVocable!\n
        This tool has been designed to allow people to enhance their vocabulary a foreign Language
        using the FlashCards and the LEITNER Method
        Creator: Kevin DUIGOU. Release: 19 November 2012. Version: 2.0\n\n\n'''
        text_to_display+='''### Flash Card ###\n        A flashcard or flash card is a set of cards bearing information,
        as words or numbers, on either or both sides, used in classroom drills or in private study. 
        One writes a question on a card and an answer overleaf. 
        Flashcards can bear vocabulary, historical dates, 
        formulas or any subject matter that can be learned via a question and answer format. 
        Flashcards are widely used as a learning drill to aid memorization by way of spaced repetition.\n\n\n'''
        text_to_display+='''### The LEITNER Method ###\n        The Leitner system is a widely used method to efficiently use flashcards that was proposed 
        by the German science journalist Sebastian Leitner in the 1970s.
        It is a simple implementation of the principle of spaced repetition,
        where cards are reviewed at increasing interval.

        In this method flashcards are sorted into groups according to how well you know each one
        in the Leitner's learning box. This is how it works: you try to recall the solution written on a flashcard.
        If you succeed, you send the card to the next group.
        But if you fail, you send it back to the first group.
        Each succeeding group has a longer period of time before you are required to revisit the cards.'''
        easygui.textbox(title='HELP', text=text_to_display, codebox=0)

