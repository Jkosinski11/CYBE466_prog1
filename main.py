import sys
import os

friends = {}
lists = []
viewing = False
picturedict = dict()
profileOwner = False
friendfile = open("friends.txt", "w")
audit = open("audit.txt", "w")
listfile = open("lists.txt", "w")

def auditprint(str):
    print(str)
    audit.write(str)

def checkinput(input):
    if(len(input)<31):
        if("/" not in input or ":" not in input or (s.isspace for s in input) == False ):
            return True
    auditprint(f"{input} is too long or contains invalid characters.")

    return False

def friendadd(friendname):
    if checkinput(friendname) == False:
       return
    if (profileOwner == False):
        profileOwner = friendname
        viewing = profileOwner
    if(viewing != profileOwner):
        auditprint("You do not have permission to execute this command")
    if friendname in friends:
        auditprint("Friend already added \n") 
    elif checkinput(friendname) == False:
       return
    else:
        auditprint(f"{friendname} added to friends")
        friends.add(friendname)
        friendfile.write(friendname + "\n")
        
   
def viewby(friendname):
    if friendname in friends:
        auditprint("Viewing by " + friendname)
        viewing = friendname
    else:
        auditprint(f"{friendname} not found")

def logout():
    if(viewing != False):
        auditprint(f"{viewing} succesfully logged out")
        viewing = False
        return
    auditprint("no profile viewers")
    


def listadd(listname):
    if listname in lists:
        auditprint("List already added")
    elif(listname == "nil"):
        auditprint("Reserved list name")
    else:
        lists.add(listname)
        auditprint(f"{listname} successfully created")


def friendlist(friendname, listname):
    if friendname in friends:
        if listname in lists:
            listname.add(friendname)
            auditprint(f"{friendname} added to {listname}")
        else:
            auditprint("List not found")
    else:
        auditprint("Friend not found")

def postpicture(picturename):
    if(viewing == False):
        auditprint("No one viewing profile")
        return
    if(checkinput(picturename) == False):
        return
    if picturename in picturedict:
        auditprint(f"{picturename} already exists")
        return
    picturedict[picturename]= {"owner":viewing, "list":"nil", "permissionO":"rw", "permissionL":"--", "permissionR":"--"}
    if({picturename}.txt == None):
        {picturename}.txt = open(f"{picturename}.txt", "w")
    {picturename}.txt.write({picturename})
    {picturename}.txt.close()

def chlst(picturename, listname):
    if(picturename not in picturedict):
        auditprint("picture does not exist")
        return
    if(listname not in lists):
        auditprint("list does not exist")
        return
    if(viewing == False or profileOwner == False):
        auditprint("No one viewing profile")
        return
    if(viewing not in lists[listname]):
        auditprint("User is not a member of this community")
        return
    picturedict[picturename]= {"list": listname}
    auditprint(f"{picturename} succesfully added to {listname}")
    


def chmod(picturename, rwO, rwL, rwR):
    if(len(rwO)!=2 or len(rwL)!=2 or len(rwR)!=2):
        return
    if (rwO not in {"r","w","-"} or rwL not in {"r","w","-"} or rwR not in {"r","w","-"}):
        return
    if(picturename not in picturedict):
        auditprint("picture does not exist")
        return
    picturedict[picturename]= {"permissionO":rwO, "permissionL":rwL,  "permissionR":rwR}
    auditprint(f"{picturename} changed permissions to {rwO} {rwL} {rwR}")

def chown(picturename, friendname):
    if(profileOwner ==  viewing):
        return
    if(picturename not in picturedict):
        print(f"{picturename} does not exist")
    if(friendname not in friendlist):
        print(f"{friendname} is not currently a friend")
    picturedict[picturename]= {"owner":friendname}

def readcomments(picturename):
    if(picturename not in picturedict):
        return
    if(viewing == False):
        return
    if(viewing != picturedict[picturename].get("owner")):
        return
    if("rw" != picturedict[picturename].get("permissionO") and "r-" != picturedict[picturename].get("permissionO")):
        return
    if("rw" != picturedict[picturename].get("permissionR") and "r-" != picturedict[picturename].get("permissionR")):
        return

#def writecomments(picturename, text):

def end():
    friendfile.close()
    audit.close()
    listfile.write(lists)
    listfile.close()



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
            line()
    
if __name__ == "__main__":
        main()
