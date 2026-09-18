int throttlePin = 36;          //sends signal to pump
const int pulseInterval = 20;  // interval between pulses [ms], creates 50 Hz
int pulseWidth = 2000;

void setup() {
  pinMode(throttlePin, OUTPUT);  // Set the throttle pin as an output
  digitalWrite(throttlePin, LOW);
  Serial.begin(9600);

  Serial.print("Pulse sent: ");
  Serial.print(pulseWidth);
  Serial.println(" µs");
}

void loop() {

  //PUMP TESTING
  //Apply PWM command

  digitalWrite(throttlePin, HIGH);
  // Generate the pulse for the motor controller
  // digitalWrite(throttlePin, HIGH);       // Start the pulse
  // delayMicroseconds(pulseWidth);         // Hold high for the pulse width
  // digitalWrite(throttlePin, LOW);        // End the pulse


  // // Wait for the rest of the 20 ms period
  // delay(pulseInterval - pulseWidth/1000);
}
