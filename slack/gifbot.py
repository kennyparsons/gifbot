import os
import re
import requests

IMAGE_REGEX = re.compile(r"<@.*?>\s+(?P<image_name>\w+\.gif)")

GIF_REPO_URL = "https://gifs.example.com/"

def handler(req, res):
    # Extract the message text from the request body
    message_text = req.get("text")

    # Check if the message matches the image request pattern
    match = IMAGE_REGEX.match(message_text)
    if match:
        # Extract the image name from the message
        image_name = match.group("image_name")

        # Construct the URL of the image
        image_url = GIF_REPO_URL + image_name

        # Download the image
        response = requests.get(image_url)

        # Send the image as a response to the original message
        res.status(200).send({
            "blocks": [
                {"type": "image", "image_url": image_url, "alt_text": image_name}
            ]
        })
    else:
        # If the message doesn't match the image request pattern, send an error message
        res.status(200).send({"text": "Sorry, I didn't understand that."})

# Start the app
if __name__ == "__main__":
    app = Vercel(handler=handler)
    app.listen()
