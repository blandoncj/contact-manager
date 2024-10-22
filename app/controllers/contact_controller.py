from entity.contact import ContactEntity
from dao.contact_dao import ContactDAO


class ContactController:
    def __init__(self) -> None:
        self.contact_dao = ContactDAO()

    def list_contact_phones(self, contact_id: int) -> list[str]:
        return self.contact_dao.list_contact_phones(contact_id)

    def list_all_contacts(self, user_id: int) -> list[ContactEntity]:
        return self.contact_dao.list_all_contacts(user_id)

    def list_contacts_by_query(self, query: str, user_id: int) -> list[ContactEntity]:
        return self.contact_dao.list_contacts_by_query(query, user_id)

    def find_contact_by_id(self, contact_id: int) -> ContactEntity:
        return self.contact_dao.find_contact_by_id(contact_id)

    def create_contact(self, contact: ContactEntity, user_id: int) -> None:
        self.contact_dao.create_contact(contact, user_id)

    def update_contact(self, contact: ContactEntity) -> None:
        self.contact_d_dao.update_contact(contact)

    def delete_contact(self, contact_id: int) -> None:
        self.contact_dao.delete_contact(contact_id)
