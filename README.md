# ChatAPI
This is an API powered with a Machine Learning retrieval chatbot engine.

INSTALLATION
With Python >= 3.10, clone the github repository.
cd into webchat directory containing the requirements.txt file
run pip install -r requirements.txt

STARTING SERVER
From the directory ~webchat directory containing the manage.py file run command python manage.py runserver.
Server can be accessed via http://localhost:8000/

ENDPOINT
REGISTRATION:register/
METHOD:POST
Request Parameters:
{username,email,password,password_confirm}

LOGGING IN: login/
METHOD:POST
Request Parameters:
{username,password}
NOTE: Loggging in returns a refresh and access token.

CHATTING: chat/
METHOD:POST
REQUEST Parameters:
{text}.
NOTE: The access token used for authorization should be sent through the request Header. The Authorization header should have the format Bearer <token> when making requests through postman.

ACCESSING CHAT HISTORY:chat/
METHOD:GET
NOTE: The access token used for authorization should be sent through the request Header. The Authorization header should have the format Bearer <token> when mak
ing requests through postman.

CHECKIN AVAILABLE TOKEN:token/
METHOD:GET
NOTE: The access token used for authorization should be sent through the request Header. The Authorization header should have the format Bearer <token> when mak
ing requests through postman.
