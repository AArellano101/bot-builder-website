# Distinctiveness and Complexity
My project, Tedious.com is a website in which the user deisgns bots. I believe it satisfies the requirements of a distinct and complex project because I think the customisablity is not alike to any other project in this past course. Designing the bots require dragging and dropping blocks that represent actions (alike to shopify or scratch) that the bot will take, and I believe this is one of the reasons it is so disctinct. The simple user interface defines my project to be different because a bot designed by a user is not something similar to any project, because a bot designer is not made in the past course, nor is the ability to create something dynamic. I think is a creative idea to make something like a robot designable by a normal human with no experience, and I believe I did well in allowing so. Another reason I think my project is distinct and complex is because of the simplicity of the design. Although in the back-end code the actions the program does can become very complex, I think that being able to do all these in the press of a button (i.e. the coordinate finder that finds the coordinates of the mouse on the screen ever millisecond, the run button that runs the bot as it is, the keys used for the failsafe while the bot is running, etc.) is both distinctive and complex. I am very proud of the final product of this project, and I am content with the work I have put into it. As well, there is a EXPLORE section in my website in which created can be explored and ran.

# Files

- views.py 

The file in which the back-end code occurs, including the standard redirects, renders, JsonResponses, and django model post/put/get requests, but the actions that the bots use occurs here. PYAUTOGUI is a python library that automates mouse and keyboard actions, and it is used here, getting the customized actions from the webpage and using the data to use it in action. As well, loops that are created in the webpage get translated to a normal form in views.py

- models.py 

For each bot, each action in each bot, and each information of each action in each bot, the data is stored in django models created in models.py

- layout.html

The basic layout of the website for all (non-jsonresponse) paths. Purple heading with three links- the index, create, and explore page.

- index.html

The html layout of the index page, which is the front of the website. Includes descriptions and how-tos of the websites features.

- create.html

The html layout and corresponding javascript of the create page, which allows for the drag and drop user interface for the customisability by dynamically updating the webpage with no need for refreshing. Other main features are the save and run buttons, which update django model and send data of custom bot to views.py to run them. Another feature is the failsafe, which allows for the user to type in a password that they create to stop the bot from running when it is. The other main feature is the coordinate tracker, which, when turned on, sends repeated fetch requests for the mouses coordinates, and displaying on a screen.

- explore.html

Showcases all created bots 

- bot.html

Showcases information on the bot that was selected, and allows for the user to run them and see its actions.

# Runnning

1. Go to directory of capstone file
2. run "python manage.py runserver"
3. In **GOOGLE CHROME**, go to link provided

# IMPORTANT 

**WEBSITE ONLY WORKS ON GOOGLE CHROME, MUST USE GOOGLE CHROME WHILE USING WEBSITE OR ELSE MULTIPLE FEATURES OF THE WEBSITRE WONT WORK**

# AArellano101.github.io
