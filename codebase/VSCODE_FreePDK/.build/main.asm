;--------------------------------------------------------
; File Created by SDCC : free open source ANSI-C Compiler
; Version 4.2.0 #13081 (Linux)
;--------------------------------------------------------
	.module main
	.optsdcc -mpdk13
	

; default segment ordering in RAM for linker
	.area DATA
	.area OSEG (OVR,DATA)

;--------------------------------------------------------
; Public variables in this module
;--------------------------------------------------------
	.globl __sdcc_external_startup
	.globl _main
	.globl __delay_loop_32
	.globl __delay_loop_16
	.globl __delay_loop_8
	.globl __misc
	.globl __gpcs
	.globl __gpcc
	.globl __bgtr
	.globl __tm2b
	.globl __tm2s
	.globl __tm2ct
	.globl __tm2c
	.globl __t16c
	.globl __t16m
	.globl __paph
	.globl __pac
	.globl __pa
	.globl __padier
	.globl __integs
	.globl __intrq
	.globl __inten
	.globl __eoscr
	.globl __ilrcr
	.globl __ihrcr
	.globl __clkmd
	.globl __sp
	.globl __flag
	.globl __delay_loop_32_PARM_1
	.globl __delay_loop_16_PARM_1
	.globl __delay_loop_8_PARM_1
;--------------------------------------------------------
; special function registers
;--------------------------------------------------------
	.area RSEG (ABS)
	.org 0x0000
__flag	=	0x0000
__sp	=	0x0002
__clkmd	=	0x0003
__ihrcr	=	0x000b
__ilrcr	=	0x001f
__eoscr	=	0x000a
__inten	=	0x0004
__intrq	=	0x0005
__integs	=	0x000c
__padier	=	0x000d
__pa	=	0x0010
__pac	=	0x0011
__paph	=	0x0012
__t16m	=	0x0006
__t16c::
	.ds 2
__tm2c	=	0x001c
__tm2ct	=	0x001d
__tm2s	=	0x0017
__tm2b	=	0x0009
__bgtr	=	0x0019
__gpcc	=	0x001a
__gpcs	=	0x001e
__misc	=	0x001b
;--------------------------------------------------------
; ram data
;--------------------------------------------------------
	.area DATA
__delay_loop_8_PARM_1:
	.ds 1
__delay_loop_16_PARM_1:
	.ds 2
__delay_loop_32_PARM_1:
	.ds 4
_timer16Load:
	.ds 2
_activeDelayMilliseconds_PARM_1:
	.ds 2
_sleepTicks_PARM_1:
	.ds 2
_sleepTicks_PARM_2:
	.ds 1
_startTone_PARM_1:
	.ds 1
_startupChirps_sloc1_1_0:
	.ds 2
_startupChirps_sloc2_1_0:
	.ds 1
_startupChirps_sloc3_1_0:
	.ds 1
_startupChirps_sloc4_1_0:
	.ds 1
_startupChirps_sloc5_1_0:
	.ds 2
_startupChirps_sloc6_1_0:
	.ds 2
_startupChirps_sloc7_1_0:
	.ds 2
_activeAlert_sloc8_1_0:
	.ds 1
;--------------------------------------------------------
; overlayable items in ram
;--------------------------------------------------------
	.area	OSEG (OVR,DATA)
_sleepTicks_sloc0_1_0:
	.ds 1
;--------------------------------------------------------
; Stack segment in internal ram
;--------------------------------------------------------
	.area	SSEG
__start__stack:
	.ds	1

;--------------------------------------------------------
; absolute external ram data
;--------------------------------------------------------
	.area DABS (ABS)
;--------------------------------------------------------
; interrupt vector
;--------------------------------------------------------
	.area HOME
__interrupt_vect:
	.area	HEADER (ABS)
	.org	 0x0020
	reti
;--------------------------------------------------------
; global & static initialisations
;--------------------------------------------------------
	.area HOME
	.area GSINIT
	.area GSFINAL
	.area GSINIT
	.area	PREG (ABS)
	.org 0x00
p::
	.ds 2
	.area	HEADER (ABS)
	.org 0x0000
	nop
	clear	p+1
	mov	a, #s_OSEG
	add	a, #l_OSEG + 1
	and	a, #0xfe
	mov.io	sp, a
	call	__sdcc_external_startup
	goto	s_GSINIT
	.area GSINIT
__sdcc_init_data:
	mov	a, #s_DATA
	mov	p, a
	goto	00002$
00001$:
	mov	a, #0x00
	idxm	p, a
	inc	p
	mov	a, #s_DATA
00002$:
	add	a, #l_DATA
	ceqsn	a, p
	goto	00001$
	.area GSFINAL
	goto	__sdcc_program_startup
;--------------------------------------------------------
; Home
;--------------------------------------------------------
	.area HOME
	.area HOME
__sdcc_program_startup:
	goto	_main
;	return from main will return to caller
;--------------------------------------------------------
; code
;--------------------------------------------------------
	.area CODE
;	./include/delay.h: 34: void _delay_loop_8(uint8_t loop_ctr) {
;	-----------------------------------------
;	 function _delay_loop_8
;	-----------------------------------------
__delay_loop_8:
;	./include/delay.h: 44: __endasm;
	00001$:
; 4 cycles per loop
	dzsn	__delay_loop_8_PARM_1 ; 1 cycle + 1 cycle for final skip
	goto	00001$ ; 2 cycles
00101$:
;	./include/delay.h: 45: }
	ret
;	./include/delay.h: 48: void _delay_loop_16(uint16_t loop_ctr) {
;	-----------------------------------------
;	 function _delay_loop_16
;	-----------------------------------------
__delay_loop_16:
;	./include/delay.h: 65: __endasm;
	00001$:
; 8 cycles per loop
	nop	; 1 cycle
	dec	__delay_loop_16_PARM_1+0 ; 1 cycle
	subc	__delay_loop_16_PARM_1+1 ; 1 cycle
	mov	a, __delay_loop_16_PARM_1+0 ; 1 cycle
	or	a, __delay_loop_16_PARM_1+1 ; 1 cycle
	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
	goto	00001$ ; 2 cycles
00101$:
;	./include/delay.h: 66: }
	ret
;	./include/delay.h: 69: void _delay_loop_32(uint32_t loop_ctr) {
;	-----------------------------------------
;	 function _delay_loop_32
;	-----------------------------------------
__delay_loop_32:
;	./include/delay.h: 94: __endasm;
	00001$:
; 12 cycles per loop
	nop	; 1 cycle
	dec	__delay_loop_32_PARM_1+0 ; 1 cycle
	subc	__delay_loop_32_PARM_1+1 ; 1 cycle
	subc	__delay_loop_32_PARM_1+2 ; 1 cycle
	subc	__delay_loop_32_PARM_1+3 ; 1 cycle
	mov	a, __delay_loop_32_PARM_1+0 ; 1 cycle
	or	a, __delay_loop_32_PARM_1+1 ; 1 cycle
	or	a, __delay_loop_32_PARM_1+2 ; 1 cycle
	or	a, __delay_loop_32_PARM_1+3 ; 1 cycle
	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
	goto	00001$ ; 2 cycles
00101$:
;	./include/delay.h: 95: }
	ret
;	main.c: 84: static void piezoInput(void)
;	-----------------------------------------
;	 function piezoInput
;	-----------------------------------------
_piezoInput:
;	main.c: 86: TM2C = TM2C_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__tm2c, a
;	main.c: 87: INTRQ &= (uint8_t)~INTRQ_TM2;
	set0.io	__intrq, #6
;	main.c: 88: PA &= (uint8_t)~PIEZO_MASK;
	set0.io	__pa, #3
;	main.c: 89: PAC &= (uint8_t)~PIEZO_MASK;
	set0.io	__pac, #3
;	main.c: 90: }
	ret
;	main.c: 92: static uint8_t activeDelayMilliseconds(uint16_t milliseconds)
;	-----------------------------------------
;	 function activeDelayMilliseconds
;	-----------------------------------------
_activeDelayMilliseconds:
;	main.c: 94: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 101: if (milliseconds == PIEZO_GAP_MS)
	mov	a, _activeDelayMilliseconds_PARM_1+1
	mov	p, a
	mov	a, _activeDelayMilliseconds_PARM_1+0
	ceqsn	a, #0x32
	goto	00102$
	mov	a, p
	ceqsn	a, #0x00
	goto	00102$
;	main.c: 102: _delay_ms(PIEZO_GAP_MS);
	mov	a, #0x43
	mov	__delay_loop_16_PARM_1+0, a
	mov	a, #0x01
	mov	__delay_loop_16_PARM_1+1, a
	call	__delay_loop_16
	goto	00103$
00102$:
;	main.c: 104: _delay_ms(LED_PULSE_MS);
	mov	a, #0x80
	mov	__delay_loop_16_PARM_1+0, a
	clear	__delay_loop_16_PARM_1+1
	call	__delay_loop_16
00103$:
;	main.c: 106: return buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 107: }
	ret
;	main.c: 109: static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
;	-----------------------------------------
;	 function sleepTicks
;	-----------------------------------------
_sleepTicks:
;	main.c: 113: T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
	mov	a, #0xc7
	mov.io	__t16m, a
;	main.c: 114: timer16Load = (uint16_t)(65535u - ticks + 1u);
	mov	a, #0x00
	sub	a, _sleepTicks_PARM_1+0
	mov	_timer16Load+0, a
	mov	a, #0x00
	subc	a, _sleepTicks_PARM_1+1
	mov	_timer16Load+1, a
;	main.c: 117: __endasm;
	stt16	_timer16Load
;	main.c: 118: INTEGS |= INTEGS_T16_FALLING;
	set1.io	__integs, #4
;	main.c: 119: INTRQ &= (uint8_t)~INTRQ_T16;
	set0.io	__intrq, #2
;	main.c: 126: (piezoWake ? PIEZO_MASK : (uint8_t)0u));
	mov	a, _sleepTicks_PARM_2+0
	ceqsn	a, #0x00
	goto	00109$
	goto	00103$
00109$:
	mov	a, #0x08
	goto	00104$
00103$:
	mov	a, #0x00
00104$:
	or	a, #0x40
	mov.io	__padier, a
;	main.c: 130: __endasm;
	stopexe
;	main.c: 133: buttonPressed = buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
	mov	_sleepTicks_sloc0_1_0+0, a
;	main.c: 134: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 135: INTRQ &= (uint8_t)~INTRQ_T16;
	set0.io	__intrq, #2
;	main.c: 137: return buttonPressed;
	mov	a, _sleepTicks_sloc0_1_0+0
;	main.c: 138: }
	ret
;	main.c: 144: static void startTone(uint8_t timerDivisor)
;	-----------------------------------------
;	 function startTone
;	-----------------------------------------
_startTone:
;	main.c: 147: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 148: PAC |= PIEZO_MASK;
	set1.io	__pac, #3
;	main.c: 149: TM2CT = 0;
	mov	a, #0x00
	mov.io	__tm2ct, a
;	main.c: 150: TM2B = (uint8_t)(timerDivisor - 1u);
	mov	a, _startTone_PARM_1+0
	sub	a, #0x01
	mov.io	__tm2b, a
;	main.c: 151: TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
	mov	a, #0x00
	mov.io	__tm2s, a
;	main.c: 152: TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
	mov	a, #0x48
	mov.io	__tm2c, a
;	main.c: 153: }
	ret
;	main.c: 155: static uint8_t tonePulse(void)
;	-----------------------------------------
;	 function tonePulse
;	-----------------------------------------
_tonePulse:
;	main.c: 157: startTone(PIEZO_TONE_BOUND + 1u);
	mov	a, #0x06
	mov	_startTone_PARM_1+0, a
	call	_startTone
;	main.c: 158: _delay_ms(PIEZO_TONE_MS);
	mov	a, #0x43
	mov	__delay_loop_16_PARM_1+0, a
	mov	a, #0x01
	mov	__delay_loop_16_PARM_1+1, a
	call	__delay_loop_16
;	main.c: 159: piezoInput();
	call	_piezoInput
;	main.c: 161: return buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 162: }
	ret
;	main.c: 164: static uint8_t startupChirps(void)
;	-----------------------------------------
;	 function startupChirps
;	-----------------------------------------
_startupChirps:
;	main.c: 166: uint16_t offset = 0;
	clear	_startupChirps_sloc1_1_0+0
	clear	_startupChirps_sloc1_1_0+1
;	main.c: 169: while (step--)
	mov	a, #0x0a
	mov	_startupChirps_sloc2_1_0+0, a
00109$:
	mov	a, _startupChirps_sloc2_1_0+0
	dec	_startupChirps_sloc2_1_0+0
	ceqsn	a, #0x00
	goto	00138$
	goto	00111$
00138$:
;	main.c: 171: uint8_t timerDivisor = chirpPattern[offset];
	mov	a, #<(_chirpPattern + 0)
	add	a, _startupChirps_sloc1_1_0+0
	mov	p, a
	mov	a, #>(_chirpPattern + 0x8000 + 0)
	addc	a, _startupChirps_sloc1_1_0+1
	call	__gptrget
	mov	_startupChirps_sloc3_1_0+0, a
;	main.c: 172: uint16_t duration = (uint16_t)chirpPattern[offset + 1u] |
	mov	a, _startupChirps_sloc1_1_0+0
	mov	_startupChirps_sloc4_1_0+0, a
	add	a, #0x01
	add	a, #<(_chirpPattern + 0)
	mov	p, a
	mov	a, #0x00
	addc	a
	add	a, #>(_chirpPattern + 0x8000 + 0)
	call	__gptrget
	mov	_startupChirps_sloc5_1_0+0, a
	clear	_startupChirps_sloc5_1_0+1
	mov	a, _startupChirps_sloc4_1_0+0
	add	a, #0x02
	add	a, #<(_chirpPattern + 0)
	mov	p, a
	mov	a, #0x00
	addc	a
	add	a, #>(_chirpPattern + 0x8000 + 0)
	call	__gptrget
	mov	p, a
	mov	a, #0x00
	or	a, _startupChirps_sloc5_1_0+0
	mov	_startupChirps_sloc6_1_0+0, a
	mov	a, p
	or	a, _startupChirps_sloc5_1_0+1
	mov	_startupChirps_sloc6_1_0+1, a
;	main.c: 174: offset += CHIRP_STEP_BYTES;
	mov	a, _startupChirps_sloc1_1_0+0
	add	a, #0x03
	mov	p, a
	mov	a, _startupChirps_sloc1_1_0+1
	addc	a
	mov	_startupChirps_sloc1_1_0+1, a
	mov	a, p
	mov	_startupChirps_sloc1_1_0+0, a
;	main.c: 176: if (timerDivisor)
	mov	a, _startupChirps_sloc3_1_0+0
	ceqsn	a, #0x00
	goto	00139$
	goto	00102$
00139$:
;	main.c: 177: startTone(timerDivisor);
	mov	a, _startupChirps_sloc3_1_0+0
	mov	_startTone_PARM_1+0, a
	call	_startTone
	goto	00103$
00102$:
;	main.c: 179: piezoInput();
	call	_piezoInput
00103$:
;	main.c: 181: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 182: while (duration--)
	mov	a, _startupChirps_sloc6_1_0+0
	mov	_startupChirps_sloc7_1_0+0, a
	mov	a, _startupChirps_sloc6_1_0+1
	mov	_startupChirps_sloc7_1_0+1, a
00106$:
	mov	a, _startupChirps_sloc7_1_0+1
	mov	p, a
	mov	a, _startupChirps_sloc7_1_0+0
	dec	_startupChirps_sloc7_1_0+0
	subc	_startupChirps_sloc7_1_0+1
	or	a, p
	ceqsn	a, #0x00
	goto	00140$
	goto	00109$
00140$:
;	main.c: 184: _delay_ms(1);
	mov	a, #0x05
	mov	__delay_loop_16_PARM_1+0, a
	clear	__delay_loop_16_PARM_1+1
	call	__delay_loop_16
;	main.c: 185: if (buttonIsPressed())
	mov.io	a, __pa
	mov	p, a
	t1sn	p, #6
	goto	00106$
;	main.c: 187: piezoInput();
	call	_piezoInput
;	main.c: 188: return 1;
	ret	#0x01
00111$:
;	main.c: 193: piezoInput();
	call	_piezoInput
;	main.c: 194: return 0;
;	main.c: 195: }
	ret	#0x00
;	main.c: 201: static void waitForButtonRelease(void)
;	-----------------------------------------
;	 function waitForButtonRelease
;	-----------------------------------------
_waitForButtonRelease:
;	main.c: 203: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 205: while (buttonIsPressed())
00101$:
	mov.io	a, __pa
	mov	p, a
	t1sn	p, #6
	goto	00103$
;	main.c: 207: T16M = T16M_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 211: __endasm;
	stopexe
	goto	00101$
00103$:
;	main.c: 214: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 215: }
	ret
;	main.c: 217: static void deepSleep(void)
;	-----------------------------------------
;	 function deepSleep
;	-----------------------------------------
_deepSleep:
;	main.c: 221: turnLedOff();
	set1.io	__pa, #4
;	main.c: 222: piezoInput();
	call	_piezoInput
;	main.c: 223: T16M = T16M_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 230: PADIER = BUTTON_MASK | PIEZO_MASK;
	mov	a, #0x48
	mov.io	__padier, a
;	main.c: 234: __endasm;
	stopsys
;	main.c: 237: buttonPressed = buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 238: PADIER = 0;
	push	af
	mov	a, #0x00
	mov.io	__padier, a
	pop	af
;	main.c: 241: if (buttonPressed)
	ceqsn	a, #0x00
	goto	00109$
	goto	00103$
00109$:
;	main.c: 242: waitForButtonRelease();
	goto	_waitForButtonRelease
00103$:
;	main.c: 243: }
	ret
;	main.c: 249: static void setup(void)
;	-----------------------------------------
;	 function setup
;	-----------------------------------------
_setup:
;	main.c: 252: PA = LED_MASK;
	mov	a, #0x10
	mov.io	__pa, a
;	main.c: 253: PAC = LED_MASK;
	mov	a, #0x10
	mov.io	__pac, a
;	main.c: 254: PAPH = 0;
	mov	a, #0x00
	mov.io	__paph, a
;	main.c: 255: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 257: GPCC = 0;
	mov	a, #0x00
	mov.io	__gpcc, a
;	main.c: 258: GPCS = 0;
	mov	a, #0x00
	mov.io	__gpcs, a
;	main.c: 259: TM2C = 0;
	mov	a, #0x00
	mov.io	__tm2c, a
;	main.c: 260: T16M = 0;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 262: MISC |= MISC_LVR_DISABLE;
	set1.io	__misc, #2
;	main.c: 270: CLKMD_ENABLE_IHRC);
	mov.io	a, __clkmd
	and	a, #0xec
	mov.io	__clkmd, a
;	main.c: 272: INTEN = 0;
	mov	a, #0x00
	mov.io	__inten, a
;	main.c: 273: INTRQ = 0;
	mov	a, #0x00
	mov.io	__intrq, a
;	main.c: 274: }
	ret
;	main.c: 276: static uint8_t activeAlert(void)
;	-----------------------------------------
;	 function activeAlert
;	-----------------------------------------
_activeAlert:
;	main.c: 278: uint8_t flashCount = 0;
	clear	_activeAlert_sloc8_1_0+0
;	main.c: 280: while (1)
00114$:
;	main.c: 282: turnLedOn();
	set0.io	__pa, #4
;	main.c: 284: if (activeDelayMilliseconds(LED_PULSE_MS))
	mov	a, #0x14
	mov	_activeDelayMilliseconds_PARM_1+0, a
	clear	_activeDelayMilliseconds_PARM_1+1
	call	_activeDelayMilliseconds
	ceqsn	a, #0x00
	goto	00146$
	goto	00102$
00146$:
;	main.c: 286: turnLedOff();
	set1.io	__pa, #4
;	main.c: 287: return 1;
	ret	#0x01
00102$:
;	main.c: 290: turnLedOff();
	set1.io	__pa, #4
;	main.c: 292: if (++flashCount >= LED_FLASHES_PER_BEEPS)
	inc	_activeAlert_sloc8_1_0+0
	mov	a, _activeAlert_sloc8_1_0+0
	sub	a, #0x04
	t0sn.io	f, c
	goto	00110$
;	main.c: 294: flashCount = 0;
	clear	_activeAlert_sloc8_1_0+0
;	main.c: 296: if (tonePulse())
	call	_tonePulse
	ceqsn	a, #0x00
	goto	00147$
	goto	00104$
00147$:
;	main.c: 297: return 1;
	ret	#0x01
00104$:
;	main.c: 299: if (activeDelayMilliseconds(PIEZO_GAP_MS))
	mov	a, #0x32
	mov	_activeDelayMilliseconds_PARM_1+0, a
	clear	_activeDelayMilliseconds_PARM_1+1
	call	_activeDelayMilliseconds
	ceqsn	a, #0x00
	goto	00148$
	goto	00106$
00148$:
;	main.c: 300: return 1;
	ret	#0x01
00106$:
;	main.c: 302: if (tonePulse())
	call	_tonePulse
	ceqsn	a, #0x00
	goto	00149$
	goto	00110$
00149$:
;	main.c: 303: return 1;
	ret	#0x01
00110$:
;	main.c: 310: if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
	mov	a, #0x20
	mov	_sleepTicks_PARM_1+0, a
	mov	a, #0xcb
	mov	_sleepTicks_PARM_1+1, a
	clear	_sleepTicks_PARM_2+0
	call	_sleepTicks
	ceqsn	a, #0x00
	goto	00150$
	goto	00114$
00150$:
;	main.c: 311: return 1;
;	main.c: 313: }
	ret	#0x01
;	main.c: 315: void main(void)
;	-----------------------------------------
;	 function main
;	-----------------------------------------
_main:
;	main.c: 317: setup();
	call	_setup
;	main.c: 319: while (1)
00104$:
;	main.c: 322: if (startupChirps())
	call	_startupChirps
	ceqsn	a, #0x00
	goto	00116$
	goto	00102$
00116$:
;	main.c: 324: waitForButtonRelease();
	call	_waitForButtonRelease
;	main.c: 325: deepSleep();
	call	_deepSleep
;	main.c: 326: continue;
	goto	00104$
00102$:
;	main.c: 329: activeAlert();
	call	_activeAlert
;	main.c: 330: waitForButtonRelease();
	call	_waitForButtonRelease
;	main.c: 331: deepSleep();
	call	_deepSleep
	goto	00104$
;	main.c: 333: }
	ret
;	main.c: 339: unsigned char STARTUP_FUNCTION(void)
;	-----------------------------------------
;	 function _sdcc_external_startup
;	-----------------------------------------
__sdcc_external_startup:
;	main.c: 341: AUTO_INIT_SYSCLOCK();
	mov	a, #0xf4
	mov.io	__clkmd, a
;	main.c: 342: AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);
	and	a, #'R'                       
	and	a, #'C'                       
	and	a, #(2)            
	and	a, #((52000))     
	and	a, #((52000)>>8)  
	and	a, #((52000)>>16) 
	and	a, #((52000)>>24) 
	and	a, #((2800))     
	and	a, #((2800)>>8)  
	and	a, #(0x1f)             
;	main.c: 344: return 0;
;	main.c: 345: }
	ret	#0x00
	.area CODE
	.area CONST
_chirpPattern:
	ret #0x1a	; 26
	ret #0x28	; 40
	ret #0x00	; 0
	ret #0x00	; 0
	ret #0x0f	; 15
	ret #0x00	; 0
	ret #0x06	; 6
	ret #0x19	; 25
	ret #0x00	; 0
	ret #0x00	; 0
	ret #0x0f	; 15
	ret #0x00	; 0
	ret #0x1a	; 26
	ret #0x14	; 20
	ret #0x00	; 0
	ret #0x00	; 0
	ret #0x0f	; 15
	ret #0x00	; 0
	ret #0x06	; 6
	ret #0x19	; 25
	ret #0x00	; 0
	ret #0x00	; 0
	ret #0x0f	; 15
	ret #0x00	; 0
	ret #0x1a	; 26
	ret #0x28	; 40
	ret #0x00	; 0
	ret #0x00	; 0
	ret #0x19	; 25
	ret #0x00	; 0
	.area CABS (ABS)
