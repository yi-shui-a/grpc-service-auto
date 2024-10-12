class Message:
    def __init__(self):
        self._name = ""
        self._label = ""
        self._fields = [] # vector of fields

    def set_fields(self, fields):
        self._fields.append(fields)
        
    def toString(self) -> str:
        """
        Generate a string representation of the Message object.
    
        Parameters:
        -----------
        self : Message
            The Message object for which the string representation is to be generated.
    
        Returns:
        --------
        str
            A string representation of the Message object in the format:
            "Message Name: <name>, Label: <label>, Fields: <fields>"
        """
        return f"Message Name: {self.__name}, Label: {self.__label}, Fields: {self.__fields}"
        
