char c;
int SeisPin;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}



void loop() {
  // put your main code here, to run repeatedly:
  if(Serial.available())
  {
    c=Serial.read();
    if(c=='A')
    {
      
      Serial.print("ts: ");
      Serial.print(millis());
      Serial.print(",");
      Serial.print("d: ");
      Serial.print(analogRead(A0));
      Serial.print(",");
      
    }
  }
}
