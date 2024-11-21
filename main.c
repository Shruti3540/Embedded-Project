#include "project.h" // Include the PSoC5 project header
#include "stdio.h"
CY_ISR(my_isr){
    
    Pin_1_Write(1);
    //UART_WriteTxData(UART_ReadRxData());
    uint8_t var;
    var = UART_GetChar();
    UART_PutChar(var);
    isr_1_ClearPending();
}
int main(void)
{
    UART_Start(); 
    CyGlobalIntEnable;
    isr_1_StartEx(my_isr);
    
    UART_ClearRxBuffer();
    UART_ClearTxBuffer();
    
    while(1){}
}