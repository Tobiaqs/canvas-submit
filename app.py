from canvasapi import Canvas
from canvasapi.upload import Uploader
from canvasapi.requester import Requester
import argparse
from os import environ, path

# Default values for various parameters
default_api_url = None
default_api_token = None
default_assignment = None
default_course = None

# Read parameters from environment variables
if "CANVAS_SUBMIT_API_URL" in environ:
    default_api_url = environ["CANVAS_SUBMIT_API_URL"]

if "CANVAS_SUBMIT_API_TOKEN" in environ:
    default_api_token = environ["CANVAS_SUBMIT_API_TOKEN"]

if "CANVAS_SUBMIT_ASSIGNMENT" in environ:
    default_assignment = environ["CANVAS_SUBMIT_ASSIGNMENT"]

if "CANVAS_SUBMIT_COURSE" in environ:
    default_course = environ["CANVAS_SUBMIT_COURSE"]

# Create an argument parser, passing in the default values as set above
parser = argparse.ArgumentParser("Create a submission on Canvas.")
parser.add_argument("files", nargs="+", type=str, metavar="file", help="A file to submit.")
parser.add_argument("--course", type=int, metavar="ID", required="CANVAS_SUBMIT_COURSE" not in environ, help="The course id. Can also be passed through CANVAS_SUBMIT_COURSE.", default=default_course)
parser.add_argument("--assignment", type=int, metavar="ID", required="CANVAS_SUBMIT_ASSIGNMENT" not in environ, help="The assignment id. Can also be passed through CANVAS_SUBMIT_ASSIGNMENT.", default=default_assignment)
parser.add_argument("--api-url", type=str, metavar="URL", required="CANVAS_SUBMIT_API_URL" not in environ, help="The Canvas base url. Can also be passed through CANVAS_SUBMIT_API_URL.", default=default_api_url)
parser.add_argument("--api-token", type=str, metavar="TOKEN", required="CANVAS_SUBMIT_API_TOKEN" not in environ, help="A valid API token. Can also be passed through CANVAS_SUBMIT_API_TOKEN.", default=default_api_token)

# Read arguments from the parser
args = parser.parse_args()

# Requester necessary for uploading files
requester = Requester(args.api_url, args.api_token)

# Canvas for API calls
canvas = Canvas(args.api_url, args.api_token)

# Method that uploads files and returns a JSON file descriptor
def upload_file(file_path):
    uploader = Uploader(requester, "/api/v1/courses/" + str(args.course) + "/assignments/" + str(args.assignment) + "/submissions/self/files", file_path)
    response = uploader.start()

    if not response[0]:
        print("One of the files (" + file_path + ") could not be uploaded.")
        exit(1)

    return response[1]

# Check that all files actually exist
for file_path in args.files:
    if not path.isfile(file_path):
        print("One of the files (" + file_path + ") does not exist.")
        exit(1)

# Upload all files and store their Canvas IDs
file_ids = []
for file_path in args.files:
    response = upload_file(file_path)
    file_ids.append(response["id"])

# Get the assignment
course = canvas.get_course(args.course)
assignment = course.get_assignment(args.assignment)

# Create a submission
submission = {
    "submission_type": "online_upload",
    "file_ids": file_ids
}

# Post the submission to Canvas
submission_submitted = assignment.submit(submission)

# Print result
print(submission_submitted)