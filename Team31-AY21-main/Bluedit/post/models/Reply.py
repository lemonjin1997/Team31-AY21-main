class Reply:
    def __init__(self, replyID, replyContent, postID, replyTime, replyStatus, replyLikes, UUID):
        self.__replyID = replyID
        self.__replyContent = replyContent
        self.__postID = postID
        self.__replyTime = replyTime
        self.__replyStatus = replyStatus
        self.__replyLikes = replyLikes
        self.__UUID = UUID

    @property
    def replyID(self):
        return self.__replyID

    @replyID.setter
    def replyID(self, replyID):
        self.__replyID = replyID

    @property
    def replyContent(self):
        return self.__replyContent

    @replyContent.setter
    def replyContent(self, replyContent):
        self.__replyContent = replyContent

    @property
    def postID(self):
        return self.__postID

    @postID.setter
    def postID(self, postID):
        self.__postID = postID

    @property
    def replyTime(self):
        return self.__replyTime

    @replyTime.setter
    def replyTime(self, replyTime):
        self.__replyTime = replyTime

    @property
    def replyStatus(self):
        return self.__replyStatus

    @replyStatus.setter
    def replyStatus(self, replyStatus):
        self.__replyStatus = replyStatus

    @property
    def replyLikes(self):
        return self.__replyLikes

    @replyLikes.setter
    def replyLikes(self, replyLikes):
        self.__replyLikes = replyLikes

    @property
    def UUID(self):
        return self.__UUID

    @UUID.setter
    def UUID(self, UUID):
        self.__UUID = UUID
