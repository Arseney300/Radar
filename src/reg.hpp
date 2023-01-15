/// @file reg.hpp
/// @brief main registers of radar

#ifndef REG_HPP
#define REG_HPP
/* To communicate with the radar, the display unit sends registers with the values of the range, the filters, the focus... The first number of the register is its number, the second is always C1 - it works like a checksum - and then commences the parametrs' setting */

// Checksum
#define RAD_CHECKSUM 0xC1

// Turn on/off 0
#define RAD_TURN_ON_OFF_0 0x00

// Turn on/off 1
#define RAD_TURN_ON_OFF_1 0x01

#define RAD_KEEP_ALIVE 0xA0

// zoom level
#define RAD_ZOOMLEVEL 0x03

// zoom level set as 4 byte value
// TODO: write enum


// filters and preprocessing
#define RAD_FILTER 0x06
// TODO: write numbers for distance

// interference rejection
#define RAD_INTER_REJ 0x08

// target boost
#define RAD_TARGET_BOOST 0x0A

// local interference filter
#define RAD_LOC_INTER_FILTER 0x0E

// scan speed
#define RAD_SCAN_SPEED 0x0F

// operation maintain
#define RAD_OPER_MAINTAIN 0xA0


#endif
