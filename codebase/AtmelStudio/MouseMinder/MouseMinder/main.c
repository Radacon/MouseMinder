#define F_CPU 1000000UL
#include <avr/io.h>
#include <util/delay.h>
#include <avr/interrupt.h>
#include <avr/sleep.h>
#include <avr/wdt.h>

// -------------------- helpers --------------------

// Toggle PB2 by writing 1 to PINB bit
static inline void pb2_toggle(void) {
	asm volatile("sbi %0, %1" :: "I"(_SFR_IO_ADDR(PINB)), "I"(PB2));
}

// 125 µs half period @ 1 MHz
static inline void half_period_125us(void) {
	uint8_t n = 41; // 3*n - 1 = 122 cycles
	asm volatile(
	"1: dec %[n]   \n\t"
	"brne 1b       \n\t"
	"nop           \n\t"
	: [n] "+r"(n)
	);
}

// 4 kHz tone on PB2
static inline void tone_pb2_4khz_ms(uint16_t duration_ms)
{
	uint16_t periods = duration_ms * 4;

	while (periods--) {
		pb2_toggle();
		half_period_125us();
		pb2_toggle();
		half_period_125us();
	}

	PORTB &= ~(1 << PB2); // force low
}

// 20 ms pulse on PB0
static inline void pulse_pb0_20ms(void)
{
	PORTB |=  (1 << PB0);
	_delay_ms(20);
	PORTB &= ~(1 << PB0);
}

// -------------------- watchdog sleep --------------------

volatile uint8_t wdt_woke = 0;

ISR(WDT_vect)
{
	wdt_woke = 1;
}

static void watchdog_init_1s_interrupt(void)
{
	cli();
	wdt_reset();

	// Clear watchdog reset flag
	RSTFLR &= ~(1 << WDRF);

	// Timed sequence required on ATtiny10
	CCP = 0xD8;
	WDTCSR = (1 << WDIE) | (1 << WDP2) | (1 << WDP1); // ~1 second, interrupt only

	sei();
}

static void sleep_until_wdt(void)
{
	wdt_woke = 0;

	set_sleep_mode(SLEEP_MODE_PWR_DOWN);
	sleep_enable();

	// Optional: disable brown-out here if your headers/device support it
	// sleep_bod_disable();

	sei();
	sleep_cpu();

	// resumes here after watchdog interrupt
	sleep_disable();

	while (!wdt_woke) {
		// should already be set by ISR, this is just defensive
	}
}

int main(void)
{
	// PB2 + PB0 outputs
	DDRB  |= (1 << PB2) | (1 << PB0);
	PORTB &= ~((1 << PB2) | (1 << PB0));

	// Shut off ADC to save power
	ADCSRA &= ~(1 << ADEN);

	watchdog_init_1s_interrupt();

	// Startup chirps
	tone_pb2_4khz_ms(50);
	_delay_ms(50);
	tone_pb2_4khz_ms(50);
	_delay_ms(50);
	tone_pb2_4khz_ms(50);

	uint8_t flash_count = 0;

	while (1)
	{
		// LED pulse every ~1 second
		pulse_pb0_20ms();

		flash_count++;

		// Two beeps every 4 seconds
		if (flash_count >= 4)
		{
			flash_count = 0;

			tone_pb2_4khz_ms(50);
			_delay_ms(50);
			tone_pb2_4khz_ms(50);
		}

		// Sleep for ~1 second between events
		sleep_until_wdt();
	}
}