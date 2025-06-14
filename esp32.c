/********************************************************************
 *  3‑phase generator governor – ESP32
 *  Inputs : H11AA1 -> GPIO25, GPIO26, GPIO27  (D25, D26, D27)
 *  Output : Servo  -> GPIO16 (D16)
 *  Target : 50.00 Hz
 ********************************************************************/

#include <ESP32Servo.h>
#include <PID_v1.h>

/* ------------------- Pin assignments ------------------- */
constexpr uint8_t PIN_PHASE_A = 25;   // D25
constexpr uint8_t PIN_PHASE_B = 26;   // D26
constexpr uint8_t PIN_PHASE_C = 27;   // D27
constexpr uint8_t PIN_SERVO   = 16;   // D16

/* ------------------- Servo limits ---------------------- */
constexpr int SERVO_MIN =  80;   // tune for your linkage
constexpr int SERVO_MAX = 120;   // "
/* Servo starts wherever the mechanical governor left it;
   we won't write anything until we see a valid frequency. */
int servoPos = -1;               // -1 = “not initialised yet”

/* ---------------- Frequency measurement ---------------- */
volatile uint32_t lastT_A = 0, lastT_B = 0, lastT_C = 0;
volatile uint32_t periodA = 0,  periodB = 0,  periodC = 0;

/* ISR – record the time between consecutive rising edges */
void IRAM_ATTR isrA() { uint32_t now = micros(); periodA = now - lastT_A; lastT_A = now; }
void IRAM_ATTR isrB() { uint32_t now = micros(); periodB = now - lastT_B; lastT_B = now; }
void IRAM_ATTR isrC() { uint32_t now = micros(); periodC = now - lastT_C; lastT_C = now; }

/* ------------------- PID parameters -------------------- */
double setpoint = 100.0;   // 50 Hz
double input    = 0.0;    // averaged measured Hz
double output   = 0.0;    // servo change request

/* Tune these three numbers on your rig */
double Kp = 2.0;
double Ki = 0.7;
double Kd = 0.5;

PID pid(&input, &output, &setpoint, Kp, Ki, Kd, DIRECT);

/* ------------------- Servo object ---------------------- */
Servo governor;

/* Helper – convert period (µs) to Hz, guard against zero */
inline double periodToHz(uint32_t p) { return (p > 0) ? 1e6 / double(p) : 0.0; }

/* -------------------------- SETUP ---------------------- */
void setup()
{
  Serial.begin(115200);

  pinMode(PIN_PHASE_A, INPUT);
  pinMode(PIN_PHASE_B, INPUT);
  pinMode(PIN_PHASE_C, INPUT);

  attachInterrupt(digitalPinToInterrupt(PIN_PHASE_A), isrA, RISING);
  attachInterrupt(digitalPinToInterrupt(PIN_PHASE_B), isrB, RISING);
  attachInterrupt(digitalPinToInterrupt(PIN_PHASE_C), isrC, RISING);

  governor.attach(PIN_SERVO);
  /* No initial write() here – keeps servo exactly where it already is */

  pid.SetOutputLimits(-1, 1);   // max ±3 deg change per loop
  pid.SetSampleTime(50);        // run PID every 50 ms
  pid.SetMode(AUTOMATIC);

  Serial.println("PID governor ready");
}

/* -------------------------- LOOP ----------------------- */
void loop()
{
  /* ----- 1. Calculate average frequency ----- */
  uint32_t pA, pB, pC;
  noInterrupts();
  pA = periodA; pB = periodB; pC = periodC;
  interrupts();

  /* Require all three periods non‑zero to declare “valid” */
  if (pA && pB && pC) {
    double fA = periodToHz(pA);
    double fB = periodToHz(pB);
    double fC = periodToHz(pC);
    input = (fA + fB + fC) / 3.0;
  } else {
    /* not running yet – skip control */
    delay(20);
    return;
  }

  /* ----- 2. First‑time servo initialisation ----- */
  if (servoPos < 0) {                 // first valid reading
    servoPos = governor.read();       // whatever angle servo is at now
    pid.SetMode(AUTOMATIC);           // ensure PID active
  }

  /* ----- 3. PID compute & servo update ----- */
  pid.Compute();            // updates ‘output’
  servoPos += int(output);  // apply incremental change
  servoPos = constrain(servoPos, SERVO_MIN, SERVO_MAX);
  governor.write(servoPos);

  /* ----- 4. Debug print (optional) ----- */
  static uint32_t dbgTimer = 0;
  if (millis() - dbgTimer > 500) {
    dbgTimer = millis();
    Serial.print("Hz:");
    Serial.print(input, 2);
    Serial.print("  Servo:");
    Serial.println(servoPos);
  }

  delay(20);   // main loop ~50 Hz
}
