class Patient:
    def __init__(self, first_name='', last_name=''):
        self.first_name = first_name
        self.last_name = last_name

    def get_full_name(self):
        fullname = ''
        if self.first_name:
            fullname = self.first_name
            if self.last_name:
                fullname += '_' + self.last_name
        elif self.last_name:
            fullname = self.last_name

        return fullname