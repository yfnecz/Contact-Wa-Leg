from flask import Flask, render_template, request, redirect, url_for, session
import cohere, pandas as pd, requests
from prompt import prompt
from apikeys import api_keys
from db import db
from representatives import repr
from shapefiles import shapefiles


app = Flask(__name__)


db = db.Database()
base_prompt = prompt.Prompt()
api = api_keys.api_keys()
(ai_key, maps_api_key, site_key, site_secret, app_secret) = api.get_keys()
repr_get = repr.DistrictRepresentatives()
shp = shapefiles.LegislativeDistrictLocator()

app.secret_key = app_secret

def clean_legislators(legislators):
    for leg in legislators:
        for key in ['la', 'la_email', 'position']:
            if pd.isna(leg.get(key)):
                leg[key] = ''
    return legislators

@app.route("/", methods=["GET", "POST"])
def index():
    name = request.args.get('name', '')
    address = request.args.get('address', '')
    intro_text = base_prompt.get_intro_text()
    if request.method == "POST":
        return redirect(url_for('index'))
    return render_template("index.html", google_api_key=maps_api_key, site_key=site_key, intro_text=intro_text)

@app.route("/results", methods=["GET", "POST"])
def results():
    if request.method == "POST":
        recaptcha_response = request.form.get('g-recaptcha-response')
        verify_url = "https://www.google.com/recaptcha/api/siteverify"
        payload = {'secret': site_secret, 'response': recaptcha_response}
        r = requests.post(verify_url, data=payload)
        result = r.json()
        if not result.get('success'):
            # Show the form again with an error
            return render_template(
                "index.html",
                error="Please complete the CAPTCHA.",
                google_api_key=maps_api_key,
                site_key=site_key
            )
        name = request.form.get("name")
        address = request.form.get("address")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        user_addition = request.form.get("user_addition", "")
        
        district_info = shp.get_district(lat, lng)
        district_number = district_info['ID']
    
        if not district_number:
            return render_template(
                "index.html",
                error="Could not determine your legislative district. Please check your address.",
                google_api_key=maps_api_key,
                site_key=site_key
            )
        
        representatives = repr_get.get_representatives(district_number)
        representatives = clean_legislators(representatives)
        
        new_prompt = base_prompt.get_prompt()
        if user_addition:
            new_prompt += f"\n\nThe constituent adds: {user_addition.strip()}"

        try:
            db.increment_usage()
            co = cohere.Client(ai_key)
            response = co.chat(
                model="command-a-03-2025",
                message=new_prompt,
                temperature=1.0,
                p=0.9,
                k=40,
                max_tokens=500
            )
            response = response.text

        except Exception as e:
            print(f"Error calling Cohere API: {e}")
            response = "An error occurred while generating the message."

        message_body = response.strip()
        subject = "Message from Constituent"

        if response.startswith("Subject:"):
            subject, _, body = response.partition('\n')
            subject = subject.replace("Subject:", "").strip()
            message_body = body.strip()

        message_body += f"\n{name.strip()}\n{address.strip()}\n"

        # Store data in session instead of URL
        session['name'] = name
        session['address'] = address
        session['subject'] = subject
        session['message'] = message_body
        session['district'] = district_number
        session['representatives'] = representatives
        
        return redirect(url_for('results'))
    
    required_keys = ['name', 'address', 'representatives', 'subject', 'message', 'district']
    if not all(key in session for key in required_keys):
        # Redirect to index if session data is missing
        return redirect(url_for('index'))

    # Get data from session
    return render_template(
        "results.html",
        name=session.get('name'),
        address=session.get('address'),
        legislators=session.get('representatives'),
        subject=session.get('subject'),
        message=session.get('message'),
        district=session.get('district')
    )


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=10000)
