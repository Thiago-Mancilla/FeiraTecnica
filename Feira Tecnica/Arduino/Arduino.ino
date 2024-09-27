#include <Servo.h>  // Inclui a biblioteca Servo

Servo servoMotor;   // Cria um objeto Servo
char cmd;           // Variável para os comandos seriais
int posicaoAtual = 90;  // Inicializa a posição atual do servo em 90 graus

void setup() {
  Serial.begin(9600);   // Inicia o Monitor Serial
  servoMotor.attach(2); // Define o pino 2 como a saída para o servo motor
  servoMotor.write(posicaoAtual); // Move o servo para a posição inicial
}

void loop() {
  if (Serial.available() > 0) {  // Se houver dados seriais disponíveis
    cmd = Serial.read();         // Lê o comando

    // Controle do servo motor com base no comando recebido
    if (cmd == '1') {            // Se o comando for '1' (polegar levantado)
      posicaoAtual = 0;          // Mover para 0 graus
    }
    else if (cmd == '0') {       // Se o comando for '0' (polegar abaixado)
      posicaoAtual = 180;       // Mover para 180 graus
    }

    servoMotor.write(posicaoAtual); // Move o servo para a nova posição
  }
}
