char c;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    c=Serial.read();
    if(c=='A')
    {
      delay(1000);
      Serial.print("OK");
    }
  }
}
