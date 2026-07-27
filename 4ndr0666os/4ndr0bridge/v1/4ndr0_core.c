#include "4ndr0_core.h"

#include

#include

#include

// SHA-256 Compact Implementation

typedef struct {

uint8_t data[64];

uint32_t datalen;

unsigned long long bitlen;

uint32_t state[8];

} SHA256_CTX;

#define ROTRIGHT(a,b) (((a) >> (b)) | ((a) > 3))

#define SIG1(x) (ROTRIGHT(x,17) ^ ROTRIGHT(x,19) ^ ((x) >> 10))

static const uint32_t k[64] = {

0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,

0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,

0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,

0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,

0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,

0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,

0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,

0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2

};

void sha256_transform(SHA256_CTX *ctx, const uint8_t data[]) {

uint32_t a, b, c, d, e, f, g, h, i, j, t1, t2, m[64];

for (i = 0, j = 0; i state[0]; b = ctx->state[1]; c = ctx->state[2]; d = ctx->state[3];

e = ctx->state[4]; f = ctx->state[5]; g = ctx->state[6]; h = ctx->state[7];

for (i = 0; i state[0] += a; ctx->state[1] += b; ctx->state[2] += c; ctx->state[3] += d;

ctx->state[4] += e; ctx->state[5] += f; ctx->state[6] += g; ctx->state[7] += h;

}

void sha256_init(SHA256_CTX *ctx) {

ctx->datalen = 0; ctx->bitlen = 0;

ctx->state[0] = 0x6a09e667; ctx->state[1] = 0xbb67ae85; ctx->state[2] = 0x3c6ef372; ctx->state[3] = 0xa54ff53a;

ctx->state[4] = 0x510e527f; ctx->state[5] = 0x9b05688c; ctx->state[6] = 0x1f83d9ab; ctx->state[7] = 0x5be0cd19;

}

void sha256_update(SHA256_CTX *ctx, const uint8_t data[], size_t len) {

for (size_t i = 0; i data[ctx->datalen] = data[i];

ctx->datalen++;

if (ctx->datalen == 64) {

sha256_transform(ctx, ctx->data);

ctx->bitlen += 512;

ctx->datalen = 0;

}

}

}

void sha256_final(SHA256_CTX *ctx, uint8_t hash[]) {

uint32_t i = ctx->datalen;

if (ctx->datalen data[i++] = 0x80;

while (i data[i++] = 0x00;

} else {

ctx->data[i++] = 0x80;

while (i data[i++] = 0x00;

sha256_transform(ctx, ctx->data);

memset(ctx->data, 0, 56);

}

ctx->bitlen += ctx->datalen * 8;

for (int j = 0; j data[63-j] = (uint8_t)(ctx->bitlen >> (j*8));

sha256_transform(ctx, ctx->data);

for (i = 0; i state[j] >> (24 - i * 8)) & 0xFF;

}

}

// Logic Core Implementation

LogicCore* logic_core_init(uint32_t seed, uint8_t complexity) {

LogicCore ctx = (LogicCore)malloc(sizeof(LogicCore));

if (!ctx) return NULL;

ctx->seed = seed;

ctx->iteration = 0;

ctx->complexity = complexity;

return ctx;

}

void logic_core_transform(LogicCore ctx, uint8_t data, size_t len) {

uint8_t key[32];

char input_str[64];

sprintf(input_str, "%u-%u", ctx->seed, ctx->iteration);

SHA256_CTX sha_ctx;

sha256_init(&sha_ctx);

sha256_update(&sha_ctx, (uint8_t*)input_str, strlen(input_str));

sha256_final(&sha_ctx, key);

for (size_t i = 0; i iteration += 1;

ctx->seed = (uint32_t)((ctx->seed + 0x9E3779B9) & 0xFFFFFFFF);

}

void logic_core_destroy(LogicCore* ctx) {

if (ctx) free(ctx);

}

int main(int argc, char argv) {

if (argc < 3) return 0;

uint32_t seed = (uint32_t)strtoul(argv[1], NULL, 0);

LogicCore* core = logic_core_init(seed, 1);

uint8_t data = (uint8_t)strdup(argv[2]);

size_t len = strlen(argv[2]);

logic_core_transform(core, data, len);

for (size_t i = 0; i < len; i++) printf("%02x", data[i]);

printf("\n");

logic_core_destroy(core);

return 0;

}



