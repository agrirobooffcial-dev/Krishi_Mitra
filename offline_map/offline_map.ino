#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

ESP8266WebServer server(80);
TinyGPSPlus gps;
SoftwareSerial gpsSerial(14, 12);

// GPS values
double lat = 0.0, lng = 0.0;
double speed_kmph = 0.0;
double course_deg = 0.0;
double totalDistance = 0.0;

// Previous point
double prevLat = 0.0, prevLng = 0.0;
bool hasPrev = false;

void handleRoot() {
  String page =
"<!DOCTYPE html><html><head>"
"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
"<title>Krishi Mitra GPS</title>"
"<style>"
"body{font-family:Arial;background:#111;color:#0f0;text-align:center;}"
".box{border:1px solid #0f0;padding:10px;margin:10px;font-size:18px;}"
"</style>"
"</head><body>"

"<h2>Krishi Mitra – Offline GPS</h2>"
"<div class='box'>Latitude: <span id='lat'>--</span></div>"
"<div class='box'>Longitude: <span id='lng'>--</span></div>"
"<div class='box'>Speed (km/h): <span id='spd'>--</span></div>"
"<div class='box'>Heading (°): <span id='hdg'>--</span></div>"
"<div class='box'>Distance (m): <span id='dist'>0</span></div>"

"<script>"
"function update(){"
"fetch('/gps').then(r=>r.json()).then(d=>{"
"lat.innerText=d.lat.toFixed(6);"
"lng.innerText=d.lng.toFixed(6);"
"spd.innerText=d.spd.toFixed(2);"
"hdg.innerText=d.hdg.toFixed(2);"
"dist.innerText=d.dist.toFixed(2);"
"});"
"}"
"setInterval(update,1000);"
"</script>"

"</body></html>";

  server.send(200, "text/html", page);
}

void handleGPS() {
  String json = "{";
  json += "\"lat\":" + String(lat,6) + ",";
  json += "\"lng\":" + String(lng,6) + ",";
  json += "\"spd\":" + String(speed_kmph,2) + ",";
  json += "\"hdg\":" + String(course_deg,2) + ",";
  json += "\"dist\":" + String(totalDistance,2);
  json += "}";

  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);

  // ESP8266 Access Point (offline)
  WiFi.mode(WIFI_AP);
  WiFi.softAP("Krishi_Shatru", "12345678");

  Serial.print("AP IP: ");
  Serial.println(WiFi.softAPIP()); // 192.168.4.1

  server.on("/", handleRoot);
  server.on("/gps", handleGPS);
  server.begin();
}

void loop() {
  while (gpsSerial.available()) {
    gps.encode(gpsSerial.read());
  }

  if (gps.location.isUpdated()) {
    lat = gps.location.lat();
    lng = gps.location.lng();

    speed_kmph = gps.speed.kmph();
    course_deg = gps.course.deg();

    if (hasPrev) {
      totalDistance += TinyGPSPlus::distanceBetween(
        prevLat, prevLng, lat, lng
      );
    }

    prevLat = lat;
    prevLng = lng;
    hasPrev = true;
  }

  server.handleClient();
}