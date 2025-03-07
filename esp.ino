#include <BLEDevice.h>
#include <BLEUtils.h>
#include <BLEServer.h>
#include <string.h>

#define uS_TO_S_FACTOR 1000000ULL /* Conversion factor for micro seconds to seconds */
#define TIME_TO_SLEEP 60          /* Time ESP32 will go to sleep (in seconds) */
#define TIME_TO_WAIT 30
#define SERVICE_UUID "4fafc201-1fb5-459e-8fcc-c5c9c331914b"
#define SENSOR_UUID "beb5483e-36e1-4688-b7f5-ea07361b26a8"
#define SensorPin 34
#define outPin 2

RTC_DATA_ATTR int bootCount = 0;

/*
Method to print the reason by which ESP32
has been awaken from sleep
*/
void print_wakeup_reason()
{
    esp_sleep_wakeup_cause_t wakeup_reason;

    wakeup_reason = esp_sleep_get_wakeup_cause();

    switch (wakeup_reason)
    {
    case ESP_SLEEP_WAKEUP_EXT0:
        Serial.println("Wakeup caused by external signal using RTC_IO");
        break;
    case ESP_SLEEP_WAKEUP_EXT1:
        Serial.println("Wakeup caused by external signal using RTC_CNTL");
        break;
    case ESP_SLEEP_WAKEUP_TIMER:
        Serial.println("Wakeup caused by timer");
        break;
    case ESP_SLEEP_WAKEUP_TOUCHPAD:
        Serial.println("Wakeup caused by touchpad");
        break;
    case ESP_SLEEP_WAKEUP_ULP:
        Serial.println("Wakeup caused by ULP program");
        break;
    default:
        Serial.printf("Wakeup was not caused by deep sleep: %d\n", wakeup_reason);
        break;
    }
}

class CharCallbacks : public BLECharacteristicCallbacks
{
    void onWrite(BLECharacteristic *pCharacteristic)
    {
        Serial.println("Char written");
        sleep();
    };
};

void sleep()
{
    Serial.println(TIME_TO_SLEEP - millis() / 1000.0);
    esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR - millis() * 1000);
    esp_deep_sleep_start();
}

void setup()
{
    pinMode(outPin, OUTPUT);
    Serial.begin(115200);
    delay(1000); //Take some time to open up the Serial Monitor

    //Increment boot number and print it every reboot
    ++bootCount;
    Serial.println("Boot number: " + String(bootCount));

    //Print the wakeup reason for ESP32
    print_wakeup_reason();
    analogRead(SensorPin);
    float sensorValue = 0;
    digitalWrite(outPin, HIGH);
    for (int i = 0; i <= 200; i++)
    {
        sensorValue = sensorValue + analogRead(SensorPin);
        delay(2);
    }
    digitalWrite(outPin, LOW);
    sensorValue = sensorValue / 200.0;
    Serial.println("Sensor value: " + String(sensorValue));
    int mapped = (int)map(sensorValue, 0, 2000, 0, 100);
    Serial.println("Mapped value: " + String(mapped));

    BLEDevice::init("ESP32-1");
    BLEServer *pServer = BLEDevice::createServer();
    BLEService *pService = pServer->createService(SERVICE_UUID);
    BLECharacteristic *sensorCharacteristic = pService->createCharacteristic(
        SENSOR_UUID,
        BLECharacteristic::PROPERTY_READ |
            BLECharacteristic::PROPERTY_WRITE |
            BLECharacteristic::PROPERTY_NOTIFY);

    sensorCharacteristic->setCallbacks(new CharCallbacks());
    sensorCharacteristic->setValue(mapped);
    pService->start();
    // BLEAdvertising *pAdvertising = pServer->getAdvertising();  // this still is working for backward compatibility
    BLEAdvertising *pAdvertising = BLEDevice::getAdvertising();
    pAdvertising->addServiceUUID(SERVICE_UUID);
    pAdvertising->setScanResponse(true);
    pAdvertising->setMinPreferred(0x06); // functions that help with iPhone connections issue
    pAdvertising->setMinPreferred(0x12);
    BLEDevice::startAdvertising();
    Serial.println("Characteristic defined! Now you can read it in your phone!");
}

void loop()
{
    delay(1000);
    Serial.println("waiting...");
    if (millis() / 1000 > TIME_TO_WAIT)
    {
        sleep();
    }
}