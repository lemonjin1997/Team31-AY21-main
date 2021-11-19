class Post:
    def __init__(self, postID, postTitle, postContent, postTime, postLikes, postReplies, postSaves, postImage,
                 postStatus, postLock, postCat, UUID):
        self.__postID = postID
        self.__postTitle = postTitle
        self.__postContent = postContent
        self.__postTime = postTime
        self.__postLikes = postLikes
        self.__postReplies = postReplies
        self.__postSaves = postSaves
        self.__postImage = postImage
        self.__postStatus = postStatus
        self.__postLock = postLock
        self.__postCat = postCat
        self.__UUID = UUID

    @property
    def postID(self):
        return self.__postID

    @postID.setter
    def postID(self, postID):
        self.__postID = postID

    @property
    def postTitle(self):
        return self.__postTitle

    @postTitle.setter
    def postTitle(self, postTitle):
        self.__postTitle = postTitle

    @property
    def postContent(self):
        return self.__postContent

    @postContent.setter
    def postContent(self, postContent):
        self.__postContent = postContent

    @property
    def postTime(self):
        return self.__postTime

    @postTime.setter
    def postTime(self, postTime):
        self.__postTime = postTime

    @property
    def postLikes(self):
        return self.__postLikes

    @postLikes.setter
    def postLikes(self, postLikes):
        self.__postLikes = postLikes

    @property
    def postReplies(self):
        return self.__postReplies

    @postReplies.setter
    def postReplies(self, postReplies):
        self.__postReplies = postReplies

    @property
    def postSaves(self):
        return self.__postSaves

    @postSaves.setter
    def postSaves(self, postSaves):
        self.__postSaves = postSaves

    @property
    def postImage(self):
        return self.__postImage

    @postImage.setter
    def postImage(self, postImage):
        self.__postImage = postImage

    @property
    def postStatus(self):
        return self.__postStatus

    @postStatus.setter
    def postStatus(self, postStatus):
        self.__postStatus = postStatus

    @property
    def postLock(self):
        return self.__postLock

    @postLock.setter
    def postLock(self, postLock):
        self.__postLock = postLock

    @property
    def postCat(self):
        return self.__postCat

    @postCat.setter
    def postCat(self, postCat):
        self.__postCat = postCat

    @property
    def UUID(self):
        return self.__UUID

    @UUID.setter
    def UUID(self, UUID):
        self.__UUID = UUID
