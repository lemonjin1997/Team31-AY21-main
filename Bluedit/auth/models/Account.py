class Account:
    def __init__(self, userID, email, password, salt, dateCreated, accStatus, activated, emailAuth, otpkey, passwordDate):
        self.__userID = userID
        self.__email = email
        self.__password = password
        self.__salt = salt
        self.__dateCreated = dateCreated
        self.__accStatus = accStatus
        self.__activated = activated
        self.__emailAuth = emailAuth
        self.__otpkey = otpkey
        self.__passwordDate = passwordDate

    @property
    def userID(self):
        return self.__userID

    @userID.setter
    def userID(self, userID):
        self.__userID = userID

    @property
    def email(self):
        return self.__email

    @email.setter
    def email(self, email):
        self.__email = email

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password):
        self.__password = password

    @property
    def salt(self):
        return self.__salt

    @salt.setter
    def salt(self, salt):
        self.__salt = salt

    @property
    def dateCreated(self):
        return self.__dateCreated

    @dateCreated.setter
    def dateCreated(self, dateCreated):
        self.__dateCreated = dateCreated

    @property
    def accStatus(self):
        return self.__accStatus

    @accStatus.setter
    def accStatus(self, accStatus):
        self.__accStatus = accStatus

    @property
    def activated(self):
        return self.__activated

    @activated.setter
    def activated(self, activated):
        self.__activated = activated

    @property
    def emailAuth(self):
        return self.__emailAuth

    @emailAuth.setter
    def emailAuth(self, emailAuth):
        self.__emailAuth = emailAuth

    @property
    def otpkey(self):
        return self.__otpkey

    @otpkey.setter
    def otpkey(self, otpkey):
        self.__otpkey = otpkey

    @property
    def passwordDate(self):
        return self.__passwordDate

    @passwordDate.setter
    def passwordDate(self, passwordDate):
        self.__passwordDate = passwordDate

