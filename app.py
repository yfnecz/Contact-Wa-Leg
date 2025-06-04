from flask import Flask, render_template, request, redirect, url_for
import cohere

app = Flask(__name__)

with open("/Users/Natali/PycharmProjects/contact-wa/flask-template/api.key") as file:
    api_key = file.read().strip()
with open("/Users/Natali/PycharmProjects/contact-wa/flask-template/geo-api.key") as file:
    geo_api_key = file.read().strip()
with open("/Users/Natali/PycharmProjects/contact-wa/flask-template/ai.key") as file:
    ai_key = file.read().strip()

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
    return render_template("index.html", google_api_key=api_key, geo_api_key=geo_api_key)


@app.route("/results")
def results():
    # Dummy legislators
    legislators = [
        {"name": "Rep. Alice Smith", "district": "District 1"},
        {"name": "Sen. Bob Johnson", "district": "District 1"}
    ]

    name = request.args.get("name")

    # Pre-filled message
    prompt = f"""
You are a concerned constituent from Washington State writing a heartfelt letter to your state legislator about improving child custody and visitation laws to better protect children from potentially dangerous parents.

Recently, a tragic case in Wenatchee involving the Decker girls exposed serious gaps in the current laws.

Washington State passed a bill, SB 5175, in April 2025 to address some of these concerns, but sadly it was not enough to prevent this tragedy.

Other states, like California with its AB 275 law, have implemented more effective measures, including emergency custody modifications and closer monitoring of parents with mental health or compliance challenges.

Use these facts to craft a sincere, respectful, and urgent message urging [leg_name] to consider strengthening Washington’s laws, perhaps by amending or expanding SB 5175 to better safeguard children.

Make sure each message you generate is unique: vary sentence structures, word choices, and tone slightly while maintaining clarity and respect.

Feel free to add natural personal touches or emotions to make the letter sound like it truly comes from a concerned citizen.

Include the name of the message sender as {name} in a natural way.

Only return the message content itself—no explanations, formatting notes, or AI disclosures.

Do not include all details every time; use the information flexibly to create a fresh, authentic letter each time.

"""

    co = cohere.ClientV2(ai_key)
    response = co.chat(
        model="command-a-03-2025", 
        messages=[{"role": "user", "content": prompt}]
    )

    return render_template(
        "results.html",
        name=request.args.get("name"),
        address=request.args.get("address"),
        legislators=legislators,
        message=response.message.content[0].text
    )


if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=5000)
