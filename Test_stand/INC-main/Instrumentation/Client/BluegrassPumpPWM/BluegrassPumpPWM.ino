// Define the output pin for the signal
const int throttlePin = 10;  // Connect to the pin you want to output the signal on
const int potPin = A0;
 
// Define the pulse width in microseconds
// 1000 µs - Negative throttle, 1500 µs - OFF throttle, 2000 µs - High throttle
// int pulseWidth = 2000; // Set to desired throttle level
 
// Define the interval between pulses in milliseconds (20 ms for 50 Hz signal)
const int pulseInterval = 20;
 
void setup() {
  pinMode(throttlePin, OUTPUT);  // Set the throttle pin as an output
  pinMode(potPin,INPUT);
}
 
void loop() {
 
  int potVal = analogRead(potPin);
 
  if (potVal == HIGH)
  {
    int pulseWidth = map(potVal,0,1023,1000,2000);
  
    digitalWrite(throttlePin, HIGH);        // Start the pulse
    delayMicroseconds(pulseWidth);          // Hold high for the pulse width
    digitalWrite(throttlePin, LOW);         // End the pulse
    delay(pulseInterval - pulseWidth / 1000); // Wait for the rest of the 20 ms period
  }
  else
  {
    digitalWrite(throttlePin, LOW);
  }
}
 
