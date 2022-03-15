#!/bin/bash

# example of using arguments to a script
python ./ocr_pipeline/pipeline.py &
rq worker --url redis://redis &
uvicorn main:app --host 0.0.0.0 --port 8000
