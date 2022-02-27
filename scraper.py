#Dependencies
from array import array
from operator import mod
from statistics import mode
from unicodedata import name
import praw
import os
from datetime import datetime
import time
from prawcore.exceptions import NotFound
import json


abs_path = os.path.abspath(__file__)
dir_name = os.path.dirname(abs_path)
os.chdir(dir_name)

reddit = praw.Reddit( #instance of praw reddit for API access
    client_id = 'g1newHxnqEdQYH8vN8hSLw',
    client_secret = '34WhZ0gJxY5bmnrd1OpPDocqMWV8Wg',
    password = 'Bestlangpython666',
    user_agent = 'andrew_web_scraper',
    username = 'Ok-General847',
)
reddit.read_only = True;

def UserExists(name: str): #Check if username exists
    try:
        reddit.redditor(name).id
    except NotFound:
        return False
    return True

def GetUsernameInput(): #Check if inputted username is valid
    name = input("Enter username (eg _dancingrain_): ")
    if (not UserExists(name)):
        print("\nUsername not found, try again\n")
        return GetUsernameInput()
    return name;

class UserInfo:
    id: str #user's id - short series of alphanumeric charaacters
    name: str #user's name
    cake_day: str #month/day/year
    age: str #in days
    karma_comments: str #comment karma, may be slightly off
    karma_overall: str #comment karma + post karma, may be slightly off
    moderator: str #user is a subreddit moderator
    suspended: str #user is suspended from reddit
    five_most_voted_submissions: str
    five_most_voted_comments: str
    vote_distribution: str
    most_active_subs: str
    info_map: map
    
    def __init__(self, id="", name="", cake_day="", age="", karma_comments="", karma_overall="", moderator="False", suspended="False", txt_delimiter = "UserInfo_delim"):
        self.id = id
        self.name = name
        self.cake_day = cake_day
        self.age = age
        self.karma_comments = karma_comments
        self.karma_overall = karma_overall
        self.moderator = moderator
        self.suspended = suspended
        self.info_map = {"Username":self.name, "Cake Day":self.cake_day, "Age":self.age, "User Comment Karma":self.karma_comments, "User Overall Karma":self.karma_overall, "User is a moderator":self.moderator, "User is suspended":self.suspended, "User ID":self.id}
    
    def SetBasicInfo(self):
        #Username
        self.name = user_as_redditor.name
        #Is user suspended
        self.suspended = "True"
        shadowbanned = True
        try:
            self.user_as_redditor.is_suspended
        except AttributeError:
            self.suspended = "False"
            shadowbanned = False
        if not shadowbanned: 
            #ID
            self.id = user_as_redditor.id
            #UTC
            self.cake_day = datetime.utcfromtimestamp(int(user_as_redditor.created_utc)).strftime("%m/%d/%Y, %H:%M:%S") + " UTC"
            #Days
            self.age = str(int((time.time()-user_as_redditor.created_utc)/86400)) + " days"
            #PRAW Karma may vary from actual
            self.karma_comments = str(user_as_redditor.comment_karma) + " karma"
            self.karma_overall = str(user_as_redditor.link_karma + user_as_redditor.comment_karma) + " karma"
            #Is user a moderator
            self.moderator = "False";
            if (user_as_redditor.is_mod):
                self.moderator = "True";
            self.info_map = {"Username":self.name, "Cake Day":self.cake_day, "Age":self.age, "User Comment Karma":self.karma_comments, "User Overall Karma":self.karma_overall, "User is a moderator":self.moderator, "User is suspended":self.suspended, "User ID":self.id}
            
    def SetUserInfo(self, data:map):
        for i,(k,v) in enumerate(data.items()):
            self.info_map[k] = v
        
            
    def IsSuspended(self):
        return self.suspended == "True"
    
    def ConvertBasicInfoToTxt(self):
        with open("scraper_output.json", "r") as f:   
            feed = json.load(f) 
        with open("scraper_output.json", "w") as outfile:
            feed.append({"UserInfo":self.info_map})
            json.dump(list(feed), outfile, indent=2)
        
    def PrintBasicInfo(self):
        for i,(k,v) in enumerate(self.info_map.items()):
            print(str(k) + ": " + str(v))
class TopFiveVotedSubmissionsData:
    descriptive_header: str
    info_list_of_maps: list
    
    def __init__(self, descriptive_header="\nTop 5 most upvoted posts (Out of last 99 posts):\n", txt_delimiter = "TopFiveVotedSubmissionsData_delim"):
        self.descriptive_header = descriptive_header
        self.info_list_of_maps = []
        
    def FindFiveMostVotedSubmissions(self):
        sorted_submissions = sorted(user_submissions_list,key=lambda x:x.score, reverse=True)
        idx = 0
        for submission in sorted_submissions:
            if idx < 5 and idx < len(sorted_submissions):
                self.info_list_of_maps.append({"Rank":str(idx + 1), "Score":str(submission.score),"Time:":str(datetime.utcfromtimestamp(int(submission.created_utc)).strftime("%m/%d/%Y, %H:%M:%S")), "Comments":str(submission.num_comments), "Title":str(submission.title)})
            idx+=1
            
    def PrintFiveMostVotedSubmissions(self):
        print(self.descriptive_header)
        for idx in range(0,len(self.info_list_of_maps)):
            to_print = ""
            for idx1,(k,v) in enumerate(self.info_list_of_maps[idx].items()):
                to_print += str(k) + ": " + str(v)
                if idx1 < len(self.info_list_of_maps[idx]):
                    to_print += " | "
            print(to_print)
            
    def ConvertFiveMostVotedSubmissionsToTxt(self):
        with open("scraper_output.json", "r") as f:   
            feed = json.load(f) 
        with open("scraper_output.json", "w") as outfile:
            info_map = {}
            for i in range(0,len(self.info_list_of_maps)):
                submission_map = {}
                for idx, (k,v) in enumerate(self.info_list_of_maps[i].items()):
                    submission_map[k] = v
                info_map.update({i+1:submission_map.copy()})
            to_append = {"FiveMostVotedSubmissions":info_map}
            feed.append(to_append)
            json.dump(list(feed), outfile, indent=2)
            
    
    def SetFiveMostVotedSubmissionsFromJsonMap(self, data:map):
        for i,(k,v) in enumerate(data.items()):
            self.info_list_of_maps.append({k:v})
class TopFiveVotedCommentsData:
    descriptive_header: str
    info_list_of_maps: list
    def __init__(self, descriptive_header="\nTop 5 most upvoted comments (Out of last 99 posts):\n", txt_delimiter = "TopFiveVotedCommentsData_delim"):
        self.descriptive_header = descriptive_header
        self.info_list_of_maps = []
        
    def FindFiveMostVotedComments(self):
        sorted_comments = sorted(user_comments_list,key=lambda x:x.score, reverse=True)
        idx = 0
        for comments in sorted_comments:
            if idx < 5 and idx < len(sorted_comments):
                self.info_list_of_maps.append({"Rank":str(idx+1),"Score":str(comments.score), "Time":str(datetime.utcfromtimestamp(int(comments.created_utc)).strftime("%m/%d/%Y, %H:%M:%S")), "Replies":str(len(comments.replies)), "Body":(comments.body.replace("\n","")[0:35]+"...")})
            idx+=1
        
    def PrintFiveMostVotedComments(self):
        print(self.descriptive_header)
        for idx in range(0,len(self.info_list_of_maps)):
            to_print = ""
            for idx1,(k,v) in enumerate(self.info_list_of_maps[idx].items()):
                to_print += str(k) + ": " + str(v)
                if idx1 < len(self.info_list_of_maps[idx]):
                    to_print += " | "
            print(to_print)
            
    def ConvertFiveMostVotedCommentsToTxt(self):
        with open("scraper_output.json", "r") as f:   
            feed = json.load(f) 
        with open("scraper_output.json", "w") as outfile:
            info_map = {}
            for i in range(0,len(self.info_list_of_maps)):
                submission_map = {}
                for idx, (k,v) in enumerate(self.info_list_of_maps[i].items()):
                    submission_map[k] = v
                info_map.update({i+1:submission_map.copy()})
            to_append = {"FiveMostVotedComments":info_map}
            feed.append(to_append)
            json.dump(list(feed), outfile, indent=2)
            
    def SetFiveMostVotedCommentsFromJsonMap(self, data:map):
        for i,(k,v) in enumerate(data.items()):
            self.info_list_of_maps.append({k:v})
class VoteDistribution:
    descriptive_header: str
    info_list_of_maps: list
    def __init__(self, descriptive_header="\nUser's top subreddits ranked by comment/submission upvotes (Out of last 198 interactions):\n", txt_delimiter = "VoteDistribution_delim"):
        self.descriptive_header = descriptive_header
        self.info_list_of_maps = []
        
    def FindVoteDistribution(self): 
        active_subreddits_map = {}
        #combine comments and submissions into dictionary format {sub name, upvote count} to easily organize subreddits and increment their upvote counts
        for comments in user_comments_list:
            sub_name = comments.subreddit.display_name
            upvote_qty = comments.score
            if sub_name in active_subreddits_map.keys():
                active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + upvote_qty
            else:
                active_subreddits_map[sub_name] = upvote_qty
        for submissions in user_submissions_list:
            sub_name = submissions.subreddit.display_name
            upvote_qty = submissions.score
            if sub_name in active_subreddits_map.keys():
                active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + upvote_qty
            else:
                active_subreddits_map[sub_name] = upvote_qty
        #convert map back to list, then use built-in triple parameter sort method to sort subreddits by upvote count
        active_subreddits_list = []
        for i,(k, v) in enumerate(active_subreddits_map.items()):
            active_subreddits_list.append([k, v])
        descending_subreddit_by_activity = sorted(active_subreddits_list,key=lambda x:x[1], reverse=True)
        idx = 0
        #print subreddit upvote distribution in descending order
        for subreddit in descending_subreddit_by_activity:
            self.info_list_of_maps.append({"Rank":str(idx+1),"Subreddit":subreddit[0], "Vote Count":str(subreddit[1])})
            idx+=1
            
    def PrintVoteDistribution(self):
        print(self.descriptive_header)
        for idx in range(0,len(self.info_list_of_maps)):
            to_print = ""
            for idx1,(k,v) in enumerate(self.info_list_of_maps[idx].items()):
                to_print += str(k) + ": " + str(v)
                if idx1 < len(self.info_list_of_maps[idx]):
                    to_print += " | "
            print(to_print)
            
    def ConvertVoteDistributionToTxt(self):
        with open("scraper_output.json", "r") as f:   
            feed = json.load(f) 
        with open("scraper_output.json", "w") as outfile:
            info_map = {}
            for i in range(0,len(self.info_list_of_maps)):
                submission_map = {}
                for idx, (k,v) in enumerate(self.info_list_of_maps[i].items()):
                    submission_map[k] = v
                info_map.update({i+1:submission_map.copy()})
            to_append = {"VoteDistribution":info_map}
            feed.append(to_append)
            json.dump(list(feed), outfile, indent=2)
            
    def SetVoteDistributionFromJsonMap(self,data:map):
        for i,(k,v) in enumerate(data.items()):
            self.info_list_of_maps.append({k:v})
class MostActiveSubs:
    descriptive_header: str
    info_list_of_maps: list
    def __init__(self, descriptive_header="\nTop active subreddits ranked by quantity of comments and submissions (Out of last 198 interactions):\n", txt_delimiter = "MostActiveSubs_delim"):
        self.descriptive_header = descriptive_header
        self.info_list_of_maps = []
        
    def FindMostActive(self):
        active_subreddits_map = {}
        #combine comments and submissions into dictionary format {sub name, upvote count} to easily organize subreddits and increment their interaction count
        for comments in user_comments_list:
            sub_name = comments.subreddit.display_name
            if sub_name in active_subreddits_map.keys():
                active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + 1
            else:
                active_subreddits_map[sub_name] = 1
        for submissions in user_submissions_list:
            sub_name = submissions.subreddit.display_name
            if sub_name in active_subreddits_map.keys():
                active_subreddits_map[sub_name] = active_subreddits_map[sub_name] + 1
            else:
                active_subreddits_map[sub_name] = 1
        #convert map back to list, then use built-in triple parameter sort method to sort subreddits by upvote count
        active_subreddits_list = []
        for i,(k, v) in enumerate(active_subreddits_map.items()):
            active_subreddits_list.append([k, v])
        descending_subreddit_by_activity = sorted(active_subreddits_list,key=lambda x:x[1], reverse=True)
        idx = 0
        #print subreddit interactions in descending order
        for subreddit in descending_subreddit_by_activity:
            self.info_list_of_maps.append({"Rank":str(idx+1),"Subreddit":subreddit[0], "Post/Repl Count":str(subreddit[1])})
            idx+=1
    
    def PrintActiveSubs(self):
        print(self.descriptive_header)
        for idx in range(0,len(self.info_list_of_maps)):
            to_print = ""
            for idx1,(k,v) in enumerate(self.info_list_of_maps[idx].items()):
                to_print += str(k) + ": " + str(v)
                if idx1 < len(self.info_list_of_maps[idx]):
                    to_print += " | "
            print(to_print)
            
    def ConvertActiveSubsToTxt(self):
        with open("scraper_output.json", "r") as f:   
            feed = json.load(f) 
        with open("scraper_output.json", "w") as outfile:
            info_map = {}
            for i in range(0,len(self.info_list_of_maps)):
                submission_map = {}
                for idx, (k,v) in enumerate(self.info_list_of_maps[i].items()):
                    submission_map[k] = v
                info_map.update({i+1:submission_map.copy()})
            to_append = {"MostActiveSubreddits":info_map}
            feed.append(to_append)
            json.dump(list(feed), outfile, indent=2)
    
    def SetMostActiveFromJsonMap(self,data:map):
        for i,(k,v) in enumerate(data.items()):
            self.info_list_of_maps.append({k:v})
            
def GetUserFromJson(file_name:str):
    to_return = {}
    with open(file_name, mode='r') as outfile:
        data = json.load(outfile)
    for i in data:
        type = str(list(i.keys())[0])
        data = list(i.values())[0]
        if(type == "UserInfo"):
            instance = UserInfo()
            instance.SetUserInfo(data)
            to_return[type] = instance
        elif(type == "FiveMostVotedSubmissions"):
            instance = TopFiveVotedSubmissionsData()
            instance.SetFiveMostVotedSubmissionsFromJsonMap(data)
            to_return[type] = instance
        elif(type == "FiveMostVotedComments"):
            instance = TopFiveVotedCommentsData()
            instance.SetFiveMostVotedCommentsFromJsonMap(data)
            to_return[type] = instance
        elif(type == "VoteDistribution"):
            instance = VoteDistribution()
            instance.SetVoteDistributionFromJsonMap(data)
            to_return[type] = instance
        elif(type == "MostActiveSubreddits"):
            instance = MostActiveSubs()
            instance.SetMostActiveFromJsonMap(data)
            to_return[type] = instance
    return to_return

if __name__ == '__main__':
    print()
    user_name = GetUsernameInput()
    print()
    
    with open("scraper_output.json", mode='w') as outfile:
        json.dump([], outfile, indent=2)
        
    user_as_redditor = reddit.redditor(user_name)
    user_info = UserInfo()
    
    user_comments_list = list(user_as_redditor.comments.new(limit=99)).copy() #Limited to 100 historical submissions by Reddit API
    user_submissions_list = list(user_as_redditor.submissions.new(limit=99)).copy() #Limited to 100 historical submissions by Reddit API
    
    
    if user_info.IsSuspended(): #todo issuspended status needs to be updated accurately prior
        print("User is shadowbanned - only contains name and is_suspended attributes")
    else:
        user_info.SetBasicInfo()
        user_info.PrintBasicInfo()
        user_info.ConvertBasicInfoToTxt()
        
        u1 = TopFiveVotedSubmissionsData()
        u1.FindFiveMostVotedSubmissions()
        u1.PrintFiveMostVotedSubmissions()
        u1.ConvertFiveMostVotedSubmissionsToTxt()
        
        u2 = TopFiveVotedCommentsData()
        u2.FindFiveMostVotedComments()
        u2.PrintFiveMostVotedComments()
        u2.ConvertFiveMostVotedCommentsToTxt()
        
        u3 = VoteDistribution()
        u3.FindVoteDistribution()
        u3.PrintVoteDistribution()
        u3.ConvertVoteDistributionToTxt()
        
        u4 = MostActiveSubs()
        u4.FindMostActive()
        u4.PrintActiveSubs()
        u4.ConvertActiveSubsToTxt()
        
        #test json reader
        '''print("")
        temp = GetUserFromJson("scraper_output.json")
        temp["UserInfo"].PrintBasicInfo()
        temp["FiveMostVotedSubmissions"].PrintFiveMostVotedSubmissions()
        temp["FiveMostVotedComments"].PrintFiveMostVotedComments()
        temp["VoteDistribution"].PrintVoteDistribution()
        temp["MostActiveSubreddits"].PrintActiveSubs()'''
        print("")