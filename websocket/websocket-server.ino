#include "WiFi.h"
#include "ESPAsyncWebServer.h"

const char* ssid = "Your Network ID";
const char* password = "Your Password";

String cmd = "";

AsyncWebServer server(80);
AsyncWebSocket ws("/");

void onWsEvent(AsyncWebSocket *server, AsyncWebSocketClient *client, AwsEventType type, void *arg, uint8_t *data, size_t len)
{
  if (type == WS_EVT_CONNECT)
  {
    Serial.println("Websocket client connection received");
    client->text("ESP32-Server : Hello.");
  }
  else if (type == WS_EVT_DISCONNECT)
  {
    Serial.println("Client disconnected");
  }
  else if (type == WS_EVT_DATA)
  {
    for (int i = 0; i < len; i++)
    {
      cmd = cmd + (char)data[i];
    }
    Serial.println(cmd);
    cmd = "";
  }
}
void setup(){
  Serial.begin(115200);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connect...");
  }

  Serial.println(WiFi.localIP());

  ws.onEvent(onWsEvent);
  server.addHandler(&ws);

  server.begin();
}

void loop(){}
