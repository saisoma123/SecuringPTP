#pragma once
#include <stdint.h>

#define TA_TIMEGUARD_UUID \
	{ 0x7f3b8d40, 0x6c6a, 0x4f2b, \
	  { 0x91, 0x4c, 0x39, 0x38, 0x9d, 0x12, 0x44, 0xa1 } }

enum {
	TG_CMD_REGISTER   = 0x0001,
	TG_CMD_GET_TRUST  = 0x0002,  
	TG_CMD_GET_SECURE_TIME = 0x0003,  
	TG_CMD_WATCHDOG_ERROR  = 0x0004,
	TG_CMD_SET_TIME  = 0x0005,
  TG_CMD_PASSIVE_MRU     =       0x0006,
  TG_CMD_PASSIVE_RANDOM   =     0x0007,
  TG_CMD_PASSIVE_FREQ      =    0x0008,
  TG_CMD_PASSIVE_SCHEDTRACE =   0x0009,

};

struct tg_register_in {
	uint8_t device_secret[32];  
};

struct tg_register_out {
	uint32_t proxy_hi;          
	uint32_t proxy_lo;           
};

struct tg_trust_out {
	uint32_t trust_ok;           
};

struct tg_time_out {
	uint64_t seconds;            
	uint32_t nanoseconds;        
};

struct tg_set_time_in {
    uint64_t phc_seconds;
    uint32_t phc_nanoseconds;
};

struct tg_watchdog_error_in {
	int64_t err_ns;   
};

struct tg_watchdog_error_out {
    int64_t seconds;      
    int32_t nanoseconds;  
};

struct tg_passive_policy_in {
    int64_t phc_ns;  
    int32_t core_id;  
};

struct tg_passive_policy_out {
    int64_t base_diff_ns;  
};