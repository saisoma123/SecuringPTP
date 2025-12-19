#pragma once

#include "../bmca_ta.h" 

#define TA_UUID TA_BMCA_UUID

#define TA_FLAGS (TA_FLAG_USER_MODE | TA_FLAG_EXEC_DDR |            \
                  TA_FLAG_SINGLE_INSTANCE | TA_FLAG_MULTI_SESSION | \
                  TA_FLAG_INSTANCE_KEEP_ALIVE)
#define TA_STACK_SIZE (2 * 1024)
#define TA_DATA_SIZE (32 * 1024)
