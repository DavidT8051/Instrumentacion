int valorADC = 0;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  int i;
  int sumaADC=0;
  for(i=0;i<=100;i++)
  {
      valorADC = analogRead(A0);
      if(valorADC<40)
      {
          valorADC = 40;
      } 
      sumaADC+=valorADC;
      delay(1);
  }

  valorADC = int(sumaADC/100);
  Serial.println(valorADC); //0.1
}
