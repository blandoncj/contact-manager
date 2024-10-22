import sqlite3 as sql
from db.db_connection import DatabaseConnection
from entity.contact import ContactEntity


class ContactDAO:

    def list_contact_phones(self, contact_id: int) -> list[str]:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT phone FROM contact_phones WHERE contact_id = ?",
                    (contact_id,),
                )
                return [phone[0] for phone in cursor.fetchall()]
        except sql.Error as e:
            print(f"Error on list_contact_phones: {e}")
            return []

    def list_all_contacts(self, user_id: int) -> list[ContactEntity]:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM contacts WHERE user_id = ?", (user_id,))
                results = cursor.fetchall()
                contacts = []
                for result in results:
                    phones = self.list_contact_phones(result[0])
                    contacts.append(
                        ContactEntity(
                            result[0],
                            result[1],
                            result[2],
                            phones,
                            result[3],
                            result[4],
                            result[5],
                            result[6],
                        )
                    )
                return contacts
        except sql.Error as e:
            print(f"Error on list_all: {e}")
            return []

    def list_contacts_by_query(self, query: str, user_id: int) -> list[ContactEntity]:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM contacts WHERE user_id = ? AND (name LIKE ? OR lastname LIKE ? OR category LIKE ? OR address LIKE ? OR email LIKE ?)",
                    (
                        user_id,
                        f"%{query}%",
                        f"%{query}%",
                        f"%{query}%",
                        f"%{query}%",
                        f"%{query}%",
                    ),
                )
                results = cursor.fetchall()
                contacts = []
                for result in results:
                    phones = self.list_contact_phones(result[0])
                    contacts.append(
                        ContactEntity(
                            result[0],
                            result[1],
                            result[2],
                            phones,
                            result[3],
                            result[4],
                            result[5],
                            result[6],
                        )
                    )
                return contacts
        except sql.Error as e:
            print(f"Error on list_by_query: {e}")
            return []

    def find_contact_by_id(self, contact_id: int) -> ContactEntity:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM contacts WHERE id = ?", (contact_id,))
                result = cursor.fetchone()
                phones = self.list_contact_phones(contact_id)
                return (
                    ContactEntity(
                        result[0],
                        result[1],
                        result[2],
                        phones,
                        result[3],
                        result[4],
                        result[5],
                        result[6],
                    )
                    if result
                    else None
                )
        except sql.Error as e:
            print(f"Error on find_by_id: {e}")
            return None

    def create_contact(self, contact: ContactEntity, user_id: int) -> None:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO contacts (name, lastname, category, address, email, is_favorite, user_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    (
                        contact.name,
                        contact.lastname,
                        contact.category,
                        contact.address,
                        contact.email,
                        contact.is_favorite,
                        user_id,
                    ),
                )
                conn.commit()
                contact_id = cursor.lastrowid

                for phone in contact.phones:
                    cursor.execute(
                        "INSERT INTO contact_phones (phone, contact_id) VALUES (?, ?)",
                        (phone, contact_id),
                    )
                    conn.commit()
        except sql.Error as e:
            print(f"Error on create: {e}")

    def update_contact(self, contact: ContactEntity) -> None:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE contacts SET name = ?, lastname = ?, category = ?, address = ?, email = ?, is_favorite = ? WHERE id = ?",
                    (
                        contact.name,
                        contact.lastname,
                        contact.category,
                        contact.address,
                        contact.email,
                        contact.is_favorite,
                        contact.id,
                    ),
                )
                conn.commit()

                cursor.execute(
                    "DELETE FROM contact_phones WHERE contact_id = ?", (contact.id,)
                )
                conn.commit()

                for phone in contact.phones:
                    cursor.execute(
                        "INSERT INTO contact_phones (phone, contact_id) VALUES (?, ?)",
                        (phone, contact.id),
                    )
                    conn.commit()
        except sql.Error as e:
            print(f"Error on update: {e}")

    def delete_contact(self, contact_id: int) -> None:
        try:
            with DatabaseConnection() as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM contacts WHERE id = ?", (contact_id,))
                conn.commit()
        except sql.Error as e:
            print(f"Error on delete: {e}")
