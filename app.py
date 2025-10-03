from flask import Flask, render_template, request
import requests
import folium

app = Flask(__name__)

# Function to get geolocation info by IP
def get_location(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}").json()
        if response.get("status") == "success":
            return {
                "lat": response.get("lat"),
                "lon": response.get("lon"),
                "city": response.get("city"),
                "region": response.get("regionName"),
                "country": response.get("country"),
                "isp": response.get("isp")
            }
    except Exception as e:
        print("Error in get_location:", e)
    return None

@app.route("/", methods=["GET", "POST"])
def index():
    location = None
    map_html = None

    if request.method == "POST":
        ip = request.form.get("ip", "").strip()
        if ip:
            location = get_location(ip)
            if location:
                # Create map with folium
                m = folium.Map(location=[location["lat"], location["lon"]], zoom_start=10)
                folium.Marker(
                    [location["lat"], location["lon"]],
                    popup=f"{location['city']}, {location['country']} ({location['isp']})"
                ).add_to(m)
                map_html = m._repr_html_()

    return render_template("index.html", location=location, map_html=map_html)

if __name__ == "__main__":
    app.run(debug=True)
