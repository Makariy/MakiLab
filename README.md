# MakiLab
### Video hosting

MakiLab is a videohosting,  <br />
And it is written in Sanic and ReactJS.  <br />

***

##### Deploy information 

###### Data storage
Data storage is being mounted into www/videos directory. 
It must contain two directories with content.  <br />
First, with video previews.  <br />
Second, with videos.  <br />
You can change the videos and previews directory names in src/config.py file.  <br />

###### Serving data
All the files from www directory are being served with NGINX, and not the Sanic application.  <br />

