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
      00000B                         88 _sleepTicks_PARM_1:
      00000B                         89 	.ds 2
      00000D                         90 _sleepTicks_PARM_2:
      00000D                         91 	.ds 1
      00000E                         92 _sleepMilliseconds_PARM_1:
      00000E                         93 	.ds 2
      000010                         94 _sleepMilliseconds_PARM_2:
      000010                         95 	.ds 1
      000011                         96 _sleepMilliseconds_sloc1_1_0:
      000011                         97 	.ds 2
      000013                         98 _sleepMilliseconds_sloc2_1_0:
      000013                         99 	.ds 2
      000015                        100 _sleepMilliseconds_sloc3_1_0:
      000015                        101 	.ds 2
      000017                        102 _sleepMilliseconds_sloc4_1_0:
      000017                        103 	.ds 2
      000019                        104 _startTone_PARM_1:
      000019                        105 	.ds 1
      00001A                        106 _startupChirps_sloc5_1_0:
      00001A                        107 	.ds 2
      00001C                        108 _startupChirps_sloc6_1_0:
      00001C                        109 	.ds 1
      00001D                        110 _startupChirps_sloc7_1_0:
      00001D                        111 	.ds 1
      00001E                        112 _startupChirps_sloc8_1_0:
      00001E                        113 	.ds 1
      00001F                        114 _startupChirps_sloc9_1_0:
      00001F                        115 	.ds 2
      000021                        116 _startupChirps_sloc10_1_0:
      000021                        117 	.ds 2
      000023                        118 _startupChirps_sloc11_1_0:
      000023                        119 	.ds 2
      000025                        120 _activeAlert_sloc12_1_0:
      000025                        121 	.ds 1
                                    122 ;--------------------------------------------------------
                                    123 ; overlayable items in ram
                                    124 ;--------------------------------------------------------
                                    125 	.area	OSEG (OVR,DATA)
      000026                        126 _sleepTicks_sloc0_1_0:
      000026                        127 	.ds 1
                                    128 ;--------------------------------------------------------
                                    129 ; Stack segment in internal ram
                                    130 ;--------------------------------------------------------
                                    131 	.area	SSEG
      000027                        132 __start__stack:
      000027                        133 	.ds	1
                                    134 
                                    135 ;--------------------------------------------------------
                                    136 ; absolute external ram data
                                    137 ;--------------------------------------------------------
                                    138 	.area DABS (ABS)
                                    139 ;--------------------------------------------------------
                                    140 ; interrupt vector
                                    141 ;--------------------------------------------------------
                                    142 	.area HOME
      000022                        143 __interrupt_vect:
                                    144 	.area	HEADER (ABS)
      000020                        145 	.org	 0x0020
      000020 3B 00                  146 	reti
                                    147 ;--------------------------------------------------------
                                    148 ; global & static initialisations
                                    149 ;--------------------------------------------------------
                                    150 	.area HOME
                                    151 	.area GSINIT
                                    152 	.area GSFINAL
                                    153 	.area GSINIT
                                    154 	.area	PREG (ABS)
      000000                        155 	.org 0x00
      000000                        156 p::
      000000                        157 	.ds 2
                                    158 	.area	HEADER (ABS)
      000000                        159 	.org 0x0000
      000000 00 00                  160 	nop
      000002 81 09                  161 	clear	p+1
      000004 26 17                  162 	mov	a, #s_OSEG
      000006 02 10                  163 	add	a, #l_OSEG + 1
      000008 FE 14                  164 	and	a, #0xfe
      00000A 82 00                  165 	mov.io	sp, a
      00000C 87 1D                  166 	call	__sdcc_external_startup
      00000E 12 18                  167 	goto	s_GSINIT
                                    168 	.area GSINIT
      000024                        169 __sdcc_init_data:
      000024 02 17                  170 	mov	a, #s_DATA
      000026 C0 05                  171 	mov	p, a
      000028 19 18                  172 	goto	00002$
      00002A                        173 00001$:
      00002A 00 17                  174 	mov	a, #0x00
      00002C E0 00                  175 	idxm	p, a
      00002E 00 09                  176 	inc	p
      000030 02 17                  177 	mov	a, #s_DATA
      000032                        178 00002$:
      000032 24 10                  179 	add	a, #l_DATA
      000034 80 0B                  180 	ceqsn	a, p
      000036 15 18                  181 	goto	00001$
                                    182 	.area GSFINAL
      000038 11 18                  183 	goto	__sdcc_program_startup
                                    184 ;--------------------------------------------------------
                                    185 ; Home
                                    186 ;--------------------------------------------------------
                                    187 	.area HOME
                                    188 	.area HOME
      000022                        189 __sdcc_program_startup:
      000022 7A 19                  190 	goto	_main
                                    191 ;	return from main will return to caller
                                    192 ;--------------------------------------------------------
                                    193 ; code
                                    194 ;--------------------------------------------------------
                                    195 	.area CODE
                                    196 ;	./include/delay.h: 34: void _delay_loop_8(uint8_t loop_ctr) {
                                    197 ;	-----------------------------------------
                                    198 ;	 function _delay_loop_8
                                    199 ;	-----------------------------------------
      00003A                        200 __delay_loop_8:
                                    201 ;	./include/delay.h: 44: __endasm;
      00003A                        202 	00001$:
                                    203 ; 4 cycles per loop
      00003A C2 08                  204 	dzsn	__delay_loop_8_PARM_1 ; 1 cycle + 1 cycle for final skip
      00003C 1D 18                  205 	goto	00001$ ; 2 cycles
      00003E                        206 00101$:
                                    207 ;	./include/delay.h: 45: }
      00003E 3A 00                  208 	ret
                                    209 ;	./include/delay.h: 48: void _delay_loop_16(uint16_t loop_ctr) {
                                    210 ;	-----------------------------------------
                                    211 ;	 function _delay_loop_16
                                    212 ;	-----------------------------------------
      000040                        213 __delay_loop_16:
                                    214 ;	./include/delay.h: 65: __endasm;
      000040                        215 	00001$:
                                    216 ; 8 cycles per loop
      000040 00 00                  217 	nop	; 1 cycle
      000042 43 09                  218 	dec	__delay_loop_16_PARM_1+0 ; 1 cycle
      000044 44 08                  219 	subc	__delay_loop_16_PARM_1+1 ; 1 cycle
      000046 C3 07                  220 	mov	a, __delay_loop_16_PARM_1+0 ; 1 cycle
      000048 44 07                  221 	or	a, __delay_loop_16_PARM_1+1 ; 1 cycle
      00004A 00 0D                  222 	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
      00004C 20 18                  223 	goto	00001$ ; 2 cycles
      00004E                        224 00101$:
                                    225 ;	./include/delay.h: 66: }
      00004E 3A 00                  226 	ret
                                    227 ;	./include/delay.h: 69: void _delay_loop_32(uint32_t loop_ctr) {
                                    228 ;	-----------------------------------------
                                    229 ;	 function _delay_loop_32
                                    230 ;	-----------------------------------------
      000050                        231 __delay_loop_32:
                                    232 ;	./include/delay.h: 94: __endasm;
      000050                        233 	00001$:
                                    234 ; 12 cycles per loop
      000050 00 00                  235 	nop	; 1 cycle
      000052 45 09                  236 	dec	__delay_loop_32_PARM_1+0 ; 1 cycle
      000054 46 08                  237 	subc	__delay_loop_32_PARM_1+1 ; 1 cycle
      000056 47 08                  238 	subc	__delay_loop_32_PARM_1+2 ; 1 cycle
      000058 48 08                  239 	subc	__delay_loop_32_PARM_1+3 ; 1 cycle
      00005A C5 07                  240 	mov	a, __delay_loop_32_PARM_1+0 ; 1 cycle
      00005C 46 07                  241 	or	a, __delay_loop_32_PARM_1+1 ; 1 cycle
      00005E 47 07                  242 	or	a, __delay_loop_32_PARM_1+2 ; 1 cycle
      000060 48 07                  243 	or	a, __delay_loop_32_PARM_1+3 ; 1 cycle
      000062 00 0D                  244 	t1sn.io	f, z ; 1 cycle + 1 cycle for final skip
      000064 28 18                  245 	goto	00001$ ; 2 cycles
      000066                        246 00101$:
                                    247 ;	./include/delay.h: 95: }
      000066 3A 00                  248 	ret
                                    249 ;	main.c: 76: static void piezoInput(void)
                                    250 ;	-----------------------------------------
                                    251 ;	 function piezoInput
                                    252 ;	-----------------------------------------
      000068                        253 _piezoInput:
                                    254 ;	main.c: 78: TM2C = TM2C_CLK_DISABLE;
      000068 00 17                  255 	mov	a, #0x00
      00006A 9C 00                  256 	mov.io	__tm2c, a
                                    257 ;	main.c: 79: INTRQ &= (uint8_t)~INTRQ_TM2;
      00006C C5 0E                  258 	set0.io	__intrq, #6
                                    259 ;	main.c: 80: PA &= (uint8_t)~PIEZO_MASK;
      00006E 70 0E                  260 	set0.io	__pa, #3
                                    261 ;	main.c: 81: PAC &= (uint8_t)~PIEZO_MASK;
      000070 71 0E                  262 	set0.io	__pac, #3
                                    263 ;	main.c: 82: }
      000072 3A 00                  264 	ret
                                    265 ;	main.c: 84: static uint8_t activeLedPulseDelay(void)
                                    266 ;	-----------------------------------------
                                    267 ;	 function activeLedPulseDelay
                                    268 ;	-----------------------------------------
      000074                        269 _activeLedPulseDelay:
                                    270 ;	main.c: 86: PADIER = BUTTON_MASK;
      000074 40 17                  271 	mov	a, #0x40
      000076 8D 00                  272 	mov.io	__padier, a
                                    273 ;	main.c: 93: _delay_ms(LED_PULSE_MS);
      000078 3F 17                  274 	mov	a, #0x3f
      00007A C3 05                  275 	mov	__delay_loop_16_PARM_1+0, a
      00007C 84 09                  276 	clear	__delay_loop_16_PARM_1+1
      00007E 20 1C                  277 	call	__delay_loop_16
                                    278 ;	main.c: 95: return buttonIsPressed();
      000080 B0 00                  279 	mov.io	a, __pa
      000082 80 09                  280 	clear	p
      000084 40 14                  281 	and	a, #0x40
      000086 80 09                  282 	clear	p
      000088 40 07                  283 	or	a, p
      00008A 01 11                  284 	sub	a, #0x01
      00008C 00 17                  285 	mov	a, #0x00
      00008E 1D 00                  286 	slc	a
      000090 01 16                  287 	xor	a, #0x01
                                    288 ;	main.c: 96: }
      000092 3A 00                  289 	ret
                                    290 ;	main.c: 98: static uint8_t sleepTicks(uint16_t ticks, uint8_t piezoWake)
                                    291 ;	-----------------------------------------
                                    292 ;	 function sleepTicks
                                    293 ;	-----------------------------------------
      000094                        294 _sleepTicks:
                                    295 ;	main.c: 102: T16M = (uint8_t)TIMER16_SLEEP_CONFIG;
      000094 C7 17                  296 	mov	a, #0xc7
      000096 86 00                  297 	mov.io	__t16m, a
                                    298 ;	main.c: 103: timer16Load = (uint16_t)(32768u - ticks);
      000098 00 17                  299 	mov	a, #0x00
      00009A 4B 06                  300 	sub	a, _sleepTicks_PARM_1+0
      00009C C9 05                  301 	mov	_timer16Load+0, a
      00009E 80 17                  302 	mov	a, #0x80
      0000A0 CC 06                  303 	subc	a, _sleepTicks_PARM_1+1
      0000A2 CA 05                  304 	mov	_timer16Load+1, a
                                    305 ;	main.c: 106: __endasm;
      0000A4 C9 00                  306 	stt16	_timer16Load
                                    307 ;	main.c: 107: INTEGS &= (uint8_t)~INTEGS_T16_FALLING;
      0000A6 8C 0E                  308 	set0.io	__integs, #4
                                    309 ;	main.c: 108: INTRQ &= (uint8_t)~INTRQ_T16;
      0000A8 45 0E                  310 	set0.io	__intrq, #2
                                    311 ;	main.c: 115: (piezoWake ? PIEZO_MASK : (uint8_t)0u));
      0000AA CD 07                  312 	mov	a, _sleepTicks_PARM_2+0
      0000AC 00 12                  313 	ceqsn	a, #0x00
      0000AE 59 18                  314 	goto	00109$
      0000B0 5B 18                  315 	goto	00103$
      0000B2                        316 00109$:
      0000B2 08 17                  317 	mov	a, #0x08
      0000B4 5C 18                  318 	goto	00104$
      0000B6                        319 00103$:
      0000B6 00 17                  320 	mov	a, #0x00
      0000B8                        321 00104$:
      0000B8 40 15                  322 	or	a, #0x40
      0000BA 8D 00                  323 	mov.io	__padier, a
                                    324 ;	main.c: 119: __endasm;
      0000BC 37 00                  325 	stopexe
                                    326 ;	main.c: 122: buttonPressed = buttonIsPressed();
      0000BE B0 00                  327 	mov.io	a, __pa
      0000C0 80 09                  328 	clear	p
      0000C2 40 14                  329 	and	a, #0x40
      0000C4 80 09                  330 	clear	p
      0000C6 40 07                  331 	or	a, p
      0000C8 01 11                  332 	sub	a, #0x01
      0000CA 00 17                  333 	mov	a, #0x00
      0000CC 1D 00                  334 	slc	a
      0000CE 01 16                  335 	xor	a, #0x01
      0000D0 E6 05                  336 	mov	_sleepTicks_sloc0_1_0+0, a
                                    337 ;	main.c: 123: PADIER = 0;
      0000D2 00 17                  338 	mov	a, #0x00
      0000D4 8D 00                  339 	mov.io	__padier, a
                                    340 ;	main.c: 124: INTRQ &= (uint8_t)~INTRQ_T16;
      0000D6 45 0E                  341 	set0.io	__intrq, #2
                                    342 ;	main.c: 126: return buttonPressed;
      0000D8 E6 07                  343 	mov	a, _sleepTicks_sloc0_1_0+0
                                    344 ;	main.c: 127: }
      0000DA 3A 00                  345 	ret
                                    346 ;	main.c: 129: static uint8_t sleepMilliseconds(uint16_t milliseconds, uint8_t piezoWake)
                                    347 ;	-----------------------------------------
                                    348 ;	 function sleepMilliseconds
                                    349 ;	-----------------------------------------
      0000DC                        350 _sleepMilliseconds:
                                    351 ;	main.c: 133: while (milliseconds > 500u)
      0000DC                        352 00103$:
      0000DC CE 07                  353 	mov	a, _sleepMilliseconds_PARM_1+0
      0000DE D1 05                  354 	mov	_sleepMilliseconds_sloc1_1_0+0, a
      0000E0 CF 07                  355 	mov	a, _sleepMilliseconds_PARM_1+1
      0000E2 D2 05                  356 	mov	_sleepMilliseconds_sloc1_1_0+1, a
      0000E4 F4 17                  357 	mov	a, #0xf4
      0000E6 51 06                  358 	sub	a, _sleepMilliseconds_sloc1_1_0+0
      0000E8 01 17                  359 	mov	a, #0x01
      0000EA D2 06                  360 	subc	a, _sleepMilliseconds_sloc1_1_0+1
      0000EC 20 0D                  361 	t1sn.io	f, c
      0000EE 8D 18                  362 	goto	00105$
                                    363 ;	main.c: 135: if (sleepTicks((uint16_t)(F_CPU / 2u), piezoWake))
      0000F0 90 17                  364 	mov	a, #0x90
      0000F2 CB 05                  365 	mov	_sleepTicks_PARM_1+0, a
      0000F4 65 17                  366 	mov	a, #0x65
      0000F6 CC 05                  367 	mov	_sleepTicks_PARM_1+1, a
      0000F8 D0 07                  368 	mov	a, _sleepMilliseconds_PARM_2+0
      0000FA CD 05                  369 	mov	_sleepTicks_PARM_2+0, a
      0000FC 4A 1C                  370 	call	_sleepTicks
      0000FE 00 12                  371 	ceqsn	a, #0x00
      000100 82 18                  372 	goto	00126$
      000102 83 18                  373 	goto	00102$
      000104                        374 00126$:
                                    375 ;	main.c: 136: return 1;
      000104 01 01                  376 	ret	#0x01
      000106                        377 00102$:
                                    378 ;	main.c: 138: milliseconds -= 500u;
      000106 D1 07                  379 	mov	a, _sleepMilliseconds_sloc1_1_0+0
      000108 F4 11                  380 	sub	a, #0xf4
      00010A C0 05                  381 	mov	p, a
      00010C D2 07                  382 	mov	a, _sleepMilliseconds_sloc1_1_0+1
      00010E 11 00                  383 	subc	a
      000110 01 11                  384 	sub	a, #0x01
      000112 CF 05                  385 	mov	_sleepMilliseconds_PARM_1+1, a
      000114 C0 07                  386 	mov	a, p
      000116 CE 05                  387 	mov	_sleepMilliseconds_PARM_1+0, a
      000118 6E 18                  388 	goto	00103$
      00011A                        389 00105$:
                                    390 ;	main.c: 141: if (!milliseconds)
      00011A CE 07                  391 	mov	a, _sleepMilliseconds_PARM_1+0
      00011C 4F 07                  392 	or	a, _sleepMilliseconds_PARM_1+1
      00011E 00 12                  393 	ceqsn	a, #0x00
      000120 92 18                  394 	goto	00107$
                                    395 ;	main.c: 142: return 0;
      000122 00 01                  396 	ret	#0x00
      000124                        397 00107$:
                                    398 ;	main.c: 145: ticks = (uint16_t)((milliseconds << 5) +
      000124 CE 07                  399 	mov	a, _sleepMilliseconds_PARM_1+0
      000126 D3 05                  400 	mov	_sleepMilliseconds_sloc2_1_0+0, a
      000128 CF 07                  401 	mov	a, _sleepMilliseconds_PARM_1+1
      00012A D4 05                  402 	mov	_sleepMilliseconds_sloc2_1_0+1, a
      00012C 05 17                  403 	mov	a, #5
      00012E                        404 00127$:
      00012E D3 0A                  405 	sl	_sleepMilliseconds_sloc2_1_0+0
      000130 54 0B                  406 	slc	_sleepMilliseconds_sloc2_1_0+1
      000132 13 00                  407 	dzsn	a
      000134 97 18                  408 	goto	00127$
                                    409 ;	main.c: 146: (milliseconds << 4) +
      000136 CE 07                  410 	mov	a, _sleepMilliseconds_PARM_1+0
      000138 D5 05                  411 	mov	_sleepMilliseconds_sloc3_1_0+0, a
      00013A CF 07                  412 	mov	a, _sleepMilliseconds_PARM_1+1
      00013C D6 05                  413 	mov	_sleepMilliseconds_sloc3_1_0+1, a
      00013E 04 17                  414 	mov	a, #4
      000140                        415 00128$:
      000140 D5 0A                  416 	sl	_sleepMilliseconds_sloc3_1_0+0
      000142 56 0B                  417 	slc	_sleepMilliseconds_sloc3_1_0+1
      000144 13 00                  418 	dzsn	a
      000146 A0 18                  419 	goto	00128$
      000148 D3 07                  420 	mov	a, _sleepMilliseconds_sloc2_1_0+0
      00014A 15 06                  421 	add	a, _sleepMilliseconds_sloc3_1_0+0
      00014C D7 05                  422 	mov	_sleepMilliseconds_sloc4_1_0+0, a
      00014E D4 07                  423 	mov	a, _sleepMilliseconds_sloc2_1_0+1
      000150 96 06                  424 	addc	a, _sleepMilliseconds_sloc3_1_0+1
      000152 D8 05                  425 	mov	_sleepMilliseconds_sloc4_1_0+1, a
                                    426 ;	main.c: 147: (milliseconds << 2));
      000154 CF 07                  427 	mov	a, _sleepMilliseconds_PARM_1+1
      000156 C0 05                  428 	mov	p, a
      000158 CE 07                  429 	mov	a, _sleepMilliseconds_PARM_1+0
      00015A 1B 00                  430 	sl	a
      00015C 40 0B                  431 	slc	p
      00015E 1B 00                  432 	sl	a
      000160 40 0B                  433 	slc	p
      000162 17 06                  434 	add	a, _sleepMilliseconds_sloc4_1_0+0
      000164 CB 05                  435 	mov	_sleepTicks_PARM_1+0, a
      000166 D8 07                  436 	mov	a, _sleepMilliseconds_sloc4_1_0+1
      000168 80 06                  437 	addc	a, p
      00016A CC 05                  438 	mov	_sleepTicks_PARM_1+1, a
                                    439 ;	main.c: 149: return sleepTicks(ticks, piezoWake);
      00016C D0 07                  440 	mov	a, _sleepMilliseconds_PARM_2+0
      00016E CD 05                  441 	mov	_sleepTicks_PARM_2+0, a
      000170 4A 18                  442 	goto	_sleepTicks
                                    443 ;	main.c: 150: }
      000172 3A 00                  444 	ret
                                    445 ;	main.c: 156: static void startTone(uint8_t timerDivisor)
                                    446 ;	-----------------------------------------
                                    447 ;	 function startTone
                                    448 ;	-----------------------------------------
      000174                        449 _startTone:
                                    450 ;	main.c: 159: PADIER = BUTTON_MASK;
      000174 40 17                  451 	mov	a, #0x40
      000176 8D 00                  452 	mov.io	__padier, a
                                    453 ;	main.c: 160: PAC |= PIEZO_MASK;
      000178 71 0F                  454 	set1.io	__pac, #3
                                    455 ;	main.c: 161: TM2CT = 0;
      00017A 00 17                  456 	mov	a, #0x00
      00017C 9D 00                  457 	mov.io	__tm2ct, a
                                    458 ;	main.c: 162: TM2B = (uint8_t)(timerDivisor - 1u);
      00017E D9 07                  459 	mov	a, _startTone_PARM_1+0
      000180 01 11                  460 	sub	a, #0x01
      000182 89 00                  461 	mov.io	__tm2b, a
                                    462 ;	main.c: 163: TM2S = TM2S_PRESCALE_NONE | TM2S_SCALE_NONE;
      000184 00 17                  463 	mov	a, #0x00
      000186 97 00                  464 	mov.io	__tm2s, a
                                    465 ;	main.c: 164: TM2C = TM2C_CLK_ILRC | TM2C_MODE_PERIOD | TM2C_OUT_PA3;
      000188 48 17                  466 	mov	a, #0x48
      00018A 9C 00                  467 	mov.io	__tm2c, a
                                    468 ;	main.c: 165: }
      00018C 3A 00                  469 	ret
                                    470 ;	main.c: 167: static uint8_t startupChirps(void)
                                    471 ;	-----------------------------------------
                                    472 ;	 function startupChirps
                                    473 ;	-----------------------------------------
      00018E                        474 _startupChirps:
                                    475 ;	main.c: 169: uint16_t offset = 0;
      00018E 9A 09                  476 	clear	_startupChirps_sloc5_1_0+0
      000190 9B 09                  477 	clear	_startupChirps_sloc5_1_0+1
                                    478 ;	main.c: 172: while (step--)
      000192 0A 17                  479 	mov	a, #0x0a
      000194 DC 05                  480 	mov	_startupChirps_sloc6_1_0+0, a
      000196                        481 00109$:
      000196 DC 07                  482 	mov	a, _startupChirps_sloc6_1_0+0
      000198 5C 09                  483 	dec	_startupChirps_sloc6_1_0+0
      00019A 00 12                  484 	ceqsn	a, #0x00
      00019C D0 18                  485 	goto	00138$
      00019E 1B 19                  486 	goto	00111$
      0001A0                        487 00138$:
                                    488 ;	main.c: 174: uint8_t timerDivisor = chirpPattern[offset];
      0001A0 A0 17                  489 	mov	a, #<(_chirpPattern + 0)
      0001A2 1A 06                  490 	add	a, _startupChirps_sloc5_1_0+0
      0001A4 C0 05                  491 	mov	p, a
      0001A6 81 17                  492 	mov	a, #>(_chirpPattern + 0x8000 + 0)
      0001A8 9B 06                  493 	addc	a, _startupChirps_sloc5_1_0+1
      0001AA 94 1D                  494 	call	__gptrget
      0001AC DD 05                  495 	mov	_startupChirps_sloc7_1_0+0, a
                                    496 ;	main.c: 175: uint16_t duration = (uint16_t)chirpPattern[offset + 1u] |
      0001AE DA 07                  497 	mov	a, _startupChirps_sloc5_1_0+0
      0001B0 DE 05                  498 	mov	_startupChirps_sloc8_1_0+0, a
      0001B2 01 10                  499 	add	a, #0x01
      0001B4 A0 10                  500 	add	a, #<(_chirpPattern + 0)
      0001B6 C0 05                  501 	mov	p, a
      0001B8 00 17                  502 	mov	a, #0x00
      0001BA 10 00                  503 	addc	a
      0001BC 81 10                  504 	add	a, #>(_chirpPattern + 0x8000 + 0)
      0001BE 94 1D                  505 	call	__gptrget
      0001C0 DF 05                  506 	mov	_startupChirps_sloc9_1_0+0, a
      0001C2 A0 09                  507 	clear	_startupChirps_sloc9_1_0+1
      0001C4 DE 07                  508 	mov	a, _startupChirps_sloc8_1_0+0
      0001C6 02 10                  509 	add	a, #0x02
      0001C8 A0 10                  510 	add	a, #<(_chirpPattern + 0)
      0001CA C0 05                  511 	mov	p, a
      0001CC 00 17                  512 	mov	a, #0x00
      0001CE 10 00                  513 	addc	a
      0001D0 81 10                  514 	add	a, #>(_chirpPattern + 0x8000 + 0)
      0001D2 94 1D                  515 	call	__gptrget
      0001D4 C0 05                  516 	mov	p, a
      0001D6 00 17                  517 	mov	a, #0x00
      0001D8 5F 07                  518 	or	a, _startupChirps_sloc9_1_0+0
      0001DA E1 05                  519 	mov	_startupChirps_sloc10_1_0+0, a
      0001DC C0 07                  520 	mov	a, p
      0001DE 60 07                  521 	or	a, _startupChirps_sloc9_1_0+1
      0001E0 E2 05                  522 	mov	_startupChirps_sloc10_1_0+1, a
                                    523 ;	main.c: 177: offset += CHIRP_STEP_BYTES;
      0001E2 DA 07                  524 	mov	a, _startupChirps_sloc5_1_0+0
      0001E4 03 10                  525 	add	a, #0x03
      0001E6 C0 05                  526 	mov	p, a
      0001E8 DB 07                  527 	mov	a, _startupChirps_sloc5_1_0+1
      0001EA 10 00                  528 	addc	a
      0001EC DB 05                  529 	mov	_startupChirps_sloc5_1_0+1, a
      0001EE C0 07                  530 	mov	a, p
      0001F0 DA 05                  531 	mov	_startupChirps_sloc5_1_0+0, a
                                    532 ;	main.c: 179: if (timerDivisor)
      0001F2 DD 07                  533 	mov	a, _startupChirps_sloc7_1_0+0
      0001F4 00 12                  534 	ceqsn	a, #0x00
      0001F6 FD 18                  535 	goto	00139$
      0001F8 01 19                  536 	goto	00102$
      0001FA                        537 00139$:
                                    538 ;	main.c: 180: startTone(timerDivisor);
      0001FA DD 07                  539 	mov	a, _startupChirps_sloc7_1_0+0
      0001FC D9 05                  540 	mov	_startTone_PARM_1+0, a
      0001FE BA 1C                  541 	call	_startTone
      000200 02 19                  542 	goto	00103$
      000202                        543 00102$:
                                    544 ;	main.c: 182: piezoInput();
      000202 34 1C                  545 	call	_piezoInput
      000204                        546 00103$:
                                    547 ;	main.c: 184: PADIER = BUTTON_MASK;
      000204 40 17                  548 	mov	a, #0x40
      000206 8D 00                  549 	mov.io	__padier, a
                                    550 ;	main.c: 185: while (duration--)
      000208 E1 07                  551 	mov	a, _startupChirps_sloc10_1_0+0
      00020A E3 05                  552 	mov	_startupChirps_sloc11_1_0+0, a
      00020C E2 07                  553 	mov	a, _startupChirps_sloc10_1_0+1
      00020E E4 05                  554 	mov	_startupChirps_sloc11_1_0+1, a
      000210                        555 00106$:
      000210 E4 07                  556 	mov	a, _startupChirps_sloc11_1_0+1
      000212 C0 05                  557 	mov	p, a
      000214 E3 07                  558 	mov	a, _startupChirps_sloc11_1_0+0
      000216 63 09                  559 	dec	_startupChirps_sloc11_1_0+0
      000218 64 08                  560 	subc	_startupChirps_sloc11_1_0+1
      00021A 40 07                  561 	or	a, p
      00021C 00 12                  562 	ceqsn	a, #0x00
      00021E 11 19                  563 	goto	00140$
      000220 CB 18                  564 	goto	00109$
      000222                        565 00140$:
                                    566 ;	main.c: 187: _delay_ms(1);
      000222 05 17                  567 	mov	a, #0x05
      000224 C3 05                  568 	mov	__delay_loop_16_PARM_1+0, a
      000226 84 09                  569 	clear	__delay_loop_16_PARM_1+1
      000228 20 1C                  570 	call	__delay_loop_16
                                    571 ;	main.c: 188: if (buttonIsPressed())
      00022A B0 00                  572 	mov.io	a, __pa
      00022C C0 05                  573 	mov	p, a
      00022E D0 02                  574 	t1sn	p, #6
      000230 08 19                  575 	goto	00106$
                                    576 ;	main.c: 190: piezoInput();
      000232 34 1C                  577 	call	_piezoInput
                                    578 ;	main.c: 191: return 1;
      000234 01 01                  579 	ret	#0x01
      000236                        580 00111$:
                                    581 ;	main.c: 196: piezoInput();
      000236 34 1C                  582 	call	_piezoInput
                                    583 ;	main.c: 197: return 0;
                                    584 ;	main.c: 198: }
      000238 00 01                  585 	ret	#0x00
                                    586 ;	main.c: 204: static void waitForButtonRelease(void)
                                    587 ;	-----------------------------------------
                                    588 ;	 function waitForButtonRelease
                                    589 ;	-----------------------------------------
      00023A                        590 _waitForButtonRelease:
                                    591 ;	main.c: 206: PADIER = BUTTON_MASK;
      00023A 40 17                  592 	mov	a, #0x40
      00023C 8D 00                  593 	mov.io	__padier, a
                                    594 ;	main.c: 208: while (buttonIsPressed())
      00023E                        595 00101$:
      00023E B0 00                  596 	mov.io	a, __pa
      000240 C0 05                  597 	mov	p, a
      000242 D0 02                  598 	t1sn	p, #6
      000244 27 19                  599 	goto	00103$
                                    600 ;	main.c: 210: T16M = T16M_CLK_DISABLE;
      000246 00 17                  601 	mov	a, #0x00
      000248 86 00                  602 	mov.io	__t16m, a
                                    603 ;	main.c: 214: __endasm;
      00024A 37 00                  604 	stopexe
      00024C 1F 19                  605 	goto	00101$
      00024E                        606 00103$:
                                    607 ;	main.c: 217: PADIER = 0;
      00024E 00 17                  608 	mov	a, #0x00
      000250 8D 00                  609 	mov.io	__padier, a
                                    610 ;	main.c: 218: }
      000252 3A 00                  611 	ret
                                    612 ;	main.c: 220: static void deepSleep(void)
                                    613 ;	-----------------------------------------
                                    614 ;	 function deepSleep
                                    615 ;	-----------------------------------------
      000254                        616 _deepSleep:
                                    617 ;	main.c: 224: turnLedOff();
      000254 90 0E                  618 	set0.io	__pa, #4
                                    619 ;	main.c: 225: piezoInput();
      000256 34 1C                  620 	call	_piezoInput
                                    621 ;	main.c: 226: T16M = T16M_CLK_DISABLE;
      000258 00 17                  622 	mov	a, #0x00
      00025A 86 00                  623 	mov.io	__t16m, a
                                    624 ;	main.c: 233: PADIER = BUTTON_MASK | PIEZO_MASK;
      00025C 48 17                  625 	mov	a, #0x48
      00025E 8D 00                  626 	mov.io	__padier, a
                                    627 ;	main.c: 237: __endasm;
      000260 36 00                  628 	stopsys
                                    629 ;	main.c: 240: buttonPressed = buttonIsPressed();
      000262 B0 00                  630 	mov.io	a, __pa
      000264 80 09                  631 	clear	p
      000266 40 14                  632 	and	a, #0x40
      000268 80 09                  633 	clear	p
      00026A 40 07                  634 	or	a, p
      00026C 01 11                  635 	sub	a, #0x01
      00026E 00 17                  636 	mov	a, #0x00
      000270 1D 00                  637 	slc	a
      000272 01 16                  638 	xor	a, #0x01
                                    639 ;	main.c: 241: PADIER = 0;
      000274 32 00                  640 	push	af
      000276 00 17                  641 	mov	a, #0x00
      000278 8D 00                  642 	mov.io	__padier, a
      00027A 33 00                  643 	pop	af
                                    644 ;	main.c: 244: if (buttonPressed)
      00027C 00 12                  645 	ceqsn	a, #0x00
      00027E 41 19                  646 	goto	00109$
      000280 42 19                  647 	goto	00103$
      000282                        648 00109$:
                                    649 ;	main.c: 245: waitForButtonRelease();
      000282 1D 19                  650 	goto	_waitForButtonRelease
      000284                        651 00103$:
                                    652 ;	main.c: 246: }
      000284 3A 00                  653 	ret
                                    654 ;	main.c: 252: static void setup(void)
                                    655 ;	-----------------------------------------
                                    656 ;	 function setup
                                    657 ;	-----------------------------------------
      000286                        658 _setup:
                                    659 ;	main.c: 255: PA = 0;
      000286 00 17                  660 	mov	a, #0x00
      000288 90 00                  661 	mov.io	__pa, a
                                    662 ;	main.c: 256: PAC = LED_MASK;
      00028A 10 17                  663 	mov	a, #0x10
      00028C 91 00                  664 	mov.io	__pac, a
                                    665 ;	main.c: 257: PAPH = 0;
      00028E 00 17                  666 	mov	a, #0x00
      000290 92 00                  667 	mov.io	__paph, a
                                    668 ;	main.c: 258: PADIER = 0;
      000292 00 17                  669 	mov	a, #0x00
      000294 8D 00                  670 	mov.io	__padier, a
                                    671 ;	main.c: 260: GPCC = 0;
      000296 00 17                  672 	mov	a, #0x00
      000298 9A 00                  673 	mov.io	__gpcc, a
                                    674 ;	main.c: 261: GPCS = 0;
      00029A 00 17                  675 	mov	a, #0x00
      00029C 9E 00                  676 	mov.io	__gpcs, a
                                    677 ;	main.c: 262: TM2C = 0;
      00029E 00 17                  678 	mov	a, #0x00
      0002A0 9C 00                  679 	mov.io	__tm2c, a
                                    680 ;	main.c: 263: T16M = 0;
      0002A2 00 17                  681 	mov	a, #0x00
      0002A4 86 00                  682 	mov.io	__t16m, a
                                    683 ;	main.c: 265: MISC |= MISC_LVR_DISABLE;
      0002A6 5B 0F                  684 	set1.io	__misc, #2
                                    685 ;	main.c: 273: CLKMD_ENABLE_IHRC);
      0002A8 A3 00                  686 	mov.io	a, __clkmd
      0002AA EC 14                  687 	and	a, #0xec
      0002AC 83 00                  688 	mov.io	__clkmd, a
                                    689 ;	main.c: 275: INTEN = 0;
      0002AE 00 17                  690 	mov	a, #0x00
      0002B0 84 00                  691 	mov.io	__inten, a
                                    692 ;	main.c: 276: INTRQ = 0;
      0002B2 00 17                  693 	mov	a, #0x00
      0002B4 85 00                  694 	mov.io	__intrq, a
                                    695 ;	main.c: 277: }
      0002B6 3A 00                  696 	ret
                                    697 ;	main.c: 279: static uint8_t activeAlert(void)
                                    698 ;	-----------------------------------------
                                    699 ;	 function activeAlert
                                    700 ;	-----------------------------------------
      0002B8                        701 _activeAlert:
                                    702 ;	main.c: 281: uint8_t flashCount = 0;
      0002B8 A5 09                  703 	clear	_activeAlert_sloc12_1_0+0
                                    704 ;	main.c: 283: while (1)
      0002BA                        705 00110$:
                                    706 ;	main.c: 285: turnLedOn();
      0002BA 90 0F                  707 	set1.io	__pa, #4
                                    708 ;	main.c: 287: if (activeLedPulseDelay())
      0002BC 3A 1C                  709 	call	_activeLedPulseDelay
      0002BE 00 12                  710 	ceqsn	a, #0x00
      0002C0 62 19                  711 	goto	00134$
      0002C2 64 19                  712 	goto	00102$
      0002C4                        713 00134$:
                                    714 ;	main.c: 289: turnLedOff();
      0002C4 90 0E                  715 	set0.io	__pa, #4
                                    716 ;	main.c: 290: return 1;
      0002C6 01 01                  717 	ret	#0x01
      0002C8                        718 00102$:
                                    719 ;	main.c: 293: turnLedOff();
      0002C8 90 0E                  720 	set0.io	__pa, #4
                                    721 ;	main.c: 295: if (++flashCount >= LED_FLASHES_PER_CHIRP)
      0002CA 25 09                  722 	inc	_activeAlert_sloc12_1_0+0
      0002CC E5 07                  723 	mov	a, _activeAlert_sloc12_1_0+0
      0002CE 05 11                  724 	sub	a, #0x05
      0002D0 20 0C                  725 	t0sn.io	f, c
      0002D2 70 19                  726 	goto	00106$
                                    727 ;	main.c: 297: flashCount = 0;
      0002D4 A5 09                  728 	clear	_activeAlert_sloc12_1_0+0
                                    729 ;	main.c: 299: if (startupChirps())
      0002D6 C7 1C                  730 	call	_startupChirps
      0002D8 00 12                  731 	ceqsn	a, #0x00
      0002DA 6F 19                  732 	goto	00135$
      0002DC 70 19                  733 	goto	00106$
      0002DE                        734 00135$:
                                    735 ;	main.c: 300: return 1;
      0002DE 01 01                  736 	ret	#0x01
      0002E0                        737 00106$:
                                    738 ;	main.c: 307: if (sleepMilliseconds(EVENT_SLEEP_MS, 0))
      0002E0 E8 17                  739 	mov	a, #0xe8
      0002E2 CE 05                  740 	mov	_sleepMilliseconds_PARM_1+0, a
      0002E4 03 17                  741 	mov	a, #0x03
      0002E6 CF 05                  742 	mov	_sleepMilliseconds_PARM_1+1, a
      0002E8 90 09                  743 	clear	_sleepMilliseconds_PARM_2+0
      0002EA 6E 1C                  744 	call	_sleepMilliseconds
      0002EC 00 12                  745 	ceqsn	a, #0x00
      0002EE 79 19                  746 	goto	00136$
      0002F0 5D 19                  747 	goto	00110$
      0002F2                        748 00136$:
                                    749 ;	main.c: 308: return 1;
                                    750 ;	main.c: 310: }
      0002F2 01 01                  751 	ret	#0x01
                                    752 ;	main.c: 312: void main(void)
                                    753 ;	-----------------------------------------
                                    754 ;	 function main
                                    755 ;	-----------------------------------------
      0002F4                        756 _main:
                                    757 ;	main.c: 314: setup();
      0002F4 43 1D                  758 	call	_setup
                                    759 ;	main.c: 316: while (1)
      0002F6                        760 00104$:
                                    761 ;	main.c: 319: if (startupChirps())
      0002F6 C7 1C                  762 	call	_startupChirps
      0002F8 00 12                  763 	ceqsn	a, #0x00
      0002FA 7F 19                  764 	goto	00116$
      0002FC 82 19                  765 	goto	00102$
      0002FE                        766 00116$:
                                    767 ;	main.c: 321: waitForButtonRelease();
      0002FE 1D 1D                  768 	call	_waitForButtonRelease
                                    769 ;	main.c: 322: deepSleep();
      000300 2A 1D                  770 	call	_deepSleep
                                    771 ;	main.c: 323: continue;
      000302 7B 19                  772 	goto	00104$
      000304                        773 00102$:
                                    774 ;	main.c: 326: activeAlert();
      000304 5C 1D                  775 	call	_activeAlert
                                    776 ;	main.c: 327: waitForButtonRelease();
      000306 1D 1D                  777 	call	_waitForButtonRelease
                                    778 ;	main.c: 328: deepSleep();
      000308 2A 1D                  779 	call	_deepSleep
      00030A 7B 19                  780 	goto	00104$
                                    781 ;	main.c: 330: }
      00030C 3A 00                  782 	ret
                                    783 ;	main.c: 336: unsigned char STARTUP_FUNCTION(void)
                                    784 ;	-----------------------------------------
                                    785 ;	 function _sdcc_external_startup
                                    786 ;	-----------------------------------------
      00030E                        787 __sdcc_external_startup:
                                    788 ;	main.c: 338: AUTO_INIT_SYSCLOCK();
      00030E F4 17                  789 	mov	a, #0xf4
      000310 83 00                  790 	mov.io	__clkmd, a
                                    791 ;	main.c: 339: AUTO_CALIBRATE_SYSCLOCK(TARGET_VDD_MV);
      000312 52 14                  792 	and	a, #'R'                       
      000314 43 14                  793 	and	a, #'C'                       
      000316 02 14                  794 	and	a, #(2)            
      000318 20 14                  795 	and	a, #((52000))     
      00031A CB 14                  796 	and	a, #((52000)>>8)  
      00031C 00 14                  797 	and	a, #((52000)>>16) 
      00031E 00 14                  798 	and	a, #((52000)>>24) 
      000320 F0 14                  799 	and	a, #((2800))     
      000322 0A 14                  800 	and	a, #((2800)>>8)  
      000324 1F 14                  801 	and	a, #(0x1f)             
                                    802 ;	main.c: 341: return 0;
                                    803 ;	main.c: 342: }
      000326 00 01                  804 	ret	#0x00
                                    805 	.area CODE
                                    806 	.area CONST
      000340                        807 _chirpPattern:
      000340 1A 01                  808 	ret #0x1a	; 26
      000342 28 01                  809 	ret #0x28	; 40
      000344 00 01                  810 	ret #0x00	; 0
      000346 00 01                  811 	ret #0x00	; 0
      000348 0F 01                  812 	ret #0x0f	; 15
      00034A 00 01                  813 	ret #0x00	; 0
      00034C 06 01                  814 	ret #0x06	; 6
      00034E 19 01                  815 	ret #0x19	; 25
      000350 00 01                  816 	ret #0x00	; 0
      000352 00 01                  817 	ret #0x00	; 0
      000354 0F 01                  818 	ret #0x0f	; 15
      000356 00 01                  819 	ret #0x00	; 0
      000358 1A 01                  820 	ret #0x1a	; 26
      00035A 14 01                  821 	ret #0x14	; 20
      00035C 00 01                  822 	ret #0x00	; 0
      00035E 00 01                  823 	ret #0x00	; 0
      000360 0F 01                  824 	ret #0x0f	; 15
      000362 00 01                  825 	ret #0x00	; 0
      000364 06 01                  826 	ret #0x06	; 6
      000366 19 01                  827 	ret #0x19	; 25
      000368 00 01                  828 	ret #0x00	; 0
      00036A 00 01                  829 	ret #0x00	; 0
      00036C 0F 01                  830 	ret #0x0f	; 15
      00036E 00 01                  831 	ret #0x00	; 0
      000370 1A 01                  832 	ret #0x1a	; 26
      000372 28 01                  833 	ret #0x28	; 40
      000374 00 01                  834 	ret #0x00	; 0
      000376 00 01                  835 	ret #0x00	; 0
      000378 19 01                  836 	ret #0x19	; 25
      00037A 00 01                  837 	ret #0x00	; 0
                                    838 	.area CABS (ABS)
