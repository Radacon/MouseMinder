/*
  MouseMinder low-power alarm

  PMS150C-U06

  PA6: sleep/wake pushbutton, externally pulled low, switch to VDD
  PA4: LED, active low
  PA3: piezo input while quiet; Timer2 tone output while sounding
*/

#include <stdint.h>
#include "sdcc_intellisense.h"
#include <pdk/device.h>

#include "auto_sysclock.h"
#include "startup.h"
#include "delay.h"

/*------------------------------------------------------------------
  User tuning
 ------------------------------------------------------------------*/

#define LED_PULSE_MS               20u
#define EVENT_SLEEP_MS           1000u

#define PIEZO_TONE_MS              50u
#define PIEZO_GAP_MS               50u
#define STARTUP_BEEP_COUNT          3u
#define LED_FLASHES_PER_BEEPS       4u

/*
 * Timer2 period mode toggles PA3 at:
 *
 *   F_CPU / (2 * (PIEZO_TONE_BOUND + 1))
 *
 * 52 kHz / (2 * 6) = approximately 4.33 kHz.
 */
#define PIEZO_TONE_BOUND            5u

/*------------------------------------------------------------------
  Pins
 ------------------------------------------------------------------*/

#define PIEZO_BIT                   3u
#define LED_BIT                     4u
#define BUTTON_BIT                  6u

#define PIEZO_MASK          (1u << PIEZO_BIT)
#define LED_MASK            (1u << LED_BIT)
#define BUTTON_MASK         (1u << BUTTON_BIT)

#define turnLedOn()         (PA &= (uint8_t)~LED_MASK)
#define turnLedOff()        (PA |= LED_MASK)
#define buttonIsPressed()   ((PA & BUTTON_MASK) != 0)

/*------------------------------------------------------------------
  Timer16 timed STOPEXE sleep
 ------------------------------------------------------------------*/

/*
 * Timer16 uses undivided ILRC and wakes on the falling edge of bit 15.
 * Loading 65536 - ticks therefore gives a delay of "ticks" ILRC clocks.
 */
#define TIMER16_SLEEP_CONFIG \
    (T16M_CLK_ILRC | T16M_CLK_DIV1 | T16M_INTSRC_15BIT)

#define MS_TO_ILRC_TICKS(ms) \
    ((uint16_t)(((uint32_t)(ms) * (uint32_t)F_CPU + 999u) / 1000u))

#define sleepMilliseconds(ms, piezoWake) \
    sleepTicks(MS_TO_ILRC_TICKS(ms), piezoWake)

static uint16_t timer16Load;

static void piezoInput(void)
{
    TM2C = TM2C_CLK_DISABLE;
    INTRQ &= (uint8_t)~INTRQ_TM2;
    PA &= (uint8_t)~PIEZO_MASK;
    PAC &= (uint8_t)~PIEZO_MASK;
}

static uint8_t activeDelayMilliseconds(uint16_t milliseconds)
{
    PADIER = BUTTON_MASK;

    /*
     * This helper is used only with compile-time constants.  Staying awake
     * here matches the ATtiny's _delay_ms() cadence and avoids PMS150C
     * STOPEXE wake-up latency on short delays.
     */
    if (milliseconds == PIEZO_GAP_MS)
        _delay_ms(PIEZO_GAP_MS);
    else
        _delay_ms(LED_PULSE_MS);

    return buttonIsPressed();
}

static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
{
    uint8_t buttonPressed;

    T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
    timer16Load = (uint16_t)(65535u - ticks + 1u);
    __asm
        stt16 _timer16Load
    __endasm;
    INTEGS |= INTEGS_T16_FALLING;
    INTRQ &= (uint8_t)~INTRQ_T16;

    /*
     * PA6 always wakes active waits.  PA3 also wakes quiet waits, but is
     * excluded while Timer2 is driving the tone.
     */
    PADIER = (uint8_t)(BUTTON_MASK |
                      (piezoWake ? PIEZO_MASK : (uint8_t)0u));

    __asm
        stopexe
    __endasm;

    /* Read PA6 before disabling its digital input buffer. */
    buttonPressed = buttonIsPressed();
    PADIER = 0;
    INTRQ &= (uint8_t)~INTRQ_T16;

    return buttonPressed;
}

/*------------------------------------------------------------------
  Piezo tone
 ------------------------------------------------------------------*/

static void startTone(void)
{
    /* Keep the PA6 button readable; PA3 is driven by Timer2. */
    PADIER = BUTTON_MASK;
    PAC |= PIEZO_MASK;
    TM2CT = 0;
    TM2B = PIEZO_TONE_BOUND;
    TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
    TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
}

static uint8_t tonePulse(void)
{
    startTone();
    _delay_ms(PIEZO_TONE_MS);
    piezoInput();

    return buttonIsPressed();
}

static uint8_t startupChirps(void)
{
    uint8_t count = STARTUP_BEEP_COUNT;

    while (count--)
    {
        if (tonePulse())
            return 1;

        /* Match the ATtiny sequence: gaps only between startup chirps. */
        if (count && activeDelayMilliseconds(PIEZO_GAP_MS))
            return 1;
    }

    return 0;
}

/*------------------------------------------------------------------
  Deep sleep
 ------------------------------------------------------------------*/

static void waitForButtonRelease(void)
{
    PADIER = BUTTON_MASK;

    while (buttonIsPressed())
    {
        T16M = T16M_CLK_DISABLE;

        __asm
            stopexe
        __endasm;
    }

    PADIER = 0;
}

static void deepSleep(void)
{
    uint8_t buttonPressed;

    turnLedOff();
    piezoInput();
    T16M = T16M_CLK_DISABLE;

    /*
     * PMS150C GPIO sleep wake detects a pin transition rather than a
     * selectable edge.  With PA6 externally pulled low, software accepts
     * the high level as the wake-button press.
     */
    PADIER = BUTTON_MASK | PIEZO_MASK;

    __asm
        stopsys
    __endasm;

    /* Determine whether PA6 or the PA3 piezo caused the wake. */
    buttonPressed = buttonIsPressed();
    PADIER = 0;

    /* Do not interpret the same held button press as an immediate off. */
    if (buttonPressed)
        waitForButtonRelease();
}

/*------------------------------------------------------------------
  Setup and active pattern
 ------------------------------------------------------------------*/

static void setup(void)
{
    /* LED off; button and piezo initially inputs. */
    PA = LED_MASK;
    PAC = LED_MASK;
    PAPH = 0;
    PADIER = 0;

    GPCC = 0;
    GPCS = 0;
    TM2C = 0;
    T16M = 0;

    MISC |= MISC_LVR_DISABLE;

    /*
     * PA5 reset, watchdog and IHRC are disabled.  ILRC remains the system
     * clock and is automatically stopped by STOPSYS.
     */
    CLKMD &= (uint8_t)~(CLKMD_ENABLE_PRSTB |
                        CLKMD_ENABLE_WATCHDOG |
                        CLKMD_ENABLE_IHRC);

    INTEN = 0;
    INTRQ = 0;
}

static uint8_t activeAlert(void)
{
    uint8_t flashCount = 0;

    while (1)
    {
        turnLedOn();

        if (activeDelayMilliseconds(LED_PULSE_MS))
        {
            turnLedOff();
            return 1;
        }

        turnLedOff();

        if (++flashCount >= LED_FLASHES_PER_BEEPS)
        {
            flashCount = 0;

            if (tonePulse())
                return 1;

            if (activeDelayMilliseconds(PIEZO_GAP_MS))
                return 1;

            if (tonePulse())
                return 1;
        }

        /*
         * Match the ATtiny cadence: the approximately one-second sleep
         * begins after the LED pulse and any scheduled pair of beeps.
         */
        if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
            return 1;
    }
}

void main(void)
{
    setup();

    while (1)
    {
        /* Power-up and every wake begin with the introductory beep pattern. */
        if (startupChirps())
        {
            waitForButtonRelease();
            deepSleep();
            continue;
        }

        activeAlert();
        waitForButtonRelease();
        deepSleep();
    }
}

/*------------------------------------------------------------------
  Startup
 ------------------------------------------------------------------*/

unsigned char STARTUP_FUNCTION(void)
{
    AUTO_INIT_SYSCLOCK();
    AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);

    return 0;
}
