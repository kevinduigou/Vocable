#!/Library/Frameworks/Python.framework/Versions/3.2

import re
import copy
import sys
import os
import lib.easygui as easygui
import lib.dictionary as dictionary

if __name__=="__main__":
    '''
    Welcome in PythonVocable!
    This tool has been designed to allow people to enhance their vocabulary knowledge in a foreign Language
    Creator: Kevin DUIGOU. Release: 10 October 2012. Version: 1.0
    Please Select your DataBase (CSV File)
    '''
    user=None
    language=None
    dictionary_file_path=""
    for arg in sys.argv:
        print (arg)
        if re.search("-u=(.*)",arg) is not None:
            user=re.search("-u=(.*)",arg).group(1)
        elif re.search("-l=(.*)",arg) is not None:
            language=re.search("-l=(.*)",arg).group(1)
    if not  user==None and not language==None:
        if os.path.isdir(os.getcwd()+"/dictionary/"+user+"/"+language):
            for file_name in os.listdir(os.getcwd()+"/dictionary/"+user+"/"+language):
                if re.search("^[.]",file_name) is None:
                    dictionary_file_path=os.getcwd()+"/dictionary/"+user+"/"+language+"/"+file_name
                    dictionary_of_work=dictionary.dictionary()
                    dictionary_of_work.upload_dictionary(dictionary_file_path)

    __mode__=""
    while dictionary_file_path=="" and not __mode__==None:
    
        msg     = "Welcome in Vocable.\nWhat do you want to do?"
        title   = "VocablePython"
        choices = ["01-           Create a Dictionary",
        "02-           Load a Dictionary",
        "03-           Help",
        "04-           Quit"]
        __mode__   = easygui.choicebox(msg, title, choices)
        if __mode__==None:
            pass
        elif re.search("Create a Dictionary",__mode__) is not None:
            dictionary_file_path=easygui.filesavebox(default="dictionary_name.csv")
            if not dictionary_file_path== None:
               dictionary_of_work=dictionary.dictionary()
               dictionary_of_work.save(dictionary_file_path)
            else:
                dictionary_file_path=""
        elif re.search("Load a Dictionary",__mode__) is not None:
             dictionary_file_path=easygui.fileopenbox(msg="Select The Dictionary you want to use",title="Dictionary Selection")
             if not dictionary_file_path== None:
                 dictionary_of_work=dictionary.dictionary()
                 dictionary_of_work.upload_dictionary(dictionary_file_path)
             else:
                dictionary_file_path=""
        elif re.search("Help",__mode__) is not None:
            dictionary_of_work=dictionary.dictionary()
            dictionary_of_work.help()
        elif re.search("Quit",__mode__) is not None:
            __mode__=None
    
    __number_of_word_to_learn_by_serie__=20
    __day_in_advance__=0
    while not __mode__==None:
        
        #dictionary_of_work.upload_dictionary(dictionary_file_path)
        msg     = "What do you want to do?\nWith the Current Dictionary: "+dictionary_file_path
        title   = "Vocable"
        choices = [
        "00-           Learn",
        "11-           Add Words",
        "12-           Delete Words",
        "13-           Modify Words",
        "21-           Modify Configuration",
        "22-           Get Statistic",
        "31-           Create a Dictionary",
        "32-           Load an other Dictionary",
        "33-           ReLoad this Dictionary",
        "40-           Help",
        "50-           Quit"]
        __mode__   = easygui.choicebox(msg, title, choices)

        
        
        if __mode__==None:
            pass
        elif re.search("Learn",__mode__) is not None:
            dictionary_of_work.create_new_interogation(
                list=[],
                number_of_word_to_learn=__number_of_word_to_learn_by_serie__,
                day_in_advance=__day_in_advance__,
                mode="marathon")
        elif re.search("Add Words",__mode__) is not None:
            dictionary_of_work.add_word()
        elif re.search("Delete Words",__mode__) is not None:
            dictionary_of_work.del_word()
        elif re.search("Modify Words",__mode__) is not None:
            dictionary_of_work.modify_word()
        elif re.search("Modify Configuration",__mode__) is not None:
            config_dict=easygui.multenterbox(msg='Configuation', title='Configuration Box', 
            fields=('Number of word by interogation',"Number of day in advance"), values=(str(__number_of_word_to_learn_by_serie__),str(__day_in_advance__)))
            if not config_dict==None:
                __number_of_word_to_learn_by_serie__=int(config_dict[0])

                __day_in_advance__=int(config_dict[1])
                
        elif re.search("Get Statistic",__mode__) is not None:
            dictionary_of_work.stat_display()
        elif re.search("Create a Dictionary",__mode__) is not None:
            old_dictionary_file_path=copy.copy(dictionary_file_path)
            dictionary_file_path=easygui.filesavebox(default="dictionary_name.csv")
            if not dictionary_file_path==None:
                dictionary_of_work=dictionary.dictionary()
                dictionary_of_work.save(dictionary_file_path)
            else:
                dictionary_file_path=old_dictionary_file_path
        elif re.search("ReLoad this Dictionary",__mode__) is not None:
            dictionary_of_work.upload_dictionary(dictionary_file_path)
        elif re.search("Load an other Dictionary",__mode__) is not None:
            old_dictionary_file_path=copy.copy(dictionary_file_path)
            dictionary_file_path=easygui.fileopenbox(msg="Select The Dictionary you want to use",title="Dictionary Selection")
            if not dictionary_file_path==None:
                dictionary_of_work=dictionary.dictionary()
                dictionary_of_work.upload_dictionary(dictionary_file_path)
            else:
                dictionary_file_path=old_dictionary_file_path
        elif re.search("Help",__mode__) is not None:
            dictionary_of_work.help()
        elif re.search("Quit",__mode__) is not None:
            __mode__=None
        
        
        #time.sleep(#1)
        dictionary_of_work.save(dictionary_file_path)



