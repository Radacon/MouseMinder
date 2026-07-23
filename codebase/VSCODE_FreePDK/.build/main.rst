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
      000010                         94 _startupChirps_sloc1_1_0:
      000010                         95 	.ds 1
      000011                         96 _activeAlert_sloc2_1_0:
      000011                         97 	.ds 1
                                     98 ;--------------------------------------------------------
                                     99 ; overlayable items in ram
                                    100 ;--------------------------------------------------------
                                    101 	.area	OSEG (OVR,DATA)
      000012                        102 _sleepTicks_sloc0_1_0:
      000012                        103 	.ds 1
                                    104 ;--------------------------------------------------------
                                    105 ; Stack segment in internal ram
                                    106 ;--------------------------------------------------------
                                    107 	.area	SSEG
      000013                        108 __start__stack:
      000013                        109 	.ds	1
                                    110 
                                    111 ;--------------------------------------------------------
                                    112 ; absolute external ram data
                                    113 ;--------------------------------------------------------
                                    114 	.area DABS (ABS)
                                    115 ;--------------------------------------------------------
                                    116 ; interrupt vector
                                    117 ;--------------------------------------------------------
                                    118 	.area HOME
      000022                        119 __interrupt_vect:
                                    120 	.area	HEADER (ABS)
      000020                        121 	.org	 0x0020
      000020 3B 00                  122 	reti
                                    123 ;--------------------------------------------------------
                                    124 ; global & static initialisations
                                    125 ;--------------------------------------------------------
                                    126 	.area HOME
                                    127 	.area GSINIT
                                    128 	.area GSFINAL
                                    129 	.area GSINIT
                                    130 	.area	PREG (ABS)
      000000                        131 	.org 0x00
      000000                        132 p::
      000000                        133 	.ds 2
                                    134 	.area	HEADER (ABS)
      000000                        135 	.org 0x0000
      000000 00 00                  136 	nop
      000002 81 09                  137 	clear	p+1
      000004 12 17                  138 	mov	a, #s_OSEG
      000006 02 10                  139 	add	a, #l_OSEG + 1
      000008 FE 14                  140 	and	a, #0xfe
      00000A 82 00                  141 	mov.io	sp, a
      00000C 2C 1D                  142 	call	__sdcc_external_startup
      00000E 12 18                  143 	goto	s_GSINIT
                                    144 	.area GSINIT
      000024                        145 __sdcc_init_data:
      000024 02 17                  146 	mov	a, #s_DATA
      000026 C0 05                  147 	mov	p, a
      000028 19 18                  148 	goto	00002$
      00002A                        149 00001$:
      00002A 00 17                  150 	mov	a, #0x00
      00002C E0 00                  151 	idxm	p, a
      00002E 00 09                  152 	inc	p
      000030 02 17                  153 	mov	a, #s_DATA
      000032                        154 00002$:
      000032 10 10                  155 	add	a, #l_DATA
      000034 80 0B                  156 	ceqsn	a, p
      000036 15 18                  157 	goto	00001$
                                    158 	.area GSFINAL
      000038 11 18                  159 	goto	__sdcc_program_startup
                                    160 ;--------------------------------------------------------
                                    161 ; Home
                                    162 ;--------------------------------------------------------
                                    163 	.area HOME
                                    164 	.area HOME
      000022                        165 __sdcc_program_startup:
      000022 1F 19                  166 	goto	_main
                                    167 ;	return from main will return to caller
                                    168 ;--------------------------------------------------------
                                    169 ; code
                                    170 ;--------------------------------------------------------
                                    171 	.area CODE
                                    172 ;	./include/delay.h: 34: void _delay_loop_8(uint8_t loop_ctr) {
                                    173 ;	-----------------------------------------
                                    174 ;	 function _delay_loop_8
                                    175 ;	-----------------------------------------
      00003A                        176 __delay_loop_8:
                                    177 ;	./include/delay.h: 44: __endasm;
      00003A                        178 	00001$:
                                    179 ; 4 cycles per loop
      00003A C2 08                  180 	dzsn	__delay_loop_8_PARM_1 ; 1 cycle + 1 cycle for final skip
      00003C 1D 18                  181 	goto	00001$ ; 2 cycles
      00003E                        182 00101$:
                                    183 ;	./include/delay.h: 45: }
      00003E 3A 00                  184 	ret
                                    185 ;	./include/delay.h: 48: void _delay_loop_16(uint16_t loop_ctr) {
                                    186 ;	-----------------------------------------
                                    187 ;	 function _delay_loop_16
                                    188 ;	-----------------------------------------
      000040                        189 __delay_loop_16:
                                    190 ;	./include/delay.h: 65: __endasm;
      000040                        191 	00001$:
                                    192 ; 8 cycles per loop
      000040 00 00                  193 	nop	; 1 cycle
      000042 43 09                  194 	dec	__delay_loop_16_PARM_1+0 ; 1 cycle
      000044 44 08                  195 	subc	__delay_loop_16_PARM_1+1 ; 1 cycle
      000046 C3 07                  196 	mov	a, __delay_loop_16_PARM_1+0 ; 1 cycle
      000048 44 07                  197 	or	a, __delay_loop_16_PARM_1+1 ; 1 cycle
      00004A 00 0D                  198 	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
      00004C 20 18                  199 	goto	00001$ ; 2 cycles
      00004E                        200 00101$:
                                    201 ;	./include/delay.h: 66: }
      00004E 3A 00                  202 	ret
                                    203 ;	./include/delay.h: 69: void _delay_loop_32(uint32_t loop_ctr) {
                                    204 ;	-----------------------------------------
                                    205 ;	 function _delay_loop_32
                                    206 ;	-----------------------------------------
      000050                        207 __delay_loop_32:
                                    208 ;	./include/delay.h: 94: __endasm;
      000050                        209 	00001$:
                                    210 ; 12 cycles per loop
      000050 00 00                  211 	nop	; 1 cycle
      000052 45 09                  212 	dec	__delay_loop_32_PARM_1+0 ; 1 cycle
      000054 46 08                  213 	subc	__delay_loop_32_PARM_1+1 ; 1 cycle
      000056 47 08                  214 	subc	__delay_loop_32_PARM_1+2 ; 1 cycle
      000058 48 08                  215 	subc	__delay_loop_32_PARM_1+3 ; 1 cycle
      00005A C5 07                  216 	mov	a, __delay_loop_32_PARM_1+0 ; 1 cycle
      00005C 46 07                  217 	or	a, __delay_loop_32_PARM_1+1 ; 1 cycle
      00005E 47 07                  218 	or	a, __delay_loop_32_PARM_1+2 ; 1 cycle
      000060 48 07                  219 	or	a, __delay_loop_32_PARM_1+3 ; 1 cycle
      000062 00 0D                  220 	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
      000064 28 18                  221 	goto	00001$ ; 2 cycles
      000066                        222 00101$:
                                    223 ;	./include/delay.h: 95: }
      000066 3A 00                  224 	ret
                                    225 ;	main.c: 75: static void piezoInput(void)
                                    226 ;	-----------------------------------------
                                    227 ;	 function piezoInput
                                    228 ;	-----------------------------------------
      000068                        229 _piezoInput:
                                    230 ;	main.c: 77: TM2C = TM2C_CLK_DISABLE;
      000068 00 17                  231 	mov	a, #0x00
      00006A 9C 00                  232 	mov.io	__tm2c, a
                                    233 ;	main.c: 78: INTRQ &= (uint8_t)~INTRQ_TM2;
      00006C C5 0E                  234 	set0.io	__intrq, #6
                                    235 ;	main.c: 79: PA &= (uint8_t)~PIEZO_MASK;
      00006E 70 0E                  236 	set0.io	__pa, #3
                                    237 ;	main.c: 80: PAC &= (uint8_t)~PIEZO_MASK;
      000070 71 0E                  238 	set0.io	__pac, #3
                                    239 ;	main.c: 81: }
      000072 3A 00                  240 	ret
                                    241 ;	main.c: 83: static uint8_t activeDelayMilliseconds(uint16_t milliseconds)
                                    242 ;	-----------------------------------------
                                    243 ;	 function activeDelayMilliseconds
                                    244 ;	-----------------------------------------
      000074                        245 _activeDelayMilliseconds:
                                    246 ;	main.c: 85: PADIER = BUTTON_MASK;
      000074 40 17                  247 	mov	a, #0x40
      000076 8D 00                  248 	mov.io	__padier, a
                                    249 ;	main.c: 92: if (milliseconds == PIEZO_GAP_MS)
      000078 CC 07                  250 	mov	a, _activeDelayMilliseconds_PARM_1+1
      00007A C0 05                  251 	mov	p, a
      00007C CB 07                  252 	mov	a, _activeDelayMilliseconds_PARM_1+0
      00007E 32 12                  253 	ceqsn	a, #0x32
      000080 4A 18                  254 	goto	00102$
      000082 C0 07                  255 	mov	a, p
      000084 00 12                  256 	ceqsn	a, #0x00
      000086 4A 18                  257 	goto	00102$
                                    258 ;	main.c: 93: _delay_ms(PIEZO_GAP_MS);
      000088 43 17                  259 	mov	a, #0x43
      00008A C3 05                  260 	mov	__delay_loop_16_PARM_1+0, a
      00008C 01 17                  261 	mov	a, #0x01
      00008E C4 05                  262 	mov	__delay_loop_16_PARM_1+1, a
      000090 20 1C                  263 	call	__delay_loop_16
      000092 4E 18                  264 	goto	00103$
      000094                        265 00102$:
                                    266 ;	main.c: 95: _delay_ms(LED_PULSE_MS);
      000094 80 17                  267 	mov	a, #0x80
      000096 C3 05                  268 	mov	__delay_loop_16_PARM_1+0, a
      000098 84 09                  269 	clear	__delay_loop_16_PARM_1+1
      00009A 20 1C                  270 	call	__delay_loop_16
      00009C                        271 00103$:
                                    272 ;	main.c: 97: return buttonIsPressed();
      00009C B0 00                  273 	mov.io	a, __pa
      00009E 80 09                  274 	clear	p
      0000A0 40 14                  275 	and	a, #0x40
      0000A2 80 09                  276 	clear	p
      0000A4 40 07                  277 	or	a, p
      0000A6 01 11                  278 	sub	a, #0x01
      0000A8 00 17                  279 	mov	a, #0x00
      0000AA 1D 00                  280 	slc	a
      0000AC 01 16                  281 	xor	a, #0x01
                                    282 ;	main.c: 98: }
      0000AE 3A 00                  283 	ret
                                    284 ;	main.c: 100: static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
                                    285 ;	-----------------------------------------
                                    286 ;	 function sleepTicks
                                    287 ;	-----------------------------------------
      0000B0                        288 _sleepTicks:
                                    289 ;	main.c: 104: T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
      0000B0 C7 17                  290 	mov	a, #0xc7
      0000B2 86 00                  291 	mov.io	__t16m, a
                                    292 ;	main.c: 105: timer16Load = (uint16_t)(65535u - ticks + 1u);
      0000B4 00 17                  293 	mov	a, #0x00
      0000B6 4D 06                  294 	sub	a, _sleepTicks_PARM_1+0
      0000B8 C9 05                  295 	mov	_timer16Load+0, a
      0000BA 00 17                  296 	mov	a, #0x00
      0000BC CE 06                  297 	subc	a, _sleepTicks_PARM_1+1
      0000BE CA 05                  298 	mov	_timer16Load+1, a
                                    299 ;	main.c: 108: __endasm;
      0000C0 C9 00                  300 	stt16	_timer16Load
                                    301 ;	main.c: 109: INTEGS |= INTEGS_T16_FALLING;
      0000C2 8C 0F                  302 	set1.io	__integs, #4
                                    303 ;	main.c: 110: INTRQ &= (uint8_t)~INTRQ_T16;
      0000C4 45 0E                  304 	set0.io	__intrq, #2
                                    305 ;	main.c: 117: (piezoWake ? PIEZO_MASK : (uint8_t)0u));
      0000C6 CF 07                  306 	mov	a, _sleepTicks_PARM_2+0
      0000C8 00 12                  307 	ceqsn	a, #0x00
      0000CA 67 18                  308 	goto	00109$
      0000CC 69 18                  309 	goto	00103$
      0000CE                        310 00109$:
      0000CE 08 17                  311 	mov	a, #0x08
      0000D0 6A 18                  312 	goto	00104$
      0000D2                        313 00103$:
      0000D2 00 17                  314 	mov	a, #0x00
      0000D4                        315 00104$:
      0000D4 40 15                  316 	or	a, #0x40
      0000D6 8D 00                  317 	mov.io	__padier, a
                                    318 ;	main.c: 121: __endasm;
      0000D8 37 00                  319 	stopexe
                                    320 ;	main.c: 124: buttonPressed = buttonIsPressed();
      0000DA B0 00                  321 	mov.io	a, __pa
      0000DC 80 09                  322 	clear	p
      0000DE 40 14                  323 	and	a, #0x40
      0000E0 80 09                  324 	clear	p
      0000E2 40 07                  325 	or	a, p
      0000E4 01 11                  326 	sub	a, #0x01
      0000E6 00 17                  327 	mov	a, #0x00
      0000E8 1D 00                  328 	slc	a
      0000EA 01 16                  329 	xor	a, #0x01
      0000EC D2 05                  330 	mov	_sleepTicks_sloc0_1_0+0, a
                                    331 ;	main.c: 125: PADIER = 0;
      0000EE 00 17                  332 	mov	a, #0x00
      0000F0 8D 00                  333 	mov.io	__padier, a
                                    334 ;	main.c: 126: INTRQ &= (uint8_t)~INTRQ_T16;
      0000F2 45 0E                  335 	set0.io	__intrq, #2
                                    336 ;	main.c: 128: return buttonPressed;
      0000F4 D2 07                  337 	mov	a, _sleepTicks_sloc0_1_0+0
                                    338 ;	main.c: 129: }
      0000F6 3A 00                  339 	ret
                                    340 ;	main.c: 135: static void startTone(void)
                                    341 ;	-----------------------------------------
                                    342 ;	 function startTone
                                    343 ;	-----------------------------------------
      0000F8                        344 _startTone:
                                    345 ;	main.c: 138: PADIER = BUTTON_MASK;
      0000F8 40 17                  346 	mov	a, #0x40
      0000FA 8D 00                  347 	mov.io	__padier, a
                                    348 ;	main.c: 139: PAC |= PIEZO_MASK;
      0000FC 71 0F                  349 	set1.io	__pac, #3
                                    350 ;	main.c: 140: TM2CT = 0;
      0000FE 00 17                  351 	mov	a, #0x00
      000100 9D 00                  352 	mov.io	__tm2ct, a
                                    353 ;	main.c: 141: TM2B = PIEZO_TONE_BOUND;
      000102 05 17                  354 	mov	a, #0x05
      000104 89 00                  355 	mov.io	__tm2b, a
                                    356 ;	main.c: 142: TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
      000106 00 17                  357 	mov	a, #0x00
      000108 97 00                  358 	mov.io	__tm2s, a
                                    359 ;	main.c: 143: TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
      00010A 48 17                  360 	mov	a, #0x48
      00010C 9C 00                  361 	mov.io	__tm2c, a
                                    362 ;	main.c: 144: }
      00010E 3A 00                  363 	ret
                                    364 ;	main.c: 146: static uint8_t tonePulse(void)
                                    365 ;	-----------------------------------------
                                    366 ;	 function tonePulse
                                    367 ;	-----------------------------------------
      000110                        368 _tonePulse:
                                    369 ;	main.c: 148: startTone();
      000110 7C 1C                  370 	call	_startTone
                                    371 ;	main.c: 149: _delay_ms(PIEZO_TONE_MS);
      000112 43 17                  372 	mov	a, #0x43
      000114 C3 05                  373 	mov	__delay_loop_16_PARM_1+0, a
      000116 01 17                  374 	mov	a, #0x01
      000118 C4 05                  375 	mov	__delay_loop_16_PARM_1+1, a
      00011A 20 1C                  376 	call	__delay_loop_16
                                    377 ;	main.c: 150: piezoInput();
      00011C 34 1C                  378 	call	_piezoInput
                                    379 ;	main.c: 152: return buttonIsPressed();
      00011E B0 00                  380 	mov.io	a, __pa
      000120 80 09                  381 	clear	p
      000122 40 14                  382 	and	a, #0x40
      000124 80 09                  383 	clear	p
      000126 40 07                  384 	or	a, p
      000128 01 11                  385 	sub	a, #0x01
      00012A 00 17                  386 	mov	a, #0x00
      00012C 1D 00                  387 	slc	a
      00012E 01 16                  388 	xor	a, #0x01
                                    389 ;	main.c: 153: }
      000130 3A 00                  390 	ret
                                    391 ;	main.c: 155: static uint8_t startupChirps(void)
                                    392 ;	-----------------------------------------
                                    393 ;	 function startupChirps
                                    394 ;	-----------------------------------------
      000132                        395 _startupChirps:
                                    396 ;	main.c: 159: while (count--)
      000132 03 17                  397 	mov	a, #0x03
      000134 D0 05                  398 	mov	_startupChirps_sloc1_1_0+0, a
      000136                        399 00106$:
      000136 D0 07                  400 	mov	a, _startupChirps_sloc1_1_0+0
      000138 50 09                  401 	dec	_startupChirps_sloc1_1_0+0
      00013A 00 12                  402 	ceqsn	a, #0x00
      00013C A0 18                  403 	goto	00131$
      00013E B1 18                  404 	goto	00108$
      000140                        405 00131$:
                                    406 ;	main.c: 161: if (tonePulse())
      000140 88 1C                  407 	call	_tonePulse
      000142 00 12                  408 	ceqsn	a, #0x00
      000144 A4 18                  409 	goto	00132$
      000146 A5 18                  410 	goto	00102$
      000148                        411 00132$:
                                    412 ;	main.c: 162: return 1;
      000148 01 01                  413 	ret	#0x01
      00014A                        414 00102$:
                                    415 ;	main.c: 165: if (count && activeDelayMilliseconds(PIEZO_GAP_MS))
      00014A D0 07                  416 	mov	a, _startupChirps_sloc1_1_0+0
      00014C 00 12                  417 	ceqsn	a, #0x00
      00014E A9 18                  418 	goto	00133$
      000150 9B 18                  419 	goto	00106$
      000152                        420 00133$:
      000152 32 17                  421 	mov	a, #0x32
      000154 CB 05                  422 	mov	_activeDelayMilliseconds_PARM_1+0, a
      000156 8C 09                  423 	clear	_activeDelayMilliseconds_PARM_1+1
      000158 3A 1C                  424 	call	_activeDelayMilliseconds
      00015A 00 12                  425 	ceqsn	a, #0x00
      00015C B0 18                  426 	goto	00134$
      00015E 9B 18                  427 	goto	00106$
      000160                        428 00134$:
                                    429 ;	main.c: 166: return 1;
      000160 01 01                  430 	ret	#0x01
      000162                        431 00108$:
                                    432 ;	main.c: 169: return 0;
                                    433 ;	main.c: 170: }
      000162 00 01                  434 	ret	#0x00
                                    435 ;	main.c: 176: static void waitForButtonRelease(void)
                                    436 ;	-----------------------------------------
                                    437 ;	 function waitForButtonRelease
                                    438 ;	-----------------------------------------
      000164                        439 _waitForButtonRelease:
                                    440 ;	main.c: 178: PADIER = BUTTON_MASK;
      000164 40 17                  441 	mov	a, #0x40
      000166 8D 00                  442 	mov.io	__padier, a
                                    443 ;	main.c: 180: while (buttonIsPressed())
      000168                        444 00101$:
      000168 B0 00                  445 	mov.io	a, __pa
      00016A C0 05                  446 	mov	p, a
      00016C D0 02                  447 	t1sn	p, #6
      00016E BC 18                  448 	goto	00103$
                                    449 ;	main.c: 182: T16M = T16M_CLK_DISABLE;
      000170 00 17                  450 	mov	a, #0x00
      000172 86 00                  451 	mov.io	__t16m, a
                                    452 ;	main.c: 186: __endasm;
      000174 37 00                  453 	stopexe
      000176 B4 18                  454 	goto	00101$
      000178                        455 00103$:
                                    456 ;	main.c: 189: PADIER = 0;
      000178 00 17                  457 	mov	a, #0x00
      00017A 8D 00                  458 	mov.io	__padier, a
                                    459 ;	main.c: 190: }
      00017C 3A 00                  460 	ret
                                    461 ;	main.c: 192: static void deepSleep(void)
                                    462 ;	-----------------------------------------
                                    463 ;	 function deepSleep
                                    464 ;	-----------------------------------------
      00017E                        465 _deepSleep:
                                    466 ;	main.c: 196: turnLedOff();
      00017E 90 0F                  467 	set1.io	__pa, #4
                                    468 ;	main.c: 197: piezoInput();
      000180 34 1C                  469 	call	_piezoInput
                                    470 ;	main.c: 198: T16M = T16M_CLK_DISABLE;
      000182 00 17                  471 	mov	a, #0x00
      000184 86 00                  472 	mov.io	__t16m, a
                                    473 ;	main.c: 205: PADIER = BUTTON_MASK | PIEZO_MASK;
      000186 48 17                  474 	mov	a, #0x48
      000188 8D 00                  475 	mov.io	__padier, a
                                    476 ;	main.c: 209: __endasm;
      00018A 36 00                  477 	stopsys
                                    478 ;	main.c: 212: buttonPressed = buttonIsPressed();
      00018C B0 00                  479 	mov.io	a, __pa
      00018E 80 09                  480 	clear	p
      000190 40 14                  481 	and	a, #0x40
      000192 80 09                  482 	clear	p
      000194 40 07                  483 	or	a, p
      000196 01 11                  484 	sub	a, #0x01
      000198 00 17                  485 	mov	a, #0x00
      00019A 1D 00                  486 	slc	a
      00019C 01 16                  487 	xor	a, #0x01
                                    488 ;	main.c: 213: PADIER = 0;
      00019E 32 00                  489 	push	af
      0001A0 00 17                  490 	mov	a, #0x00
      0001A2 8D 00                  491 	mov.io	__padier, a
      0001A4 33 00                  492 	pop	af
                                    493 ;	main.c: 216: if (buttonPressed)
      0001A6 00 12                  494 	ceqsn	a, #0x00
      0001A8 D6 18                  495 	goto	00109$
      0001AA D7 18                  496 	goto	00103$
      0001AC                        497 00109$:
                                    498 ;	main.c: 217: waitForButtonRelease();
      0001AC B2 18                  499 	goto	_waitForButtonRelease
      0001AE                        500 00103$:
                                    501 ;	main.c: 218: }
      0001AE 3A 00                  502 	ret
                                    503 ;	main.c: 224: static void setup(void)
                                    504 ;	-----------------------------------------
                                    505 ;	 function setup
                                    506 ;	-----------------------------------------
      0001B0                        507 _setup:
                                    508 ;	main.c: 227: PA = LED_MASK;
      0001B0 10 17                  509 	mov	a, #0x10
      0001B2 90 00                  510 	mov.io	__pa, a
                                    511 ;	main.c: 228: PAC = LED_MASK;
      0001B4 10 17                  512 	mov	a, #0x10
      0001B6 91 00                  513 	mov.io	__pac, a
                                    514 ;	main.c: 229: PAPH = 0;
      0001B8 00 17                  515 	mov	a, #0x00
      0001BA 92 00                  516 	mov.io	__paph, a
                                    517 ;	main.c: 230: PADIER = 0;
      0001BC 00 17                  518 	mov	a, #0x00
      0001BE 8D 00                  519 	mov.io	__padier, a
                                    520 ;	main.c: 232: GPCC = 0;
      0001C0 00 17                  521 	mov	a, #0x00
      0001C2 9A 00                  522 	mov.io	__gpcc, a
                                    523 ;	main.c: 233: GPCS = 0;
      0001C4 00 17                  524 	mov	a, #0x00
      0001C6 9E 00                  525 	mov.io	__gpcs, a
                                    526 ;	main.c: 234: TM2C = 0;
      0001C8 00 17                  527 	mov	a, #0x00
      0001CA 9C 00                  528 	mov.io	__tm2c, a
                                    529 ;	main.c: 235: T16M = 0;
      0001CC 00 17                  530 	mov	a, #0x00
      0001CE 86 00                  531 	mov.io	__t16m, a
                                    532 ;	main.c: 237: MISC |= MISC_LVR_DISABLE;
      0001D0 5B 0F                  533 	set1.io	__misc, #2
                                    534 ;	main.c: 245: CLKMD_ENABLE_IHRC);
      0001D2 A3 00                  535 	mov.io	a, __clkmd
      0001D4 EC 14                  536 	and	a, #0xec
      0001D6 83 00                  537 	mov.io	__clkmd, a
                                    538 ;	main.c: 247: INTEN = 0;
      0001D8 00 17                  539 	mov	a, #0x00
      0001DA 84 00                  540 	mov.io	__inten, a
                                    541 ;	main.c: 248: INTRQ = 0;
      0001DC 00 17                  542 	mov	a, #0x00
      0001DE 85 00                  543 	mov.io	__intrq, a
                                    544 ;	main.c: 249: }
      0001E0 3A 00                  545 	ret
                                    546 ;	main.c: 251: static uint8_t activeAlert(void)
                                    547 ;	-----------------------------------------
                                    548 ;	 function activeAlert
                                    549 ;	-----------------------------------------
      0001E2                        550 _activeAlert:
                                    551 ;	main.c: 253: uint8_t flashCount = 0;
      0001E2 91 09                  552 	clear	_activeAlert_sloc2_1_0+0
                                    553 ;	main.c: 255: while (1)
      0001E4                        554 00114$:
                                    555 ;	main.c: 257: turnLedOn();
      0001E4 90 0E                  556 	set0.io	__pa, #4
                                    557 ;	main.c: 259: if (activeDelayMilliseconds(LED_PULSE_MS))
      0001E6 14 17                  558 	mov	a, #0x14
      0001E8 CB 05                  559 	mov	_activeDelayMilliseconds_PARM_1+0, a
      0001EA 8C 09                  560 	clear	_activeDelayMilliseconds_PARM_1+1
      0001EC 3A 1C                  561 	call	_activeDelayMilliseconds
      0001EE 00 12                  562 	ceqsn	a, #0x00
      0001F0 FA 18                  563 	goto	00146$
      0001F2 FC 18                  564 	goto	00102$
      0001F4                        565 00146$:
                                    566 ;	main.c: 261: turnLedOff();
      0001F4 90 0F                  567 	set1.io	__pa, #4
                                    568 ;	main.c: 262: return 1;
      0001F6 01 01                  569 	ret	#0x01
      0001F8                        570 00102$:
                                    571 ;	main.c: 265: turnLedOff();
      0001F8 90 0F                  572 	set1.io	__pa, #4
                                    573 ;	main.c: 267: if (++flashCount >= LED_FLASHES_PER_BEEPS)
      0001FA 11 09                  574 	inc	_activeAlert_sloc2_1_0+0
      0001FC D1 07                  575 	mov	a, _activeAlert_sloc2_1_0+0
      0001FE 04 11                  576 	sub	a, #0x04
      000200 20 0C                  577 	t0sn.io	f, c
      000202 15 19                  578 	goto	00110$
                                    579 ;	main.c: 269: flashCount = 0;
      000204 91 09                  580 	clear	_activeAlert_sloc2_1_0+0
                                    581 ;	main.c: 271: if (tonePulse())
      000206 88 1C                  582 	call	_tonePulse
      000208 00 12                  583 	ceqsn	a, #0x00
      00020A 07 19                  584 	goto	00147$
      00020C 08 19                  585 	goto	00104$
      00020E                        586 00147$:
                                    587 ;	main.c: 272: return 1;
      00020E 01 01                  588 	ret	#0x01
      000210                        589 00104$:
                                    590 ;	main.c: 274: if (activeDelayMilliseconds(PIEZO_GAP_MS))
      000210 32 17                  591 	mov	a, #0x32
      000212 CB 05                  592 	mov	_activeDelayMilliseconds_PARM_1+0, a
      000214 8C 09                  593 	clear	_activeDelayMilliseconds_PARM_1+1
      000216 3A 1C                  594 	call	_activeDelayMilliseconds
      000218 00 12                  595 	ceqsn	a, #0x00
      00021A 0F 19                  596 	goto	00148$
      00021C 10 19                  597 	goto	00106$
      00021E                        598 00148$:
                                    599 ;	main.c: 275: return 1;
      00021E 01 01                  600 	ret	#0x01
      000220                        601 00106$:
                                    602 ;	main.c: 277: if (tonePulse())
      000220 88 1C                  603 	call	_tonePulse
      000222 00 12                  604 	ceqsn	a, #0x00
      000224 14 19                  605 	goto	00149$
      000226 15 19                  606 	goto	00110$
      000228                        607 00149$:
                                    608 ;	main.c: 278: return 1;
      000228 01 01                  609 	ret	#0x01
      00022A                        610 00110$:
                                    611 ;	main.c: 285: if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
      00022A 20 17                  612 	mov	a, #0x20
      00022C CD 05                  613 	mov	_sleepTicks_PARM_1+0, a
      00022E CB 17                  614 	mov	a, #0xcb
      000230 CE 05                  615 	mov	_sleepTicks_PARM_1+1, a
      000232 8F 09                  616 	clear	_sleepTicks_PARM_2+0
      000234 58 1C                  617 	call	_sleepTicks
      000236 00 12                  618 	ceqsn	a, #0x00
      000238 1E 19                  619 	goto	00150$
      00023A F2 18                  620 	goto	00114$
      00023C                        621 00150$:
                                    622 ;	main.c: 286: return 1;
                                    623 ;	main.c: 288: }
      00023C 01 01                  624 	ret	#0x01
                                    625 ;	main.c: 290: void main(void)
                                    626 ;	-----------------------------------------
                                    627 ;	 function main
                                    628 ;	-----------------------------------------
      00023E                        629 _main:
                                    630 ;	main.c: 292: setup();
      00023E D8 1C                  631 	call	_setup
                                    632 ;	main.c: 294: while (1)
      000240                        633 00104$:
                                    634 ;	main.c: 297: if (startupChirps())
      000240 99 1C                  635 	call	_startupChirps
      000242 00 12                  636 	ceqsn	a, #0x00
      000244 24 19                  637 	goto	00116$
      000246 27 19                  638 	goto	00102$
      000248                        639 00116$:
                                    640 ;	main.c: 299: waitForButtonRelease();
      000248 B2 1C                  641 	call	_waitForButtonRelease
                                    642 ;	main.c: 300: deepSleep();
      00024A BF 1C                  643 	call	_deepSleep
                                    644 ;	main.c: 301: continue;
      00024C 20 19                  645 	goto	00104$
      00024E                        646 00102$:
                                    647 ;	main.c: 304: activeAlert();
      00024E F1 1C                  648 	call	_activeAlert
                                    649 ;	main.c: 305: waitForButtonRelease();
      000250 B2 1C                  650 	call	_waitForButtonRelease
                                    651 ;	main.c: 306: deepSleep();
      000252 BF 1C                  652 	call	_deepSleep
      000254 20 19                  653 	goto	00104$
                                    654 ;	main.c: 308: }
      000256 3A 00                  655 	ret
                                    656 ;	main.c: 314: unsigned char STARTUP_FUNCTION(void)
                                    657 ;	-----------------------------------------
                                    658 ;	 function _sdcc_external_startup
                                    659 ;	-----------------------------------------
      000258                        660 __sdcc_external_startup:
                                    661 ;	main.c: 316: AUTO_INIT_SYSCLOCK();
      000258 F4 17                  662 	mov	a, #0xf4
      00025A 83 00                  663 	mov.io	__clkmd, a
                                    664 ;	main.c: 317: AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);
      00025C 52 14                  665 	and	a, #'R'                       
      00025E 43 14                  666 	and	a, #'C'                       
      000260 02 14                  667 	and	a, #(2)            
      000262 20 14                  668 	and	a, #((52000))     
      000264 CB 14                  669 	and	a, #((52000)>>8)  
      000266 00 14                  670 	and	a, #((52000)>>16) 
      000268 00 14                  671 	and	a, #((52000)>>24) 
      00026A F0 14                  672 	and	a, #((2800))     
      00026C 0A 14                  673 	and	a, #((2800)>>8)  
      00026E 1F 14                  674 	and	a, #(0x1f)             
                                    675 ;	main.c: 319: return 0;
                                    676 ;	main.c: 320: }
      000270 00 01                  677 	ret	#0x00
                                    678 	.area CODE
                                    679 	.area CONST
                                    680 	.area CABS (ABS)
