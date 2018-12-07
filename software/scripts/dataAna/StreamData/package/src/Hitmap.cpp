#include "../include/Hitmap.h"
#include <stdio.h>
#include <iostream>
#include <stdlib.h>
#include <unistd.h>
#include <sstream>
Hitmap::Hitmap()
{
}

Hitmap::~Hitmap()
{
}

void Hitmap::add(uint16_t data_16)
{
    int Row,Col,Muli_flag,DV_flag;
    int ind=0;
    Row = data_16 & 0x007f;
    Col = data_16 & 0x0f80; Col>>=7;
    Muli_flag = (data_16 & 0x1000)>0;
    DV_flag=(data_16 & 0x2000)>0;
    //Muli_flag = data_16 & 0x1000; Muli_flag>>=12;
    //DV_flag=data_16 & 0x2000; DV_flag>>=13;

    if (DV_flag>0){
        //std::cout<< "row "<<Row <<" col "<<Col<<std::endl;
        ind=Row*32+Col;
    //_hitmap[Row][Col]+=1;
    _hitmap[ind]+=1;

    }
}

int *Hitmap::getHitmap()
{
    return _hitmap;


}
