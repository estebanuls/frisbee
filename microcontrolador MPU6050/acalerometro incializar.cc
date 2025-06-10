//codigo para inicializar nuestro Acelerometro Giroscopio apara programa arduino IDE
//librerias para ser instaladas a arduino IDE
// la librerias I2C para controlar el mpu6050 
// la libreria MPU6050.h necesita I2Cdev.h
// la libreria I2Cdev.h necesita Wire.h

#include "I2Cdev.h"
#include "MPU6050.h"
#include "Wire.h"

// La dirección del MPU6050 puede ser 0x68 o 0x69, dependiendo 
// del estado de AD0. Si no se especifica, 0x68 estará implicito
MPU6050 sensor;

// Valores RAW (sin procesar) del acelerometro y giroscopio en los ejes x,y,z
int ax, ay, az;
int gx, gy, gz;

void setup() {
  Serial.begin(57600);    //Iniciando puerto serial
  Wire.begin();           //Iniciando I2C  
  sensor.initialize();    //Iniciando el sensor

  if (sensor.testConnection()) Serial.println("Sensor iniciado correctamente");
  else Serial.println("Error al iniciar el sensor");
  delay(2000);
}
void loop() {
  // Leer las aceleraciones y velocidades angulares
  sensor.getAcceleration(&ax, &ay, &az);
  sensor.getRotation(&gx, &gy, &gz);

  //Mostrar las lecturas separadas por un [tab]
   Serial.print("BEEGGLE MPU6050 -- "); 
  Serial.print("ACELERACIÓN[x y z]:\t");
  Serial.print(ax); Serial.print("  ");
  Serial.print(ay); Serial.print("  ");
  Serial.print(az); Serial.print("       ");

  Serial.print("ROTACIÓN[x y z]:\t");
  Serial.print(gx); Serial.print("  ");
  Serial.print(gy); Serial.print("  ");
  Serial.println(gz);

  delay(100);
}
