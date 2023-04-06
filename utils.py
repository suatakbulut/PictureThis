from imageai.Detection import ObjectDetection
import os
import requests
import json 

def create_output_filename(filename):
    splits = filename.split(".")
    output_filename = ".".join([ splits[0] + "_out", splits[1] ])
    return output_filename


def detected_objects(filename):
    # Initilialize ObjectDetection    
    detector = ObjectDetection()
    detector.setModelTypeAsYOLOv3()
    # model_path - currently only yolov3
    execution_path = os.getcwd()
    model_path = os.path.join(execution_path, "static/models/yolov3.pt")
    detector.setModelPath(model_path)

    detector.loadModel()
    output_filename = create_output_filename(filename)
    detections = detector.detectObjectsFromImage(input_image=filename, output_image_path=output_filename, minimum_percentage_probability=30)
    return detections


def create_content(detections):
    content = f"""
        I will provide you with the "name", "percentage_probability", and "box_points" outputs of a YOLOV3 object detection algorithm I run on a custom image. 
        I want you to come up with a tale about this image. 
        Please include a title as well. 
        Surprise the reader. 
        Do not say anything about YOLOV3, object detection, or AI. 
        Here is the output of YOLOV3: {detections}
        """
    content = content.replace("\n", "")
    return content


def request_story(content, api_key):
    url = "https://api.writesonic.com/v2/business/content/chatsonic?engine=premium"

    payload = {
        "enable_google_results": False,
        "enable_memory": False,
        "input_text": content
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API-KEY": api_key
    }

    response = requests.post(url, json=payload, headers=headers)
    response = json.loads(response.text)["message"]
    r = response.split("\n")
    title = r[0] 
    title = title.replace("Title: ", "")
    paragraphs = [p for p in r[1:] if p]
    return title, paragraphs


def is_auth_exist():
    return ("auth.json" in os.listdir())


def get_apikey():
    if is_auth_exist():
        with open("auth.json", "r") as f:
            auth = json.load(f)
        return auth["api_key"]
    else:
        # For now use this dummy api_key
        return "025654ee-be7d-45fc-8f50-a3dbd67372b5"


def get_story(filename):
    detections = detected_objects(filename)
    content = create_content(detections)
    api_key = get_apikey()
    title, paragraphs = request_story(content, api_key)
    return title, paragraphs