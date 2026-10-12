
DEVICE = PMS150C
# Run the CPU directly from the calibrated ILRC (no system-clock divider).
F_CPU = 52000
TARGET_VDD_MV = 2800
TARGET_VDD = 2.8

# ---------------------------------------------------------------------

OUTPUT_NAME = slowclocksleep_$(DEVICE)

# PMS150C uses the pdk13 backend
ARCH = pdk13

ROOT_DIR = .
BUILD_DIR = .build
OUTPUT_DIR = .output

OUTPUT = $(OUTPUT_DIR)/$(OUTPUT_NAME)

SOURCES = main.c
OBJECTS = $(patsubst %.c,$(BUILD_DIR)/%.rel,$(SOURCES))

# http://sdcc.sourceforge.net/doc/sdccman.pdf
COMPILE = sdcc -m$(ARCH) -c --std-sdcc11 --opt-code-size -D$(DEVICE) -DF_CPU=$(F_CPU) -DTARGET_VDD_MV=$(TARGET_VDD_MV) -I. -I$(ROOT_DIR)/include
LINK = sdcc -m$(ARCH)
EASYPDKPROG = /mnt/c/EASYPDKPROG/easypdkprog.exe
PROGRAM_FREQUENCY = 40000
PROGRAM_PHASE = 10

# symbolic targets:
all: size

print-%: ; @echo $* = $($*)

$(BUILD_DIR)/%.rel: %.c
	@mkdir -p $(dir $@)
	$(COMPILE) -o $@ $<

$(BUILD_DIR)/main.rel: chirp_pattern.h

$(OUTPUT).ihx: $(OBJECTS)
	@mkdir -p $(dir $(OUTPUT))
	$(LINK) --out-fmt-ihx -o $(OUTPUT).ihx $(OBJECTS)

$(OUTPUT).bin: $(OUTPUT).ihx
	makebin -p $(OUTPUT).ihx $(OUTPUT).bin

build: $(OUTPUT).bin

size: build
	@echo '---------- Segments ----------'
	@egrep '(ABS,CON)|(REL,CON)' $(OUTPUT).map | gawk --non-decimal-data '{dec = sprintf("%d","0x" $$2); print dec " " $$0}' | /usr/bin/sort -n -k1 | cut -f2- -d' '
	@echo '------------------------------'
	@stat -L --printf "Size of $(OUTPUT_NAME).bin: %s bytes\n" $(OUTPUT).bin

program: size
	$(EASYPDKPROG) --frequency $(PROGRAM_FREQUENCY) --phase $(PROGRAM_PHASE) -n $(DEVICE) write $(OUTPUT).ihx

run:
	$(EASYPDKPROG) -r $(TARGET_VDD) start

clean:
	rm -r -f $(BUILD_DIR) $(OUTPUT_DIR)
