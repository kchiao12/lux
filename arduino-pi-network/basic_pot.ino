int potPin = 1;
int outPin = 2;
int inPin = 5;
int val = 0;

void setup() {
  Serial.begin(9600);
  pinMode(outPin, OUTPUT);  
  pinMode(inPin, INPUT);
}

void loop() {
  val = analogRead(potPin);
  //Serial.println(val);
  analogWrite(outPin, val / 4);
  Serial.println(analogRead(inPin));
}

