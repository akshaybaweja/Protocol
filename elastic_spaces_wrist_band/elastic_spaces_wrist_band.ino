//#define DEBUG

const int Nx = 6;
const int Ny = 3;
const int Nxy = Nx * Ny;

const int N_MOTORS = Nxy;

int motors[N_MOTORS] = {
  A5, A4, A3, A2, A1, A0,
  2, 3, 4, 5, 6, 7,
  8, 9, 10, 11, 12, 13
};

void setup() {
  Serial.begin(115200);
  for (int i = 0; i < N_MOTORS; i++) {
    pinMode(motors[i], OUTPUT);
    digitalWrite(motors[i], HIGH);
  }
  //  runTest();
}

void loop() {
}

void serialEvent() {
  if (Serial.read() == '*') {
    String rawData = Serial.readStringUntil('*');
    handleSerialEvent(rawData);
  }
}

void resetMotors() {
  for (int i = 0; i < N_MOTORS; i++)
    digitalWrite(motors[i], HIGH);
}

void runTest() {
  for (int i = 0; i < N_MOTORS; i++) {
    digitalWrite(motors[i], LOW);
    delay(200);
    digitalWrite(motors[i], HIGH);
    delay(1000);
  }
}

void runAnimation(int frame[][Nx][Ny], int frames, int intensity, int frameDelay) {
  resetMotors();
  for (int k = 0; k < frames; k++) {
    for (int i = 0; i < Nx; i++) {
      for (int j = 0; j < Ny; j++) {
        if (frame[k][i][j])
          digitalWrite(motors[Nx * i + j], LOW);
        else
          digitalWrite(motors[Nx * i + j], HIGH);
      }
    }
    delay(intensity);
    resetMotors();
    delay(frameDelay);
  }
}

void handleSerialEvent(String rawData) {
  // *<intensity>@<frameDelay>$<frames>#<frameData>*
  // *200@120$2#000000000000000010*

  int at = rawData.indexOf('@');
  int dollar = rawData.indexOf('$');
  int hash = rawData.indexOf('#');

  int intensity = rawData.substring(0, at).toInt();
  int frameDelay = rawData.substring(at + 1, hash).toInt();
  int frames = rawData.substring(dollar + 1, hash).toInt();
  String data = rawData.substring(hash + 1);

#ifdef DEBUG
  Serial.println("Raw: " + rawData);
  Serial.print("Intensity: "); Serial.println(intensity);
  Serial.print("Frame Delay: "); Serial.println(frameDelay);
  Serial.print("Frames: "); Serial.println(frames);
#endif

  string2frames(data, frames, intensity, frameDelay);
}

void string2frames(String data, int nFrames, int intensity, int frameDelay) {
  int frames[nFrames][Nx][Ny];
  for (int k = 0; k < nFrames; k++) {
    for (int i = 0; i < Nx; i++) {
      for (int j = 0; j < Ny; j++) {
        frames[k][i][j] = int(data[Nxy * k + Nx * i + j]) - 48;
      }
    }
  }

#ifdef DEBUG
  print3DArray(frames, nFrames);
#endif

  runAnimation(frames, nFrames, intensity, frameDelay);
}

void print3DArray(int frames[][Nx][Ny], int nFrames) {
  Serial.println();
  for (int k = 0; k < nFrames; k++) {
    Serial.println("===== Frame =====");
    for (int i = 0; i < Nx; i++) {
      for (int j = 0; j < Ny; j++) {
        Serial.print(frames[k][i][j]);
        Serial.print('\t');
      }
      Serial.println();
    }
  }
}
