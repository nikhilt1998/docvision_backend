import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from utils.redis_fun import set_dict_redis,get_dict_redis
from rq import Queue
from redis import Redis
import glob
from fastapi.middleware.cors import CORSMiddleware
import random
from typing import List
import shutil
from ocr_pipeline.pipeline import pipeline
from utils.certi_preprocess import deskew_img


print("This is main file")
q = Queue(connection=Redis(host='redis'))
app = FastAPI()

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
    """
    Post endpoint to upload multiple images tagged to one candidate
    Inout: Candidate ID, List<Images>
    Output: Success/Error
    """
    for img in uploaded_file:
        # Save the uploaded_docs image in uploaded_docs folder
        file_location = f"data/uploaded_docs/{img.filename}"
        with open(file_location, "wb") as file_object:
            shutil.copyfileobj(img.file, file_object)
        
        # Deskew the image using haugh transform and replace the previous image
        deskew_img(file_location)

        key = img.filename.split('.')[0]

        # setting up the redis directory 
        image_status = get_dict_redis("image_status")
        image_status[key] = {"Status":"Unprocessed","Details":{},"candidate_id":candidate_id}
        set_dict_redis("image_status", image_status)

        print(key)
        print("Image Status: ", get_dict_redis("image_status"))
        print(q)

        # adding the image in redis queue for processing
        q.enqueue(pipeline,img.filename)
    return "done"

@app.get("/fileinfo")
async def fileinfo():
    """
    Get endpoint to get the processing state of the image
    Input: None
    Output: File Name, Processing state
    """
    list_files=glob.glob("data/uploaded_docs/*.png")
    keys=[x.split("/")[-1].split('.')[0] for x in list_files]
    all={}
    for key in keys:
        temp=get_dict_redis("image_status")[key]
        all[key]= temp["Status"]
    return all

@app.get("/filedetails")
async def fileDetails(fileid):
    """
    Get endpoint to fetch the extracted information for the image once processed_docs
    Input: File name
    Output: details (JSON)
    """
    temp=get_dict_redis("image_status")[fileid]
    return temp

@app.post("/processed")
async def process_image(fileid):
    """
    Post endpoint to fetch the processed_docs image
    Input: File Name
    Output: processed_docs Image 
    """
    response = FileResponse(path='data/processed_docs/'+fileid+".png",media_type="image/png")
    return response

@app.post("/thumbnail")
async def thumbnail_image(fileid):
    """
    Post endpoint to fetch the original image
    Input: File Name
    Output: Originale Image
    """
    response = FileResponse(path='data/uploaded_docs/'+fileid+".png",media_type="image/png")
    return response
    
@app.post("/addCandidates")
async def addCandidate(candidateId, name, status):
    """
    Post endpoint to add the candidate information.
    Input: Candidate ID, Candidate name, Current candiate status
    Output: Success/Error
    """
    candidate_list = get_dict_redis("candidate_list")
    candidate_list[candidateId] = {
        "Name":name,
        "Status":status
    }
    set_dict_redis("candidate_list",candidate_list)
    return "Updated"

@app.get("/candidateInfo")
async def CandidateInfo():
    """
    Get endpoint to fetch candidate information
    Input: None
    Output: Candidate Details (JSON)
    """
    candidate_list = get_dict_redis("candidate_list")
    image_status = get_dict_redis("image_status")

    educational_details = {}
    
    for candidate_id in candidate_list:
        educational_details[candidate_id] = []

    for image_name in image_status:
        if image_status[image_name]["Status"]=="processed_docs":

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


