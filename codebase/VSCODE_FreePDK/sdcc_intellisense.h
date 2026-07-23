#ifndef SDCC_INTELLISENSE_H
#define SDCC_INTELLISENSE_H

#if defined(__INTELLISENSE__)
#define __sfr volatile
#define __at(x)
#define __sbit volatile unsigned char
#define __bit unsigned char
#define __idata
#define __xdata
#define __code
#define __reentrant
#define __interrupt(x)
#define __using(x)
#define __asm
#define __endasm
#endif

#endif
