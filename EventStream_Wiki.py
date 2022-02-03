import time 
import json
from sseclient import SSEClient as EventSource

url = 'https://stream.wikimedia.org/v2/stream/revision-create'

dic={}            #this stores domain as key and its number of pages updated as value        
dic2={}           #this stores users as key and their edit count as the updated value

timer = 0         #for keeping tab on time
total_cnt_pgs=0   #this stores total pages updated

start=-1
end=1

for event in EventSource(url):
    if event.event == 'message':
        time.sleep(1)
        timer=timer+1  
        try:
            change = json.loads(event.data)
        except ValueError:
            pass
        else:
            #key doesnt exist i.e. change made to that domain for 1st time
            if(change["meta"]["domain"]) not in dic:
             dic[change["meta"]["domain"]]=1
            else:
             dic[change["meta"]["domain"]]=dic[change["meta"]["domain"]]+1
            total_cnt_pgs=total_cnt_pgs+1
            
            if((change["performer"]["user_is_bot"]==False) and (change["meta"]["domain"]=="en.wikipedia.org")):
             if((change["performer"]["user_text"]) not in dic2):
              dic2[change["performer"]["user_text"]]=change["performer"]["user_edit_count"]
             else:
              dic2[change["performer"]["user_text"]]=max(dic2[change["performer"]["user_text"]],change["performer"]["user_edit_count"])

        #because we have to print after 60 seconds
        if(timer>60):

         #updating the endpoints for printing
         start=start+1
         end=end+1

         print("Printing data from "+str(start)+"-"+str(end)+" mins")
         print("Total number of Wikipedia Domains Updated: "+str(total_cnt_pgs))
         for i in dic:
          print(str(i)+": "+str(dic[i])+" pages updated")
         print()
         print("Users who made changes to en.wikipedia.org with their max edit count:")
         if(len(dic2)==0):
          print("Nil")
         else:
          for i in dic2:
           print(str(i)+": "+str(dic2[i]))
         print()
         #resetting for counting new updates in next run
         dic={}
         dic2={}
         timer=0
         total_cnt_pgs=0
