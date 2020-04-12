char c;
int SeisPin;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
	// wait for start signal 
	while(true) {
		// repeatedly check for start signal
		if(Serial.available){
			c = Serial.read();
			if(c == 'A'){
				break;
			}
		}
	}
	
	// read and transmit data
  	while(true){
		delay(1);
    	Serial.print("ts: ");
    	Serial.print(millis());
    	Serial.print(",");
    	Serial.print("d: ");
    	Serial.print(analogRead(A0));
    	Serial.print(",");
		
		// stop condition
//		if(c == 'B'){
//			break;
//		}

	}
}
