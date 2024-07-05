from locust import HttpUser, between, task
import csv
import json

class UserBehaviour(HttpUser):
    wait_time = between(1, 4)
    host = "http://openlibrary.org"

    def on_start(self):
        self.book_titles = self.load_book('books.csv', 100)
        self.current_index = 0

    def load_book(self, csv_file, limit):
        with open(csv_file, newline='') as csvfile:
            csvreader = csv.DictReader(csvfile)
            titles = [row['Title'] for row in csvreader]
            return titles[:limit]

    @task(1)

    def search_get_book(self):
        if self.current_index >= len(self.book_titles):
            self.current_index = 0
        book_title = self.book_titles[self.current_index]
        self.current_index +=1
        
        search_response = self.client.get(f"/search.json?q={book_title}")
        search_data = search_response.json()

        if search_data['docs']:
            isbns = [doc.get('isbn',[None])[0] for doc in search_data['docs'] if 'isbn' in doc][:100]

            if isbns:
                bibkeys = ','.join([f'ISBN:{isbn}' for isbn in isbns if isbn])
                book_response = self.client.get(f"https://openlibrary.org/api/books?bibkeys={bibkeys}&format=json")
                book_data = book_response.json()

                print(json.dumps(book_data, indent=2))
                print()
            else:
                print(f"No ISBN found in search results for '{book_title}'")
        else:
            print(f"No search result found for '{book_title}'")


class WebsiteUser(HttpUser):
    tasks = [UserBehaviour]
    wait_time = between(1, 4)
    host = "http://openlibrary.org"
