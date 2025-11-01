//INCLUSAO DE BIBLIOTECAS 
#include <DHT.h>
#include <WiFi.h>
#include <IOXhop_FirebaseESP32.h>
#include <ArduinoJson.h>

//DECLARACOES
#define DHTPIN 12
#define DHTTYPE DHT11
DHT dht(DHTPIN, DHTTYPE);
#define sensor_terra 33
#define sensor_ldr 14

#define led_bomba 26
bool bool_led_bomba = false;
#define led_cooler 25
bool bool_led_cooler = false;
#define led_ldr 33
bool bool_led_ldr = false;
#define rele_bomba 32
bool bool_rele_bomba = false;
#define rele_cooler 35
bool bool_rele_cooler = false;

// CONFIGURAÇÃO DE WIFI
#define WIFI_SSID "Falha na Conexao 2.4G"
#define WIFI_PASSWORD "@Leduh1313#$%"

// CONFIG FIREBASE
#define FIREBASE_HOST "urbanplanting-128db-default-rtdb.firebaseio.com"
#define FIREBASE_AUTH "ehJp3GsR9eG0bvZnmgHFvzzavFeQEaRM8zfvxlu1"

void setup(){
  //SENSORES E ATUADORES
  dht.begin();
  pinMode(sensor_terra, INPUT);
  pinMode(sensor_ldr, INPUT);
  pinMode(led_bomba, OUTPUT);
  pinMode(led_cooler, OUTPUT);
  pinMode(led_ldr, OUTPUT);
  pinMode(rele_bomba, OUTPUT);
  pinMode(rele_cooler, OUTPUT);
  Serial.begin(115200);

  //CONEXAO WIFI
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);
  Serial.print("Conectando ao Wi-Fi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("\nWiFi conectado!");
  Serial.print("IP: ");
  Serial.println(WiFi.localIP());

  //FIREBASE
  Firebase.begin(FIREBASE_HOST, FIREBASE_AUTH);
}

void loop(){
  //LEITURAS
  float h = dht.readHumidity();
  float t = dht.readTemperature();
  if (isnan(h) || isnan(t)) return;

  int leitura_umidade_terra = map(analogRead(sensor_terra), 0, 4095, 100, 0);

  float leitura_ldr = analogRead(sensor_ldr);

  //MUDANCA NO BANCO DE DADOS E MOSTRAR NA SERIAL
  Serial.print("Umidade ar: "); Serial.println(h);
  Firebase.setFloat("projeto/sensores/umidade", h);

  Serial.print("Temperatura: "); Serial.println(t);
  Firebase.setFloat("projeto/sensores/temperatura", t);

  Serial.print("Umidade solo: "); Serial.println(leitura_umidade_terra);
  Firebase.setFloat("projeto/sensores/umidade_terra", leitura_umidade_terra);

  Serial.print("Luz: "); Serial.println(leitura_ldr);
  Firebase.setInt("projeto/sensores/luminosidade", leitura_ldr);

  //ATUADORES
  if(leitura_umidade_terra < 25){
    bool_led_bomba = true;
    bool_rele_bomba = true;
    Serial.println("Umidade do solo BAIXA - Rele ACIONADO");
    Firebase.setBool("projeto/atuadores/bomba", bool_led_bomba);
    Firebase.setBool("projeto/atuadores/led_bomba", bool_rele_bomba);
    digitalWrite(led_bomba, 1);
  }

  else{
    bool_led_bomba = false;
    bool_rele_bomba = false;
    Serial.println("Umidade do solo NORMAL - Rele DESLIGADO");
    Firebase.setBool("projeto/atuadores/bomba", bool_led_bomba);
    Firebase.setBool("projeto/atuadores/led_bomba", bool_rele_bomba);
    digitalWrite(led_bomba, 0);
  }

  if(h < 35 || t > 30){
    bool_led_cooler = true;
    bool_rele_cooler = true;
    Serial.println("Umidade ou Temperatura ALARME - Reles ACIONADO");
    Firebase.setBool("projeto/atuadores/cooler", bool_led_cooler);
    Firebase.setBool("projeto/atuadores/led_cooler", bool_rele_cooler);
    digitalWrite(led_bomba, 1);
  }

  else{
    bool_led_cooler = false;
    bool_rele_cooler = false;
    Serial.println("Umidade ou Temperatura NORMAL - Reles DESLIGADO");
    Firebase.setBool("projeto/atuadores/cooler", bool_led_cooler);
    Firebase.setBool("projeto/atuadores/led_cooler", bool_rele_cooler);
    digitalWrite(led_bomba, 0);
  }

  if(leitura_ldr < 400){
    bool_led_ldr = true;
    Serial.println("Luminosidade BAIXA - Led ACIONADO");
    Firebase.setBool("projeto/atuadores/led_ldr", bool_led_ldr);
    digitalWrite(led_ldr, 1);
  }

  else{
    bool_led_ldr = false;
    Serial.println("Luminosidade NORMAL - Led DESLIGADO");
    Firebase.setBool("projeto/atuadores/led_ldr", bool_led_ldr);
    digitalWrite(led_ldr, 0);
  }

}

