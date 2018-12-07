#include "../include/ReadConfigure.h"
#include "../include/comm.h"

ReadConfigure::ReadConfigure()
{
}

ReadConfigure::ReadConfigure(std::string File_configure)
{

    std::string parameter_c;
    std::string parameter_ct;
    std::string a="Changing";
    std::string b="Taking";
    int a1=1;
    int frames_perstep;
    std::vector<int> parameter_v;
    std::vector<int> pv_pt;
    std::string parameter_vt;
    std::string p1,p2,p3;
    int valueLine=0;
    std::ifstream in(File_configure.c_str());
    while(!in.eof()){
        in >> parameter_ct;
        if (parameter_ct==a){
            in >> _parameter_changed;
            in >> _steps;
        } 
        if (parameter_ct==b){
            in >> frames_perstep;
            in >> p1;
            in >> p2;
            in >> p3;
            valueLine=1; 
        }
        if (valueLine==1){
            while (1){
                in >> parameter_vt;
                if (parameter_vt == "end"){ break;}
                pv_pt=split_string_h(parameter_vt);
                if (pv_pt.size()==2){
                   if (pv_pt[0]>0){_parameter_values.push_back(pv_pt[0]);_frames_atStep.push_back(pv_pt[1]);}}
                if (pv_pt.size()==1){
                   if (pv_pt[0]>0){_parameter_values.push_back(pv_pt[0]);_frames_atStep.push_back(frames_perstep*a1);a1++;}}
            }
        }
        valueLine=0; 


    } 
}

ReadConfigure::~ReadConfigure()
{
}


std::string ReadConfigure::getParameterChanged()
{
    return _parameter_changed;
}

int ReadConfigure::getSteps()
{
    return _steps;
}

std::vector<int> ReadConfigure::getFramesatStep()
{
    return _frames_atStep;
}
std::vector<int> ReadConfigure::getParameterValues()
{
    return _parameter_values;
}
