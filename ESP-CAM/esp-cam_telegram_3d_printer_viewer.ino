#include <WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h>
#include "esp_camera.h"
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27
#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22
#define FLASH_LED_PIN 4

// Wifi network station credentials
#define WIFI_SSID "YOUR SSID"
#define WIFI_PASSWORD "YOUR PASSWORD"

// Telegram BOT Token (Get from Botfather)
#define BOT_TOKEN "YOUR BOT TOKEN"
String chat_id = "YOUR CHAT ID";

bool isMoreDataAvailable();
bool dataAvailable = false;
bool flashState = LOW;
byte *getNextBuffer();
int getNextBufferLen();
unsigned long bot_lasttime; // last time messages' scan has been done

WiFiClientSecure secured_client;
UniversalTelegramBot bot(BOT_TOKEN, secured_client);
camera_fb_t *fb = NULL;

void handleNewMessages(int numNewMessages)
{
  Serial.println("handleNewMessages");
  Serial.println(String(numNewMessages));

  for (int i = 0; i < numNewMessages; i++)
  {
    String text = bot.messages[i].text;

    String from_name = bot.messages[i].from_name;
    if (from_name == "")
      from_name = "Guest";

    if (text == "FLASH")
    {
      flashState = !flashState;
      digitalWrite(FLASH_LED_PIN, flashState);
      if (flashState == LOW)
      {
        bot.sendMessage(chat_id, "Flash is OFF", "");
      }
      else
      {
        bot.sendMessage(chat_id, "Flash is ON", "");
      }
    }

    if (text == "CAPTURE")
    {
      fb = NULL;
      // Take Picture with Camera
      fb = esp_camera_fb_get();
      if (!fb)
      {
        Serial.println("Camera capture failed");
        bot.sendMessage(chat_id, "Camera capture failed", "");
        return;
      }
      dataAvailable = true;
      Serial.println("Sending");
      bot.sendPhotoByBinary(chat_id, "image/jpeg", fb->len, isMoreDataAvailable, nullptr, getNextBuffer, getNextBufferLen);
      Serial.println("done!");
      esp_camera_fb_return(fb);
    }

    if (text == "/start")
    {
      String welcome = "Welcome to Mandloh's 3d printer viewer bot.\n\n";
      welcome += "FLASH : Toggle flash.\n";
      welcome += "CAPUTRE : Show picture.\n";
      bot.sendMessage(chat_id, welcome, "Markdown");

      String keyboardJson = "[[\"CAPTURE\"],[\"FLASH\"]]";
      bot.sendMessageWithReplyKeyboard(chat_id, "Choose button", "", keyboardJson, true);
    }
  }
}

bool isMoreDataAvailable()
{
  if (dataAvailable)
  {
    dataAvailable = false;
    return true;
  }
  else
  {
    return false;
  }
}

byte *getNextBuffer()
{
  if (fb)
  {
    return fb->buf;
  }
  else
  {
    return nullptr;
  }
}

int getNextBufferLen()
{
  if (fb)
  {
    return fb->len;
  }
  else
  {
    return 0;
  }
}

bool setupCamera()
{
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sscb_sda = SIOD_GPIO_NUM;
  config.pin_sscb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.frame_size = FRAMESIZE_VGA; // FRAMESIZE_ + QVGA|CIF|VGA|SVGA|XGA|SXGA|UXGA
  config.jpeg_quality = 15;
  config.fb_count = 2;

  // camera init
  esp_err_t err = esp_camera_init(&config);
  if (err != ESP_OK)
  {
    Serial.printf("Camera init failed with error 0x%x", err);
    return false;
  }
  return true;
}

void setup()
{
  Serial.begin(115200);
  Serial.println();

  pinMode(FLASH_LED_PIN, OUTPUT);
  digitalWrite(FLASH_LED_PIN, flashState); //defaults to low

  if (!setupCamera())
  {
    Serial.println("Camera Setup Failed!");
    while (true)
    {
      delay(100);
    }
  }

  // attempt to connect to Wifi network:
  Serial.print("Connecting to Wifi SSID ");
  Serial.print(WIFI_SSID);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  secured_client.setCACert(TELEGRAM_CERTIFICATE_ROOT);
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(500);
  }
  Serial.print("\nWiFi connected. IP address: ");
  Serial.println(WiFi.localIP());

  Serial.print("Retrieving time: ");
  configTime(0, 0, "pool.ntp.org"); // get UTC time via NTP
  time_t now = time(nullptr);
  while (now < 24 * 3600)
  {
    Serial.print(".");
    delay(100);
    now = time(nullptr);
  }
  Serial.println(now);
  
  // Make the bot wait for a new message for up to 60seconds
  bot.longPoll = 60;
  bot.sendMessage(chat_id, "3D printer viewer is ready.", "");

  String keyboardJson = "[[\"CAPTURE\"],[\"FLASH\"]]";
  bot.sendMessageWithReplyKeyboard(chat_id, "Choose button", "", keyboardJson, true);
}

void loop()
{
  if (millis() - bot_lasttime > 1000) // mean time between scan messages
  {
    int numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    while (numNewMessages)
    {
      Serial.println("got response");
      handleNewMessages(numNewMessages);
      numNewMessages = bot.getUpdates(bot.last_message_received + 1);
    }
    bot_lasttime = millis();
  }
}
