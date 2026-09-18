const int fuck_this_analog = A1;
const int fuck_this_digital = 2;

void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);
}

void loop() {
  float analog = 5*analogRead(fuck_this_analog)/1023;
  float digital = 5*digitalRead(fuck_this_digital)/1023;
    
    Serial.print("Analog Voltage: ");
    Serial.print(analog);
    Serial.println(" V");
    Serial.print("Digital Voltage: ");
    Serial.print(digital);
    Serial.println(" V");

    delay(500);  // Delay to avoid flooding the serial output

}
