Web based Book Review Application

This application is useful for viewing the details of various books and providing feeback on them.

This web application is written mainly in Python (using Flask web framework). Data of around 5000 books is stored in PostgreSQL database, which also stores the details of users and their feedback. Web pages are written using HTML and Javascript with minor styling.


User Guide (Google chrome is suggested website):

1. When user enters the website, Register/Login page will be displayed.
2. If the user's already registered, then the user's credentials can be used to login. Else, he has to register in the website by entering details. To access the website without logging in, the Enter without login link can be used. But, feedback on a book can only be provided for the users who have registered and logged in.
3. After logging in, the user will be directed to the search page. There he can search for books, by providing a substring of Title or ISBN or Author name (For Example: if he enters "ada" in Title, then all the books which contain "ada" in their title will be displayed).
4. After the book names are displayed based on the search, then the user can click on any of the books, to view its details and feedback.
5. After the user enters a specific book page, details of the book along with feedback from users (if any) can be found. If the user is logged in then he can see the options to provide review and rating for that book, but feedback can only be provided once, options to review and rate cannot be found after submitting once.
6. User can use logout option for logging out.


Future Improvements:

1. Restricting username, password or other fields to follow certain rules.
2. Adding methods to retrieve username or password when user forgets.
3. Verifying each user before activating account i.e. sending OTP to phone numbers to confirm the phone number of a user when he registers.
4. Encrypting/Decrypting passwords.
5. Adding edit feature to user details and reviews provided by users for books.
6. Styling the web page in a more user friendly way.

Website Link: https://shan9.herokuapp.com/




