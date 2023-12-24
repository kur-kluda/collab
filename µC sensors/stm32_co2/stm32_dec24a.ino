#include <STM32ADC.h>

const int maxSamples = 8; // 8 channels

// Array for the ADC data
uint16_t dataPoints[maxSamples];

void setup() {
  // put your setup code here, to run once:
pinMode(PC13, OUTPUT);
STM32ADC myADC(ADC1);
//calibrate ADC
myADC.calibrate();
/*
    Set the ADC Sampling Rate.
    ADC_SMPR_1_5,               < 1.5 ADC cycles
    ADC_SMPR_7_5,               < 7.5 ADC cycles
    ADC_SMPR_13_5,              < 13.5 ADC cycles
    ADC_SMPR_28_5,              < 28.5 ADC cycles
    ADC_SMPR_41_5,              < 41.5 ADC cycles
    ADC_SMPR_55_5,              < 55.5 ADC cycles
    ADC_SMPR_71_5,              < 71.5 ADC cycles
    ADC_SMPR_239_5,             < 239.5 ADC cycles
*/
//Channels to be acquired.
uint8 pins[] = {PB0};
pinMode(pins[0], INPUT_ANALOG);
myADC.setSampleRate(ADC_SMPR_1_5);//set the Sample Rate
// myADC.setScanMode(); //set the ADC in Scan mode.
myADC.setPins(pins, 1); //set how many and which pins to convert.
myADC.setContinuous(); //set the ADC in continuous mode.

//set the DMA transfer for the ADC.
//in this case we want to increment the memory side and run it in circular mode
//By doing this, we can read the last value sampled from the channels by reading the dataPoints array
myADC.setDMA(dataPoints, 8, (DMA_MINC_MODE | DMA_CIRC_MODE), NULL);

//start the conversion.
//because the ADC is set as continuous mode and in circular fashion, this can be done
//on setup().
myADC.startConversion();

Serial.begin(9600);
  while (!Serial) {
    delay(1);  // wait for USB to enumerate
  }
  Serial.println("ciao");
  delay(3000);
}

int c =0;
void loop() {
  // put your main code here, to run repeatedly:
digitalWrite(PC13, HIGH);   // turn the LED on (HIGH is the voltage level)
Serial.println("hellow "+String(c));
c++;
  for(unsigned int i = 0; i < maxSamples; i ++) {
    Serial.print("sample[");
    Serial.print(i);
    Serial.print("] = ");
    Serial.println(dataPoints[i]);
    }
  int analogValue = analogRead(2);
 // int analogVolts = analogReadMilliVolts(2);
  
  // print out the values you read:
  Serial.println("ADC 2 analog value = "+ String(analogValue));
 // Serial.println("ADC millivolts value = " + String(analogVolts));

   int analogValueB = analogRead(B0);
//  int analogVolts = analogReadMilliVolts(B0);
  
  // print out the values you read:
  Serial.println("ADC B0 analog value = "+String(analogValueB));
  //Serial.println("ADC B0 millivolts value = %d\n",analogVolts); 
  delay(1000);              // wait for a second
  digitalWrite(PC13, LOW);    // turn the LED off by making the voltage LOW
  delay(1000);              // wait for a second
}
