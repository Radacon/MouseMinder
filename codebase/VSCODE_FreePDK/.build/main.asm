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
_sleepTicks_PARM_1:
	.ds 2
_sleepTicks_PARM_2:
	.ds 1
_sleepMilliseconds_PARM_1:
	.ds 2
_sleepMilliseconds_PARM_2:
	.ds 1
_sleepMilliseconds_sloc1_1_0:
	.ds 2
_sleepMilliseconds_sloc2_1_0:
	.ds 2
_sleepMilliseconds_sloc3_1_0:
	.ds 2
_sleepMilliseconds_sloc4_1_0:
	.ds 2
_startTone_PARM_1:
	.ds 1
_startupChirps_sloc5_1_0:
	.ds 2
_startupChirps_sloc6_1_0:
	.ds 1
_startupChirps_sloc7_1_0:
	.ds 1
_startupChirps_sloc8_1_0:
	.ds 1
_startupChirps_sloc9_1_0:
	.ds 2
_startupChirps_sloc10_1_0:
	.ds 2
_startupChirps_sloc11_1_0:
	.ds 2
_activeAlert_sloc12_1_0:
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
;	main.c: 76: static void piezoInput(void)
;	-----------------------------------------
;	 function piezoInput
;	-----------------------------------------
_piezoInput:
;	main.c: 78: TM2C = TM2C_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__tm2c, a
;	main.c: 79: INTRQ &= (uint8_t)~INTRQ_TM2;
	set0.io	__intrq, #6
;	main.c: 80: PA &= (uint8_t)~PIEZO_MASK;
	set0.io	__pa, #3
;	main.c: 81: PAC &= (uint8_t)~PIEZO_MASK;
	set0.io	__pac, #3
;	main.c: 82: }
	ret
;	main.c: 84: static uint8_t activeLedPulseDelay(void)
;	-----------------------------------------
;	 function activeLedPulseDelay
;	-----------------------------------------
_activeLedPulseDelay:
;	main.c: 86: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 93: _delay_ms(LED_PULSE_MS);
	mov	a, #0x3f
	mov	__delay_loop_16_PARM_1+0, a
	clear	__delay_loop_16_PARM_1+1
	call	__delay_loop_16
;	main.c: 95: return buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 96: }
	ret
;	main.c: 98: static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
;	-----------------------------------------
;	 function sleepTicks
;	-----------------------------------------
_sleepTicks:
;	main.c: 102: T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
	mov	a, #0xc7
	mov.io	__t16m, a
;	main.c: 103: timer16Load = (uint16_t)(32768u - ticks);
	mov	a, #0x00
	sub	a, _sleepTicks_PARM_1+0
	mov	_timer16Load+0, a
	mov	a, #0x80
	subc	a, _sleepTicks_PARM_1+1
	mov	_timer16Load+1, a
;	main.c: 106: __endasm;
	stt16	_timer16Load
;	main.c: 107: INTEGS &= (uint8_t)~INTEGS_T16_FALLING;
	set0.io	__integs, #4
;	main.c: 108: INTRQ &= (uint8_t)~INTRQ_T16;
	set0.io	__intrq, #2
;	main.c: 115: (piezoWake ? PIEZO_MASK : (uint8_t)0u));
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
;	main.c: 119: __endasm;
	stopexe
;	main.c: 122: buttonPressed = buttonIsPressed();
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
;	main.c: 123: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 124: INTRQ &= (uint8_t)~INTRQ_T16;
	set0.io	__intrq, #2
;	main.c: 126: return buttonPressed;
	mov	a, _sleepTicks_sloc0_1_0+0
;	main.c: 127: }
	ret
;	main.c: 129: static uint8_t sleepMilliseconds(uint16_t milliseconds, uint8_t piezoWake)
;	-----------------------------------------
;	 function sleepMilliseconds
;	-----------------------------------------
_sleepMilliseconds:
;	main.c: 133: while (milliseconds > 500u)
00103$:
	mov	a, _sleepMilliseconds_PARM_1+0
	mov	_sleepMilliseconds_sloc1_1_0+0, a
	mov	a, _sleepMilliseconds_PARM_1+1
	mov	_sleepMilliseconds_sloc1_1_0+1, a
	mov	a, #0xf4
	sub	a, _sleepMilliseconds_sloc1_1_0+0
	mov	a, #0x01
	subc	a, _sleepMilliseconds_sloc1_1_0+1
	t1sn.io	f, c
	goto	00105$
;	main.c: 135: if (sleepTicks((uint16_t)(F_CPU / 2u), piezoWake))
	mov	a, #0x90
	mov	_sleepTicks_PARM_1+0, a
	mov	a, #0x65
	mov	_sleepTicks_PARM_1+1, a
	mov	a, _sleepMilliseconds_PARM_2+0
	mov	_sleepTicks_PARM_2+0, a
	call	_sleepTicks
	ceqsn	a, #0x00
	goto	00126$
	goto	00102$
00126$:
;	main.c: 136: return 1;
	ret	#0x01
00102$:
;	main.c: 138: milliseconds -= 500u;
	mov	a, _sleepMilliseconds_sloc1_1_0+0
	sub	a, #0xf4
	mov	p, a
	mov	a, _sleepMilliseconds_sloc1_1_0+1
	subc	a
	sub	a, #0x01
	mov	_sleepMilliseconds_PARM_1+1, a
	mov	a, p
	mov	_sleepMilliseconds_PARM_1+0, a
	goto	00103$
00105$:
;	main.c: 141: if (!milliseconds)
	mov	a, _sleepMilliseconds_PARM_1+0
	or	a, _sleepMilliseconds_PARM_1+1
	ceqsn	a, #0x00
	goto	00107$
;	main.c: 142: return 0;
	ret	#0x00
00107$:
;	main.c: 145: ticks = (uint16_t)((milliseconds << 5) +
	mov	a, _sleepMilliseconds_PARM_1+0
	mov	_sleepMilliseconds_sloc2_1_0+0, a
	mov	a, _sleepMilliseconds_PARM_1+1
	mov	_sleepMilliseconds_sloc2_1_0+1, a
	mov	a, #5
00127$:
	sl	_sleepMilliseconds_sloc2_1_0+0
	slc	_sleepMilliseconds_sloc2_1_0+1
	dzsn	a
	goto	00127$
;	main.c: 146: (milliseconds << 4) +
	mov	a, _sleepMilliseconds_PARM_1+0
	mov	_sleepMilliseconds_sloc3_1_0+0, a
	mov	a, _sleepMilliseconds_PARM_1+1
	mov	_sleepMilliseconds_sloc3_1_0+1, a
	mov	a, #4
00128$:
	sl	_sleepMilliseconds_sloc3_1_0+0
	slc	_sleepMilliseconds_sloc3_1_0+1
	dzsn	a
	goto	00128$
	mov	a, _sleepMilliseconds_sloc2_1_0+0
	add	a, _sleepMilliseconds_sloc3_1_0+0
	mov	_sleepMilliseconds_sloc4_1_0+0, a
	mov	a, _sleepMilliseconds_sloc2_1_0+1
	addc	a, _sleepMilliseconds_sloc3_1_0+1
	mov	_sleepMilliseconds_sloc4_1_0+1, a
;	main.c: 147: (milliseconds << 2));
	mov	a, _sleepMilliseconds_PARM_1+1
	mov	p, a
	mov	a, _sleepMilliseconds_PARM_1+0
	sl	a
	slc	p
	sl	a
	slc	p
	add	a, _sleepMilliseconds_sloc4_1_0+0
	mov	_sleepTicks_PARM_1+0, a
	mov	a, _sleepMilliseconds_sloc4_1_0+1
	addc	a, p
	mov	_sleepTicks_PARM_1+1, a
;	main.c: 149: return sleepTicks(ticks, piezoWake);
	mov	a, _sleepMilliseconds_PARM_2+0
	mov	_sleepTicks_PARM_2+0, a
	goto	_sleepTicks
;	main.c: 150: }
	ret
;	main.c: 156: static void startTone(uint8_t timerDivisor)
;	-----------------------------------------
;	 function startTone
;	-----------------------------------------
_startTone:
;	main.c: 159: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 160: PAC |= PIEZO_MASK;
	set1.io	__pac, #3
;	main.c: 161: TM2CT = 0;
	mov	a, #0x00
	mov.io	__tm2ct, a
;	main.c: 162: TM2B = (uint8_t)(timerDivisor - 1u);
	mov	a, _startTone_PARM_1+0
	sub	a, #0x01
	mov.io	__tm2b, a
;	main.c: 163: TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
	mov	a, #0x00
	mov.io	__tm2s, a
;	main.c: 164: TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
	mov	a, #0x48
	mov.io	__tm2c, a
;	main.c: 165: }
	ret
;	main.c: 167: static uint8_t startupChirps(void)
;	-----------------------------------------
;	 function startupChirps
;	-----------------------------------------
_startupChirps:
;	main.c: 169: uint16_t offset = 0;
	clear	_startupChirps_sloc5_1_0+0
	clear	_startupChirps_sloc5_1_0+1
;	main.c: 172: while (step--)
	mov	a, #0x0a
	mov	_startupChirps_sloc6_1_0+0, a
00109$:
	mov	a, _startupChirps_sloc6_1_0+0
	dec	_startupChirps_sloc6_1_0+0
	ceqsn	a, #0x00
	goto	00138$
	goto	00111$
00138$:
;	main.c: 174: uint8_t timerDivisor = chirpPattern[offset];
	mov	a, #<(_chirpPattern + 0)
	add	a, _startupChirps_sloc5_1_0+0
	mov	p, a
	mov	a, #>(_chirpPattern + 0x8000 + 0)
	addc	a, _startupChirps_sloc5_1_0+1
	call	__gptrget
	mov	_startupChirps_sloc7_1_0+0, a
;	main.c: 175: uint16_t duration = (uint16_t)chirpPattern[offset + 1u] |
	mov	a, _startupChirps_sloc5_1_0+0
	mov	_startupChirps_sloc8_1_0+0, a
	add	a, #0x01
	add	a, #<(_chirpPattern + 0)
	mov	p, a
	mov	a, #0x00
	addc	a
	add	a, #>(_chirpPattern + 0x8000 + 0)
	call	__gptrget
	mov	_startupChirps_sloc9_1_0+0, a
	clear	_startupChirps_sloc9_1_0+1
	mov	a, _startupChirps_sloc8_1_0+0
	add	a, #0x02
	add	a, #<(_chirpPattern + 0)
	mov	p, a
	mov	a, #0x00
	addc	a
	add	a, #>(_chirpPattern + 0x8000 + 0)
	call	__gptrget
	mov	p, a
	mov	a, #0x00
	or	a, _startupChirps_sloc9_1_0+0
	mov	_startupChirps_sloc10_1_0+0, a
	mov	a, p
	or	a, _startupChirps_sloc9_1_0+1
	mov	_startupChirps_sloc10_1_0+1, a
;	main.c: 177: offset += CHIRP_STEP_BYTES;
	mov	a, _startupChirps_sloc5_1_0+0
	add	a, #0x03
	mov	p, a
	mov	a, _startupChirps_sloc5_1_0+1
	addc	a
	mov	_startupChirps_sloc5_1_0+1, a
	mov	a, p
	mov	_startupChirps_sloc5_1_0+0, a
;	main.c: 179: if (timerDivisor)
	mov	a, _startupChirps_sloc7_1_0+0
	ceqsn	a, #0x00
	goto	00139$
	goto	00102$
00139$:
;	main.c: 180: startTone(timerDivisor);
	mov	a, _startupChirps_sloc7_1_0+0
	mov	_startTone_PARM_1+0, a
	call	_startTone
	goto	00103$
00102$:
;	main.c: 182: piezoInput();
	call	_piezoInput
00103$:
;	main.c: 184: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 185: while (duration--)
	mov	a, _startupChirps_sloc10_1_0+0
	mov	_startupChirps_sloc11_1_0+0, a
	mov	a, _startupChirps_sloc10_1_0+1
	mov	_startupChirps_sloc11_1_0+1, a
00106$:
	mov	a, _startupChirps_sloc11_1_0+1
	mov	p, a
	mov	a, _startupChirps_sloc11_1_0+0
	dec	_startupChirps_sloc11_1_0+0
	subc	_startupChirps_sloc11_1_0+1
	or	a, p
	ceqsn	a, #0x00
	goto	00140$
	goto	00109$
00140$:
;	main.c: 187: _delay_ms(1);
	mov	a, #0x05
	mov	__delay_loop_16_PARM_1+0, a
	clear	__delay_loop_16_PARM_1+1
	call	__delay_loop_16
;	main.c: 188: if (buttonIsPressed())
	mov.io	a, __pa
	mov	p, a
	t1sn	p, #6
	goto	00106$
;	main.c: 190: piezoInput();
	call	_piezoInput
;	main.c: 191: return 1;
	ret	#0x01
00111$:
;	main.c: 196: piezoInput();
	call	_piezoInput
;	main.c: 197: return 0;
;	main.c: 198: }
	ret	#0x00
;	main.c: 204: static void waitForButtonRelease(void)
;	-----------------------------------------
;	 function waitForButtonRelease
;	-----------------------------------------
_waitForButtonRelease:
;	main.c: 206: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 208: while (buttonIsPressed())
00101$:
	mov.io	a, __pa
	mov	p, a
	t1sn	p, #6
	goto	00103$
;	main.c: 210: T16M = T16M_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 214: __endasm;
	stopexe
	goto	00101$
00103$:
;	main.c: 217: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 218: }
	ret
;	main.c: 220: static void deepSleep(void)
;	-----------------------------------------
;	 function deepSleep
;	-----------------------------------------
_deepSleep:
;	main.c: 224: turnLedOff();
	set0.io	__pa, #4
;	main.c: 225: piezoInput();
	call	_piezoInput
;	main.c: 226: T16M = T16M_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 233: PADIER = BUTTON_MASK | PIEZO_MASK;
	mov	a, #0x48
	mov.io	__padier, a
;	main.c: 237: __endasm;
	stopsys
;	main.c: 240: buttonPressed = buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 241: PADIER = 0;
	push	af
	mov	a, #0x00
	mov.io	__padier, a
	pop	af
;	main.c: 244: if (buttonPressed)
	ceqsn	a, #0x00
	goto	00109$
	goto	00103$
00109$:
;	main.c: 245: waitForButtonRelease();
	goto	_waitForButtonRelease
00103$:
;	main.c: 246: }
	ret
;	main.c: 252: static void setup(void)
;	-----------------------------------------
;	 function setup
;	-----------------------------------------
_setup:
;	main.c: 255: PA = 0;
	mov	a, #0x00
	mov.io	__pa, a
;	main.c: 256: PAC = LED_MASK;
	mov	a, #0x10
	mov.io	__pac, a
;	main.c: 257: PAPH = 0;
	mov	a, #0x00
	mov.io	__paph, a
;	main.c: 258: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 260: GPCC = 0;
	mov	a, #0x00
	mov.io	__gpcc, a
;	main.c: 261: GPCS = 0;
	mov	a, #0x00
	mov.io	__gpcs, a
;	main.c: 262: TM2C = 0;
	mov	a, #0x00
	mov.io	__tm2c, a
;	main.c: 263: T16M = 0;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 265: MISC |= MISC_LVR_DISABLE;
	set1.io	__misc, #2
;	main.c: 273: CLKMD_ENABLE_IHRC);
	mov.io	a, __clkmd
	and	a, #0xec
	mov.io	__clkmd, a
;	main.c: 275: INTEN = 0;
	mov	a, #0x00
	mov.io	__inten, a
;	main.c: 276: INTRQ = 0;
	mov	a, #0x00
	mov.io	__intrq, a
;	main.c: 277: }
	ret
;	main.c: 279: static uint8_t activeAlert(void)
;	-----------------------------------------
;	 function activeAlert
;	-----------------------------------------
_activeAlert:
;	main.c: 281: uint8_t flashCount = 0;
	clear	_activeAlert_sloc12_1_0+0
;	main.c: 283: while (1)
00110$:
;	main.c: 285: turnLedOn();
	set1.io	__pa, #4
;	main.c: 287: if (activeLedPulseDelay())
	call	_activeLedPulseDelay
	ceqsn	a, #0x00
	goto	00134$
	goto	00102$
00134$:
;	main.c: 289: turnLedOff();
	set0.io	__pa, #4
;	main.c: 290: return 1;
	ret	#0x01
00102$:
;	main.c: 293: turnLedOff();
	set0.io	__pa, #4
;	main.c: 295: if (++flashCount >= LED_FLASHES_PER_CHIRP)
	inc	_activeAlert_sloc12_1_0+0
	mov	a, _activeAlert_sloc12_1_0+0
	sub	a, #0x05
	t0sn.io	f, c
	goto	00106$
;	main.c: 297: flashCount = 0;
	clear	_activeAlert_sloc12_1_0+0
;	main.c: 299: if (startupChirps())
	call	_startupChirps
	ceqsn	a, #0x00
	goto	00135$
	goto	00106$
00135$:
;	main.c: 300: return 1;
	ret	#0x01
00106$:
;	main.c: 307: if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
	mov	a, #0xe8
	mov	_sleepMilliseconds_PARM_1+0, a
	mov	a, #0x03
	mov	_sleepMilliseconds_PARM_1+1, a
	clear	_sleepMilliseconds_PARM_2+0
	call	_sleepMilliseconds
	ceqsn	a, #0x00
	goto	00136$
	goto	00110$
00136$:
;	main.c: 308: return 1;
;	main.c: 310: }
	ret	#0x01
;	main.c: 312: void main(void)
;	-----------------------------------------
;	 function main
;	-----------------------------------------
_main:
;	main.c: 314: setup();
	call	_setup
;	main.c: 316: while (1)
00104$:
;	main.c: 319: if (startupChirps())
	call	_startupChirps
	ceqsn	a, #0x00
	goto	00116$
	goto	00102$
00116$:
;	main.c: 321: waitForButtonRelease();
	call	_waitForButtonRelease
;	main.c: 322: deepSleep();
	call	_deepSleep
;	main.c: 323: continue;
	goto	00104$
00102$:
;	main.c: 326: activeAlert();
	call	_activeAlert
;	main.c: 327: waitForButtonRelease();
	call	_waitForButtonRelease
;	main.c: 328: deepSleep();
	call	_deepSleep
	goto	00104$
;	main.c: 330: }
	ret
;	main.c: 336: unsigned char STARTUP_FUNCTION(void)
;	-----------------------------------------
;	 function _sdcc_external_startup
;	-----------------------------------------
__sdcc_external_startup:
;	main.c: 338: AUTO_INIT_SYSCLOCK();
	mov	a, #0xf4
	mov.io	__clkmd, a
;	main.c: 339: AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);
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
;	main.c: 341: return 0;
;	main.c: 342: }
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
