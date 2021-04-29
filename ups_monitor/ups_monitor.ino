#define pwrIndicator 2
#define red 4
#define yellow 6
#define alarm 8
#define green 10 

//Keeps track of how mant times the pwrIndicator indicates offline status
//  Incriments once every second
unsigned int offLnCnt = 0;
unsigned int maxOffLnCnt = 20;
unsigned long timeLastCnt = 0;


bool beepOn = false; //Holds value of whether beep is on or not | used in the beep method
unsigned long beepStart = 0;

//Values used for sendSerial
unsigned long serialTime = 0;
unsigned long serialDelay = 1000;

//Timeout so green light stops blinking
unsigned long greenTimeout = 300000; //300000 millis = 5 min
unsigned long greenTimeoutStart = 0;

//Turn buzzer on or off
void buzzer(bool on) 
{
  //if(on) digitalWrite(alarm, LOW);
  //else if(!on) digitalWrite(alarm, HIGH);
}

//Turn buzzer on then off after certain time
void beep(unsigned long bzzLngth)
{
  if (!beepOn) //If beep is not currently running then...  
  {
    //beepOn = true; //Say beep is currently running by setting beepOn to true
    //beepStart = millis(); //Set buzzerStart to the current time
  }
  if (millis() - beepStart >= bzzLngth) //If buzzer timer has reached limit then... 
  {
    buzzer(false); //Turn buzzer off
  }
  else buzzer(true); //Otherwise turn buzzer on
}

/*Check to see if ups is online
  Will return True if ups is online
*/
bool OnlineCheck()
{
  return digitalRead(pwrIndicator) == HIGH;
}

//Method for if ups is online
void online()
{
  greenTimeoutStart = millis(); //Records time that online method was initially started
  
  offLnCnt = 0; //Set offline counter to 0
   
  while(OnlineCheck()) //Loop until not online
  {
    
    digitalWrite(LED_BUILTIN, HIGH); //Turn the onboard led on
 
    sendSerial("ONLINE"); //Send ONLINE over serial
    
    if (millis() - greenTimeoutStart >= greenTimeout) digitalWrite(green, HIGH); //If greenTimeout is reached turn green led off
    else digitalWrite(green, LOW); //If greenTimeout is not reached turn green led on    
    digitalWrite(yellow, HIGH); //Turn yellow light off 
    digitalWrite(red, HIGH); //Turn red light off
  }
}

//Method for if ups is offline
void offline()
{
  while(!OnlineCheck())
  {
    beep(5000); //Beep for 1 sec 
    if (offLnCnt >= maxOffLnCnt)//If Offline has timedout move to the Shutdown method
    {
      Shutdown();  
    }else
    {
      //Send OFFLINE over serial
      sendSerial("OFFLINE"); //Send OFFLINE over serial
      
      //Turn yellow led on
      digitalWrite(green, HIGH); //Turn green light off
      digitalWrite(yellow, LOW); //Turn yellow light on
      digitalWrite(red, HIGH); //Turn red light off  
    }
    //Increment offLnCnt
    if(millis() - timeLastCnt >= 1000)
    {
      offLnCnt++;
      timeLastCnt = millis();
    
    }
  }
}

//Method for if ups is offline for to long
void Shutdown()
{
  beepOn=false;//Tell that beep is no longer running
  while(!OnlineCheck())
  {
    beep(1000);
    
    sendSerial("SHUTDOWN");//Send SHUTDOWN over serial
  
    digitalWrite(green, HIGH); //Turn green light off
    digitalWrite(yellow, HIGH); //Turn yellow light off
    digitalWrite(red, LOW); //Turn red light on
  }
}

//Method to delay serial
void sendSerial(String mess)
{
  if (millis() - serialTime >= serialDelay)
  {
    Serial.println(mess);
    serialTime = millis();
  }
}

void setup() {
  // put your setup code here, to run once:
  
  //Setup pins
  pinMode(pwrIndicator, INPUT);
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(green, OUTPUT);
  pinMode(yellow, OUTPUT);
  pinMode(red, OUTPUT);
  pinMode(alarm, OUTPUT);
  
  //Set output pins to proper initial output
  digitalWrite(LED_BUILTIN, LOW);
  digitalWrite(green, HIGH);
  digitalWrite(yellow, HIGH);
  digitalWrite(red, HIGH);
  digitalWrite(alarm, HIGH);
  
  //Enable serial coms
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  beepOn = false; //State that beep is not on
  buzzer(false); //Turn buzzer off
  
  online(); //Only runs if ups is online, has an internal check
  offline(); //Only runs if ups is offline, has an internal check
}
