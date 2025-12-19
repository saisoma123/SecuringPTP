#ifndef BMCA_TA_H
#define BMCA_TA_H

#include <stdint.h>


#define TA_BMCA_UUID \
    {0x12345679, 0x9abc, 0x4def, {0x81, 0x23, 0x45, 0x67, 0x89, 0xab, 0xcd, 0xef}}

#define TA_BMCA_CMD_DECIDE 0x00000001

#define TA_BMCA_CMD_SET_DEFAULT_DS 0x00000002

#define TA_BMCA_CMD_PTP_FSM         0x00000004

#define TA_BMCA_CMD_PTP_SLAVE_FSM   0x00000005

#define CMD_IMPORT_KEY          0x0100
#define CMD_MAC_COMPUTE         0x0101
#define CMD_MAC_VERIFY          0x0102
#define CMD_DELETE_KEY          0x0103


struct BmcaClockQuality
{
    uint8_t clockClass;
    uint8_t clockAccuracy;
    uint16_t offsetScaledLogVariance;
} __attribute__((packed));

struct BmcaPortIdentity
{
    uint8_t clockIdentity[8];
    uint16_t portNumber;
} __attribute__((packed));

struct BmcaDataset
{
    uint8_t identity[8];
    uint8_t priority1;
    struct BmcaClockQuality quality;
    uint8_t priority2;
    uint16_t stepsRemoved;
    struct BmcaPortIdentity sender;
    struct BmcaPortIdentity receiver;
} __attribute__((packed));

struct BmcaDefaultDS
{
    uint8_t priority1;
    uint8_t priority2;
    struct BmcaClockQuality quality;
    uint8_t identity[8];             
} __attribute__((packed));

struct BmcaInput
{
    struct BmcaDataset clock_best;
    struct BmcaDataset port_best;

    uint8_t has_clock_best;
    uint8_t has_port_best;

    uint8_t current_port_state;      
    uint8_t bmca_mode;               
    uint8_t clock_class;            
    uint8_t clock_best_is_this_port; 

    uint8_t comparator_type;
} __attribute__((packed));

struct BmcaOutput
{
    uint8_t decided_state; 
} __attribute__((packed));


struct BmcaFsmInput
{
    uint8_t state;  
    uint8_t event;  
    int32_t mdiff;  
} __attribute__((packed));

struct BmcaFsmOutput
{
    uint8_t next_state; 
} __attribute__((packed));

#endif 
