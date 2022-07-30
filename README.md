# MakiLab
### Video hosting

MakiLab is a videohosting,  \
And it is written in Sanic and ReactJS. \
***

###### Deploy information 
Data storage is being mounted into www/videos directory. 
It must contain two directories with content.  \
First, with video previews.  \
Second, with videos.  \ 
You can change the videos and previews directory names in src/config.py file.  \

All the files from www directory are being served with NGINX, and not the Sanic application.  \

