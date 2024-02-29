Pythonanywhere deployed url: https://sc20jtj.pythonanywhere.com
Module leader login details:
  - Username: ammar
  - Password: ModuleLeader123

Client Instructions:
To pass in parameters to the commands, you need to leave a space between each parameter. For example command parameter1 parameter2 etc.
Commands:
  - exit:
    Parameters: This command has no parameters.
    This command will exit the client.

  - login:
    Parameters:
      url (REQUIRED): The url of the service you want to log in.
      Example login https://sc20jtj.pythonanywhere.com
    This command will log you in to the service passed in from the url parameter, and the commands logout, post and delete will use this url to send the requests to.
    This command will ask for your username and password, and will log you in to the system if valid credentials have been passed in.
  
  - logout
    Parameters: This command has no parameters.
    This command will log you out, and will forget the url you passed in (if login has been run) during login. In order to use post and delete commands you will need to log back in with a valid url and valid credentials.

  - post
    Parameters: This command has no parameters.
    This command will only run if a valid url is passed and you are logged in successfully.
    This command will ask you to pass in a value for headline, category, region and details, and will create a new news post on the directory logged in under the author of the logged in user.

  - news
    Parameters:
      -id= (optional) The id of the service you want to get news from, if left out it will get news from all services.
      -cat= (optional) Filters the news by the category provided, if left out it will get news for all categories.
      -reg= (optional) Filters the news by the region provided, if left out it will get news for all regions.
      -date= (optional) Filters the news by the date provided,it will filter the date by any news published on or after the date provided, if left out it will get news for all dates.
      Example: news -id=jtj02 -cat=tech -reg=uk -date=24/02/2024
    This command will get a list of all news stories from the filters provided. It will give the key, headline, category, region, author, date and details for the filtered news stories. 

  - list
  Parameters: This command has no parameters.
  This command will get a list of all news services. This will get the agency name, url and code of all services.

  - delete
  Parameters:
    story_key (REQUIRED) The key of the story you want to delete from the news provider.
    Example: delete 9
  This command will delete the new story with the key provided by the user, and it will delete the story on the service logged in to.


