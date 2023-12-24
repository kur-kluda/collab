#include <STM32ADC.h>

const bool __DEBUG__CALIBR__1__ = true;
const bool __DEBUG__CALIBR__2__ = false;
const int maxMeasures = 120; // 120 measures stored in the memory to be averaged on send.

// Arrays for the ADC data
uint16_t dataPoints[maxMeasures];
uint16_t dataPoints2[maxMeasures];


void setup() {
pinMode(PC13, OUTPUT);
STM32ADC myADC(ADC1);
//STM32ADC myADC2(ADC2);
//calibrate ADC
myADC.calibrate();
//myADC2.calibrate();
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
uint8 pins[] = {PB0, PA7};
pinMode(pins[0], INPUT_ANALOG);
pinMode(pins[1], INPUT_ANALOG);
myADC.setSampleRate(ADC_SMPR_7_5);//set the Sample Rate
//myADC2.setSampleRate(ADC_SMPR_7_5);//set the Sample Rate (results in zeroing the first ADC, both do not calculate to comparable

// myADC.setScanMode(); //set the ADC in Scan mode.
myADC.setPins(pins, 1); //set how many and which pins to convert.
//myADC2.setPins(pins, 1); //set how many and which pins to convert.

myADC.setContinuous(); //set the ADC in continuous mode.
//myADC2.setContinuous(); //set the ADC in continuous mode.

//set the DMA transfer for the ADC.
//in this case we want to increment the memory side and run it in circular mode
//By doing this, we can read the last value sampled from the channels by reading the dataPoints array
myADC.setDMA(dataPoints, 120, (DMA_MINC_MODE | DMA_CIRC_MODE), NULL);
//myADC2.setDMA(dataPoints2, 120, (DMA_MINC_MODE | DMA_CIRC_MODE), NULL);

//start the conversion.
//because the ADC is set as continuous mode and in circular fashion, this can be done
//on setup().
myADC.startConversion();
//on setup().
//myADC2.startConversion();
//on setup().

Serial.begin(9600);
  while (!Serial) {
    delay(1);  // wait for Serial to enumerate
  }
  Serial.println("ciao");
  delay(2000);
}

int c =0;
float lastKnownZeroCurrent_VoltageSkew = 315.0206299; //372.3636364;


void loop() {
digitalWrite(PC13, HIGH);   // turn the LED on (HIGH is the voltage level)
if(__DEBUG__CALIBR__1__){
Serial.println("hellow "+String(c));
c++;
}

float vals = 0.0;
float last_calculated_mili_amps = 0.0;
float valcnt = 0;
  for(unsigned int i = 0; i < maxMeasures; i ++) {
    vals += dataPoints[i];
    valcnt++;
    }
    if(__DEBUG__CALIBR__1__){
   Serial.print("average value: ");
   Serial.print(vals/valcnt, 7);
   Serial.print("\t Voltage Eq = ");
   //TODO: get VREF vs BUS ??
   Serial.print(((vals+1)/valcnt)* 3300 / 4096, 7);
   Serial.print("\t miliAmps Eq = ");
   //last_calculated_mili_amps = (vals/valcnt+1-lastKnownZeroCurrent_VoltageSkew) *(20-4)/ 4096*3300/4096+4;
   last_calculated_mili_amps = ((vals+1-lastKnownZeroCurrent_VoltageSkew)/valcnt) *(20)/4096;
   //liela starpība, bet sanāk 4 ma un range navjāņem vērā>> jo 1. ir tuvāks 8.1315317 vs 9.244446346 @ 8.06
   Serial.print(last_calculated_mili_amps, 7);
   Serial.print("\t");
   Serial.print(((vals+1-lastKnownZeroCurrent_VoltageSkew)/valcnt) *(20-4)/ 4096*3300/4096+4, 7);
   Serial.println();
   Serial.print("\t CO2 ppm Eq = ");
   Serial.print(4600/16*(last_calculated_mili_amps-4)+400, 7);
   Serial.print("\t");
   Serial.print(287.5*last_calculated_mili_amps-750, 7);
   Serial.println();
//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ direct read single value..
  int analogValue = analogRead(2);
 // int analogVolts = analogReadMilliVolts(2);
  Serial.println("ADC 2 analog value = "+ String(analogValue));
 // Serial.println("ADC 2 millivolts value = " + String(analogVolts));

  int analogValueA7 = analogRead(PA7);
  Serial.println("ADC PA7 analog value = "+String(analogValueA7));
  Serial.println();
  /* int analogValueB = analogRead(PB0);
  Serial.println("ADC B0 analog value = "+String(analogValueB));*/

//~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ eo direct read single value..
    } else{
    Serial.print(287.5*last_calculated_mili_amps-750, 7);
    }
    
 if(__DEBUG__CALIBR__2__){ 
  for(unsigned int i = 0; i < maxMeasures; i ++) {
    Serial.print(dataPoints[i]);
    Serial.print("  ");
    }
 Serial.println();
}
  
  delay(500);              // wait for a half second
  digitalWrite(PC13, LOW);    // turn the LED off by making the voltage LOW
  delay(500);              // wait for a half second
}