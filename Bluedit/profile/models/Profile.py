class Profile:
    def __init__(self, userID, username, about, posted, commented, saved, reported, upvoted, profileImg):
        self.__userID = userID
        self.__username = username
        self.__about = about
        self.__posted = posted
        self.__commented = commented
        self.__saved = saved
        self.__reported = reported
        self.__upvoted = upvoted
        self.__profileImg = profileImg

    @property
    def userID(self):
        return self.__userID

    @userID.setter
    def userID(self, userID):
        self.__userID = userID

    @property
    def username(self):
        return self.__username

    @username.setter
    def username(self, username):
        self.__username = username

    @property
    def about(self):
        return self.__about

    @about.setter
    def about(self, about):
        self.__about = about

    @property
    def posted(self):
        return self.__posted

    @posted.setter
    def posted(self, posted):
        self.__posted = posted

    @property
    def commented(self):
        return self.__commented

    @commented.setter
    def commented(self, commented):
        self.__commented = commented

    @property
    def saved(self):
        return self.__saved

    @saved.setter
    def saved(self, saved):
        self.__saved = saved

    @property
    def reported(self):
        return self.__reported

    @reported.setter
    def reported(self, reported):
        self.__reported = reported

    @property
    def upvoted(self):
        return self.__upvoted

    @upvoted.setter
    def upvoted(self, upvoted):
        self.__upvoted = upvoted

    @property
    def profileImg(self):
        return self.__profileImg

    @profileImg.setter
    def profileImg(self, profileImg):
        self.__profileImg = profileImg
