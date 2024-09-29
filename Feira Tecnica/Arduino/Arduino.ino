#include <Servo.h>  // Inclui a biblioteca Servo

Servo polegar;   // Cria um objeto Servo para o polegar
Servo indicador; // Cria um objeto Servo para o indicador
Servo medio;     // Cria um objeto Servo para o medio
Servo anelar;    // Cria um objeto Servo para o anelar
Servo minimo;    // Cria um objeto Servo para o minimo

char cmd;           // Variável para os comandos seriais
int PosicaoPolegar = 90;  // Inicializa a posição atual do servo polegar em 90 graus
int PosicaoIndicador = 90;  // Inicializa a posição atual do servo indicador em 90 graus
int PosicaoMedio = 90;  // Inicializa a posição atual do servo medio em 90 graus
int PosicaoAnelar = 90;  // Inicializa a posição atual do servo anelar em 90 graus
int PosicaoMinimo = 90;  // Inicializa a posição atual do servo minimo em 90 graus

void setup() {
  Serial.begin(9600);   // Inicia o Monitor Serial

  polegar.attach(2); // Define o pino 2 como a saída para o servo motor polegar
  polegar.write(PosicaoPolegar); // Move o servo polegar para a posição inicial

  indicador.attach(3); // Define o pino 2 como a saída para o servo motor indicador
  indicador.write(PosicaoIndicador); // Move o servo indicador para a posição inicial

  medio.attach(4); // Define o pino 2 como a saída para o servo motor medio
  medio.write(PosicaoMedio); // Move o servo medio para a posição inicial

  anelar.attach(5); // Define o pino 2 como a saída para o servo motor anelar
  anelar.write(PosicaoAnelar); // Move o servo anelar para a posição inicial

  minimo.attach(6); // Define o pino 2 como a saída para o servo motor minimo
  minimo.write(PosicaoMinimo); // Move o servo minimo para a posição inicial
}

void loop() {
  if (Serial.available() > 0) {  // Se houver dados seriais disponíveis
    cmd = Serial.read();         // Lê o comando

    // Controle do servo motor com base no comando recebido
    if (cmd == '1') {            // Se o comando for '1' (polegar levantado)
      PosicaoPolegar = 0;          // Mover para 0 graus
    }
    else if (cmd == '0') {       // Se o comando for '0' (polegar abaixado)
      PosicaoPolegar = 180;       // Mover para 180 graus
    }

    polegar.write(PosicaoPolegar); // Move o servo para a nova posição
  }
}
