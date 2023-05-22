
# Screening Task Documentation
### Prerequisites 
The prerequisites on a system to run this code for an app are:

- Python 3.6 or later
- PyQt6
- Requests
- Random

			pip install python3-pip 
			pip install pyqt6 
			pip install requests
			pip install random

### GitHub API
GitHub API imposes rate limitations to guard against misuse and guarantee equitable usage for all developers. The amount of API queries that may be made in a given period of time is limited by these rate constraints.

GitHub provides a rate limit of 60 unauthorized API calls per hour for unauthenticated users. And this might be sufficient for a casual end user of this app.

While it might not be sufficient for frequent and ardent users of the app ,  the limitations of the unauthorized rate limits can be overcome by creating a personal access token offered by GitHub .

With the personal access token, users can enjoy an increased rate limit of 5000 API requests per hour.

To create a personal access token, follow these steps:

1.  Visit the GitHub website and log in to your account.
2.  Navigate to your account settings.
3.  Select "Developer settings" and then "Personal access tokens."
4.  Click on the "Generate new token" button.
5.  Provide a descriptive note for the token to identify its purpose.
6.  Specify the scopes or permissions for the token. 
7.  Click "Generate token" to create the token.
8.  Copy the generated token and securely store it. Be cautious not to share it publicly

After generating the PAT, modify the code in the randomimage function to
```
def randomimage():  
	url = 'https://api.github.com/repos/hfg-gmuend/openmoji/contents/src/symbols/geometric?ref=master'  
	pat = 'YOUR PERSONAL ACCESS TOKEN HERE'  
	headers = {"Authorization": f"Bearer {pat}"}  
  
	response = requests.get(url, headers=headers)  
  
	if response.status_code == 200:  
		files = response.json()  
		links = [file["download_url"] for file in files]  
		random.shuffle(links)  
		link = random.choice(links)  
		return link  
  
	else:  
		return "Error!"
```

For more detailed information and guidelines on working with personal access tokens and the GitHub API, refer to the [official GitHub API documentation.](https://docs.github.com/en/rest)

### Quick guide to work with the app
 __On click of button 1__ , random images from the [GitHub repository](https://github.com/hfg-gmuend/openmoji/tree/master/src/symbols/geometric) are rendered at random positions of the canvas considering the size of the app window. They are made selectable (right click) and moveable (left click and drag) .

An image from that repository keeps on appearing whenever this button is clicked, without removing/overwriting the previous images.

Random images that have been rendered can be selected and grouped together __On click of button 2__ , and can be moved along together (left click and drag).

When no image is available to group or no image has been selected to group , and button 2 is clicked , the app raises appropriate messages.

##### Additional Features
- When hovered on a image shown on the canvas , the location, size and color of the image can be known.
The color of the image is almost precise and rarely does show hex codes that are slightly off of the shown color , since hex codes are generated in the program by calculating the average and making approximations (floor division)

- The app also has been provided with an icon for better visual identification and identity.

### Demo

[![Demo for the screening task - Desktop App using Python-PyQt6](https://www.youtube.com/watch?v=w9e5vOQ9Hd4)


