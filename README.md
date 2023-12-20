# Secure-File-Sharing-System

Development:
1. Framework used- Flask
2. Database used- SQL (SQLite)

IMP:
1. The main.py file is the server/app file.(run it before using postman)
2. For the email verification please add your email id and password in the code for the email verification process.( in the main.py file under client_user_signup function)
3. Include the id of the file to be downloaded in the URL path
4. Please install all the depencencies using requirements.txt before running the main.py file
5. Already registered users:
   a. Ops user: username-aditya101, password-adityasingh
   b. Client user: username-abhishek101, password-abhisheksingh

I included .docx instead of .doc as i work on windows 11, but .doc can also be easily be included in the code.

## Test cases:
1. Test logging in as an Ops User with valid and invalid credentials.
2. Test uploading a valid file (pptx, docx, xlsx) and invalid file as an Ops User.
3. Test uploading a file as a Client User (should be denied).
4. Test logging as a Client User with valid and invalid credentials.
5. Test signing up with an already registered email.
6. Test downloading a file with an invalid/expired download link.
7. Test downloading a non-existent file (should be denied).

## How I plan on deploying this to the production environment:
1. Securing the database
2. Using https to protect the data being transmitted
3. Decreasing the response time by optimizing the server
4. Using environment variables for sensitive information such as email id and password
5. Using CDN for sending files

