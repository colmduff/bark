from datetime import datetime
import sys

from db_manager import DatabaseManager
    
db = DatabaseManager("bookmark.db")


class CreateBookmarksTableCommand:

    def execute(self):
        db.create_table("bookmarks", {
            "id": "integer primary key autoincrement",
            "title": "text not null",
            "url": "text not null",
            "notes": "text",
            "date_added": "text not null"
        })


class AddBookmarkCommand:

    def execute(self, data):

        data["date_added"] = datetime.utcnow().isoformat() # adds current date time
        db.add("bookmarks",data)

        return "Bookmark Added ..."

class ListBookmarksCommand:

    def __init__(self, order_by="date_added"):
        self.order_by = order_by

    def execute(self):
        return db.select("bookmarks", order_by=self.order_by).fetchall()

class DeleteBookmarkCommand:

    def execute(self, data):
        db.delete("bookmarks", {"id": data}) # delete accepts a dictionary of colum name, match value pairs
        return "Bookmark deleted ... "

class QuitCommand:

    def execute(self):
        sys.exit()