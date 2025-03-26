import sys
import os
state = {
    "friends" : set(),
    "lists" : {},
    "viewing" : False,
    "picturedict" : dict(),
    "profileOwner" : False,
    "friendfile" : open("friends.txt", "w"),
    "audit" : open("audit.txt", "w"),
    "listfile" : open("lists.txt", "w"),
}
def auditprint(str):
    print(str)
    state["audit"].write(str)

def checkinput(input):
    if(len(input)<31):
        if("/" not in input or ":" not in input or (s.isspace for s in input) == False ):
            return True
    auditprint(f"{input} is too long or contains invalid characters.\n")

    return False

def friendadd(friendname):
    if checkinput(friendname) == False:
       return
    if (state["profileOwner"] == False):
        
        state["profileOwner"]= friendname
    if(state["viewing"] != state["profileOwner"]):
        auditprint("You do not have permission to execute this command\n")
    if friendname in state["friends"]:
        auditprint("Friend already added \n") 
    elif checkinput(friendname) == False:
       return
    else:
        auditprint(f"{friendname} added to friends\n")
        state["friends"].add(friendname)
        state["friendfile"].write(friendname + "\n")
        
   
def viewby(friendname):
    if friendname in state["friends"]:
        auditprint(f"Viewing by {friendname}\n" )
        state["viewing"] = friendname
    else:
        auditprint(f"{friendname} not found\n")

def logout():
    if(state["viewing"] != False):
        auditprint(f"{state["viewing"]} succesfully logged out\n")
        state["viewing"] = False
        return
    auditprint("no profile viewers\n")
    


def listadd(listname):
    if(state["viewing"] != state["profileOwner"]):
        auditprint("User doesn't have permissions to access this feauture")
        return
    if listname in state["lists"]:
        auditprint("List already added\n")
    elif(listname == "nil"):
        auditprint("Reserved list name\n")
    else:
        state["lists"][listname] = set()
        auditprint(f"{listname} successfully created\n")


def friendlist(friendname, listname):
    if friendname in state["friends"]:
        if listname in state["lists"]:
            state["lists"][listname].add(friendname)
            auditprint(f"{friendname} added to {listname}\n")
        else:
            auditprint("List not found\n")
    else:
        auditprint("Friend not found\n")

def postpicture(picturename):
    if(state["viewing"] == False):
        auditprint("No one viewing profile\n")
        return
    if(checkinput(picturename) == False):
        return
    if picturename in state["picturedict"]:
        auditprint(f"{picturename} already exists\n")
        return
    state["picturedict"][picturename]= {"owner":state["viewing"], "list":"nil", "permissionO":"rw", "permissionL":"--", "permissionR":"--"}
    picture = open(f"{picturename}", "w")
    name = picturename.split(".")
    picture.write(f"{name[0]}\n")
    picture.close()
    
def chlst(picturename, listname):
    if(picturename not in state["picturedict"]):
        auditprint("picture does not exist\n")
        return
    if(listname not in state["lists"]):
        auditprint("list does not exist\n")
        return
    if(state["viewing"] == False or state["profileOwner"] == False):
        auditprint("No one viewing profile\n")
        return
    if(state["viewing"] not in state["lists"][listname]):
        auditprint("User is not a member of this community\n")
        return
    state["picturedict"][picturename]= {"list": listname}
    auditprint(f"{picturename} succesfully added to {listname}\n")
    


def chmod(picturename, rwO, rwL, rwR):
    if(len(rwO)!=2 or len(rwL)!=2 or len(rwR)!=2):
        return
    if (rwO not in {"r","w","-"} or rwL not in {"r","w","-"} or rwR not in {"r","w","-"}):
        return
    if(picturename not in state["picturedict"]):
        auditprint("picture does not exist\n")
        return
    state["picturedict"][picturename]= {"permissionO":rwO, "permissionL":rwL,  "permissionR":rwR}
    auditprint(f"{picturename} changed permissions to {rwO} {rwL} {rwR}\n")

def chown(picturename, friendname):
    if(state["profileOwner"] ==  state["viewing"]):
        return
    if(picturename not in state["picturedict"]):
        auditprint(f"{picturename} does not exist\n")
    if(friendname not in state["friendlist"]):
        auditprint(f"{friendname} is not currently a friend\n")
    state["picturedict"][picturename]= {"owner":friendname}

def readcomments(picturename):
    if(picturename not in state["picturedict"]):
        auditprint(f"{picturename} not found\n")
        return
    if(state["viewing"] == False):
        auditprint("No one currently viewing profile\n")
        return
    if(state["viewing"] != state["picturedict"][picturename].get("owner")):
        if state["picturedict"].get(picturename, {}).get("permissionO", "none") not in {"rw", "r-"}:
            if state["picturedict"].get(picturename, {}).get("permissionR", "none") not in {"rw", "r-"}:
                auditprint("You do not have the appropriate permissions to view this post")
                return
    else:
         picture = open(f"{picturename}", "r")
         post = picture.readlines()
         auditprint(post)

def writecomments(picturename, *text):
    if(picturename not in state["picturedict"]):
        auditprint(f"{picturename} not found\n")
        return
    if(state["viewing"] == False):
        auditprint(f"ERROR: No current viewers\n")
        return
    if(state["viewing"] != state["picturedict"][picturename].get("owner")):
        if state["picturedict"].get(picturename, {}).get("permissionO", "none") not in {"rw", "-w"}:
            if state["picturedict"].get(picturename, {}).get("permissionR", "none") not in {"rw", "-w"}:
                 auditprint("you do not have appropriate permissions to comment on this post\n")
    else:
        comment = " ".join(text)
        picture = open(f"{picturename}", "a")
        picture.write(comment)
        picture.close()   
        auditprint(f"{state["viewing"]} commented {comment} on {picturename} \n")  

def end():
    state["friendfile"].close()
    state["audit"].close()
    for lists in state["lists"]:
        state["listfile"].write(lists)
        for friend in lists:
            state["listfile"].write(friend)    
    state["listfile"].close()



def main():
    if len(sys.argv) != 2:  # Ensure the user provides exactly one argument (the text file)
        print("Usage: python script.py <inputfile>")
        sys.exit(1)  # Exit with an error code

    inputfile = sys.argv[1]  # Get the filename from the command-line argument

    if not os.path.isfile(inputfile):  # Check if the file exists
        print(f"Error: {inputfile} does not exist.")
        sys.exit(1)

    with open(inputfile, 'r') as file:
        for line in file:
            split = line.strip().split(" ")
            func = split[0]
            args = split[1:] if len(split) > 1 else []

            if func in globals():
                call = globals()[func]
                call(*args)
            else:
                print(f"Error: Function not found")
        
    
if __name__ == "__main__":
        main()
