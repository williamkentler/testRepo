from gdata.youtube import YouTubeVideoEntry
from gdata.youtube.service import YouTubeService
import gdata
from gdata.service import BadAuthentication, CaptchaRequired
from time import gmtime, strftime

from optparse import OptionParser
import sys
import time
import os

#import for calling the EXIF exe
from subprocess import check_output


debug = True

def log(line):
    global debug
    if debug:
        print "uploader-log: %s\n" % line
        

def doit(the_filename):
    


    # ****************************
    # ******* Account Info  ******
    
    dev_email="donvalepresbyterianchurch@gmail.com"
    dev_password="ZVnw656x"
    dev_application="Donvale Sermons"
    dev_key="AI39si5nnIpfo2IDTb8Sy9qpsIaw5B4ZA3iW7Inh6-2PjLbcxYqyvPQTYIo64LjG_8R3H4aNL2UKB9DqXpqHTnq7LQDLy3GSIQ"
    youtube_user="DonvalePresbyterian"
    youtube_password="ZVnw656x"
    
   # ****************************
   
    
    the_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    
    
    log("running doit with the_time=%s and the_filename=%s" % (the_time, the_filename))
    
    
    #extract metadata from the XMP embedded in the movie
    command = os.path.join(os.path.dirname(__file__), "exiftool.exe -{0} -S -t " + "\"" + the_filename + "\"" )

    print(command.format("Title"))


    Title = check_output(command.format("Title"))
    Contributor = check_output(command.format("Contributor"))
    Date = check_output(command.format("Date"))
    Type = check_output(command.format("Type"))
    Publisher = check_output(command.format("Publisher"))
    
    log("the XMP Title is %s" % (Title))
    log("the XMP Contributor is %s" % (Contributor))
    log("the XMP Date is %s" % (Date))
    log("the XMP Type is %s" % (Type))
    log("the XMP Publisher is %s" % (Publisher))
       
    
    #construct the metadata for Youtube    
    title=Title
    description = "Speaker: {0}\nDate: {1}".format(Contributor, Date)
    keywords="church,christianity," + Type

    log("the Youtube Title is %s" % (title))
    log("the Youtube Description is %s" % (description))
    log("the Youtube Keywords is %s" % (keywords))


    #check that there is at least a title
    if title == "":
            log("no title, aborting upload")
            error = "no title, aborting upload"
            print error
            raise error




    # create video entry
    # prepare a media group object to hold our video's meta-data
    my_media_group = gdata.media.Group(
      title=gdata.media.Title(text=title),
      description=gdata.media.Description(description_type='plain',
                                          text=description),
      keywords=gdata.media.Keywords(text=keywords),
      category=gdata.media.Category(
          text='People',
          scheme='http://gdata.youtube.com/schemas/2007/categories.cat',
          label='People &amp; Blogs'),
      player=None
    )
    log("created media_group")

    entry = YouTubeVideoEntry(media=my_media_group)
    log("created youtube entry")


    service = YouTubeService(email=dev_email,
                            password=dev_password,
                            source=dev_application,
                            client_id=dev_application,
                            developer_key=dev_key)
    log("created YouTubeService")


    #Login
    
    # read token from file and use that if its still good
    token_file = "youtube_login_token.txt"
    login_token = None
    
    try:
        log("attempting to find previous login token in token file")
        f = open(token_file, 'r')
        log("token file found")
        login_token = f.readline().strip()
        f.close()
        service.SetClientLoginToken(login_token)
        log("set login token to %s" % login_token)
    except Exception:
        log("unable to set previous login token, continuing with default login settings")
        pass
    
    while True:
        captcha_token = None
        captcha_response = None
        try:
            log("trying login with captcha_token=%s and captcha_response=%s" % (captcha_token, captcha_response))
            service.ClientLogin(youtube_user,youtube_password, captcha_token=captcha_token, captcha_response=captcha_response)
            # all good, lets get out of here
            log("login succeeded continuing on to upload")
            break
        except BadAuthentication:
            log("BadAuthentication returned with credentials of user: %s password: %s" % (youtube_user, youtube_password))
            error = "BadAuthentication: Incorrect login credentials. Rejected by server."
            print error
            raise error
        except CaptchaRequired:
            log("CaptchaRequired returned from clientlogin(). requesting credentials")
            print "CaptchaRequired: required captcha input from user for uploading please supply it.\n"
            print "Captcha Address: " + self.captcha_url
            os.system('open ' + self.captcha_url)
            log("attempted to open url in browser window on mac using open command")
            in_captcha = raw_input("Type in the captha you see:")
            log("captcha input received from user (%s)" % in_captcha)
            captcha_token = self.captcha_token
            captcha_response = in_captcha.strip()
            log("set new client login info from captcha, looping back")
            # loop back now and try with new credentials
        except Exception, e:
            log("Uh oh, big error doing ClientLogin: %s" % e)
            raise Exception

    # save latest version of login token to a file for the next run
    try:
        log("saving token (%s) to token file (%s)" % (service.GetClientLoginToken(), token_file))
        f = open(token_file, 'w')
        f.write(service.GetClientLoginToken())
        f.close()
    except Exception:
        log("error occurred while writing to token file : %s " % Exception)
        pass
        
    # insert video entry
    try:
        log("starting to upload video entry")
        service.InsertVideoEntry(entry, the_filename)
        log("completed upload of video entry")
    except Exception, e:
        print type(e)
        print e
        raise
    
# call routine as function if this is run as a script
# allows us to catch any errors and report back to user
if __name__ == '__main__':
    try:
        # arg 1 is the time
        # arg 2 is the filename
        doit(sys.argv[1])
    except Exception, e:
        log("Some Error ocurred, returning failure to calling script")
        print type(e)
        print e
        sys.exit(1)
    else:
        log("%s uploaded to service successfully. Returning success to calling script (0)" % strftime("%Y-%m-%d %H:%M:%S", gmtime()))
        sys.exit(0)
