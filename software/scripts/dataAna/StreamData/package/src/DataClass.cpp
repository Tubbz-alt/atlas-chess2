#include <iostream>
#include <vector>
#include "../include/DataClass.h"
#include "../include/comm.h"
#include <bitset>

DataClass::DataClass()
{
}

DataClass::~DataClass()
{
}
void DataClass::setFrame(struct Frame *frame)
{

    uint16_t data_t;
    int m_d=0;
    for (int j=0;j<(frame->payload_size/2);j++){ 
        data_t=frame->payload[j];
        if (1){
        //if (data_t>0){
            m_d=j%4;
            if (m_d!=3){add_data(data_t,m_d);}
        }

    }    
   
}
 
void DataClass::add_data(uint16_t data_t,int matrix_t)
{
    int Row,Col,Muli_flag,DV_flag;
    std::vector<int> p;
    Row = data_t & 0x007f; 
    Col = data_t & 0x0f80; Col>>=7;
    Muli_flag = (data_t & 0x1000)>0;
    DV_flag=(data_t & 0x2000)>0;
   
    if (1){
    //if (DV_flag>0){
        p.push_back(Row);
        p.push_back(Col);
        switch ( matrix_t){
            case 0: _Matrix0.push_back(p);_Matrix0_dv.push_back(DV_flag);_Matrix0_mv.push_back(Muli_flag);break;
            case 1: _Matrix1.push_back(p);_Matrix1_dv.push_back(DV_flag);_Matrix1_mv.push_back(Muli_flag);break;
            case 2: _Matrix2.push_back(p);_Matrix2_dv.push_back(DV_flag);_Matrix2_mv.push_back(Muli_flag);break;
            default: break;
        }

    }
}
std::vector<int> DataClass::get_dv(int matrix)
{
    if (matrix==0){
        return _Matrix0_dv;
    }
    if (matrix==1){
        return _Matrix1_dv;
    }
    if (matrix==2){
        return _Matrix2_dv;
    }

}
std::vector<int> DataClass::get_mv(int matrix)
{

    if (matrix==0){
        return _Matrix0_mv;
    }
    if (matrix==1){
        return _Matrix1_mv;
    }
    if (matrix==2){
        return _Matrix2_mv;
    }
}
std::vector<std::vector <int> > DataClass::get_Hitmap(int matrix)
{
    if (matrix==0){
        return _Matrix0;
    }
    if (matrix==1){
        return _Matrix1;
    }
    if (matrix==2){
        return _Matrix2;
    }
    
}

void DataClass::Init()
{
    _Matrix0.clear();
    _Matrix1.clear();
    _Matrix2.clear();
    _Matrix0_dv.clear();
    _Matrix1_dv.clear(); 
    _Matrix2_dv.clear();
    _Matrix0_mv.clear();
    _Matrix1_mv.clear();
    _Matrix2_mv.clear();
}
