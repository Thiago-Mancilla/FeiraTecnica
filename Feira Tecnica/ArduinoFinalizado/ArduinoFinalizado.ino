#include <Servo.h>  // Inclui a biblioteca Servo

Servo polegar;   // Cria um objeto Servo para o polegar
Servo indicador; // Cria um objeto Servo para o indicador
Servo medio;     // Cria um objeto Servo para o médio
Servo anelar;    // Cria um objeto Servo para o anelar
Servo minimo;    // Cria um objeto Servo para o mínimo

String cmd;           // Variável para armazenar os comandos recebidos
int PosicaoPolegar = 90;  // Inicializa a posição atual do servo polegar em 90 graus
int PosicaoIndicador = 90;  // Inicializa a posição atual do servo indicador em 90 graus
int PosicaoMedio = 90;  // Inicializa a posição atual do servo médio em 90 graus
int PosicaoAnelar = 90;  // Inicializa a posição atual do servo anelar em 90 graus
int PosicaoMinimo = 90;  // Inicializa a posição atual do servo mínimo em 90 graus

void setup() {
  Serial.begin(9600);   // Inicia o Monitor Serial

  polegar.attach(2); // Define o pino 2 como a saída para o servo motor polegar
  polegar.write(PosicaoPolegar); // Move o servo polegar para a posição inicial

  indicador.attach(3); // Define o pino 3 como a saída para o servo motor indicador
  indicador.write(PosicaoIndicador); // Move o servo indicador para a posição inicial

  medio.attach(4); // Define o pino 4 como a saída para o servo motor médio
  medio.write(PosicaoMedio); // Move o servo médio para a posição inicial

  anelar.attach(5); // Define o pino 5 como a saída para o servo motor anelar
  anelar.write(PosicaoAnelar); // Move o servo anelar para a posição inicial

  minimo.attach(6); // Define o pino 6 como a saída para o servo motor mínimo
  minimo.write(PosicaoMinimo); // Move o servo mínimo para a posição inicial
}

void loop() {
  if (Serial.available() > 0) {  // Se houver dados seriais disponíveis
    cmd = Serial.readStringUntil('\n');  // Lê o comando completo até encontrar uma nova linha

    // Controle do servo motor com base no comando recebido
    if (cmd == "11") {            // Polegar levantado
      PosicaoPolegar = 0;          
    }
    else if (cmd == "10") {       // Polegar abaixado
      PosicaoPolegar = 180;       
    }
    else if (cmd == "21") {       // Indicador levantado
      PosicaoIndicador = 0;          
    }
    else if (cmd == "20") {       // Indicador abaixado
      PosicaoIndicador = 180;       
    }
    else if (cmd == "31") {       // Médio levantado
      PosicaoMedio = 0;          
    }
    else if (cmd == "30") {       // Médio abaixado
      PosicaoMedio = 180;       
    }
    else if (cmd == "41") {       // Anelar levantado
      PosicaoAnelar = 0;          
    }
    else if (cmd == "40") {       // Anelar abaixado
      PosicaoAnelar = 180;       
    }
    else if (cmd == "51") {       // Mínimo levantado
      PosicaoMinimo = 0;          
    }
    else if (cmd == "50") {       // Mínimo abaixado
      PosicaoMinimo = 180;       
    }

    // Atualiza as posições dos servos
    polegar.write(PosicaoPolegar);
    indicador.write(PosicaoIndicador);
    medio.write(PosicaoMedio);
    anelar.write(PosicaoAnelar);
    minimo.write(PosicaoMinimo);
  }
}
