__author__ = 'Mastermind'

import glob, os, subprocess
from time import sleep

basepath = r'\\10.100.0.28\miphiles\TESTprores'
sourcedir = basepath + r'\*.*'
workinghd = basepath + r'\working\workinghd'
working540 = basepath + r'\working\workinghd\540'
hdout = basepath + r'\working\workinghd\output'
workingsd = basepath + r'\working\workingsd'
output = basepath + r'\output'
source = basepath + r'\working\source'
working1440 = basepath + r'\working\working1440'
bumperin = basepath + r'\bumper_in'
bumperout =basepath + r'\bumper_out'
bumpersound = basepath + r'\working\sound'
bumperscaler = basepath + r'\working\scaler'
openHD = basepath + r'\working\source\bumpers\openHD.mp4'
closeHD = basepath + r'\working\source\bumpers\closeHD.mp4'
openSD = basepath + r'\working\source\bumpers\openSD.mp4'
closeSD = basepath + r'\working\source\bumpers\closeSD.mp4'
open1440 = basepath + r'\working\source\bumpers\open1440.mp4'
close1440 = basepath + r'\working\source\bumpers\close1440.mp4'
open169 = basepath + r'\working\source\bumpers\open169.mp4'
close169 = basepath + r'\working\source\bumpers\close169.mp4'

X = True
inuse = True
width = ''

def Audiodetector(i):
    os.chdir('c:/mediainfo_cli')  # changes the directory to the location of MEDIAINFO
    mine = subprocess.Popen('mediainfo --Inform=Audio;%Format% ' +bumperin+'\\'+i, stdout=subprocess.PIPE, bufsize=1)  # These lines run mediainfo to determine whether audio is present
    new = (mine.communicate()[0])  # pulls the output from mine
    sound = (new.decode("ascii")).lstrip().rstrip()  # makes the output text
    if sound == "": # "" means there is no sound, so it needs to be added
        Silentadder(i) # Silentadder is the function that adds a silent audio track
    else:
        os.rename(bumperin + '\\' + tail, bumpersound + '\\' + tail)  # move the file to the working directory
        Widthcaller(bump) # call the function that gathers the width of the video, so the path to follow can be determined

def Silentadder(i): # function that adds a silent audio track
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=44100 -i " + bumperin + '\\' + tail + ' -shortest -c:v copy -c:a aac ' + bumpersound + '\\' + tail,stdout=subprocess.PIPE, bufsize=1)  # These three lines run the ffmpeg program with the desired prameters os.rename(workinghd+'\\'+hd, rghdwatch+'\\'+hd)
    os.remove(bumperin+'\\'+tail) # remove the source file since a new file with audio has been created
    Widthcaller(i) # call the function that gathers the width of the video, so the path to follow can be determined

def aspect(a): # function that determines the aspect ratrio, specifically needed to math the bumpers correctly to the content
    os.chdir('c:/mediainfo_cli')  # changes the directory to the location of MEDIAINFO
    mine = subprocess.Popen('mediainfo --Inform=Video;%DisplayAspectRatio% ' + bumpersound+'\\'+tail, stdout=subprocess.PIPE, bufsize=1)  # These three \
    # lines run mediainfo to determine the width
    new = (mine.communicate()[0])  # pulls the output from mine
    aspectratio = (new.decode("ascii")).lstrip().rstrip()  # makes the output text
    if aspectratio == '1.778': # 1.778 equals 16:9
        KScaler16(bump) # function that makes a new file from the source file with known values for 16/9
    elif aspectratio == '1.333': # 1.333 equals 4:3
        KScaler43(bump) # function that makes a new file from the source file with known values for 4/3
    else:
        print ('aspectratio not found')

def Widthcaller(bump): # function that finds the width of the incoming file and matches it to the proper workflow
    os.chdir('c:/mediainfo_cli')  # changes the directory to the location of MEDIAINFO
    mine = subprocess.Popen('mediainfo --Inform=Video;%Width% ' + bumpersound+'\\'+tail, stdout=subprocess.PIPE, bufsize=1)  # These three \
    # lines run mediainfo to determine the width
    new = (mine.communicate()[0])  # pulls the output from mine
    width = (new.decode("ascii")).lstrip().rstrip()  # makes the output text
    if width == '1440': # follow this branch if the file is 2k cut down to 1440
        aspect(bump) # function that determines the aspect ratio of the incoming file
    elif width == '1920':# follow this branch if the file is HD
        os.rename(bumpersound+'\\'+tail, bumperscaler+'\\'+tail) # move the file to the sound directory
        BumperHD(bump) #function that adds bumpers to HD material
    elif width == '720':# follow this branch if the file is SD
        SDScaler(bump) # reencode the incoming file to ensure size and aspect ratios are correct
    elif width == '2048':# follow this branch if the file is 2k
        Bigscaler(bump) # function that scales down 2k to 1440
    else:
        print (width)

def SDScaler(a): # this function reencodes the SD file to set parameters before attaching bumpers
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+bumpersound+'\\'+tail+' -vf scale=720:480,setdar=4:3,setsar=8:9 -y '+ bumperscaler+'\\'+tail, stdout=subprocess.PIPE,bufsize=1) # run the ffmpeg program to create the new input variant
    os.remove(bumpersound+'\\'+tail) #remove the input file
    BumperSD(bump) # this function adds SD bumpers

def KScaler43(a): # this function scales the input file to 4:3 parameters
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+bumpersound+'\\'+tail+' -vf scale=1440:1080,setdar=4:3,setsar=1:1 -y '+ bumperscaler+'\\'+tail, stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    os.remove(bumpersound+'\\'+tail) # delete the input file
    Bumper1440(bump) #add the 1440 bumpers

def KScaler16(a): # this function scales the input file to 16:9 parameters
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+bumpersound+'\\'+tail+' -vf scale=1440:1080,setdar=16:9,setsar=4:3 -y '+ bumperscaler+'\\'+tail, stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    os.remove(bumpersound+'\\'+tail) # remove the input file
    Bumper169(bump) # call the function to add the bumpers for this workflow

def Bigscaler(a): # function that cuts 2k files down to 1440
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+bumpersound+'\\'+tail+' -vf scale=1440:1080,setdar=4:3,setsar=1:1 -y '+ bumperscaler+'\\'+tail, stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    KScaler43(bump) # pass the file over to the 4:3 scaler

def BumperHD(x):
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+openHD+" -i "+bumperscaler+'\\'+tail+" -i "+closeHD+' -filter_complex '+'"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"'+' -map "[v]" -map "[a]"'+' -b:v 5M -pix_fmt yuv420p -y '+bumperout+'\\'+tail[0:-4]+'.mp4', stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    subprocess.call("ffmpeg -i "+openHD+" -i "+bumperscaler+'\\'+tail+" -i "+closeHD+' -filter_complex ' + '"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"' + ' -map "[v]" -map "[a]"' + ' -c:v prores_ks -profile:v 1 -qscale:v 11 -vendor ap10 -pix_fmt yuv422p10le -y ' + bumperout + '\\' + tail[0:-4]+'.mov', stdout=subprocess.PIPE, bufsize=1)# create the prores lt file
    os.remove(bumperscaler+'\\'+tail)

def Bumper1440(x):
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+open1440+" -i "+bumperscaler+'\\'+tail+" -i "+close1440+' -filter_complex '+'"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"'+' -map "[v]" -map "[a]"'+' -b:v 5M -pix_fmt yuv420p -y '+bumperout+'\\'+tail[0:-4]+'.mp4', stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    subprocess.call("ffmpeg -i "+open1440+" -i "+bumperscaler+'\\'+tail+" -i "+close1440+' -filter_complex ' + '"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"' + ' -map "[v]" -map "[a]"' + ' -c:v prores_ks -profile:v 1 -qscale:v 11 -vendor ap10 -pix_fmt yuv422p10le -y ' + bumperout + '\\' + tail[0:-4]+'.mov', stdout=subprocess.PIPE, bufsize=1)# create the prores lt file
    os.remove(bumperscaler+'\\'+tail)

def Bumper169(x):
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+open169+" -i "+bumperscaler+'\\'+tail+" -i "+close169+' -filter_complex '+'"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"'+' -map "[v]" -map "[a]"'+' -b:v 5M -pix_fmt yuv420p -y '+bumperout+'\\'+tail[0:-4]+'.mp4', stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    subprocess.call("ffmpeg -i "+open169+" -i "+bumperscaler+'\\'+tail+" -i "+close169+' -filter_complex ' + '"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"' + ' -map "[v]" -map "[a]"' + ' -c:v prores_ks -profile:v 1 -qscale:v 11 -vendor ap10 -pix_fmt yuv422p10le -y ' + bumperout + '\\' + tail[0:-4]+'.mov', stdout=subprocess.PIPE, bufsize=1)# create the prores lt file
    os.remove(bumperscaler+'\\'+tail)

def BumperSD(x): # function that ads SD bumpers
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+openSD+" -i "+bumperscaler+'\\'+tail+" -i "+closeSD+' -filter_complex '+'"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"'+' -map "[v]" -map "[a]"'+' -b:v 5M -pix_fmt yuv420p -y '+bumperout+'\\'+tail[0:-4]+'.mp4', stdout=subprocess.PIPE,bufsize=1) #These three lines run the ffmpeg program with the desired parameters to make the 4:2:0 low res file for web
    subprocess.call("ffmpeg -i "+openSD+" -i "+bumperscaler+'\\'+tail+" -i "+closeSD+' -filter_complex ' + '"[0:v:0] [0:a:0] [1:v:0] [1:a:0] [2:v:0] [2:a:0] concat=n=3:v=1:a=1 [v] [a]"' + ' -map "[v]" -map "[a]"' + ' -c:v prores_ks -profile:v 1 -qscale:v 11 -vendor ap10 -pix_fmt yuv422p10le -y ' + bumperout + '\\' + tail[0:-4]+'.mov', stdout=subprocess.PIPE, bufsize=1) # create the prores lt file
    os.remove(bumperscaler+'\\'+tail) #remove the source file

def Seperator(a):# Process that seperates files based on width for ProRes file creation
    os.chdir('c:/mediainfo_cli')  # changes the directory to the location of MEDIAINFO
    mine = subprocess.Popen('mediainfo --Inform=Video;%Width% ' +a, stdout=subprocess.PIPE,bufsize=1)  # These three \
    # lines run mediainfo to determine the width
    new = (mine.communicate()[0])  # pulls the output from mine
    width = (new.decode("ascii")).lstrip().rstrip()  # makes the output text
    if width == '720': #check to see if the file is SD
        try: #makes the program TRY the next step, but wont fail if it isnt successful
            os.remove(workingsd +'\\'+ tail)#remove a file of the same name from the working directory
        except OSError:#unless this exception occurs
            pass #if no file of the same name exists, continue to process
        os.rename(a, workingsd +'\\'+ tail)#move the file to the working direcory
    elif width == "1440":
        try: #makes the program TRY the next step, but wont fail if it isnt successful
            os.remove(working1440 +'\\'+ tail)#remove a file of the same name from the working directory
        except OSError:#unless this exception occurs
            pass #if no file of the same name exists, continue to process
        os.rename(a, working1440 +'\\'+ tail)#move the file to the working direcory
    else:
        try: #makes the program TRY the next step, but wont fail if it isnt successful
            os.remove(workinghd +'\\'+ tail.replace(' ','_'))#remove a file of the same name from the working directory
        except OSError:#unless this exception occurs
            pass #if no file of the same name exists, continue to process
        os.rename(a, workinghd +'\\'+ tail.replace(' ','_'))#move the file to the working direcory

def Ratefinder(a):
    os.chdir('c:/mediainfo_cli')  # changes the directory to the location of MEDIAINFO
    mine = subprocess.Popen('mediainfo --Inform=Video;%FrameRate% ' +a, stdout=subprocess.PIPE,bufsize=1)  # These three \
    # lines run mediainfo to determine the width
    new = (mine.communicate()[0])  # pulls the output from mine
    rate = (new.decode("ascii")).lstrip().rstrip()  # makes the output text
    print (rate)
    if rate == "48.000":
        os.rename(hdout+'\\'+tail, working540+'\\'+tail)
        Ratechanger(working540+'\\'+tail)
    else:
        pass

def Ratechanger(a):
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i "+a+' -vf scale=1920:1080,setdar=16:9,setsar=1:1 -r 24 ' + hdout + '\\' + tail[0:-4] + '.mov',stdout=subprocess.PIPE, bufsize=1)

def MAKER(x): #function that creates the ProRes transcode of the main input file (no  function for bumpers)
    try:
        os.remove(hdout + '\\' + tail[0:-4] + '.mov')
    except OSError:
        pass
    os.chdir('c:/ffmpeg/bin')  # changes the directory to the location of ffmpeg
    subprocess.call("ffmpeg -i " + hd + ' -c:v prores_ks -profile:v 1 -qscale:v 11 -vendor ap10 -pix_fmt yuv422p10le -y ' + hdout + '\\' + tail[0:-4] + '.mov',stdout=subprocess.PIPE, bufsize=1)  # These three lines run the ffmpeg program with the desired prameters
    try:
        os.remove(source + '\\' + tail)
    except OSError:
        pass
    os.remove(hd)
    Ratefinder(hdout+'\\'+tail)
    try:
        os.remove(output+'\\'+tail[0:-4]+'.mov')
    except OSError:
        pass
    os.rename(hdout + '\\' + tail[0:-4] + '.mov', output+'\\'+tail[0:-4]+'.mov')

#The follwing line begin execution of the script
while X == True: #This makes the program cycle over and over
    print ('checking for file to convert to ProRes...') #just prints to the screen
    for i in glob.glob(sourcedir): #looks for  files in the source directory
        head, tail = os.path.split(i)
        print (tail)
        if os.path.exists(i+'.part'):
            print ('file is being written')
            continue
        else:
            print ("passing")
        try: #makes the program TRY the next step, but wont fail if it isnt successful
            os.rename(i, i.replace(' ','_'))#makes sure the file is available (not being written to or locked)
            print(i + " is available for processing ") #prints that the file is available
        except OSError: #if this exception occurs, do the next thing
            print(i + " is in use!")#this prints if the file is open or in use
            continue #returns to the beginning of the loop
        Seperator(i.replace(' ','_'))#runs this function (see above for function details)
    print ('checking for HD files....')
    for hd in glob.glob(workinghd+'\\'+ '*.*'):
        head, tail = os.path.split(hd)
        try:
            os.rename(hd, hd)
            print(hd + " is available for conversion ")
        except OSError:
            print(hd + " is in use!")
        MAKER(hd)
    print('checking for files to bumper....')
    for bump in glob.glob(bumperin+'\\'+'*.*'):
        try:
            os.rename(bump, bump.replace(' ','_'))
            print(bump + " is available for conversion ")
        except PermissionError:
            print(bump + " is in use!")
            continue
        except FileExistsError:
            os.remove(bump.replace(' ','_'))
        head, tail = os.path.split(bump)
        tail = tail.replace(' ','_')
        Audiodetector(bump)
    print("looking for 1440 files......")
    for hd in glob.glob(working1440+'\\'+'*.*'):
        head, tail = os.path.split(hd)
        try:
            os.rename(hd, hd)
            print(hd + " is available for conversion ")
        except OSError:
            print(hd + " is in use!")
        MAKER(hd)
    print ('Waiting for files.....')
    sleep(30)#waits thirty seconds to check again for files
