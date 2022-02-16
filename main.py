import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from job import set_dict_redis,get_dict_redis,pipeline
from rq import Queue
from redis import Redis
import glob
from fastapi.middleware.cors import CORSMiddleware
import random


q = Queue(connection=Redis(host='redis'))
app = FastAPI()

from typing import List
import shutil 

set_dict_redis("image_status", {})
set_dict_redis("candidate_list", {})


origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload(candidate_id, uploaded_file: List[UploadFile] = File(...)): 
    for img in uploaded_file:
        file_location = f"uploaded/{img.filename}"
        with open(file_location, "wb") as file_object:
            shutil.copyfileobj(img.file, file_object)  
        key = img.filename.split('.')[0]

        image_status = get_dict_redis("image_status")
        image_status[key] = {"Status":"Unprocessed","Details":{},"candidate_id":candidate_id}
        
        set_dict_redis("image_status", image_status)

        print(key)
        print("Image Status: ", get_dict_redis("image_status"))
        print(q)

        q.enqueue(pipeline,img.filename)
    return "done"

@app.get("/fileinfo")
async def fileinfo():
    list_files=glob.glob("uploaded/*.png")
    keys=[x.split("/")[-1].split('.')[0] for x in list_files]
    all={}
    for key in keys:
        temp=get_dict_redis("image_status")[key]
        all[key]= temp["Status"]
    return all

@app.get("/filedetails")
async def fileDetails(fileid):
    temp=get_dict_redis("image_status")[fileid]
    return temp

@app.post("/processed")
async def process_image(fileid):
    response = FileResponse(path='processed/'+fileid+".png",media_type="image/png")
    return response

@app.post("/thumbnail")
async def thumbnail_image(fileid):
    response = FileResponse(path='uploaded/'+fileid+".png",media_type="image/png")
    return response
    
@app.post("/addCandidates")
async def addCandidate(candidateId, name, status):
    candidate_list = get_dict_redis("candidate_list")
    candidate_list[candidateId] = {
        "Name":name,
        "Status":status
    }
    set_dict_redis("candidate_list",candidate_list)
    return "Updated"

@app.get("/candidateInfo")
async def CandidateInfo():
    candidate_list = get_dict_redis("candidate_list")
    image_status = get_dict_redis("image_status")

    educational_details = {}
    
    for candidate_id in candidate_list:
        educational_details[candidate_id] = []

    for image_name in image_status:
        if image_status[image_name]["Status"]=="Processed":

            img_details = image_status[image_name]["Details"]
            
            details = {
                "certificate_file_Name":image_name,
                "Qualification":"",
                "Board_University":"",
                "Year":random.randint(2000,2012),
                "Marks_CGPA":"",
                "status":"Approved"
            }

            if "TOTAL_MARKS" in img_details:
                details["Marks_CGPA"] = img_details["TOTAL_MARKS"]
            elif "CGPA" in img_details:
                details["Marks_CGPA"] = img_details["CGPA"]
            else:
                details["Marks_CGPA"] = " "


            if "BOARD" in img_details:
                details["Board_University"] = img_details["BOARD"]
            else:
                details["Board_University"] = img_details["University"]


            if "LEVEL" in img_details:
                details["Qualification"] = img_details["LEVEL"]
            else:
                details["Qualification"] = "GRADUATE"
            

            educational_details[image_status[image_name]["candidate_id"]].append(details)
    print("Candidate List: ",candidate_list)
    print("")
    print("Education Details: ",educational_details)
    output_details = []
    for candidate_id in candidate_list:
        candidate_info = candidate_list[candidate_id]
        candidate_info["Id"] = candidate_id
        candidate_info["Education_Certificates"] = educational_details[candidate_id]
        output_details.append(candidate_info)

    return output_details

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


