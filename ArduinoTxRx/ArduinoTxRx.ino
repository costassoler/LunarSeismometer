char c;
int SeisPin;
int sampCount = 0;

void setup() {
  // put your setup code here, to run once:
  Serial.begin(115200);
}

void loop() {
	// wait for start signal 
	while(true) {
		// repeatedly check for start signal
		if(Serial.available()){
			c = Serial.read();
			if(c == 'A'){
				break;
			}
		}
	}
	
	// read and transmit data
  	while(true){
		delay(1);
    	Serial.print(millis());
    	Serial.print(":");
    	Serial.print(analogRead(A0));
    	
		if(sampCount > 999 ){ // print a star every 1000 samples? one idea anyway
			Serial.print("*");
			sampCount = 0;
		}else{
			Serial.print(",");
			sampCount += 1; // iterate count
	    }
		// stop condition
//		if(c == 'B'){
//			break;
//		}

	}
}
