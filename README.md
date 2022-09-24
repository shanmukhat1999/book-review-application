Web based Book Review Application

The main use of this application is to display books along with displaying and accepting feedback for each book.

This web application is written mainly in Python (using Flask web framework). Data of around 5000 books is stored in PostgreSQL database, which also stores the details of users and their feedback. Web pages are written using HTML and Javascript with minor styling.


User Guide (Google chrome is suggested website):

1. When you enter the website you will be directed to Register/Login page.
2. If you have already registered in the website, use the credentials to login, else register by your entering details. If you just want to go through the website without logging in, then use the Enter without login link provided at the bottom, but then you will not be able to provide feedback for any book.
3. After logging in you will be directed to the search page. There you can search for books, by providing a substring of Title or ISBN or Author name (For Example: if you enter "ada" in Title, then all the books which contain "ada" in their title will be displayed).
4. After the book names are displayed based on your search, then you can click on any of the books, to view its details and feedback.
5. After you enter a specific book page, details of the book along with feedback from other users (if any) can be found. If you are logged in then you can see the options to provide review and rating for that book, but feedback can be provided only once, you cannot find the options to review and rate after submitting once.
6. You can use logout option for logging out.


Future Improvements:

1. Restricting username, password or other fields to follow certain rules.
2. Adding methods to retrieve username or password when user forgets.
3. Verifying each user before activating account i.e. sending OTP to phone numbers to confirm the phone number of a user when he registers.
4. Encrypting/Decrypting passwords.
5. Adding edit feature to user details and reviews provided by users for books.
6. Styling the web page in a more user friendly way.




