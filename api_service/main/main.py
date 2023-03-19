from typing import List
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse, JSONResponse
import requests
import shutil
''' 
shutil.copyfileobj() method in Python is used to copy the contents of a file-like object to another file-like object. 
By default this method copy data in chunks and if want we can also specify the buffer size through length parameter. '''
import socket
import pandas as pd
import cv2
# import uvicorn

app = FastAPI()   # make app
img_name = ""     # declaring img name

@app.get("/")
async def root():
    ''' This is root funtion '''
    return {"message": "Welcome to Min Task"}

@app.post('/upload_file') 
async def upload_tsv(file: UploadFile = File(...)):
    ''' Any files can be uploaded. 
    if tsv file is uploaded from UI --> it will be converted to csv and save it.
    Otherwise --> it will check if the file is img file type. If yes, img_name will store the img file name. 
    After that, it will return the message about {filename} is not tsv format.
    '''
    global img_name, csv_file_name                # declaring global variables
    with open(f'{file.filename}', "wb") as buffer: 
        shutil.copyfileobj(file.file, buffer)
    file_name = file.filename.split('.')[0]       # to get file name without file format "example: .tsv"
    file_type = file.filename.split('.')[1]       # to get file type "example: tsv"
    if file_type == "tsv":                        # check if file type is in tsv
        tsv_input = pd.read_csv(file.filename,sep ='\t')  # create a data frame from tsv
        csv_file_name = file_name + '.csv'                # store the csv file name
        tsv_input.to_csv(file_name + '.csv', index=False) # save the csv file from data frame
        return JSONResponse(content = tsv_input.to_dict(orient = "records")) # returning tsv is conveted to csv
    else: 
        if file_type == "jpg" or file_type == "jpeg" or file_type == "png":  # check if it is img file
            img_name = file.filename                                         # store img file name
        return {"message": f"{file.filename} is not tsv format"}             # returning that file type is not tsv as rquested in task 1

@app.get("/download")                                           
async def download_file():
    ''' This function provide a downloadable csv file converted from tsv file '''
    global csv_file_name
    if csv_file_name == "":
        return {"message": "Please upload tsv file"}             # To request user to input tsv file
    else:
        file_path = csv_file_name                                # Replace with the path to your file
        return FileResponse(file_path, filename= csv_file_name)  # return downloadable file

@app.post('/get_bounding_box')                                   
def read_coordinates(x_topleft: int, y_topleft: int, width: int, height: int):
    ''' This function will request coordinates of bounding box and check if it fit to image'''
    global img_name                                              # declaring img_name as global variable
    if img_name == "":                                           # check if img is uploaded
        return {"message":"Please upload an image."}             # request user to upload image
    else:
        input_img = cv2.imread(img_name)                         # read the image
        if x_topleft >= 0 and y_topleft >= 0 and x_topleft + width <= input_img.shape[1] and y_topleft + height <= input_img.shape[0]: # check if bb is larger than img size
            color = (0, 255, 0)                                                                                # set color to green of bounding box
            thickness = 2                                                                                      # set thickness of bounding box
            cv2.rectangle(input_img, (x_topleft, y_topleft), (x_topleft + width, y_topleft + height), color, thickness)                # draw bounding box
            cv2.imwrite(img_name, input_img)
            return FileResponse(img_name, media_type="image/jpeg")          # returning the image file that include bounding box
        else:
            return {"message": "Bouning box does not fit the input image"}  # returning that bounding box is not fit to image as rquested in task 2

@app.post('/input_name')
def get_name(name: str):
    ''' This function will check if the input is my name.
    If yes, it will convert it to base64 by using another api from another docker.
    Otherwise, it  will return the message that input is not my name'''
    my_name = ''.join(name.split(" ")).lower()             # if name is written seperately, remove space and change all to lower case
    ip_address = get_ip()                                  # get ip address of current docker
    seperate_ip = ip_address.split(".")                    # split and assign each number in list
    seperate_ip[3] = 1                                     # changing the last item to docker network ip
    Docker_network_ip = '.'.join(map(str, seperate_ip))    # joining ip number together as string
    if my_name == "minkhantsoe" or my_name == "min":       # check if it is my name
        response = requests.get(f"http://{Docker_network_ip}:5000/input_string?input_string={my_name}") # send input to another api from another docker
        data = response.json()
        return {"message": f"base64 string of {name} is {data['base64_string']}."}                      # returning the base64 string to check
    else:
        return {"message": f"{name} is not my name."}      # returning that name is not my name as requested in task 3

def get_ip(): 
    ''' This function will return the ip address of the current docker'''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_address = s.getsockname()[0]
    s.close()
    return ip_address  


