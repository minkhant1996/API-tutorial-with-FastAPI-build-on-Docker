from fastapi import FastAPI
import base64
import uvicorn
app = FastAPI() # make app

@app.get("/")
async def root():
    ''' This is root funtion '''
    return {"message": "Welcome to Min Task base64"}

@app.get('/input_string') 
def get_string_input(input_string: str):                              # get string input
    ''' This function will convert name string to base64 string'''
    bytes_to_encode = input_string.encode('utf-8')                    # Convert a string to bytes
    base64_bytes = base64.b64encode(bytes_to_encode)                  # Encode the bytes as Base64
    base64_str = base64_bytes.decode('utf-8')                         # Convert the Base64 bytes to a string
    # print(base64_str)
    return {"base64_string": base64_str} 

# if __name__ == "__main__":
#     uvicorn.run(app, host="127.0.0.1", port=5000)