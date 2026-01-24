#include <ESP8266WiFi.h>
#include <ESP8266WebServer.h>
#include <TinyGPSPlus.h>
#include <SoftwareSerial.h>

const char* ssid = "Shayak";
const char* password = "m2f9nhsn";

ESP8266WebServer server(80);
TinyGPSPlus gps;
SoftwareSerial gpsSerial(14, 12);

double lat = 0.0;
double lng = 0.0;

void handleRoot() {
  String html =
"<!DOCTYPE html>"
"<html>"
"<head>"
"<meta name='viewport' content='width=device-width, initial-scale=1.0'>"
"<title>ESP8266 GPS Tracker</title>"
"<link rel='stylesheet' href='https://unpkg.com/leaflet/dist/leaflet.css'/>"
"<style>#map{height:100vh;}</style>"
"</head>"
"<body>"
"<div id='map'></div>"

"<script src='https://unpkg.com/leaflet/dist/leaflet.js'></script>"
"<script>"
"var map = L.map('map').setView([0,0],18);"
"L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19}).addTo(map);"
"var marker = L.marker([0,0]).addTo(map);"

"function updateLocation(){"
"fetch('/gps')"
".then(r=>r.json())"
".then(d=>{"
"if(d.lat!=0 && d.lng!=0){"
"marker.setLatLng([d.lat,d.lng]);"
"map.setView([d.lat,d.lng]);"
"}"
"});"
"}"

"setInterval(updateLocation,2000);"
"</script>"
"</body>"
"</html>";

  server.send(200, "text/html", html);
}

void handleGPS() {
  String json = "{ \"lat\": " + String(lat, 6) + ", \"lng\": " + String(lng, 6) + " }";
  server.send(200, "application/json", json);
}

void setup() {
  Serial.begin(9600);
  gpsSerial.begin(9600);
 


  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("wife connected");
  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());

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
  }

  server.handleClient();
}
