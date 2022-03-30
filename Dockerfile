# Some container that is already suitable for unicover
FROM 4108748/ocr-base-image
# ADD uploaded /app/uploaded
# ADD processed /app/processed
# ADD ner /app/ner
# ADD ./job.py /app/
# ADD ./ner.py /app/
# ADD ./spell_checker.py /app/
# ADD ./states.py /app/
# ADD ./words.txt /app/
# ADD ./main.py /app/
# ADD ./start.sh /app/
# ADD ./university.py /app/
# ADD ./deg_cert.py /app/
# ADD ./univer_spl.py /app/ 
WORKDIR '/usr/src/app/'
RUN python /usr/src/app/ocr_pipeline/pipeline.py
RUN chmod +x /usr/src/app/ocr_pipeline/pipeline.py/start.sh
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["bash","/usr/src/app/start.sh"]