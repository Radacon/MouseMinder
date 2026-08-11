                                      1 ;--------------------------------------------------------
                                      2 ; File Created by SDCC : free open source ANSI-C Compiler
                                      3 ; Version 4.2.0 #13081 (Linux)
                                      4 ;--------------------------------------------------------
                                      5 	.module main
                                      6 	.optsdcc -mpdk13
                                      7 	
                                      8 
                                      9 ; default segment ordering in RAM for linker
                                     10 	.area DATA
                                     11 	.area OSEG (OVR,DATA)
                                     12 
                                     13 ;--------------------------------------------------------
                                     14 ; Public variables in this module
                                     15 ;--------------------------------------------------------
                                     16 	.globl __sdcc_external_startup
                                     17 	.globl _main
                                     18 	.globl __delay_loop_32
                                     19 	.globl __delay_loop_16
                                     20 	.globl __delay_loop_8
                                     21 	.globl __misc
                                     22 	.globl __gpcs
                                     23 	.globl __gpcc
                                     24 	.globl __bgtr
                                     25 	.globl __tm2b
                                     26 	.globl __tm2s
                                     27 	.globl __tm2ct
                                     28 	.globl __tm2c
                                     29 	.globl __t16c
                                     30 	.globl __t16m
                                     31 	.globl __paph
                                     32 	.globl __pac
                                     33 	.globl __pa
                                     34 	.globl __padier
                                     35 	.globl __integs
                                     36 	.globl __intrq
                                     37 	.globl __inten
                                     38 	.globl __eoscr
                                     39 	.globl __ilrcr
                                     40 	.globl __ihrcr
                                     41 	.globl __clkmd
                                     42 	.globl __sp
                                     43 	.globl __flag
                                     44 	.globl __delay_loop_32_PARM_1
                                     45 	.globl __delay_loop_16_PARM_1
                                     46 	.globl __delay_loop_8_PARM_1
                                     47 ;--------------------------------------------------------
                                     48 ; special function registers
                                     49 ;--------------------------------------------------------
                                     50 	.area RSEG (ABS)
      000000                         51 	.org 0x0000
                           000000    52 __flag	=	0x0000
                           000002    53 __sp	=	0x0002
                           000003    54 __clkmd	=	0x0003
                           00000B    55 __ihrcr	=	0x000b
                           00001F    56 __ilrcr	=	0x001f
                           00000A    57 __eoscr	=	0x000a
                           000004    58 __inten	=	0x0004
                           000005    59 __intrq	=	0x0005
                           00000C    60 __integs	=	0x000c
                           00000D    61 __padier	=	0x000d
                           000010    62 __pa	=	0x0010
                           000011    63 __pac	=	0x0011
                           000012    64 __paph	=	0x0012
                           000006    65 __t16m	=	0x0006
      000000                         66 __t16c::
      000000                         67 	.ds 2
                           00001C    68 __tm2c	=	0x001c
                           00001D    69 __tm2ct	=	0x001d
                           000017    70 __tm2s	=	0x0017
                           000009    71 __tm2b	=	0x0009
                           000019    72 __bgtr	=	0x0019
                           00001A    73 __gpcc	=	0x001a
                           00001E    74 __gpcs	=	0x001e
                           00001B    75 __misc	=	0x001b
                                     76 ;--------------------------------------------------------
                                     77 ; ram data
                                     78 ;--------------------------------------------------------
                                     79 	.area DATA
      000002                         80 __delay_loop_8_PARM_1:
      000002                         81 	.ds 1
      000003                         82 __delay_loop_16_PARM_1:
      000003                         83 	.ds 2
      000005                         84 __delay_loop_32_PARM_1:
      000005                         85 	.ds 4
      000009                         86 _timer16Load:
      000009                         87 	.ds 2
      00000B                         88 _activeDelayMilliseconds_PARM_1:
      00000B                         89 	.ds 2
      00000D                         90 _sleepTicks_PARM_1:
      00000D                         91 	.ds 2
      00000F                         92 _sleepTicks_PARM_2:
      00000F                         93 	.ds 1
      000010                         94 _startTone_PARM_1:
      000010                         95 	.ds 1
      000011                         96 _startupChirps_sloc1_1_0:
      000011                         97 	.ds 2
      000013                         98 _startupChirps_sloc2_1_0:
      000013                         99 	.ds 1
      000014                        100 _startupChirps_sloc3_1_0:
      000014                        101 	.ds 1
      000015                        102 _startupChirps_sloc4_1_0:
      000015                        103 	.ds 1
      000016                        104 _startupChirps_sloc5_1_0:
      000016                        105 	.ds 2
      000018                        106 _startupChirps_sloc6_1_0:
      000018                        107 	.ds 2
      00001A                        108 _startupChirps_sloc7_1_0:
      00001A                        109 	.ds 2
      00001C                        110 _activeAlert_sloc8_1_0:
      00001C                        111 	.ds 1
                                    112 ;--------------------------------------------------------
                                    113 ; overlayable items in ram
                                    114 ;--------------------------------------------------------
                                    115 	.area	OSEG (OVR,DATA)
      00001D                        116 _sleepTicks_sloc0_1_0:
      00001D                        117 	.ds 1
                                    118 ;--------------------------------------------------------
                                    119 ; Stack segment in internal ram
                                    120 ;--------------------------------------------------------
                                    121 	.area	SSEG
      00001E                        122 __start__stack:
      00001E                        123 	.ds	1
                                    124 
                                    125 ;--------------------------------------------------------
                                    126 ; absolute external ram data
                                    127 ;--------------------------------------------------------
                                    128 	.area DABS (ABS)
                                    129 ;--------------------------------------------------------
                                    130 ; interrupt vector
                                    131 ;--------------------------------------------------------
                                    132 	.area HOME
      000022                        133 __interrupt_vect:
                                    134 	.area	HEADER (ABS)
      000020                        135 	.org	 0x0020
      000020 3B 00                  136 	reti
                                    137 ;--------------------------------------------------------
                                    138 ; global & static initialisations
                                    139 ;--------------------------------------------------------
                                    140 	.area HOME
                                    141 	.area GSINIT
                                    142 	.area GSFINAL
                                    143 	.area GSINIT
                                    144 	.area	PREG (ABS)
      000000                        145 	.org 0x00
      000000                        146 p::
      000000                        147 	.ds 2
                                    148 	.area	HEADER (ABS)
      000000                        149 	.org 0x0000
      000000 00 00                  150 	nop
      000002 81 09                  151 	clear	p+1
      000004 1D 17                  152 	mov	a, #s_OSEG
      000006 02 10                  153 	add	a, #l_OSEG + 1
      000008 FE 14                  154 	and	a, #0xfe
      00000A 82 00                  155 	mov.io	sp, a
      00000C 6C 1D                  156 	call	__sdcc_external_startup
      00000E 12 18                  157 	goto	s_GSINIT
                                    158 	.area GSINIT
      000024                        159 __sdcc_init_data:
      000024 02 17                  160 	mov	a, #s_DATA
      000026 C0 05                  161 	mov	p, a
      000028 19 18                  162 	goto	00002$
      00002A                        163 00001$:
      00002A 00 17                  164 	mov	a, #0x00
      00002C E0 00                  165 	idxm	p, a
      00002E 00 09                  166 	inc	p
      000030 02 17                  167 	mov	a, #s_DATA
      000032                        168 00002$:
      000032 1B 10                  169 	add	a, #l_DATA
      000034 80 0B                  170 	ceqsn	a, p
      000036 15 18                  171 	goto	00001$
                                    172 	.area GSFINAL
      000038 11 18                  173 	goto	__sdcc_program_startup
                                    174 ;--------------------------------------------------------
                                    175 ; Home
                                    176 ;--------------------------------------------------------
                                    177 	.area HOME
                                    178 	.area HOME
      000022                        179 __sdcc_program_startup:
      000022 5F 19                  180 	goto	_main
                                    181 ;	return from main will return to caller
                                    182 ;--------------------------------------------------------
                                    183 ; code
                                    184 ;--------------------------------------------------------
                                    185 	.area CODE
                                    186 ;	./include/delay.h: 34: void _delay_loop_8(uint8_t loop_ctr) {
                                    187 ;	-----------------------------------------
                                    188 ;	 function _delay_loop_8
                                    189 ;	-----------------------------------------
      00003A                        190 __delay_loop_8:
                                    191 ;	./include/delay.h: 44: __endasm;
      00003A                        192 	00001$:
                                    193 ; 4 cycles per loop
      00003A C2 08                  194 	dzsn	__delay_loop_8_PARM_1 ; 1 cycle + 1 cycle for final skip
      00003C 1D 18                  195 	goto	00001$ ; 2 cycles
      00003E                        196 00101$:
                                    197 ;	./include/delay.h: 45: }
      00003E 3A 00                  198 	ret
                                    199 ;	./include/delay.h: 48: void _delay_loop_16(uint16_t loop_ctr) {
                                    200 ;	-----------------------------------------
                                    201 ;	 function _delay_loop_16
                                    202 ;	-----------------------------------------
      000040                        203 __delay_loop_16:
                                    204 ;	./include/delay.h: 65: __endasm;
      000040                        205 	00001$:
                                    206 ; 8 cycles per loop
      000040 00 00                  207 	nop	; 1 cycle
      000042 43 09                  208 	dec	__delay_loop_16_PARM_1+0 ; 1 cycle
      000044 44 08                  209 	subc	__delay_loop_16_PARM_1+1 ; 1 cycle
      000046 C3 07                  210 	mov	a, __delay_loop_16_PARM_1+0 ; 1 cycle
      000048 44 07                  211 	or	a, __delay_loop_16_PARM_1+1 ; 1 cycle
      00004A 00 0D                  212 	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
      00004C 20 18                  213 	goto	00001$ ; 2 cycles
      00004E                        214 00101$:
                                    215 ;	./include/delay.h: 66: }
      00004E 3A 00                  216 	ret
                                    217 ;	./include/delay.h: 69: void _delay_loop_32(uint32_t loop_ctr) {
                                    218 ;	-----------------------------------------
                                    219 ;	 function _delay_loop_32
                                    220 ;	-----------------------------------------
      000050                        221 __delay_loop_32:
                                    222 ;	./include/delay.h: 94: __endasm;
      000050                        223 	00001$:
                                    224 ; 12 cycles per loop
      000050 00 00                  225 	nop	; 1 cycle
      000052 45 09                  226 	dec	__delay_loop_32_PARM_1+0 ; 1 cycle
      000054 46 08                  227 	subc	__delay_loop_32_PARM_1+1 ; 1 cycle
      000056 47 08                  228 	subc	__delay_loop_32_PARM_1+2 ; 1 cycle
      000058 48 08                  229 	subc	__delay_loop_32_PARM_1+3 ; 1 cycle
      00005A C5 07                  230 	mov	a, __delay_loop_32_PARM_1+0 ; 1 cycle
      00005C 46 07                  231 	or	a, __delay_loop_32_PARM_1+1 ; 1 cycle
      00005E 47 07                  232 	or	a, __delay_loop_32_PARM_1+2 ; 1 cycle
      000060 48 07                  233 	or	a, __delay_loop_32_PARM_1+3 ; 1 cycle
      000062 00 0D                  234 	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
      000064 28 18                  235 	goto	00001$ ; 2 cycles
      000066                        236 00101$:
                                    237 ;	./include/delay.h: 95: }
      000066 3A 00                  238 	ret
                                    239 ;	main.c: 84: static void piezoInput(void)
                                    240 ;	-----------------------------------------
                                    241 ;	 function piezoInput
                                    242 ;	-----------------------------------------
      000068                        243 _piezoInput:
                                    244 ;	main.c: 86: TM2C = TM2C_CLK_DISABLE;
      000068 00 17                  245 	mov	a, #0x00
      00006A 9C 00                  246 	mov.io	__tm2c, a
                                    247 ;	main.c: 87: INTRQ &= (uint8_t)~INTRQ_TM2;
      00006C C5 0E                  248 	set0.io	__intrq, #6
                                    249 ;	main.c: 88: PA &= (uint8_t)~PIEZO_MASK;
      00006E 70 0E                  250 	set0.io	__pa, #3
                                    251 ;	main.c: 89: PAC &= (uint8_t)~PIEZO_MASK;
      000070 71 0E                  252 	set0.io	__pac, #3
                                    253 ;	main.c: 90: }
      000072 3A 00                  254 	ret
                                    255 ;	main.c: 92: static uint8_t activeDelayMilliseconds(uint16_t milliseconds)
                                    256 ;	-----------------------------------------
                                    257 ;	 function activeDelayMilliseconds
                                    258 ;	-----------------------------------------
      000074                        259 _activeDelayMilliseconds:
                                    260 ;	main.c: 94: PADIER = BUTTON_MASK;
      000074 40 17                  261 	mov	a, #0x40
      000076 8D 00                  262 	mov.io	__padier, a
                                    263 ;	main.c: 101: if (milliseconds == PIEZO_GAP_MS)
      000078 CC 07                  264 	mov	a, _activeDelayMilliseconds_PARM_1+1
      00007A C0 05                  265 	mov	p, a
      00007C CB 07                  266 	mov	a, _activeDelayMilliseconds_PARM_1+0
      00007E 32 12                  267 	ceqsn	a, #0x32
      000080 4A 18                  268 	goto	00102$
      000082 C0 07                  269 	mov	a, p
      000084 00 12                  270 	ceqsn	a, #0x00
      000086 4A 18                  271 	goto	00102$
                                    272 ;	main.c: 102: _delay_ms(PIEZO_GAP_MS);
      000088 43 17                  273 	mov	a, #0x43
      00008A C3 05                  274 	mov	__delay_loop_16_PARM_1+0, a
      00008C 01 17                  275 	mov	a, #0x01
      00008E C4 05                  276 	mov	__delay_loop_16_PARM_1+1, a
      000090 20 1C                  277 	call	__delay_loop_16
      000092 4E 18                  278 	goto	00103$
      000094                        279 00102$:
                                    280 ;	main.c: 104: _delay_ms(LED_PULSE_MS);
      000094 80 17                  281 	mov	a, #0x80
      000096 C3 05                  282 	mov	__delay_loop_16_PARM_1+0, a
      000098 84 09                  283 	clear	__delay_loop_16_PARM_1+1
      00009A 20 1C                  284 	call	__delay_loop_16
      00009C                        285 00103$:
                                    286 ;	main.c: 106: return buttonIsPressed();
      00009C B0 00                  287 	mov.io	a, __pa
      00009E 80 09                  288 	clear	p
      0000A0 40 14                  289 	and	a, #0x40
      0000A2 80 09                  290 	clear	p
      0000A4 40 07                  291 	or	a, p
      0000A6 01 11                  292 	sub	a, #0x01
      0000A8 00 17                  293 	mov	a, #0x00
      0000AA 1D 00                  294 	slc	a
      0000AC 01 16                  295 	xor	a, #0x01
                                    296 ;	main.c: 107: }
      0000AE 3A 00                  297 	ret
                                    298 ;	main.c: 109: static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
                                    299 ;	-----------------------------------------
                                    300 ;	 function sleepTicks
                                    301 ;	-----------------------------------------
      0000B0                        302 _sleepTicks:
                                    303 ;	main.c: 113: T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
      0000B0 C7 17                  304 	mov	a, #0xc7
      0000B2 86 00                  305 	mov.io	__t16m, a
                                    306 ;	main.c: 114: timer16Load = (uint16_t)(65535u - ticks + 1u);
      0000B4 00 17                  307 	mov	a, #0x00
      0000B6 4D 06                  308 	sub	a, _sleepTicks_PARM_1+0
      0000B8 C9 05                  309 	mov	_timer16Load+0, a
      0000BA 00 17                  310 	mov	a, #0x00
      0000BC CE 06                  311 	subc	a, _sleepTicks_PARM_1+1
      0000BE CA 05                  312 	mov	_timer16Load+1, a
                                    313 ;	main.c: 117: __endasm;
      0000C0 C9 00                  314 	stt16	_timer16Load
                                    315 ;	main.c: 118: INTEGS |= INTEGS_T16_FALLING;
      0000C2 8C 0F                  316 	set1.io	__integs, #4
                                    317 ;	main.c: 119: INTRQ &= (uint8_t)~INTRQ_T16;
      0000C4 45 0E                  318 	set0.io	__intrq, #2
                                    319 ;	main.c: 126: (piezoWake ? PIEZO_MASK : (uint8_t)0u));
      0000C6 CF 07                  320 	mov	a, _sleepTicks_PARM_2+0
      0000C8 00 12                  321 	ceqsn	a, #0x00
      0000CA 67 18                  322 	goto	00109$
      0000CC 69 18                  323 	goto	00103$
      0000CE                        324 00109$:
      0000CE 08 17                  325 	mov	a, #0x08
      0000D0 6A 18                  326 	goto	00104$
      0000D2                        327 00103$:
      0000D2 00 17                  328 	mov	a, #0x00
      0000D4                        329 00104$:
      0000D4 40 15                  330 	or	a, #0x40
      0000D6 8D 00                  331 	mov.io	__padier, a
                                    332 ;	main.c: 130: __endasm;
      0000D8 37 00                  333 	stopexe
                                    334 ;	main.c: 133: buttonPressed = buttonIsPressed();
      0000DA B0 00                  335 	mov.io	a, __pa
      0000DC 80 09                  336 	clear	p
      0000DE 40 14                  337 	and	a, #0x40
      0000E0 80 09                  338 	clear	p
      0000E2 40 07                  339 	or	a, p
      0000E4 01 11                  340 	sub	a, #0x01
      0000E6 00 17                  341 	mov	a, #0x00
      0000E8 1D 00                  342 	slc	a
      0000EA 01 16                  343 	xor	a, #0x01
      0000EC DD 05                  344 	mov	_sleepTicks_sloc0_1_0+0, a
                                    345 ;	main.c: 134: PADIER = 0;
      0000EE 00 17                  346 	mov	a, #0x00
      0000F0 8D 00                  347 	mov.io	__padier, a
                                    348 ;	main.c: 135: INTRQ &= (uint8_t)~INTRQ_T16;
      0000F2 45 0E                  349 	set0.io	__intrq, #2
                                    350 ;	main.c: 137: return buttonPressed;
      0000F4 DD 07                  351 	mov	a, _sleepTicks_sloc0_1_0+0
                                    352 ;	main.c: 138: }
      0000F6 3A 00                  353 	ret
                                    354 ;	main.c: 144: static void startTone(uint8_t timerDivisor)
                                    355 ;	-----------------------------------------
                                    356 ;	 function startTone
                                    357 ;	-----------------------------------------
      0000F8                        358 _startTone:
                                    359 ;	main.c: 147: PADIER = BUTTON_MASK;
      0000F8 40 17                  360 	mov	a, #0x40
      0000FA 8D 00                  361 	mov.io	__padier, a
                                    362 ;	main.c: 148: PAC |= PIEZO_MASK;
      0000FC 71 0F                  363 	set1.io	__pac, #3
                                    364 ;	main.c: 149: TM2CT = 0;
      0000FE 00 17                  365 	mov	a, #0x00
      000100 9D 00                  366 	mov.io	__tm2ct, a
                                    367 ;	main.c: 150: TM2B = (uint8_t)(timerDivisor - 1u);
      000102 D0 07                  368 	mov	a, _startTone_PARM_1+0
      000104 01 11                  369 	sub	a, #0x01
      000106 89 00                  370 	mov.io	__tm2b, a
                                    371 ;	main.c: 151: TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
      000108 00 17                  372 	mov	a, #0x00
      00010A 97 00                  373 	mov.io	__tm2s, a
                                    374 ;	main.c: 152: TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
      00010C 48 17                  375 	mov	a, #0x48
      00010E 9C 00                  376 	mov.io	__tm2c, a
                                    377 ;	main.c: 153: }
      000110 3A 00                  378 	ret
                                    379 ;	main.c: 155: static uint8_t tonePulse(void)
                                    380 ;	-----------------------------------------
                                    381 ;	 function tonePulse
                                    382 ;	-----------------------------------------
      000112                        383 _tonePulse:
                                    384 ;	main.c: 157: startTone(PIEZO_TONE_BOUND + 1u);
      000112 06 17                  385 	mov	a, #0x06
      000114 D0 05                  386 	mov	_startTone_PARM_1+0, a
      000116 7C 1C                  387 	call	_startTone
                                    388 ;	main.c: 158: _delay_ms(PIEZO_TONE_MS);
      000118 43 17                  389 	mov	a, #0x43
      00011A C3 05                  390 	mov	__delay_loop_16_PARM_1+0, a
      00011C 01 17                  391 	mov	a, #0x01
      00011E C4 05                  392 	mov	__delay_loop_16_PARM_1+1, a
      000120 20 1C                  393 	call	__delay_loop_16
                                    394 ;	main.c: 159: piezoInput();
      000122 34 1C                  395 	call	_piezoInput
                                    396 ;	main.c: 161: return buttonIsPressed();
      000124 B0 00                  397 	mov.io	a, __pa
      000126 80 09                  398 	clear	p
      000128 40 14                  399 	and	a, #0x40
      00012A 80 09                  400 	clear	p
      00012C 40 07                  401 	or	a, p
      00012E 01 11                  402 	sub	a, #0x01
      000130 00 17                  403 	mov	a, #0x00
      000132 1D 00                  404 	slc	a
      000134 01 16                  405 	xor	a, #0x01
                                    406 ;	main.c: 162: }
      000136 3A 00                  407 	ret
                                    408 ;	main.c: 164: static uint8_t startupChirps(void)
                                    409 ;	-----------------------------------------
                                    410 ;	 function startupChirps
                                    411 ;	-----------------------------------------
      000138                        412 _startupChirps:
                                    413 ;	main.c: 166: uint16_t offset = 0;
      000138 91 09                  414 	clear	_startupChirps_sloc1_1_0+0
      00013A 92 09                  415 	clear	_startupChirps_sloc1_1_0+1
                                    416 ;	main.c: 169: while (step--)
      00013C 0A 17                  417 	mov	a, #0x0a
      00013E D3 05                  418 	mov	_startupChirps_sloc2_1_0+0, a
      000140                        419 00109$:
      000140 D3 07                  420 	mov	a, _startupChirps_sloc2_1_0+0
      000142 53 09                  421 	dec	_startupChirps_sloc2_1_0+0
      000144 00 12                  422 	ceqsn	a, #0x00
      000146 A5 18                  423 	goto	00138$
      000148 F0 18                  424 	goto	00111$
      00014A                        425 00138$:
                                    426 ;	main.c: 171: uint8_t timerDivisor = chirpPattern[offset];
      00014A 85 17                  427 	mov	a, #<(_chirpPattern + 0)
      00014C 11 06                  428 	add	a, _startupChirps_sloc1_1_0+0
      00014E C0 05                  429 	mov	p, a
      000150 81 17                  430 	mov	a, #>(_chirpPattern + 0x8000 + 0)
      000152 92 06                  431 	addc	a, _startupChirps_sloc1_1_0+1
      000154 79 1D                  432 	call	__gptrget
      000156 D4 05                  433 	mov	_startupChirps_sloc3_1_0+0, a
                                    434 ;	main.c: 172: uint16_t duration = (uint16_t)chirpPattern[offset + 1u] |
      000158 D1 07                  435 	mov	a, _startupChirps_sloc1_1_0+0
      00015A D5 05                  436 	mov	_startupChirps_sloc4_1_0+0, a
      00015C 01 10                  437 	add	a, #0x01
      00015E 85 10                  438 	add	a, #<(_chirpPattern + 0)
      000160 C0 05                  439 	mov	p, a
      000162 00 17                  440 	mov	a, #0x00
      000164 10 00                  441 	addc	a
      000166 81 10                  442 	add	a, #>(_chirpPattern + 0x8000 + 0)
      000168 79 1D                  443 	call	__gptrget
      00016A D6 05                  444 	mov	_startupChirps_sloc5_1_0+0, a
      00016C 97 09                  445 	clear	_startupChirps_sloc5_1_0+1
      00016E D5 07                  446 	mov	a, _startupChirps_sloc4_1_0+0
      000170 02 10                  447 	add	a, #0x02
      000172 85 10                  448 	add	a, #<(_chirpPattern + 0)
      000174 C0 05                  449 	mov	p, a
      000176 00 17                  450 	mov	a, #0x00
      000178 10 00                  451 	addc	a
      00017A 81 10                  452 	add	a, #>(_chirpPattern + 0x8000 + 0)
      00017C 79 1D                  453 	call	__gptrget
      00017E C0 05                  454 	mov	p, a
      000180 00 17                  455 	mov	a, #0x00
      000182 56 07                  456 	or	a, _startupChirps_sloc5_1_0+0
      000184 D8 05                  457 	mov	_startupChirps_sloc6_1_0+0, a
      000186 C0 07                  458 	mov	a, p
      000188 57 07                  459 	or	a, _startupChirps_sloc5_1_0+1
      00018A D9 05                  460 	mov	_startupChirps_sloc6_1_0+1, a
                                    461 ;	main.c: 174: offset += CHIRP_STEP_BYTES;
      00018C D1 07                  462 	mov	a, _startupChirps_sloc1_1_0+0
      00018E 03 10                  463 	add	a, #0x03
      000190 C0 05                  464 	mov	p, a
      000192 D2 07                  465 	mov	a, _startupChirps_sloc1_1_0+1
      000194 10 00                  466 	addc	a
      000196 D2 05                  467 	mov	_startupChirps_sloc1_1_0+1, a
      000198 C0 07                  468 	mov	a, p
      00019A D1 05                  469 	mov	_startupChirps_sloc1_1_0+0, a
                                    470 ;	main.c: 176: if (timerDivisor)
      00019C D4 07                  471 	mov	a, _startupChirps_sloc3_1_0+0
      00019E 00 12                  472 	ceqsn	a, #0x00
      0001A0 D2 18                  473 	goto	00139$
      0001A2 D6 18                  474 	goto	00102$
      0001A4                        475 00139$:
                                    476 ;	main.c: 177: startTone(timerDivisor);
      0001A4 D4 07                  477 	mov	a, _startupChirps_sloc3_1_0+0
      0001A6 D0 05                  478 	mov	_startTone_PARM_1+0, a
      0001A8 7C 1C                  479 	call	_startTone
      0001AA D7 18                  480 	goto	00103$
      0001AC                        481 00102$:
                                    482 ;	main.c: 179: piezoInput();
      0001AC 34 1C                  483 	call	_piezoInput
      0001AE                        484 00103$:
                                    485 ;	main.c: 181: PADIER = BUTTON_MASK;
      0001AE 40 17                  486 	mov	a, #0x40
      0001B0 8D 00                  487 	mov.io	__padier, a
                                    488 ;	main.c: 182: while (duration--)
      0001B2 D8 07                  489 	mov	a, _startupChirps_sloc6_1_0+0
      0001B4 DA 05                  490 	mov	_startupChirps_sloc7_1_0+0, a
      0001B6 D9 07                  491 	mov	a, _startupChirps_sloc6_1_0+1
      0001B8 DB 05                  492 	mov	_startupChirps_sloc7_1_0+1, a
      0001BA                        493 00106$:
      0001BA DB 07                  494 	mov	a, _startupChirps_sloc7_1_0+1
      0001BC C0 05                  495 	mov	p, a
      0001BE DA 07                  496 	mov	a, _startupChirps_sloc7_1_0+0
      0001C0 5A 09                  497 	dec	_startupChirps_sloc7_1_0+0
      0001C2 5B 08                  498 	subc	_startupChirps_sloc7_1_0+1
      0001C4 40 07                  499 	or	a, p
      0001C6 00 12                  500 	ceqsn	a, #0x00
      0001C8 E6 18                  501 	goto	00140$
      0001CA A0 18                  502 	goto	00109$
      0001CC                        503 00140$:
                                    504 ;	main.c: 184: _delay_ms(1);
      0001CC 05 17                  505 	mov	a, #0x05
      0001CE C3 05                  506 	mov	__delay_loop_16_PARM_1+0, a
      0001D0 84 09                  507 	clear	__delay_loop_16_PARM_1+1
      0001D2 20 1C                  508 	call	__delay_loop_16
                                    509 ;	main.c: 185: if (buttonIsPressed())
      0001D4 B0 00                  510 	mov.io	a, __pa
      0001D6 C0 05                  511 	mov	p, a
      0001D8 D0 02                  512 	t1sn	p, #6
      0001DA DD 18                  513 	goto	00106$
                                    514 ;	main.c: 187: piezoInput();
      0001DC 34 1C                  515 	call	_piezoInput
                                    516 ;	main.c: 188: return 1;
      0001DE 01 01                  517 	ret	#0x01
      0001E0                        518 00111$:
                                    519 ;	main.c: 193: piezoInput();
      0001E0 34 1C                  520 	call	_piezoInput
                                    521 ;	main.c: 194: return 0;
                                    522 ;	main.c: 195: }
      0001E2 00 01                  523 	ret	#0x00
                                    524 ;	main.c: 201: static void waitForButtonRelease(void)
                                    525 ;	-----------------------------------------
                                    526 ;	 function waitForButtonRelease
                                    527 ;	-----------------------------------------
      0001E4                        528 _waitForButtonRelease:
                                    529 ;	main.c: 203: PADIER = BUTTON_MASK;
      0001E4 40 17                  530 	mov	a, #0x40
      0001E6 8D 00                  531 	mov.io	__padier, a
                                    532 ;	main.c: 205: while (buttonIsPressed())
      0001E8                        533 00101$:
      0001E8 B0 00                  534 	mov.io	a, __pa
      0001EA C0 05                  535 	mov	p, a
      0001EC D0 02                  536 	t1sn	p, #6
      0001EE FC 18                  537 	goto	00103$
                                    538 ;	main.c: 207: T16M = T16M_CLK_DISABLE;
      0001F0 00 17                  539 	mov	a, #0x00
      0001F2 86 00                  540 	mov.io	__t16m, a
                                    541 ;	main.c: 211: __endasm;
      0001F4 37 00                  542 	stopexe
      0001F6 F4 18                  543 	goto	00101$
      0001F8                        544 00103$:
                                    545 ;	main.c: 214: PADIER = 0;
      0001F8 00 17                  546 	mov	a, #0x00
      0001FA 8D 00                  547 	mov.io	__padier, a
                                    548 ;	main.c: 215: }
      0001FC 3A 00                  549 	ret
                                    550 ;	main.c: 217: static void deepSleep(void)
                                    551 ;	-----------------------------------------
                                    552 ;	 function deepSleep
                                    553 ;	-----------------------------------------
      0001FE                        554 _deepSleep:
                                    555 ;	main.c: 221: turnLedOff();
      0001FE 90 0F                  556 	set1.io	__pa, #4
                                    557 ;	main.c: 222: piezoInput();
      000200 34 1C                  558 	call	_piezoInput
                                    559 ;	main.c: 223: T16M = T16M_CLK_DISABLE;
      000202 00 17                  560 	mov	a, #0x00
      000204 86 00                  561 	mov.io	__t16m, a
                                    562 ;	main.c: 230: PADIER = BUTTON_MASK | PIEZO_MASK;
      000206 48 17                  563 	mov	a, #0x48
      000208 8D 00                  564 	mov.io	__padier, a
                                    565 ;	main.c: 234: __endasm;
      00020A 36 00                  566 	stopsys
                                    567 ;	main.c: 237: buttonPressed = buttonIsPressed();
      00020C B0 00                  568 	mov.io	a, __pa
      00020E 80 09                  569 	clear	p
      000210 40 14                  570 	and	a, #0x40
      000212 80 09                  571 	clear	p
      000214 40 07                  572 	or	a, p
      000216 01 11                  573 	sub	a, #0x01
      000218 00 17                  574 	mov	a, #0x00
      00021A 1D 00                  575 	slc	a
      00021C 01 16                  576 	xor	a, #0x01
                                    577 ;	main.c: 238: PADIER = 0;
      00021E 32 00                  578 	push	af
      000220 00 17                  579 	mov	a, #0x00
      000222 8D 00                  580 	mov.io	__padier, a
      000224 33 00                  581 	pop	af
                                    582 ;	main.c: 241: if (buttonPressed)
      000226 00 12                  583 	ceqsn	a, #0x00
      000228 16 19                  584 	goto	00109$
      00022A 17 19                  585 	goto	00103$
      00022C                        586 00109$:
                                    587 ;	main.c: 242: waitForButtonRelease();
      00022C F2 18                  588 	goto	_waitForButtonRelease
      00022E                        589 00103$:
                                    590 ;	main.c: 243: }
      00022E 3A 00                  591 	ret
                                    592 ;	main.c: 249: static void setup(void)
                                    593 ;	-----------------------------------------
                                    594 ;	 function setup
                                    595 ;	-----------------------------------------
      000230                        596 _setup:
                                    597 ;	main.c: 252: PA = LED_MASK;
      000230 10 17                  598 	mov	a, #0x10
      000232 90 00                  599 	mov.io	__pa, a
                                    600 ;	main.c: 253: PAC = LED_MASK;
      000234 10 17                  601 	mov	a, #0x10
      000236 91 00                  602 	mov.io	__pac, a
                                    603 ;	main.c: 254: PAPH = 0;
      000238 00 17                  604 	mov	a, #0x00
      00023A 92 00                  605 	mov.io	__paph, a
                                    606 ;	main.c: 255: PADIER = 0;
      00023C 00 17                  607 	mov	a, #0x00
      00023E 8D 00                  608 	mov.io	__padier, a
                                    609 ;	main.c: 257: GPCC = 0;
      000240 00 17                  610 	mov	a, #0x00
      000242 9A 00                  611 	mov.io	__gpcc, a
                                    612 ;	main.c: 258: GPCS = 0;
      000244 00 17                  613 	mov	a, #0x00
      000246 9E 00                  614 	mov.io	__gpcs, a
                                    615 ;	main.c: 259: TM2C = 0;
      000248 00 17                  616 	mov	a, #0x00
      00024A 9C 00                  617 	mov.io	__tm2c, a
                                    618 ;	main.c: 260: T16M = 0;
      00024C 00 17                  619 	mov	a, #0x00
      00024E 86 00                  620 	mov.io	__t16m, a
                                    621 ;	main.c: 262: MISC |= MISC_LVR_DISABLE;
      000250 5B 0F                  622 	set1.io	__misc, #2
                                    623 ;	main.c: 270: CLKMD_ENABLE_IHRC);
      000252 A3 00                  624 	mov.io	a, __clkmd
      000254 EC 14                  625 	and	a, #0xec
      000256 83 00                  626 	mov.io	__clkmd, a
                                    627 ;	main.c: 272: INTEN = 0;
      000258 00 17                  628 	mov	a, #0x00
      00025A 84 00                  629 	mov.io	__inten, a
                                    630 ;	main.c: 273: INTRQ = 0;
      00025C 00 17                  631 	mov	a, #0x00
      00025E 85 00                  632 	mov.io	__intrq, a
                                    633 ;	main.c: 274: }
      000260 3A 00                  634 	ret
                                    635 ;	main.c: 276: static uint8_t activeAlert(void)
                                    636 ;	-----------------------------------------
                                    637 ;	 function activeAlert
                                    638 ;	-----------------------------------------
      000262                        639 _activeAlert:
                                    640 ;	main.c: 278: uint8_t flashCount = 0;
      000262 9C 09                  641 	clear	_activeAlert_sloc8_1_0+0
                                    642 ;	main.c: 280: while (1)
      000264                        643 00114$:
                                    644 ;	main.c: 282: turnLedOn();
      000264 90 0E                  645 	set0.io	__pa, #4
                                    646 ;	main.c: 284: if (activeDelayMilliseconds(LED_PULSE_MS))
      000266 14 17                  647 	mov	a, #0x14
      000268 CB 05                  648 	mov	_activeDelayMilliseconds_PARM_1+0, a
      00026A 8C 09                  649 	clear	_activeDelayMilliseconds_PARM_1+1
      00026C 3A 1C                  650 	call	_activeDelayMilliseconds
      00026E 00 12                  651 	ceqsn	a, #0x00
      000270 3A 19                  652 	goto	00146$
      000272 3C 19                  653 	goto	00102$
      000274                        654 00146$:
                                    655 ;	main.c: 286: turnLedOff();
      000274 90 0F                  656 	set1.io	__pa, #4
                                    657 ;	main.c: 287: return 1;
      000276 01 01                  658 	ret	#0x01
      000278                        659 00102$:
                                    660 ;	main.c: 290: turnLedOff();
      000278 90 0F                  661 	set1.io	__pa, #4
                                    662 ;	main.c: 292: if (++flashCount >= LED_FLASHES_PER_BEEPS)
      00027A 1C 09                  663 	inc	_activeAlert_sloc8_1_0+0
      00027C DC 07                  664 	mov	a, _activeAlert_sloc8_1_0+0
      00027E 04 11                  665 	sub	a, #0x04
      000280 20 0C                  666 	t0sn.io	f, c
      000282 55 19                  667 	goto	00110$
                                    668 ;	main.c: 294: flashCount = 0;
      000284 9C 09                  669 	clear	_activeAlert_sloc8_1_0+0
                                    670 ;	main.c: 296: if (tonePulse())
      000286 89 1C                  671 	call	_tonePulse
      000288 00 12                  672 	ceqsn	a, #0x00
      00028A 47 19                  673 	goto	00147$
      00028C 48 19                  674 	goto	00104$
      00028E                        675 00147$:
                                    676 ;	main.c: 297: return 1;
      00028E 01 01                  677 	ret	#0x01
      000290                        678 00104$:
                                    679 ;	main.c: 299: if (activeDelayMilliseconds(PIEZO_GAP_MS))
      000290 32 17                  680 	mov	a, #0x32
      000292 CB 05                  681 	mov	_activeDelayMilliseconds_PARM_1+0, a
      000294 8C 09                  682 	clear	_activeDelayMilliseconds_PARM_1+1
      000296 3A 1C                  683 	call	_activeDelayMilliseconds
      000298 00 12                  684 	ceqsn	a, #0x00
      00029A 4F 19                  685 	goto	00148$
      00029C 50 19                  686 	goto	00106$
      00029E                        687 00148$:
                                    688 ;	main.c: 300: return 1;
      00029E 01 01                  689 	ret	#0x01
      0002A0                        690 00106$:
                                    691 ;	main.c: 302: if (tonePulse())
      0002A0 89 1C                  692 	call	_tonePulse
      0002A2 00 12                  693 	ceqsn	a, #0x00
      0002A4 54 19                  694 	goto	00149$
      0002A6 55 19                  695 	goto	00110$
      0002A8                        696 00149$:
                                    697 ;	main.c: 303: return 1;
      0002A8 01 01                  698 	ret	#0x01
      0002AA                        699 00110$:
                                    700 ;	main.c: 310: if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
      0002AA 20 17                  701 	mov	a, #0x20
      0002AC CD 05                  702 	mov	_sleepTicks_PARM_1+0, a
      0002AE CB 17                  703 	mov	a, #0xcb
      0002B0 CE 05                  704 	mov	_sleepTicks_PARM_1+1, a
      0002B2 8F 09                  705 	clear	_sleepTicks_PARM_2+0
      0002B4 58 1C                  706 	call	_sleepTicks
      0002B6 00 12                  707 	ceqsn	a, #0x00
      0002B8 5E 19                  708 	goto	00150$
      0002BA 32 19                  709 	goto	00114$
      0002BC                        710 00150$:
                                    711 ;	main.c: 311: return 1;
                                    712 ;	main.c: 313: }
      0002BC 01 01                  713 	ret	#0x01
                                    714 ;	main.c: 315: void main(void)
                                    715 ;	-----------------------------------------
                                    716 ;	 function main
                                    717 ;	-----------------------------------------
      0002BE                        718 _main:
                                    719 ;	main.c: 317: setup();
      0002BE 18 1D                  720 	call	_setup
                                    721 ;	main.c: 319: while (1)
      0002C0                        722 00104$:
                                    723 ;	main.c: 322: if (startupChirps())
      0002C0 9C 1C                  724 	call	_startupChirps
      0002C2 00 12                  725 	ceqsn	a, #0x00
      0002C4 64 19                  726 	goto	00116$
      0002C6 67 19                  727 	goto	00102$
      0002C8                        728 00116$:
                                    729 ;	main.c: 324: waitForButtonRelease();
      0002C8 F2 1C                  730 	call	_waitForButtonRelease
                                    731 ;	main.c: 325: deepSleep();
      0002CA FF 1C                  732 	call	_deepSleep
                                    733 ;	main.c: 326: continue;
      0002CC 60 19                  734 	goto	00104$
      0002CE                        735 00102$:
                                    736 ;	main.c: 329: activeAlert();
      0002CE 31 1D                  737 	call	_activeAlert
                                    738 ;	main.c: 330: waitForButtonRelease();
      0002D0 F2 1C                  739 	call	_waitForButtonRelease
                                    740 ;	main.c: 331: deepSleep();
      0002D2 FF 1C                  741 	call	_deepSleep
      0002D4 60 19                  742 	goto	00104$
                                    743 ;	main.c: 333: }
      0002D6 3A 00                  744 	ret
                                    745 ;	main.c: 339: unsigned char STARTUP_FUNCTION(void)
                                    746 ;	-----------------------------------------
                                    747 ;	 function _sdcc_external_startup
                                    748 ;	-----------------------------------------
      0002D8                        749 __sdcc_external_startup:
                                    750 ;	main.c: 341: AUTO_INIT_SYSCLOCK();
      0002D8 F4 17                  751 	mov	a, #0xf4
      0002DA 83 00                  752 	mov.io	__clkmd, a
                                    753 ;	main.c: 342: AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);
      0002DC 52 14                  754 	and	a, #'R'                       
      0002DE 43 14                  755 	and	a, #'C'                       
      0002E0 02 14                  756 	and	a, #(2)            
      0002E2 20 14                  757 	and	a, #((52000))     
      0002E4 CB 14                  758 	and	a, #((52000)>>8)  
      0002E6 00 14                  759 	and	a, #((52000)>>16) 
      0002E8 00 14                  760 	and	a, #((52000)>>24) 
      0002EA F0 14                  761 	and	a, #((2800))     
      0002EC 0A 14                  762 	and	a, #((2800)>>8)  
      0002EE 1F 14                  763 	and	a, #(0x1f)             
                                    764 ;	main.c: 344: return 0;
                                    765 ;	main.c: 345: }
      0002F0 00 01                  766 	ret	#0x00
                                    767 	.area CODE
                                    768 	.area CONST
      00030A                        769 _chirpPattern:
      00030A 1A 01                  770 	ret #0x1a	; 26
      00030C 28 01                  771 	ret #0x28	; 40
      00030E 00 01                  772 	ret #0x00	; 0
      000310 00 01                  773 	ret #0x00	; 0
      000312 0F 01                  774 	ret #0x0f	; 15
      000314 00 01                  775 	ret #0x00	; 0
      000316 06 01                  776 	ret #0x06	; 6
      000318 19 01                  777 	ret #0x19	; 25
      00031A 00 01                  778 	ret #0x00	; 0
      00031C 00 01                  779 	ret #0x00	; 0
      00031E 0F 01                  780 	ret #0x0f	; 15
      000320 00 01                  781 	ret #0x00	; 0
      000322 1A 01                  782 	ret #0x1a	; 26
      000324 14 01                  783 	ret #0x14	; 20
      000326 00 01                  784 	ret #0x00	; 0
      000328 00 01                  785 	ret #0x00	; 0
      00032A 0F 01                  786 	ret #0x0f	; 15
      00032C 00 01                  787 	ret #0x00	; 0
      00032E 06 01                  788 	ret #0x06	; 6
      000330 19 01                  789 	ret #0x19	; 25
      000332 00 01                  790 	ret #0x00	; 0
      000334 00 01                  791 	ret #0x00	; 0
      000336 0F 01                  792 	ret #0x0f	; 15
      000338 00 01                  793 	ret #0x00	; 0
      00033A 1A 01                  794 	ret #0x1a	; 26
      00033C 28 01                  795 	ret #0x28	; 40
      00033E 00 01                  796 	ret #0x00	; 0
      000340 00 01                  797 	ret #0x00	; 0
      000342 19 01                  798 	ret #0x19	; 25
      000344 00 01                  799 	ret #0x00	; 0
                                    800 	.area CABS (ABS)
