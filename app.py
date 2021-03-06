# 1. Library imports

#from numpy import double
from pydantic import BaseModel 
import uvicorn
from fastapi import FastAPI
from yoloclass import Yolo
from cartoon.functions import Cartoon

# 2. Create the app object
app = FastAPI()

model= Yolo()
cartoon_model=Cartoon()

class Data(BaseModel):
    path: str #image path

# 3. Index route, opens automatically on http://127.0.0.1:8000
@app.get('/')
def index():
    '''
    This is a first docstring.
    '''
    return {'message': 'Hello, strange'}

# 4. Route with a single parameter, returns the parameter within a message
#    Located at: http://127.0.0.1:8000/AnyNameHere
@app.post('/yolov4/')
def yolov4(params: Data):
    '''
    Corre una arquitectura Yolo V4

    '''
    
    boxes, scores, classes, num_objects, no_object = model.yolo_v4(params.path)

    print({
                'boxes': boxes,
                'score': scores,
                'classes': classes,
                'num_objects': num_objects,
                'no_object': no_object}
          )


    return {
                'boxes': boxes,
                'score': scores,
                'classes': classes,
                'num_objects': num_objects,
                'no_object': no_object,
          }
  

@app.post('/cartoon/')
def cartoon(params: Data):
    ''' 
    Deteccion de dibujos animados
    '''
    
    boxes, scores, classes, no_object= cartoon_model.proces_cartoon(params.path)

    if len(boxes)==0:

        return {
                'no_object': no_object,
            }
    
    else:

        return {
                    'boxes': boxes,
                    'score': scores.tolist(),
                    'classes': classes,
                    'no_object': no_object,
            }      
        
# 5. Run the API with uvicorn
#    Will run on http://127.0.0.1:8001
if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=8001)   