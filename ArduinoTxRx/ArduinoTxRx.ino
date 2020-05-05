char c;
int SeisPin;
int sampCount = 1;
unsigned long startTime;

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
		
		  startTime = millis();
    	Serial.print(startTime);
    	Serial.print(":");
    	Serial.print(analogRead(A0));
    	
		if(sampCount > 99 ){ // print a star every 1000 samples? one idea anyway
			Serial.print("*");
			sampCount = 1;
		}else{
			Serial.print(",");
			sampCount += 1; // iterate count
	    }
		// stop condition
//		if(c == 'B'){
//			break;
//		}

      delay(25 -(millis() - startTime)); //samples every 25 milliseconds

	}
}
