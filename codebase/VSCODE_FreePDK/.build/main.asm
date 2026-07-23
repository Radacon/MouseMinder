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
_startupChirps_sloc1_1_0:
	.ds 1
_activeAlert_sloc2_1_0:
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
;	main.c: 75: static void piezoInput(void)
;	-----------------------------------------
;	 function piezoInput
;	-----------------------------------------
_piezoInput:
;	main.c: 77: TM2C = TM2C_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__tm2c, a
;	main.c: 78: INTRQ &= (uint8_t)~INTRQ_TM2;
	set0.io	__intrq, #6
;	main.c: 79: PA &= (uint8_t)~PIEZO_MASK;
	set0.io	__pa, #3
;	main.c: 80: PAC &= (uint8_t)~PIEZO_MASK;
	set0.io	__pac, #3
;	main.c: 81: }
	ret
;	main.c: 83: static uint8_t activeDelayMilliseconds(uint16_t milliseconds)
;	-----------------------------------------
;	 function activeDelayMilliseconds
;	-----------------------------------------
_activeDelayMilliseconds:
;	main.c: 85: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 92: if (milliseconds == PIEZO_GAP_MS)
	mov	a, _activeDelayMilliseconds_PARM_1+1
	mov	p, a
	mov	a, _activeDelayMilliseconds_PARM_1+0
	ceqsn	a, #0x32
	goto	00102$
	mov	a, p
	ceqsn	a, #0x00
	goto	00102$
;	main.c: 93: _delay_ms(PIEZO_GAP_MS);
	mov	a, #0x43
	mov	__delay_loop_16_PARM_1+0, a
	mov	a, #0x01
	mov	__delay_loop_16_PARM_1+1, a
	call	__delay_loop_16
	goto	00103$
00102$:
;	main.c: 95: _delay_ms(LED_PULSE_MS);
	mov	a, #0x80
	mov	__delay_loop_16_PARM_1+0, a
	clear	__delay_loop_16_PARM_1+1
	call	__delay_loop_16
00103$:
;	main.c: 97: return buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 98: }
	ret
;	main.c: 100: static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
;	-----------------------------------------
;	 function sleepTicks
;	-----------------------------------------
_sleepTicks:
;	main.c: 104: T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
	mov	a, #0xc7
	mov.io	__t16m, a
;	main.c: 105: timer16Load = (uint16_t)(65535u - ticks + 1u);
	mov	a, #0x00
	sub	a, _sleepTicks_PARM_1+0
	mov	_timer16Load+0, a
	mov	a, #0x00
	subc	a, _sleepTicks_PARM_1+1
	mov	_timer16Load+1, a
;	main.c: 108: __endasm;
	stt16	_timer16Load
;	main.c: 109: INTEGS |= INTEGS_T16_FALLING;
	set1.io	__integs, #4
;	main.c: 110: INTRQ &= (uint8_t)~INTRQ_T16;
	set0.io	__intrq, #2
;	main.c: 117: (piezoWake ? PIEZO_MASK : (uint8_t)0u));
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
;	main.c: 121: __endasm;
	stopexe
;	main.c: 124: buttonPressed = buttonIsPressed();
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
;	main.c: 125: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 126: INTRQ &= (uint8_t)~INTRQ_T16;
	set0.io	__intrq, #2
;	main.c: 128: return buttonPressed;
	mov	a, _sleepTicks_sloc0_1_0+0
;	main.c: 129: }
	ret
;	main.c: 135: static void startTone(void)
;	-----------------------------------------
;	 function startTone
;	-----------------------------------------
_startTone:
;	main.c: 138: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 139: PAC |= PIEZO_MASK;
	set1.io	__pac, #3
;	main.c: 140: TM2CT = 0;
	mov	a, #0x00
	mov.io	__tm2ct, a
;	main.c: 141: TM2B = PIEZO_TONE_BOUND;
	mov	a, #0x05
	mov.io	__tm2b, a
;	main.c: 142: TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
	mov	a, #0x00
	mov.io	__tm2s, a
;	main.c: 143: TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
	mov	a, #0x48
	mov.io	__tm2c, a
;	main.c: 144: }
	ret
;	main.c: 146: static uint8_t tonePulse(void)
;	-----------------------------------------
;	 function tonePulse
;	-----------------------------------------
_tonePulse:
;	main.c: 148: startTone();
	call	_startTone
;	main.c: 149: _delay_ms(PIEZO_TONE_MS);
	mov	a, #0x43
	mov	__delay_loop_16_PARM_1+0, a
	mov	a, #0x01
	mov	__delay_loop_16_PARM_1+1, a
	call	__delay_loop_16
;	main.c: 150: piezoInput();
	call	_piezoInput
;	main.c: 152: return buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 153: }
	ret
;	main.c: 155: static uint8_t startupChirps(void)
;	-----------------------------------------
;	 function startupChirps
;	-----------------------------------------
_startupChirps:
;	main.c: 159: while (count--)
	mov	a, #0x03
	mov	_startupChirps_sloc1_1_0+0, a
00106$:
	mov	a, _startupChirps_sloc1_1_0+0
	dec	_startupChirps_sloc1_1_0+0
	ceqsn	a, #0x00
	goto	00131$
	goto	00108$
00131$:
;	main.c: 161: if (tonePulse())
	call	_tonePulse
	ceqsn	a, #0x00
	goto	00132$
	goto	00102$
00132$:
;	main.c: 162: return 1;
	ret	#0x01
00102$:
;	main.c: 165: if (count && activeDelayMilliseconds(PIEZO_GAP_MS))
	mov	a, _startupChirps_sloc1_1_0+0
	ceqsn	a, #0x00
	goto	00133$
	goto	00106$
00133$:
	mov	a, #0x32
	mov	_activeDelayMilliseconds_PARM_1+0, a
	clear	_activeDelayMilliseconds_PARM_1+1
	call	_activeDelayMilliseconds
	ceqsn	a, #0x00
	goto	00134$
	goto	00106$
00134$:
;	main.c: 166: return 1;
	ret	#0x01
00108$:
;	main.c: 169: return 0;
;	main.c: 170: }
	ret	#0x00
;	main.c: 176: static void waitForButtonRelease(void)
;	-----------------------------------------
;	 function waitForButtonRelease
;	-----------------------------------------
_waitForButtonRelease:
;	main.c: 178: PADIER = BUTTON_MASK;
	mov	a, #0x40
	mov.io	__padier, a
;	main.c: 180: while (buttonIsPressed())
00101$:
	mov.io	a, __pa
	mov	p, a
	t1sn	p, #6
	goto	00103$
;	main.c: 182: T16M = T16M_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 186: __endasm;
	stopexe
	goto	00101$
00103$:
;	main.c: 189: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 190: }
	ret
;	main.c: 192: static void deepSleep(void)
;	-----------------------------------------
;	 function deepSleep
;	-----------------------------------------
_deepSleep:
;	main.c: 196: turnLedOff();
	set1.io	__pa, #4
;	main.c: 197: piezoInput();
	call	_piezoInput
;	main.c: 198: T16M = T16M_CLK_DISABLE;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 205: PADIER = BUTTON_MASK | PIEZO_MASK;
	mov	a, #0x48
	mov.io	__padier, a
;	main.c: 209: __endasm;
	stopsys
;	main.c: 212: buttonPressed = buttonIsPressed();
	mov.io	a, __pa
	clear	p
	and	a, #0x40
	clear	p
	or	a, p
	sub	a, #0x01
	mov	a, #0x00
	slc	a
	xor	a, #0x01
;	main.c: 213: PADIER = 0;
	push	af
	mov	a, #0x00
	mov.io	__padier, a
	pop	af
;	main.c: 216: if (buttonPressed)
	ceqsn	a, #0x00
	goto	00109$
	goto	00103$
00109$:
;	main.c: 217: waitForButtonRelease();
	goto	_waitForButtonRelease
00103$:
;	main.c: 218: }
	ret
;	main.c: 224: static void setup(void)
;	-----------------------------------------
;	 function setup
;	-----------------------------------------
_setup:
;	main.c: 227: PA = LED_MASK;
	mov	a, #0x10
	mov.io	__pa, a
;	main.c: 228: PAC = LED_MASK;
	mov	a, #0x10
	mov.io	__pac, a
;	main.c: 229: PAPH = 0;
	mov	a, #0x00
	mov.io	__paph, a
;	main.c: 230: PADIER = 0;
	mov	a, #0x00
	mov.io	__padier, a
;	main.c: 232: GPCC = 0;
	mov	a, #0x00
	mov.io	__gpcc, a
;	main.c: 233: GPCS = 0;
	mov	a, #0x00
	mov.io	__gpcs, a
;	main.c: 234: TM2C = 0;
	mov	a, #0x00
	mov.io	__tm2c, a
;	main.c: 235: T16M = 0;
	mov	a, #0x00
	mov.io	__t16m, a
;	main.c: 237: MISC |= MISC_LVR_DISABLE;
	set1.io	__misc, #2
;	main.c: 245: CLKMD_ENABLE_IHRC);
	mov.io	a, __clkmd
	and	a, #0xec
	mov.io	__clkmd, a
;	main.c: 247: INTEN = 0;
	mov	a, #0x00
	mov.io	__inten, a
;	main.c: 248: INTRQ = 0;
	mov	a, #0x00
	mov.io	__intrq, a
;	main.c: 249: }
	ret
;	main.c: 251: static uint8_t activeAlert(void)
;	-----------------------------------------
;	 function activeAlert
;	-----------------------------------------
_activeAlert:
;	main.c: 253: uint8_t flashCount = 0;
	clear	_activeAlert_sloc2_1_0+0
;	main.c: 255: while (1)
00114$:
;	main.c: 257: turnLedOn();
	set0.io	__pa, #4
;	main.c: 259: if (activeDelayMilliseconds(LED_PULSE_MS))
	mov	a, #0x14
	mov	_activeDelayMilliseconds_PARM_1+0, a
	clear	_activeDelayMilliseconds_PARM_1+1
	call	_activeDelayMilliseconds
	ceqsn	a, #0x00
	goto	00146$
	goto	00102$
00146$:
;	main.c: 261: turnLedOff();
	set1.io	__pa, #4
;	main.c: 262: return 1;
	ret	#0x01
00102$:
;	main.c: 265: turnLedOff();
	set1.io	__pa, #4
;	main.c: 267: if (++flashCount >= LED_FLASHES_PER_BEEPS)
	inc	_activeAlert_sloc2_1_0+0
	mov	a, _activeAlert_sloc2_1_0+0
	sub	a, #0x04
	t0sn.io	f, c
	goto	00110$
;	main.c: 269: flashCount = 0;
	clear	_activeAlert_sloc2_1_0+0
;	main.c: 271: if (tonePulse())
	call	_tonePulse
	ceqsn	a, #0x00
	goto	00147$
	goto	00104$
00147$:
;	main.c: 272: return 1;
	ret	#0x01
00104$:
;	main.c: 274: if (activeDelayMilliseconds(PIEZO_GAP_MS))
	mov	a, #0x32
	mov	_activeDelayMilliseconds_PARM_1+0, a
	clear	_activeDelayMilliseconds_PARM_1+1
	call	_activeDelayMilliseconds
	ceqsn	a, #0x00
	goto	00148$
	goto	00106$
00148$:
;	main.c: 275: return 1;
	ret	#0x01
00106$:
;	main.c: 277: if (tonePulse())
	call	_tonePulse
	ceqsn	a, #0x00
	goto	00149$
	goto	00110$
00149$:
;	main.c: 278: return 1;
	ret	#0x01
00110$:
;	main.c: 285: if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
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
;	main.c: 286: return 1;
;	main.c: 288: }
	ret	#0x01
;	main.c: 290: void main(void)
;	-----------------------------------------
;	 function main
;	-----------------------------------------
_main:
;	main.c: 292: setup();
	call	_setup
;	main.c: 294: while (1)
00104$:
;	main.c: 297: if (startupChirps())
	call	_startupChirps
	ceqsn	a, #0x00
	goto	00116$
	goto	00102$
00116$:
;	main.c: 299: waitForButtonRelease();
	call	_waitForButtonRelease
;	main.c: 300: deepSleep();
	call	_deepSleep
;	main.c: 301: continue;
	goto	00104$
00102$:
;	main.c: 304: activeAlert();
	call	_activeAlert
;	main.c: 305: waitForButtonRelease();
	call	_waitForButtonRelease
;	main.c: 306: deepSleep();
	call	_deepSleep
	goto	00104$
;	main.c: 308: }
	ret
;	main.c: 314: unsigned char STARTUP_FUNCTION(void)
;	-----------------------------------------
;	 function _sdcc_external_startup
;	-----------------------------------------
__sdcc_external_startup:
;	main.c: 316: AUTO_INIT_SYSCLOCK();
	mov	a, #0xf4
	mov.io	__clkmd, a
;	main.c: 317: AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);
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
;	main.c: 319: return 0;
;	main.c: 320: }
	ret	#0x00
	.area CODE
	.area CONST
	.area CABS (ABS)
