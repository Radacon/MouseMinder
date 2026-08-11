/* MouseMinder chirp player for Arduino Uno.

   Newline-terminated commands at 115200 baud:
     PING, CLEAR, ADD <frequency_hz> <duration_ms>, PLAY,
     PAUSE, RESTART, STOP, STATUS

   A frequency of zero is a rest. Playback is non-blocking, so serial control
   remains responsive. The buzzer is connected to digital pin 8.
*/

#include <Arduino.h>

const uint8_t BUZZER_PIN = 8;
const uint8_t MAX_STEPS = 128;
const uint8_t LINE_LENGTH = 47;

struct ChirpStep {
  unsigned int frequencyHz;
  unsigned long durationMs;
};

ChirpStep sequence[MAX_STEPS];
uint8_t stepCount = 0;
uint8_t currentStep = 0;
char inputLine[LINE_LENGTH + 1];
uint8_t inputLength = 0;

enum PlayerState { STOPPED, PLAYING, PAUSED };
PlayerState playerState = STOPPED;
unsigned long stepStartedAt = 0;
unsigned long elapsedBeforePause = 0;

void silenceBuzzer() {
  noTone(BUZZER_PIN);
  digitalWrite(BUZZER_PIN, LOW);
}

void reportStatus() {
  Serial.print(F("STATUS "));
  if (playerState == PLAYING) Serial.print(F("PLAYING"));
  else if (playerState == PAUSED) Serial.print(F("PAUSED"));
  else Serial.print(F("STOPPED"));
  Serial.print(F(" STEP "));
  Serial.print(currentStep);
  Serial.print('/');
  Serial.println(stepCount);
}

void startCurrentStep(unsigned long alreadyElapsed) {
  if (currentStep >= stepCount) {
    playerState = STOPPED;
    silenceBuzzer();
    Serial.println(F("STATUS FINISHED"));
    return;
  }
  elapsedBeforePause = alreadyElapsed;
  stepStartedAt = millis() - alreadyElapsed;
  if (sequence[currentStep].frequencyHz == 0) silenceBuzzer();
  else tone(BUZZER_PIN, sequence[currentStep].frequencyHz);
  reportStatus();
}

void stopPlayback() {
  playerState = STOPPED;
  currentStep = 0;
  elapsedBeforePause = 0;
  silenceBuzzer();
}

void parseCommand(char *line) {
  char *command = strtok(line, " ");
  if (!command) return;

  if (!strcmp(command, "PING")) {
    Serial.println(F("PONG CHIRP_COMPOSER_1"));
  } else if (!strcmp(command, "CLEAR")) {
    stopPlayback();
    stepCount = 0;
    Serial.println(F("OK CLEAR"));
  } else if (!strcmp(command, "ADD")) {
    char *frequencyText = strtok(NULL, " ");
    char *durationText = strtok(NULL, " ");
    char *extra = strtok(NULL, " ");
    if (!frequencyText || !durationText || extra) {
      Serial.println(F("ERR ADD_SYNTAX"));
      return;
    }
    unsigned long frequency = strtoul(frequencyText, NULL, 10);
    unsigned long duration = strtoul(durationText, NULL, 10);
    if (stepCount >= MAX_STEPS) Serial.println(F("ERR SEQUENCE_FULL"));
    else if (frequency > 65535UL || duration == 0) Serial.println(F("ERR STEP_RANGE"));
    else {
      sequence[stepCount].frequencyHz = (unsigned int)frequency;
      sequence[stepCount].durationMs = duration;
      stepCount++;
      Serial.println(F("OK ADD"));
    }
  } else if (!strcmp(command, "PLAY")) {
    if (stepCount == 0) Serial.println(F("ERR EMPTY_SEQUENCE"));
    else if (playerState == PAUSED) {
      playerState = PLAYING;
      startCurrentStep(elapsedBeforePause);
    } else if (playerState != PLAYING) {
      currentStep = 0;
      playerState = PLAYING;
      startCurrentStep(0);
    }
  } else if (!strcmp(command, "PAUSE")) {
    if (playerState == PLAYING) {
      elapsedBeforePause = millis() - stepStartedAt;
      playerState = PAUSED;
      silenceBuzzer();
    }
    reportStatus();
  } else if (!strcmp(command, "RESTART")) {
    if (stepCount == 0) Serial.println(F("ERR EMPTY_SEQUENCE"));
    else {
      currentStep = 0;
      playerState = PLAYING;
      startCurrentStep(0);
    }
  } else if (!strcmp(command, "STOP")) {
    stopPlayback();
    reportStatus();
  } else if (!strcmp(command, "STATUS")) {
    reportStatus();
  } else {
    Serial.println(F("ERR UNKNOWN_COMMAND"));
  }
}

void readSerial() {
  while (Serial.available()) {
    char incoming = (char)Serial.read();
    if (incoming == '\r') continue;
    if (incoming == '\n') {
      inputLine[inputLength] = '\0';
      parseCommand(inputLine);
      inputLength = 0;
    } else if (inputLength < LINE_LENGTH) {
      inputLine[inputLength++] = incoming;
    } else {
      inputLength = 0;
      Serial.println(F("ERR LINE_TOO_LONG"));
    }
  }
}

void updatePlayback() {
  if (playerState != PLAYING || currentStep >= stepCount) return;
  unsigned long elapsed = millis() - stepStartedAt;
  if (elapsed >= sequence[currentStep].durationMs) {
    currentStep++;
    startCurrentStep(0);
  }
}

void setup() {
  pinMode(BUZZER_PIN, OUTPUT);
  silenceBuzzer();
  Serial.begin(115200);
  Serial.println(F("READY CHIRP_COMPOSER_1"));
}

void loop() {
  readSerial();
  updatePlayback();
}
