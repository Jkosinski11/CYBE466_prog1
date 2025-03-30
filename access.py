import sys
import os
#structure storing global variables and files
state = {
    "friends" : set(), #stores all added friends
    "lists" : {}, #dictionary of lists that contain there group members
    "viewing" : False, #current user viewing the file
    "picturedict" : {}, #dictionary storing all the pictures on myFacebook
    "profileOwner" : False, #the overall owner of the profile
    "friendfile" : open("friends.txt", "w"), #file for all friends to be stored in
    "audit" : open("audit.txt", "w"), #stores each prnted line in an output file
    "listfile" : open("lists.txt", "w"), #File storing all the lists and there members
    "permissions" : ["rw", "r-", "-w", "--"] #all valid permissions
}

#takes a string and prints it to terminal as well as adding to audit.txt
def auditprint(str):
    print(str)
    state["audit"].write(str)

#makes sure input strings from users are of a valid size and have corrct characters
def checkinput(input):
    #input must be shorter than 31 characters
    if len(input)<31:
        #checks for valid characters only in the string
        if '/' not in input and ':' not in input and not any(s.isspace for s in input): 
            auditprint(f"{input} contains invalid characters.\n")
            return False #False means input is invalid
        else:
            return True
    else:
        auditprint(f"{input} is too long\n")
        return False
#adds friends to the frined file and list 
def friendadd(friendname):
    if checkinput(friendname) == False:
       return
    if (state["profileOwner"] == False):#first friend add sets the profile owner for myFacebook
        state["profileOwner"]= friendname
        auditprint(f"{friendname} logged in as profile owner.\n")
    elif(state["viewing"] != state["profileOwner"]):# if the profile viewer isn't the owner they cannot add friends
        auditprint("You do not have permission to execute this command.\n")
        return
    elif friendname in state["friends"]: #if friends are in the list already they can't be added again
        auditprint(f"{friendname} already added to friends.\n") 
        return
    auditprint(f"{friendname} added to friends.\n")
    state["friends"].add(friendname)
    state["friendfile"].write(friendname + "\n")
        
#sets profile viewer to given friend  
def viewby(friendname):
    if friendname in state["friends"]:# sets profile viewer if the given name is in the friends list
        auditprint(f"{friendname} viewing profile.\n" )
        state["viewing"] = friendname
    else:
        auditprint(f"{friendname} not found\n")

#logs out the user and sets the viewer to False
def logout():
    if(state["viewing"] != False):
        auditprint(f"{state["viewing"]} succesfully logged out\n")
        state["viewing"] = False
        return
    auditprint("No profile viewers.\n")
    
#Creates a list to add friends to
def listadd(listname):
    if(state["viewing"] != state["profileOwner"]): #Only profile owners can create lists
        auditprint("You do not have permissions to execute this command.\n")
        return
    if listname in state["lists"]: #lists cannot be reapeated
        auditprint(f"{listname} already added.\n")
    elif(listname == "nil"): #Reserved keyword for pictures not with a list
        auditprint("Reserved list name.\n")
    else:
        state["lists"][listname] = []#Add a new empty lists to list of lists
        auditprint(f"{listname} successfully created.\n")

#Adds friends to an exisiting list
def friendlist(friendname, listname):
    if(state["viewing"] != state["profileOwner"]):#Only the profile owner can add friends to lists
        auditprint("You do not have permissions to execute this command.\n")
        return
    if friendname in state["friends"]:
        if listname in state["lists"]:
            if friendname in state["lists"]:# if friend is already in lists do not add again
                auditprint(f"{friendname} already added to {listname}.")
                return
            state["lists"][listname].append(friendname) #add friend to list if the name exists in friends list and list exists in lists
            auditprint(f"{friendname} added to {listname}.\n")
        else:
            auditprint(f"{listname} not found.\n")
    else:
        auditprint(f"{friendname} not found.\n")

#Current viewer posts a picture 
def postpicture(picturename):
    if(state["viewing"] == False):#someone must be viewing the profile to post a picture
        auditprint("No one viewing profile.\n")
        return
    if(checkinput(picturename) == False):#Check if icturename follows the input requirements
        return
    if picturename in state["picturedict"]: #Pictures cannot be posted ore than once
        auditprint(f"{picturename} already exists.\n")
        return
    state["picturedict"][picturename]= {"owner":state["viewing"], "list":"nil", "permissionO":"rw", "permissionL":"--", "permissionR":"--"} #intialize the state of the posts
    if ".txt" not in picturename:#Create the file as a txt file if it is not already
        picturenamefile = picturename +".txt"
        picture = open(f"{picturenamefile}", "w")
    else:
        picturenamefile = picturename 
        picture = open(f"{picturenamefile}", "w")
    name = picturename.split(".")#if the file is a .txt file already parse it to only get the name of the post
    picture.write(f"{name[0]}\n")
    picture.close()
    auditprint(f"{state["viewing"]} posted {picturename}.\n")
#change the list that a picture is a part of
def chlst(picturename, listname):
    if(picturename not in state["picturedict"]): #picture must exist for list to be changed
        auditprint(f"{picturename} does not exist\n")
        return
    if(listname not in state["lists"]): #list must exist for a picture to be added to it
        auditprint(f"{listname} does not exist\n")
        return
    if(state["viewing"] == False):# must be a viwer to change picture list
        auditprint("No one viewing profile.\n")
        return
    
    if(state["viewing"] == state["profileOwner"] or 
       (state["viewing"] == state["picturedict"][picturename].get("owner") and state["viewing"] in state["lists"][listname])):#User must be the profile owner or a member
        state["picturedict"][picturename]["list"] = listname
        auditprint(f"{picturename} succesfully added to {listname}.\n")
        return
    auditprint(f"{state["viewing"]} is not a member of {listname}.\n")
   
    

#Change picture permissions
def chmod(picturename, rwO, rwL, rwR):
    if (state["viewing"] == False) : # Must be a profile viewer to change permissions
        auditprint("No one viewing profile.\n")
        return
    if(picturename not in state["picturedict"]): #Picture must exist for its permissions to be changed
        auditprint(f"{picturename} does not exist\n")
        return
    if(len(rwO)!=2 or len(rwL)!=2 or len(rwR)!=2): #must be valid permissions
        auditprint("Permissions are of improper length.\n")
        return
    if (rwO not in state["permissions"] or rwL not in state["permissions"] or rwR not in state["permissions"]):#Check if they match valid permissions strings
        auditprint("Permissions can only be 'r', 'w', or '-'.\n")
        return
    if(state["viewing"] != state["profileOwner"] and state["viewing"] != state["picturedict"][picturename].get("owner") ):#if the viewer isn't the profile owner or the picture owner they can't change the pcitures permissions
        auditprint("You do not permissions to execute this command must be the profile or picture owner\n")
        return
    #Change each permission to the user given permissions
    state["picturedict"][picturename]["permissionO"]= rwO
    state["picturedict"][picturename]["permissionL"]= rwL
    state["picturedict"][picturename]["permissionR"]= rwR
    auditprint(f"{picturename} permissions changed to  {rwO} {rwL} {rwR}.\n")

#Change picture owner
def chown(picturename, friendname):
    if(state["profileOwner"] !=  state["viewing"]):# nly the profile owner can change picture ownership
        auditprint("Only the profile owner can change the picture ownership.")
        return
    if(picturename not in state["picturedict"]):# picture must exist for owner to be changed
        auditprint(f"{picturename} does not exist.\n")
        return
    if(friendname not in state["friends"]):# the new owner must exist as a friend
        auditprint(f"{friendname} is not currently a friend.\n")
        return
    else:
        state["picturedict"][picturename]["owner"] = friendname
        auditprint(f"{friendname} is now the owner of {picturename}.\n")

#read a post and its comments
def readcomments(picturename):
    if(picturename not in state["picturedict"]):#post must exist to be seen
        auditprint(f"{picturename} not found.\n")
        return
    if(state["viewing"] == False): #Must have somoen viewing the profile
        auditprint("No one currently viewing profile.\n")
        return
    #The viewer user must have the correct permissions to be able to read the comments
    if((state["viewing"] == state["picturedict"][picturename].get("owner") and  state["picturedict"][picturename].get("permissionO", "none") in {"rw", "r-"}) or
       (state["viewing"] in state["lists"].get(state["picturedict"][picturename].get("list"),[]) and state["picturedict"][picturename].get("permissionL", "none")  in {"rw", "r-"}) or
       (state["picturedict"][picturename].get("permissionR", "none") in {"rw", "r-"})):
        #if profile name isn't a txt file to be read from make it a txt file
        if ".txt" not in picturename:
            picturenamefile = picturename +".txt"
            picture = open(f"{picturenamefile}", "r")
        else:
            picturenamefile = picturename 
            picture = open(f"{picturenamefile}", "r")
        #read the post
        name = picture.readline()
        auditprint(f"{name}\nComments:\n")
        comments = picture.readlines()
        for line in comments:
            auditprint(f"{line}\n")
    else:
       auditprint(f"{state['viewing']} does not have the permissions to view {picturename} comments\n")
       return

#write commennts to a post 
def writecomments(picturename, *text):
    if(picturename not in state["picturedict"]):#picture must exist to be commented on
        auditprint(f"{picturename} not found.\n")
        return
    if(state["viewing"] == False): # must be a profile viewer to comment on a picture
        auditprint(f"No current viewers.\n")
        return
      #The viewer user must have the correct permissions to be able to write comments
    if((state["viewing"] == state["picturedict"][picturename].get("owner") and  state["picturedict"][picturename].get("permissionO", "none") in {"rw", "-w"}) or
       (state["viewing"] in state["lists"].get(state["picturedict"][picturename].get("list"), []) and state["picturedict"][picturename].get("permissionL", "none") in {"rw", "-w"}) or
       (state["picturedict"][picturename].get("permissionR", "none") in {"rw", "-w"})):
        comment = " ".join(text)
         #if profile name isn't a txt file to be read from make it a txt file
        if ".txt" not in picturename:
            picturenamefile = picturename +".txt"
            picture = open(f"{picturenamefile}", "a")
        else:
            picturenamefile = picturename 
            picture = open(f"{picturenamefile}", "a")
        picture.write(f"{comment}\n")
        picture.close()   
        auditprint(f"{state["viewing"]} commented {comment} on {picturename}.\n")  
    else:
            auditprint(f"{state['viewing']} does not have the permissions to comment on {picturename}\n")
            return
#Closes all files and exits out of myFacebook
def end():
    state["friendfile"].close()
    auditprint("System turned off...\n")
    state["audit"].close()
    lists  = list(state["lists"].items())
    for key, objects in lists:
        state["listfile"].write(f"{key}:\n")
        for object in objects:
            state["listfile"].write(f"{object} \n") 
    state["listfile"].close()
    



def main():
    if len(sys.argv) != 2:  # Ensure the user provides one argument
        print("Usage: python script.py <inputfile>")
        sys.exit(1)  # Exit with an error code

    inputfile = sys.argv[1]  # Get the filename from the command-line argument

    if not os.path.isfile(inputfile):  # Check if the file exists
        print(f"Error: {inputfile} does not exist.")
        sys.exit(1)

    with open(inputfile, 'r') as file:
        for line in file: #read each command line from the file
            split = line.strip().split(" ")
            func = split[0]
            args = split[1:] if len(split) > 1 else []
            #executes the given command lines
            if func in globals():
                call = globals()[func]
                call(*args)
            else:
                print(f"Error: Function not found")
        
    
if __name__ == "__main__":
        main()
