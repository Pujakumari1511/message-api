import copy


class Message:
    def __init__(self, title, content, sender, url):
        self.title = title
        self.content = content
        self.sender = sender
        self.url = url

    def get_message_in_dict_for_v2(self):
        return self.__dict__

    def get_message_in_dict_for_v1(self):
        # make copy of object then delete url in copy version and return new object
        copy_v1 = copy.deepcopy(self)
        del copy_v1.url
        return copy_v1.__dict__
