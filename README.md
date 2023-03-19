# API-tutorial-with-FastAPI-build-on-Docker
I have built two API systems in this tutorial.
One main API which does everything except changing the name to base64.
Task in main API, 
1. User can upload any file.
2. If uploaded file is in tsv format, it will display data in json format and provide a link for download the data in csv format.
3. If upload file is in image, it will save it for drawing bounding box on it.
4. User can type the bounding box start point (x, y), and width and height of bounding box. If bounding box does not fit to image, it will display an error.
5. User can type a name input and if the name is user's name, it will call another API to convert the name from string input to base64.

Another API which change the string input to base 64.

Both API are host on one docker compose file which are added together in a docker network.
