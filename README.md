# [Contact Your Washington State Legislators](https://contact-wa-legislators.onrender.com/)

This is a Flask web application that helps Washington State residents easily contact their state legislators. Users enter their name and address, and the app automatically finds their legislative district and representatives. The app uses AI to generate a personalized message and subject line, which users can review and send directly to their lawmakers via email.

## Features

- **Address Lookup:** Enter your address and the app finds your legislative district and representatives.
- **Legislator Info:** Displays names, contact details, and assistants for your state senator and representatives.
- **AI Message Generation:** Uses Cohere AI to generate a personalized email subject and message based on your input and optional personal note.
- **Editable Message:** Users can review and edit the AI-generated message before sending.
- **One-Click Email:** Send your message to your legislators with a single click.
- **reCAPTCHA Protection:** Prevents spam and abuse with Google reCAPTCHA.
- **Modern UI:** Clean, responsive design for desktop and mobile.

## Tech Stack

- Python 3 / Flask
- Cohere AI API
- Google Maps APIs
- reCAPTCHA
- Docker support for easy deployment

## Deployed on [Render](https://contact-wa-legislators.onrender.com/)

## Getting Started

1. **Clone the repository**
2. **Install dependencies:**  
   `pip install -r requirements.txt`
3. **Set up API keys:**  
   Place your API keys in the `apikeys/` directory as described in the code.
4. **Edit the prompt for message generation**
   `prompt/prompt.txt`
   `prompt/info.txt`
6. **Run the app:**  
   `python app.py`
7. **Open in browser:**  
   Visit `http://localhost:10000`

## Docker

To build and run with Docker (don't forget to put keys into your local apikeys/ folder):

You can just pull the image from GitHub Packages:

```sh
docker pull ghcr.io/yfnecz/contact-wa-leg:latest
docker run -p 10000:10000 -v /data -v $(pwd)/apikeys:/etc/secrets --rm ghcr.io/yfnecz/contact-wa-leg:latest
```

Or build it:


```sh
docker build -t contact-wa-leg:latest .
docker run -p 10000:10000 -v /data -v $(pwd)/apikeys:/etc/secrets --rm contact-wa-leg:latest
```

## Contributing

Pull requests and suggestions are welcome!  

## Data

Shapefiles can be downloaded here (if updated):
[Shapefiles](https://geo.wa.gov/datasets/wa-ofm::washington-state-legislative-districts-2024/about)

List of legislators can be downloaded here (if update is needed):
[List of legislators](https://leg.wa.gov/legislators/?activeView=MemberList)

## Example

![Screenshot 2025-06-16 at 11 08 46 AM](https://github.com/user-attachments/assets/25fbf0cc-f20d-47b4-9036-f8ebce85a8c2)

![Screenshot 2025-06-16 at 11 09 02 AM](https://github.com/user-attachments/assets/3a408265-cb47-449d-aec7-fd8085633959)

![Screenshot 2025-06-16 at 11 09 12 AM](https://github.com/user-attachments/assets/ff1eaf35-782d-462f-95db-449e34c0a15a)


---

**Contact:** yfnecz@gmail.com
