# PictureThis
A webapp that crease a story from a user-provided image. 

Deployed on heroku. (Here is a [link](http://suatakbulut.com/) to the app) 

Accepts an image in .jpg, .jpeg, and .png format. Detects the onject in the image using YOLOV3 object detection algorithm. 
Then creates a short tale using the detected objects' information as keywords. 


## How does it work?

As an example, Let's upload the following "test.jpeg" as an example. 
<img src="ReadMe_Files/test.jpeg" style="height:256px" >

First the Yolov3 algorithm will detect the images inside the image, label them and put them inside boxes as follows:
![Alt text](ReadMe_Files/test_out.jpeg?raw=true "Title")

Detection algorithm, in fact, returns a json file similar to:

Feeding this json into our message text and sending it to writesonic api yields a story, which we then display in our display page. 

### Have fun. 
