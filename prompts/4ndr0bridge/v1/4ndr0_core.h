#ifndef _4NDR0_CORE_H

#define _4NDR0_CORE_H

#include

#include

typedef struct {

uint32_t seed;

uint32_t iteration;

uint8_t complexity;

} LogicCore;

// Function Prototypes

LogicCore* logic_core_init(uint32_t seed, uint8_t complexity);

void logic_core_transform(LogicCore ctx, uint8_t data, size_t len);

void logic_core_destroy(LogicCore* ctx);

#endif
