from flask import Flask, render_template, request, redirect, url_for
import cohere
from prompt import prompt
from apikeys import api_keys
from db import db

app = Flask(__name__)

db = db.Database()
base_prompt = prompt.Prompt()
api = api_keys.api_keys()
(ai_key, maps_api_key, geo_api_key) = api.get_keys()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        address = request.form.get("address")
        street_number = request.form.get("street_number")
        route = request.form.get("route")
        locality = request.form.get("locality")
        administrative_area_level_1 = request.form.get("administrative_area_level_1")
        postal_code = request.form.get("postal_code")
        lat = request.form.get("lat")
        lng = request.form.get("lng")
        # For now, just pass all data to the results page
        return redirect(url_for(
            "results",
            name=name,
            address=address,
            street_number=street_number,
            route=route,
            locality=locality,
            state=administrative_area_level_1,
            postal_code=postal_code,
            lat=lat,
            lng=lng
        ))
    return render_template("index.html", google_api_key=maps_api_key, geo_api_key=geo_api_key)


@app.route("/results")
def results():
    # Dummy legislators
    legislators = [
        {"name": "Rep. Alice Smith", "district": "District 1"},
        {"name": "Sen. Bob Johnson", "district": "District 1"}
    ]

    # name = request.args.get("name")
    new_prompt = base_prompt.get_prompt()

    try:
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
        db.cache_response(response)

    except Exception as e:
        print(f"Error calling Cohere API: {e}")
        cached_response = db.get_random_cached_response()
        if cached_response:
            response = cached_response
        else:
            response = "An error occurred while generating the message."

    return render_template(
        "results.html",
        name=request.args.get("name"),
        address=request.args.get("address"),
        legislators=legislators,
        message=response
    )


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
