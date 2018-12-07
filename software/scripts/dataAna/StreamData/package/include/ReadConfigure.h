#ifndef ReadConfigure_H
#define ReadConfigure_H

#include <iostream>
#include <fstream>
#include <vector>
#include <stdint.h>
#include <string.h>
#include "comm.h"

class ReadConfigure {
    
    private:
        std::string _parameter_changed;
        int _steps;
        std::vector<int> _frames_atStep;
        std::vector<int> _parameter_values;


    public:
        ReadConfigure();
        ReadConfigure(std::string File_configure); 
        ~ReadConfigure();
        std::string getParameterChanged();
        int getSteps();
        std::vector<int> getFramesatStep();
        std::vector<int> getParameterValues();

};


#endif
