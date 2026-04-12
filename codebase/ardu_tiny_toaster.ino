#include <SPI.h>
#include "pins_arduino.h"

#define SLD    0x20
#define SLDp   0x24
#define SSTp   0x64
#define SSTPRH 0x69
#define SSTPRL 0x68
#define SKEY   0xE0
#define NVM_PROGRAM_ENABLE 0x1289AB45CDD888FFULL

#define NVMCMD 0x33
#define NVMCSR 0x32
#define NVM_NOP 0x00
#define NVM_CHIP_ERASE 0x10
#define NVM_WORD_WRITE 0x1D

#define PIN_RESET 10
#define PIN_TPIDATA_MOSI 11
#define PIN_TPIDATA_MISO 12
#define PIN_TPICLK 13
#define PIN_BATT A0
#define PIN_LATCHED A1

#define Tiny4_5 10
#define Tiny9 1
#define Tiny10 1
#define Tiny20 2
#define Tiny40 4

#define TimeOut 1
#define HexError 2
#define TooLarge 3
#define MAX_VERIFY_FLASH_BYTES 1024
#define BATT_FAIL_THRESHOLD_MV 2000

enum ToasterState {
  STATE_WAIT_GUI,
  STATE_WAIT_TEST_BUTTON,
  STATE_WAIT_RESET_BUTTON,
  STATE_WAIT_TEST_CONFIRM,
  STATE_SCAN_DEVICE,
  STATE_WAIT_HEX,
  STATE_WAIT_BATT_CLEAR
};

enum PinRoleMode {
  ROLE_INPUT,
  ROLE_OUTPUT,
  ROLE_ADC
};

unsigned short adrs = 0x0000;
uint8_t data[16];
uint8_t expectedImage[MAX_VERIFY_FLASH_BYTES];
unsigned int progSize = 0;
unsigned int expectedImageSize = 0;
bool expectedImageValid = false;

int timeout;
uint8_t b, b1, b2, b3;
char type = 0;

ToasterState state = STATE_WAIT_GUI;
bool guiConnected = false;
bool hexRequested = false;
bool lastDeviceValid = false;
bool tpiTimedOut = false;
unsigned long lastHelloAt = 0;
unsigned long lastScanAt = 0;
unsigned long lastPinReportAt = 0;
unsigned long battClearSince = 0;
unsigned long latchedHighSince = 0;
unsigned long latchedLowSince = 0;
unsigned long stateChangedAt = 0;

PinRoleMode battMode = ROLE_OUTPUT;
PinRoleMode latchedMode = ROLE_OUTPUT;
int battOutputValue = LOW;
int latchedOutputValue = LOW;

uint8_t lastId1 = 0;
uint8_t lastId2 = 0;
uint8_t lastId3 = 0;

void setState(ToasterState nextState, const __FlashStringHelper *message);
void emitHello();
void emitLog(const __FlashStringHelper *message);
void emitResult(const __FlashStringHelper *code, long detail = -1);
void emitDevice(bool valid);
void emitPins();
void emitPinBatt();
void emitPinLatched();
const __FlashStringHelper *stateName(ToasterState value);
const __FlashStringHelper *deviceNameFromId(uint8_t id1, uint8_t id2, uint8_t id3);
void configureForScan();
void configureForWaitButton();
void resetForNextDevice();
void setProgrammingPinsHighImpedance();
void setBattOutput(int value);
void setBattAdc();
void setLatchedOutput(int value);
void setLatchedAdc();
int readBattMillivolts();
int readLatchedMillivolts();
int sampleBattAverageMillivolts(unsigned long durationMs);
bool latchedIsHigh();
bool latchedIsStableHigh();
bool readSerialLine(char *buffer, size_t length);
void handleCommand(const char *line);
void processStateMachine();
void processScanDevice();
void processWaitHex();
bool runProgrammingCycle();
bool runClearCycle();
bool runMetadataReadCycle();
void completeClearRequest();
void completeMetadataReadRequest();
bool start_tpi();
void finish();
bool readDeviceIdentity(uint8_t &id1, uint8_t &id2, uint8_t &id3);
bool detectConnectedDevice();
boolean writeProgramFromSerial();
bool waitForNvmReady(unsigned long timeoutMs);
unsigned int flashByteLength();
bool supportsFlashVerify();
void resetExpectedImage();
bool storeExpectedByte(unsigned int address, uint8_t value);
bool dumpAndVerifyBlankFlash();
bool verifyWrittenFlash();
void dumpFlashWindow(unsigned int flashBytes);
bool readFlashByteAt(unsigned int flashOffset, uint8_t &value);
bool readFlashPage(unsigned int flashOffset, uint8_t *buffer, uint8_t count);
bool pageMatchesMetadata(const uint8_t *buffer, const char *text);
void emitMetadataField(const __FlashStringHelper *key, const uint8_t *buffer, uint8_t count);
bool latchedIsLow();
bool latchedIsStableLow();
int readHexChar();
void discardToLineEnd();
bool eraseChip();
void ERROR_data(char i);
void tpi_send_byte(uint8_t dataByte);
uint8_t tpi_receive_byte(void);
void send_skey(uint64_t nvm_key);
void setPointer(unsigned short address);
void writeIO(uint8_t address, uint8_t value);
uint8_t readIO(uint8_t address);
void writeCSS(uint8_t address, uint8_t value);
uint8_t readCSS(uint8_t address);
uint8_t byteval(char c1, char c2);
void outHex(unsigned int n, char l);

void setup() {
  Serial.begin(9600);
  timeout = 20000;
  setProgrammingPinsHighImpedance();
  configureForScan();
  setState(STATE_WAIT_GUI, F("WAITING_FOR_GUI"));
}

void loop() {
  if (!guiConnected && millis() - lastHelloAt >= 500) {
    emitHello();
    lastHelloAt = millis();
  }

  if (state == STATE_WAIT_HEX) {
    processWaitHex();
  } else {
    char line[96];
    if (readSerialLine(line, sizeof(line))) {
      handleCommand(line);
    }
  }

  if (guiConnected) {
    processStateMachine();
  }

  if (millis() - lastPinReportAt >= 250) {
    emitPins();
    lastPinReportAt = millis();
  }
}

void setState(ToasterState nextState, const __FlashStringHelper *message) {
  ToasterState previous = state;
  state = nextState;
  stateChangedAt = millis();
  Serial.print(F("LOG STATE_"));
  Serial.print(stateName(previous));
  Serial.print(F("_TO_"));
  Serial.println(stateName(nextState));
  Serial.print(F("STATUS "));
  Serial.print(stateName(nextState));
  Serial.print(F(" "));
  Serial.println(message);
}

const __FlashStringHelper *stateName(ToasterState value) {
  switch (value) {
    case STATE_WAIT_GUI: return F("WAIT_GUI");
    case STATE_WAIT_TEST_BUTTON: return F("WAIT_TEST_BUTTON");
    case STATE_WAIT_RESET_BUTTON: return F("WAIT_RESET_BUTTON");
    case STATE_WAIT_TEST_CONFIRM: return F("WAIT_TEST_CONFIRM");
    case STATE_SCAN_DEVICE: return F("SCAN_DEVICE");
    case STATE_WAIT_HEX: return F("WAIT_HEX");
    case STATE_WAIT_BATT_CLEAR: return F("WAIT_BATT_CLEAR");
    default: return F("UNKNOWN");
  }
}

void emitHello() {
  Serial.println(F("HELLO ARDUINO_TOASTER"));
}

void emitLog(const __FlashStringHelper *message) {
  Serial.print(F("LOG "));
  Serial.println(message);
}

void emitResult(const __FlashStringHelper *code, long detail) {
  Serial.print(F("RESULT "));
  Serial.print(code);
  if (detail >= 0) {
    Serial.print(F(" "));
    Serial.println(detail);
    return;
  }
  Serial.println();
}

const __FlashStringHelper *deviceNameFromId(uint8_t id1, uint8_t id2, uint8_t id3) {
  if (id1 == 0x1E && id2 == 0x8F && id3 == 0x0A) {
    return F("ATtiny4");
  }
  if (id1 == 0x1E && id2 == 0x8F && id3 == 0x09) {
    return F("ATtiny5");
  }
  if (id1 == 0x1E && id2 == 0x90 && id3 == 0x08) {
    return F("ATtiny9");
  }
  if (id1 == 0x1E && id2 == 0x90 && id3 == 0x03) {
    return F("ATtiny10");
  }
  if (id1 == 0x1E && id2 == 0x91 && id3 == 0x0F) {
    return F("ATtiny20");
  }
  if (id1 == 0x1E && id2 == 0x92 && id3 == 0x0E) {
    return F("ATtiny40");
  }
  return F("UNKNOWN");
}

void emitDevice(bool valid) {
  Serial.print(F("DEVICE "));
  Serial.print(valid ? F("VALID ") : F("INVALID "));
  Serial.print(valid ? deviceNameFromId(lastId1, lastId2, lastId3) : F("UNKNOWN"));
  Serial.print(F(" "));
  outHex(lastId1, 2);
  outHex(lastId2, 2);
  outHex(lastId3, 2);
  Serial.println();
}

void emitPins() {
  emitPinBatt();
  emitPinLatched();
}

void emitPinBatt() {
  Serial.print(F("PIN BATT "));
  if (battMode == ROLE_OUTPUT) {
    Serial.print(F("OUT "));
    Serial.println(battOutputValue == HIGH ? F("HIGH") : F("LOW"));
    return;
  }
  if (battMode == ROLE_ADC) {
    Serial.print(F("ADC "));
    Serial.print(readBattMillivolts());
    Serial.println(F("mV"));
    return;
  }
  Serial.print(F("IN "));
  Serial.println(digitalRead(PIN_BATT) == HIGH ? F("HIGH") : F("LOW"));
}

void emitPinLatched() {
  Serial.print(F("PIN LATCHED "));
  if (latchedMode == ROLE_OUTPUT) {
    Serial.print(F("OUT "));
    Serial.println(latchedOutputValue == HIGH ? F("HIGH") : F("LOW"));
    return;
  }
  if (latchedMode == ROLE_ADC) {
    Serial.print(F("ADC "));
    Serial.print(readLatchedMillivolts());
    Serial.println(F("mV"));
    return;
  }
  Serial.print(F("IN "));
  Serial.println(latchedIsHigh() ? F("HIGH") : F("LOW"));
}

void configureForScan() {
  setProgrammingPinsHighImpedance();
  setBattOutput(HIGH);
  setLatchedAdc();
  battClearSince = 0;
}

void configureForWaitButton() {
  configureForScan();
}

void resetForNextDevice() {
  hexRequested = false;
  latchedHighSince = 0;
  latchedLowSince = 0;
  battClearSince = 0;
  lastDeviceValid = false;
  emitDevice(false);
  configureForWaitButton();
  setState(STATE_WAIT_TEST_BUTTON, F("PRESS_TEST"));
}

void setProgrammingPinsHighImpedance() {
  SPI.end();

  pinMode(PIN_RESET, INPUT);
  digitalWrite(PIN_RESET, LOW);

  pinMode(PIN_TPIDATA_MOSI, INPUT);
  digitalWrite(PIN_TPIDATA_MOSI, LOW);

  pinMode(PIN_TPIDATA_MISO, INPUT);
  digitalWrite(PIN_TPIDATA_MISO, LOW);

  pinMode(PIN_TPICLK, INPUT);
  digitalWrite(PIN_TPICLK, LOW);
}

void setBattOutput(int value) {
  pinMode(PIN_BATT, OUTPUT);
  digitalWrite(PIN_BATT, value);
  battMode = ROLE_OUTPUT;
  battOutputValue = value;
}

void setBattAdc() {
  pinMode(PIN_BATT, INPUT);
  battMode = ROLE_ADC;
}

void setLatchedOutput(int value) {
  pinMode(PIN_LATCHED, OUTPUT);
  digitalWrite(PIN_LATCHED, value);
  latchedMode = ROLE_OUTPUT;
  latchedOutputValue = value;
}

void setLatchedAdc() {
  pinMode(PIN_LATCHED, INPUT);
  latchedMode = ROLE_ADC;
}

int readBattMillivolts() {
  long sample = analogRead(PIN_BATT);
  return (int)((sample * 5000L) / 1023L);
}

int readLatchedMillivolts() {
  long sample = analogRead(PIN_LATCHED);
  return (int)((sample * 5000L) / 1023L);
}

int sampleBattAverageMillivolts(unsigned long durationMs) {
  unsigned long started = millis();
  unsigned long total = 0;
  unsigned int count = 0;
  while (millis() - started < durationMs) {
    total += (unsigned long)readBattMillivolts();
    ++count;
    delay(10);
  }
  if (count == 0) {
    return readBattMillivolts();
  }
  return (int)(total / count);
}

bool latchedIsHigh() {
  return readLatchedMillivolts() >= 3000;
}

bool latchedIsLow() {
  return readLatchedMillivolts() <= 1000;
}

bool latchedIsStableHigh() {
  if (latchedIsHigh()) {
    if (latchedHighSince == 0) {
      latchedHighSince = millis();
    }
    latchedLowSince = 0;
    return (millis() - latchedHighSince) >= 500;
  }

  latchedHighSince = 0;
  return false;
}

bool latchedIsStableLow() {
  if (latchedIsLow()) {
    if (latchedLowSince == 0) {
      latchedLowSince = millis();
    }
    latchedHighSince = 0;
    return (millis() - latchedLowSince) >= 500;
  }

  latchedLowSince = 0;
  return false;
}

bool readSerialLine(char *buffer, size_t length) {
  static size_t index = 0;
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\r') {
      continue;
    }
    if (c == '\n') {
      if (index == 0) {
        continue;
      }
      buffer[index] = '\0';
      index = 0;
      return true;
    }
    if (index < length - 1) {
      buffer[index++] = c;
    }
  }
  return false;
}

void handleCommand(const char *line) {
  Serial.print(F("LOG CMD_RX_"));
  Serial.print(line);
  Serial.print(F("_IN_"));
  Serial.println(stateName(state));

  if (strcmp(line, "GUI_HELLO") == 0) {
    guiConnected = true;
    Serial.println(F("ACK GUI"));
    resetForNextDevice();
    return;
  }

  if (strcmp(line, "ABORT") == 0 && state == STATE_WAIT_HEX) {
    resetForNextDevice();
    return;
  }

  if (strcmp(line, "RESET_LOOP") == 0 && guiConnected) {
    emitLog(F("RESET_LOOP_RECEIVED"));
    resetForNextDevice();
    return;
  }

  if (strcmp(line, "CLEAR") == 0 && state == STATE_WAIT_HEX) {
    completeClearRequest();
    return;
  }

  if (strcmp(line, "READ_METADATA") == 0 && state == STATE_WAIT_HEX) {
    completeMetadataReadRequest();
    return;
  }
}

void processStateMachine() {
  switch (state) {
    case STATE_WAIT_GUI:
      break;
    case STATE_WAIT_TEST_BUTTON:
      if (latchedIsStableHigh()) {
        latchedHighSince = 0;
        setState(STATE_WAIT_RESET_BUTTON, F("PRESS_RESET"));
      } else if (millis() - stateChangedAt >= 2000) {
        resetForNextDevice();
      }
      break;
    case STATE_WAIT_RESET_BUTTON:
      if (latchedIsStableLow()) {
        latchedLowSince = 0;
        setState(STATE_WAIT_TEST_CONFIRM, F("PRESS_TEST_AGAIN"));
      }
      break;
    case STATE_WAIT_TEST_CONFIRM:
      if (latchedIsStableHigh()) {
        latchedHighSince = 0;
        setState(STATE_SCAN_DEVICE, F("READING_DEVICE_ID"));
      } else if (millis() - stateChangedAt >= 2000) {
        resetForNextDevice();
      }
      break;
    case STATE_SCAN_DEVICE:
      processScanDevice();
      break;
    case STATE_WAIT_HEX:
      break;
    case STATE_WAIT_BATT_CLEAR: {
      int battMv = readBattMillivolts();
      if (battMv <= 500) {
        if (battClearSince == 0) {
          battClearSince = millis();
        } else if (millis() - battClearSince >= 500) {
          resetForNextDevice();
        }
      } else {
        battClearSince = 0;
      }
      break;
    }
    default:
      break;
  }
}

void processScanDevice() {
  if (!latchedIsHigh()) {
    latchedHighSince = 0;
    latchedLowSince = 0;
    if (lastDeviceValid) {
      emitDevice(false);
      lastDeviceValid = false;
    }
    setState(STATE_WAIT_TEST_CONFIRM, F("PRESS_TEST_AGAIN"));
    return;
  }

  if (millis() - lastScanAt < 500) {
    return;
  }
  lastScanAt = millis();

  bool valid = detectConnectedDevice();
  Serial.print(F("LOG SCAN_DEVICE_VALID_"));
  Serial.println(valid ? F("YES") : F("NO"));
  if (valid != lastDeviceValid) {
    emitDevice(valid);
    lastDeviceValid = valid;
  }

  if (valid) {
    hexRequested = false;
    setState(STATE_WAIT_HEX, F("SEND_HEX_FILE"));
  }
}

void processWaitHex() {
  emitLog(F("WAIT_HEX_ENTER"));
  if (!hexRequested) {
    emitLog(F("WAIT_HEX_REQUESTED"));
    Serial.println(F("REQUEST HEX"));
    hexRequested = true;
  }

  while (Serial.available() > 0) {
    Serial.print(F("LOG WAIT_HEX_AVAIL_"));
    Serial.println(Serial.available());
    int next = Serial.peek();
    if (next == '\r' || next == '\n') {
      emitLog(F("WAIT_HEX_PEEK_EOL"));
      Serial.read();
      continue;
    }
    Serial.print(F("LOG WAIT_HEX_PEEK_"));
    Serial.println((char)next);
    if (next == ':') {
      bool success = runProgrammingCycle();
      bool batteryPass = false;
      battClearSince = 0;
      if (success) {
        emitResult(F("PROGRAM_OK"));
      } else {
        emitResult(F("PROGRAM_FAIL"));
      }

      setBattOutput(LOW);
      setLatchedOutput(LOW);
      delay(50);
      setBattAdc();
      setLatchedAdc();
      int battMv = sampleBattAverageMillivolts(100);
      if (battMv <= BATT_FAIL_THRESHOLD_MV) {
        batteryPass = true;
        emitResult(F("BATTERY_OK"), battMv);
      } else {
        emitResult(F("BATTERY_FAIL"), battMv);
      }

      setState(STATE_WAIT_BATT_CLEAR, F("REMOVE_DEVICE"));
      hexRequested = false;
      lastDeviceValid = success && batteryPass;
      return;
    }

    char line[96];
    if (readSerialLine(line, sizeof(line))) {
      Serial.print(F("LOG WAIT_HEX_RX_"));
      Serial.println(line);
      if (strcmp(line, "CLEAR") == 0) {
        completeClearRequest();
        return;
      }
      if (strcmp(line, "READ_METADATA") == 0) {
        completeMetadataReadRequest();
        return;
      }
      handleCommand(line);
    } else {
      emitLog(F("WAIT_HEX_READLINE_EMPTY"));
      return;
    }
  }
}

void completeClearRequest() {
  emitLog(F("CLEAR_RECEIVED"));
  bool success = runClearCycle();
  battClearSince = 0;
  if (success) {
    emitResult(F("CLEAR_OK"));
  } else {
    emitResult(F("CLEAR_FAIL"));
  }

  setState(STATE_WAIT_BATT_CLEAR, F("REMOVE_DEVICE"));
  hexRequested = false;
  lastDeviceValid = success;
}

void completeMetadataReadRequest() {
  emitLog(F("READ_METADATA_RECEIVED"));
  bool success = runMetadataReadCycle();
  battClearSince = 0;
  if (success) {
    emitResult(F("METADATA_OK"));
  } else {
    emitResult(F("METADATA_FAIL"));
  }

  setState(STATE_WAIT_BATT_CLEAR, F("REMOVE_DEVICE"));
  hexRequested = false;
  lastDeviceValid = success;
}

bool runProgrammingCycle() {
  emitLog(F("PROGRAMMING"));
  if (!start_tpi()) {
    finish();
    emitLog(F("TPI_START_FAILED"));
    return false;
  }

  if (!readDeviceIdentity(lastId1, lastId2, lastId3)) {
    finish();
    emitLog(F("DEVICE_ID_READ_FAILED"));
    return false;
  }

  bool valid = (type != 0);
  emitDevice(valid);
  if (!valid) {
    finish();
    emitLog(F("INVALID_DEVICE"));
    return false;
  }

  bool programmed = writeProgramFromSerial();
  bool verified = false;
  if (programmed) {
    verified = verifyWrittenFlash();
    if (!verified) {
      emitLog(F("VERIFY_FAILED"));
    }
  }
  finish();
  return programmed && verified;
}

bool runClearCycle() {
  emitLog(F("CLEARING_MEMORY"));
  if (!start_tpi()) {
    finish();
    emitLog(F("TPI_START_FAILED"));
    return false;
  }

  emitLog(F("CLEAR_TPI_STARTED"));

  if (!eraseChip()) {
    finish();
    emitLog(F("ERASE_FAILED"));
    return false;
  }
  if (!dumpAndVerifyBlankFlash()) {
    finish();
    emitLog(F("BLANK_VERIFY_FAILED"));
    return false;
  }
  emitLog(F("ERASE_COMPLETE"));
  finish();
  return true;
}

bool runMetadataReadCycle() {
  if (!start_tpi()) {
    finish();
    emitLog(F("TPI_START_FAILED"));
    return false;
  }

  if (!readDeviceIdentity(lastId1, lastId2, lastId3)) {
    finish();
    emitLog(F("DEVICE_ID_READ_FAILED"));
    return false;
  }

  bool valid = (type != 0);
  emitDevice(valid);
  if (!valid) {
    finish();
    emitLog(F("INVALID_DEVICE"));
    return false;
  }

  const char verse[] = "Luke 19:39-40";
  uint8_t page[16];
  bool found = false;
  unsigned int verseOffset = 0;

  for (unsigned int offset = 0; offset + 16 <= flashByteLength(); offset += 16) {
    if (!readFlashPage(offset, page, 16)) {
      finish();
      emitLog(F("METADATA_READ_FAILED"));
      return false;
    }
    if (pageMatchesMetadata(page, verse)) {
      verseOffset = offset;
      found = true;
      break;
    }
  }

  if (!found || verseOffset < 32) {
    finish();
    emitLog(F("METADATA_NOT_FOUND"));
    emitResult(F("METADATA_NONE"));
    return false;
  }

  if (!readFlashPage(verseOffset - 32, page, 16)) {
    finish();
    emitLog(F("METADATA_READ_FAILED"));
    return false;
  }
  emitMetadataField(F("UNIX"), page, 16);

  if (!readFlashPage(verseOffset - 16, page, 16)) {
    finish();
    emitLog(F("METADATA_READ_FAILED"));
    return false;
  }
  emitMetadataField(F("GIT"), page, 16);

  if (!readFlashPage(verseOffset, page, 16)) {
    finish();
    emitLog(F("METADATA_READ_FAILED"));
    return false;
  }
  emitMetadataField(F("VERSE"), page, 16);

  finish();
  return true;
}

bool detectConnectedDevice() {
  if (!start_tpi()) {
    emitLog(F("SCAN_TPI_START_FAILED"));
    type = 0;
    finish();
    return false;
  }

  bool valid = readDeviceIdentity(lastId1, lastId2, lastId3);
  finish();
  return valid;
}

bool start_tpi() {
  tpiTimedOut = false;
  pinMode(PIN_RESET, OUTPUT);
  digitalWrite(PIN_RESET, HIGH);
  SPI.begin();
  SPI.setBitOrder(LSBFIRST);
  SPI.setDataMode(SPI_MODE0);
  SPI.setClockDivider(SPI_CLOCK_DIV32);

  digitalWrite(PIN_RESET, LOW);
  delay(1);

  SPI.transfer(0xff);
  SPI.transfer(0xff);
  SPI.transfer(0xff);

  writeCSS(0x02, 0x04);
  send_skey(NVM_PROGRAM_ENABLE);

  unsigned long started = millis();
  while ((readCSS(0x00) & 0x02) < 1) {
    if (tpiTimedOut) {
      emitLog(F("START_TPI_TIMEOUT"));
      SPI.end();
      digitalWrite(PIN_RESET, HIGH);
      return false;
    }
    if (millis() - started > 50) {
      emitLog(F("START_TPI_READY_TIMEOUT"));
      SPI.end();
      digitalWrite(PIN_RESET, HIGH);
      return false;
    }
  }

  setPointer(0x0000);
  return true;
}

void finish() {
  writeCSS(0x00, 0x00);
  SPI.transfer(0xff);
  SPI.transfer(0xff);
  digitalWrite(PIN_RESET, HIGH);
  delay(1);
  setProgrammingPinsHighImpedance();
}

bool readDeviceIdentity(uint8_t &id1, uint8_t &id2, uint8_t &id3) {
  setPointer(0x3FC0);
  tpi_send_byte(SLDp);
  id1 = tpi_receive_byte();
  tpi_send_byte(SLDp);
  id2 = tpi_receive_byte();
  tpi_send_byte(SLDp);
  id3 = tpi_receive_byte();

  if (tpiTimedOut) {
    type = 0;
    return false;
  }

  if (id1 == 0x1E && id2 == 0x8F && id3 == 0x0A) {
    type = Tiny4_5;
  } else if (id1 == 0x1E && id2 == 0x8F && id3 == 0x09) {
    type = Tiny4_5;
  } else if (id1 == 0x1E && id2 == 0x90 && id3 == 0x08) {
    type = Tiny9;
  } else if (id1 == 0x1E && id2 == 0x90 && id3 == 0x03) {
    type = Tiny10;
  } else if (id1 == 0x1E && id2 == 0x91 && id3 == 0x0F) {
    type = Tiny20;
  } else if (id1 == 0x1E && id2 == 0x92 && id3 == 0x0E) {
    type = Tiny40;
  } else {
    type = 0;
  }

  return type != 0;
}

int readHexChar() {
  unsigned long started = millis();
  while (millis() - started < (unsigned long)timeout) {
    while (Serial.available() > 0) {
      char c = (char)Serial.read();
      if (c == '\r' || c == '\n') {
        continue;
      }
      return c;
    }
  }
  return -1;
}

void discardToLineEnd() {
  while (Serial.available() > 0) {
    char c = (char)Serial.read();
    if (c == '\n') {
      return;
    }
  }
}

boolean writeProgramFromSerial() {
  char datlength[] = "00";
  char addr[] = "0000";
  char something[] = "00";
  char chksm[] = "00";
  unsigned int currentByte = 0;
  progSize = 0;
  uint8_t linelength = 0;
  boolean fileEnd = false;
  unsigned short tadrs = 0x4000;
  unsigned long pgmStartTime = millis();
  resetExpectedImage();
  if (!eraseChip()) {
    emitLog(F("ERASE_FAILED"));
    return false;
  }

  char words = (type != Tiny4_5 ? type : 1);

  while (!fileEnd) {
    int startChar = readHexChar();
    if (startChar < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    if (startChar != ':') {
      ERROR_data(HexError);
      discardToLineEnd();
      return false;
    }

    int c = readHexChar();
    if (c < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    datlength[0] = (char)c;
    c = readHexChar();
    if (c < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    datlength[1] = (char)c;
    linelength = byteval(datlength[0], datlength[1]);

    for (int i = 0; i < 4; ++i) {
      c = readHexChar();
      if (c < 0) {
        ERROR_data(TimeOut);
        return false;
      }
      addr[i] = (char)c;
    }

    c = readHexChar();
    if (c < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    something[0] = (char)c;
    c = readHexChar();
    if (c < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    something[1] = (char)c;

    if (something[0] == '0' && something[1] == '1') {
      fileEnd = true;
    }

    if (something[0] == '0' && something[1] == '2') {
      for (int i = 0; i <= linelength; ++i) {
        if (readHexChar() < 0 || readHexChar() < 0) {
          ERROR_data(TimeOut);
          return false;
        }
      }
      continue;
    }

    if (linelength != 0x00 && addr[0] == '0' && addr[1] == '0' && addr[2] == '0' && addr[3] == '0') {
      currentByte = 0;
    }

    for (int k = 0; k < linelength; ++k) {
      int c1 = readHexChar();
      int c2 = readHexChar();
      if (c1 < 0 || c2 < 0) {
        ERROR_data(TimeOut);
        return false;
      }

      data[currentByte] = byteval((char)c1, (char)c2);
      unsigned int imageAddress = ((unsigned int)byteval(addr[0], addr[1]) << 8) | byteval(addr[2], addr[3]);
      imageAddress += k;
      if (!storeExpectedByte(imageAddress, data[currentByte])) {
        emitLog(F("VERIFY_IMAGE_TOO_LARGE"));
      }
      currentByte++;
      progSize++;

      if (progSize > (type != Tiny4_5 ? type * 1024 : 512)) {
        ERROR_data(TooLarge);
        return false;
      }

      if (currentByte == 2 * words) {
        currentByte = 0;
        setPointer(tadrs);
        writeIO(NVMCMD, NVM_WORD_WRITE);

        for (int i = 0; i < 2 * words; i += 2) {
          tpi_send_byte(SSTp);
          tpi_send_byte(data[i]);
          tpi_send_byte(SSTp);
          tpi_send_byte(data[i + 1]);
          SPI.transfer(0xff);
          SPI.transfer(0xff);
        }

        while ((readIO(NVMCSR) & (1 << 7)) != 0x00) {}
        writeIO(NVMCMD, NVM_NOP);
        SPI.transfer(0xff);
        SPI.transfer(0xff);

        setPointer(tadrs);
        for (int j = 0; j < 2 * words; ++j) {
          tpi_send_byte(SLDp);
          b = tpi_receive_byte();
          if (b != data[j]) {
            ERROR_data(HexError);
            return false;
          }
        }

        tadrs += 2 * words;
      }
    }

    c = readHexChar();
    if (c < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    chksm[0] = (char)c;
    c = readHexChar();
    if (c < 0) {
      ERROR_data(TimeOut);
      return false;
    }
    chksm[1] = (char)c;
  }

  if (currentByte > 0) {
    while (currentByte < 2 * words) {
      data[currentByte++] = 0;
    }
    currentByte = 0;
    setPointer(tadrs);
    writeIO(NVMCMD, NVM_WORD_WRITE);

    for (int i = 0; i < 2 * words; i += 2) {
      tpi_send_byte(SSTp);
      tpi_send_byte(data[i]);
      tpi_send_byte(SSTp);
      tpi_send_byte(data[i + 1]);
      SPI.transfer(0xff);
      SPI.transfer(0xff);
    }

    while ((readIO(NVMCSR) & (1 << 7)) != 0x00) {}
    writeIO(NVMCMD, NVM_NOP);
    SPI.transfer(0xff);
    SPI.transfer(0xff);
  }

  Serial.print(F("LOG PROGRAMMED_BYTES_"));
  Serial.print(progSize, DEC);
  Serial.print(F("_IN_"));
  Serial.print((millis() - pgmStartTime) / 1000.0, DEC);
  Serial.println(F("_SECONDS"));
  return true;
}

bool waitForNvmReady(unsigned long timeoutMs) {
  unsigned long started = millis();
  while ((readIO(NVMCSR) & (1 << 7)) != 0x00) {
    if (tpiTimedOut) {
      return false;
    }
    if (millis() - started > timeoutMs) {
      return false;
    }
  }
  return true;
}

unsigned int flashByteLength() {
  if (type == Tiny4_5) {
    return 512;
  }
  return (unsigned int)type * 1024U;
}

bool supportsFlashVerify() {
  return flashByteLength() <= MAX_VERIFY_FLASH_BYTES;
}

void resetExpectedImage() {
  for (unsigned int i = 0; i < MAX_VERIFY_FLASH_BYTES; ++i) {
    expectedImage[i] = 0xFF;
  }
  expectedImageSize = 0;
  expectedImageValid = supportsFlashVerify();
}

bool storeExpectedByte(unsigned int address, uint8_t value) {
  if (!expectedImageValid || address >= MAX_VERIFY_FLASH_BYTES) {
    expectedImageValid = false;
    return false;
  }
  expectedImage[address] = value;
  if (address + 1 > expectedImageSize) {
    expectedImageSize = address + 1;
  }
  return true;
}

bool readFlashByteAt(unsigned int flashOffset, uint8_t &value) {
  if (flashOffset >= flashByteLength()) {
    return false;
  }
  setPointer(0x4000 + flashOffset);
  tpi_send_byte(SLD);
  value = tpi_receive_byte();
  return !tpiTimedOut;
}

bool readFlashPage(unsigned int flashOffset, uint8_t *buffer, uint8_t count) {
  for (uint8_t i = 0; i < count; ++i) {
    if (!readFlashByteAt(flashOffset + i, buffer[i])) {
      return false;
    }
  }
  return true;
}

bool pageMatchesMetadata(const uint8_t *buffer, const char *text) {
  uint8_t i = 0;
  while (text[i] != '\0') {
    if (i >= 16 || buffer[i] != (uint8_t)text[i]) {
      return false;
    }
    ++i;
  }
  while (i < 16) {
    if (buffer[i] != 0xFF) {
      return false;
    }
    ++i;
  }
  return true;
}

void emitMetadataField(const __FlashStringHelper *key, const uint8_t *buffer, uint8_t count) {
  Serial.print(F("META "));
  Serial.print(key);
  Serial.print(F(" "));
  for (uint8_t i = 0; i < count; ++i) {
    if (buffer[i] == 0xFF) {
      break;
    }
    Serial.write((char)buffer[i]);
  }
  Serial.println();
}

void dumpFlashWindow(unsigned int flashBytes) {
  uint8_t lineBytes[16];
  for (unsigned int base = 0; base < flashBytes; base += 16) {
    unsigned int count = (flashBytes - base > 16) ? 16 : (flashBytes - base);
    for (unsigned int i = 0; i < count; ++i) {
      if (!readFlashByteAt(base + i, lineBytes[i])) {
        emitLog(F("FLASH_DUMP_READ_FAILED"));
        return;
      }
    }
    Serial.print(F("DUMP "));
    outHex(0x4000 + base, 4);
    Serial.print(F(": "));
    for (unsigned int i = 0; i < count; ++i) {
      outHex(lineBytes[i], 2);
      Serial.print(F(" "));
    }
    Serial.println();
  }
}

bool dumpAndVerifyBlankFlash() {
  unsigned int flashBytes = flashByteLength();
  if (!supportsFlashVerify()) {
    emitLog(F("BLANK_VERIFY_UNSUPPORTED"));
    return false;
  }
  dumpFlashWindow(flashBytes);
  for (unsigned int i = 0; i < flashBytes; ++i) {
    uint8_t value = 0;
    if (!readFlashByteAt(i, value)) {
      return false;
    }
    if (value != 0xFF) {
      Serial.print(F("LOG BLANK_MISMATCH_AT_"));
      outHex(0x4000 + i, 4);
      Serial.print(F("_READ_"));
      outHex(value, 2);
      Serial.println();
      return false;
    }
  }
  emitLog(F("BLANK_VERIFY_OK"));
  return true;
}

bool verifyWrittenFlash() {
  if (!expectedImageValid || !supportsFlashVerify()) {
    emitLog(F("VERIFY_UNSUPPORTED"));
    return false;
  }
  bool ok = true;
  for (unsigned int i = 0; i < expectedImageSize; ++i) {
    uint8_t value = 0;
    if (!readFlashByteAt(i, value)) {
      return false;
    }
    if (value != expectedImage[i]) {
      Serial.print(F("LOG VERIFY_MISMATCH_AT_"));
      outHex(0x4000 + i, 4);
      Serial.print(F("_EXPECTED_"));
      outHex(expectedImage[i], 2);
      Serial.print(F("_READ_"));
      outHex(value, 2);
      Serial.println();
      ok = false;
    }
  }
  if (ok) {
    Serial.print(F("LOG VERIFIED_WRITTEN_BYTES_"));
    Serial.println(expectedImageSize);
    emitLog(F("VERIFY_OK"));
  }
  return ok;
}

bool eraseChip() {
  setPointer(0x4001);
  writeIO(NVMCMD, NVM_CHIP_ERASE);
  tpi_send_byte(SSTp);
  tpi_send_byte(0xAA);
  tpi_send_byte(SSTp);
  tpi_send_byte(0xAA);
  tpi_send_byte(SSTp);
  tpi_send_byte(0xAA);
  tpi_send_byte(SSTp);
  tpi_send_byte(0xAA);
  return waitForNvmReady(500);
}

void ERROR_data(char i) {
  Serial.print(F("LOG ERROR_"));
  switch (i) {
    case TimeOut:
      Serial.println(F("TIMEOUT"));
      break;
    case HexError:
      Serial.println(F("HEX"));
      break;
    case TooLarge:
      Serial.println(F("TOO_LARGE"));
      break;
    default:
      Serial.println(F("UNKNOWN"));
      break;
  }
}

void tpi_send_byte(uint8_t dataByte) {
  uint8_t par = dataByte;
  par ^= (par >> 4);
  par ^= (par >> 2);
  par ^= (par >> 1);

  SPI.transfer(0x03 | (dataByte << 3));
  SPI.transfer(0xf0 | (par << 3) | (dataByte >> 5));
}

uint8_t tpi_receive_byte(void) {
  uint16_t guard = 0;
  do {
    b1 = SPI.transfer(0xff);
    guard++;
    if (guard > 512) {
      tpiTimedOut = true;
      return 0xFF;
    }
  } while (0xff == b1);

  b2 = SPI.transfer(0xff);
  if (0x0f == (0x0f & b1)) {
    b3 = SPI.transfer(0xff);
  }

  while (0x7f != b1) {
    b2 <<= 1;
    if (0x80 & b1) {
      b2 |= 1;
    }
    b1 <<= 1;
    b1 |= 0x01;
  }
  return b2;
}

void send_skey(uint64_t nvm_key) {
  tpi_send_byte(SKEY);
  while (nvm_key) {
    tpi_send_byte(nvm_key & 0xFF);
    nvm_key >>= 8;
  }
}

void setPointer(unsigned short address) {
  adrs = address;
  tpi_send_byte(SSTPRL);
  tpi_send_byte(address & 0xff);
  tpi_send_byte(SSTPRH);
  tpi_send_byte((address >> 8) & 0xff);
}

void writeIO(uint8_t address, uint8_t value) {
  tpi_send_byte(0x90 | (address & 0x0F) | ((address & 0x30) << 1));
  tpi_send_byte(value);
}

uint8_t readIO(uint8_t address) {
  tpi_send_byte(0x10 | (address & 0x0F) | ((address & 0x30) << 1));
  return tpi_receive_byte();
}

void writeCSS(uint8_t address, uint8_t value) {
  tpi_send_byte(0xC0 | address);
  tpi_send_byte(value);
}

uint8_t readCSS(uint8_t address) {
  tpi_send_byte(0x80 | address);
  return tpi_receive_byte();
}

uint8_t byteval(char c1, char c2) {
  uint8_t by;
  if (c1 <= '9') {
    by = c1 - '0';
  } else {
    by = c1 - 'A' + 10;
  }
  by = by << 4;
  if (c2 <= '9') {
    by += c2 - '0';
  } else {
    by += c2 - 'A' + 10;
  }
  return by;
}

void outHex(unsigned int n, char l) {
  for (char count = l - 1; count > 0; count--) {
    if (((n >> (count * 4)) & 0x0f) == 0) {
      Serial.print(F("0"));
    } else {
      break;
    }
  }
  Serial.print(n, HEX);
}
