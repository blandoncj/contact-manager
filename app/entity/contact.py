class ContactEntity:
    def __init__(
        self,
        id,
        name,
        lastname,
        phones,
        category,
        address=None,
        email=None,
        is_favorite=False,
    ):
        self.id = id
        self.name = name
        self.lastname = lastname
        self.phones = phones
        self.category = category
        self.address = address
        self.email = email
        self.is_favorite = is_favorite

    def __str__(self):
        return f"ContactEntity({self.id}, {self.name}, {self.lastname}, {self.phones}, {self.category}, {self.address}, {self.email}, {self.is_favorite})"
