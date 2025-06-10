//llamada y generada por la libreria MPU6050_tockn
#include <MPU6050_tockn.h>
#include <Wire.h>

MPU6050 mpu6050(Wire);//objeto para crear comunicacion serial

void setup() {
  Serial.begin(9600);//comunicacion serial de 9600 baudios
  Wire.begin();//comunicacion del sensor con el controlador
  mpu6050.begin();//incializar modulo
  mpu6050.calcGyroOffsets(true);//calculo de ajuste numerico en los 3 ejes 
}

void loop() {
  mpu6050.update();//actualizacion de mediciones
  Serial.print("angleX : ");
  Serial.print(mpu6050.getAngleX());//obtencion angular del eje x
  Serial.print("\tangleY : ");
  Serial.print(mpu6050.getAngleY());//obtencion angular del eje y
  Serial.print("\tangleZ : ");
  Serial.println(mpu6050.getAngleZ());//obtencion angular del eje z
}
