#include "include/DataClass.h"
#include "include/Hitmap.h"
#include "include/ReadConfigure.h"
#include "include/comm.h"
#include <vector>
#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string>
#include <sstream>

#include <TROOT.h>
#include <TFile.h>
#include <TTree.h>
#include <TH2D.h>
#include <TH1D.h>
#include <TH3D.h>


<<<<<<< HEAD
int file_number(std::string name);
std::string file_name(std::string name);
=======
int file_number(char* name);
>>>>>>> c++ package to deal with the stream readout result
int main(int argc, char* argv[]){

    std::string configure_f;
    std::string data_f;
<<<<<<< HEAD
    std::string save_name;
    FILE *file;
    if (argc==2){
        std::string txt=".txt";
        std::string save_t=argv[1]; 
        save_name=file_name(save_t);
        configure_f=save_name+txt;
        std::cout<<"--- the configure file"<<configure_f<<std::endl;
    }
    int num=0;
    num=file_number(save_name);
=======
    FILE *file;
    if (argc==2){
        std::string txt=".txt";
        configure_f=argv[1]+txt;
        std::cout<<"--- the configure file"<<configure_f<<std::endl;
    }
    int num=0;
    num=file_number(argv[1]);
>>>>>>> c++ package to deal with the stream readout result
    ReadConfigure::ReadConfigure *conf=new ReadConfigure::ReadConfigure(configure_f);

    int Steps;
    std::vector<int> frames, parameters;
    std::string paramter_name;
   
    Steps=conf->getSteps();
    frames=conf->getFramesatStep();
    parameters=conf->getParameterValues();
    paramter_name=conf->getParameterChanged();
   
    //for (int y=0;y<frames.size();y++){std::cout<< frames[y]<<std::endl;} 
    //for (int y=0;y<parameters.size();y++){std::cout<< parameters[y]<<std::endl;} 
    struct Frame frame;
   // struct Frame_Header frame_Header;
   // struct Atlas_chess2_header ach;
   // struct Payload payload;
<<<<<<< HEAD
    char file_name_s[1000];
=======
    char file_name[200];
>>>>>>> c++ package to deal with the stream readout result
    
   
    TH2D* M_0_step[Steps];  
    TH2D* M_1_step[Steps];  
    TH2D* M_2_step[Steps];  
   
    char m0_n[200],m1_n[200],m2_n[200];
    for(int m=0;m<Steps;m++){ 
    sprintf(m0_n,"Matrix0_2D_HitMap_with_TH_at_%d",parameters[m]);
    M_0_step[m]= new TH2D(m0_n,";Col;Row",32,0,32,128,0,128);
    sprintf(m1_n,"Matrix1_2D_HitMap_with_TH_at_%d",parameters[m]);
    M_1_step[m]= new TH2D(m1_n,";Col;Row",32,0,32,128,0,128);
    sprintf(m2_n,"Matrix2_2D_HitMap_with_TH_at_%d",parameters[m]);
    M_2_step[m]= new TH2D(m2_n,";Col;Row",32,0,32,128,0,128);
    }
    Hitmap::Hitmap *h0 =  new Hitmap::Hitmap();
    Hitmap::Hitmap *h1 =  new Hitmap::Hitmap();
    Hitmap::Hitmap *h2 =  new Hitmap::Hitmap();
    
    TH2D *M_0_all= new TH2D("Matrix0_2D_HitMap",";Col;Row",32,0,32,128,0,128);
    TH2D *M_1_all= new TH2D("Matrix1_2D_HitMap",";Col;Row",32,0,32,128,0,128);
    TH2D *M_2_all= new TH2D("Matrix2_2D_HitMap",";Col;Row",32,0,32,128,0,128);
  
    char h_3d[100];
    sprintf(h_3d,";Col;Row;TH");
    int p_end=parameters[Steps-1];
    TH3D *M_0_3d= new TH3D("Matrix0_3D_HitMap",h_3d,32,0,32,128,0,128,Steps,parameters[0],p_end);
    TH3D *M_1_3d= new TH3D("Matrix1_3D_HitMap",h_3d,32,0,32,128,0,128,Steps,parameters[0],p_end);
    TH3D *M_2_3d= new TH3D("Matrix2_3D_HitMap",h_3d,32,0,32,128,0,128,Steps,parameters[0],p_end);

    TH1D *m0_eff = new TH1D("Matrix0_3D_efficiency",";TH;Counts",Steps,parameters[0],p_end);
    TH1D *m1_eff = new TH1D("Matrix1_3D_efficiency",";TH;Counts",Steps,parameters[0],p_end);
    TH1D *m2_eff = new TH1D("Matrix2_3D_efficiency",";TH;Counts",Steps,parameters[0],p_end);

    std::cout<<"steps : "<<Steps<<" from "<<parameters[0]<<" to "<<p_end<<std::endl;
    int frame_number=0;
    int hist=0;
    //DataClass::DataClass *data_t = new DataClass::DataClass(&frame);
    DataClass::DataClass *data_t = new DataClass::DataClass();
    for (int file_n=1; file_n<num+1 ;file_n++){
        
<<<<<<< HEAD
        sprintf(file_name_s,"%s.dat.%d",save_name.c_str(),file_n);
        std::cout<<"reading :"<<file_name_s<< std::endl;
        file = fopen(file_name_s,"rb");
=======
        sprintf(file_name,"%s.dat.%d",argv[1],file_n);
        std::cout<<"reading :"<<file_name<< std::endl;
        file = fopen(file_name,"rb");
>>>>>>> c++ package to deal with the stream readout result
        
        while(get_next_frame(file,&frame)==0){
            if (frame.payload_size!=0){
                //std::cout<< "frame -> payload_size: "<< frame.payload_size <<std::endl;
                frame_number++;//std::cout<<"frame number : "<<frame_number<<std::endl;
                data_t->Init();
                //std::cout<<"Init "<<(data_t->get_Hitmap(0)).size()<<std::endl; 
                data_t->setFrame(&frame);
                //std::cout<<"setFrame "<<(data_t->get_Hitmap(0)).size()<<std::endl; 
                if (0){ //ignore M0
                //if ((data_t->get_Hitmap(0)).size()>0){ 
                    for (int h_0=0;h_0<(data_t->get_Hitmap(0)).size();h_0++){
                         m0_eff->Fill(parameters[hist]);
                         M_0_all->Fill((data_t->get_Hitmap(0))[h_0][1],(data_t->get_Hitmap(0))[h_0][0]);
                         M_0_step[hist]->Fill((data_t->get_Hitmap(0))[h_0][1],(data_t->get_Hitmap(0))[h_0][0]);
                         M_0_3d->Fill((data_t->get_Hitmap(0))[h_0][1],(data_t->get_Hitmap(0))[h_0][0],parameters[hist]);
                    }     
                }
                if ((data_t->get_Hitmap(1)).size()>0){ 
                    for (int h_1=0;h_1<(data_t->get_Hitmap(1)).size();h_1++){
                         m1_eff->Fill(parameters[hist]);
                   //      std::cout<<"M1: "<<(data_t->get_Hitmap(1))[h_1][1]<< " "<<(data_t->get_Hitmap(1))[h_1][0]<<std::endl;
                         M_1_all->Fill((data_t->get_Hitmap(1))[h_1][1],(data_t->get_Hitmap(1))[h_1][0]);
                         M_1_step[hist]->Fill((data_t->get_Hitmap(1))[h_1][1],(data_t->get_Hitmap(1))[h_1][0]);
                         M_1_3d->Fill((data_t->get_Hitmap(1))[h_1][1],(data_t->get_Hitmap(1))[h_1][0],parameters[hist]);
                    }    
                }
                if (0){ // ingnore M2
                //if ((data_t->get_Hitmap(2)).size()>0){ 
                    for (int h_2=0;h_2<(data_t->get_Hitmap(2)).size();h_2++){
                         m2_eff->Fill(parameters[hist]);
                         std::cout<<"M2: "<<(data_t->get_Hitmap(2))[h_2][1]<< " "<<(data_t->get_Hitmap(2))[h_2][0]<<std::endl;
                         M_2_all->Fill((data_t->get_Hitmap(2))[h_2][1],(data_t->get_Hitmap(2))[h_2][0]);
                         M_2_step[hist]->Fill((data_t->get_Hitmap(2))[h_2][1],(data_t->get_Hitmap(2))[h_2][0]);
                         M_2_3d->Fill((data_t->get_Hitmap(2))[h_2][1],(data_t->get_Hitmap(2))[h_2][0],parameters[hist]);
                    }   
                }
                if (frame_number == frames[hist]){
                    std::cout<< frames[hist] << std::endl;
                    hist+=1;
              
                }

            }
            delete_frame(&frame);
          //  std::cout<< "frame size is 0"<<std::endl;

        }
        std::cout<< "hists number in total :"<< hist <<std::endl;
        std::cout<< "frame number in total :"<<frame_number << std::endl;
        //delete_frame(&frame);
    }
    //fclose(stream);
<<<<<<< HEAD
    char save_name_root[100];
    sprintf(save_name_root,"%s_cpackage.root",save_name.c_str());
    TFile *file_r=TFile::Open(save_name_root,"RECREATE");   
=======
    char save_name[100];
    sprintf(save_name,"%s_cpackage.root",argv[1])
    TFile *file_r=TFile::Open(save_name,"RECREATE");   
>>>>>>> c++ package to deal with the stream readout result
    for (int f=0;f<hist;f++){
    M_0_step[f]->Write();
    M_1_step[f]->Write();
    M_2_step[f]->Write();
    }
    M_0_3d->Write();
    M_1_3d->Write();
    M_2_3d->Write();
    M_0_all->Write();
    M_1_all->Write();
    M_2_all->Write();
    m0_eff->Write();
    m1_eff->Write();
    m2_eff->Write();
    file_r->Close();
    std::cout<<"end"<<std::endl;
    return 1;
    
}
<<<<<<< HEAD
std::string file_name(std::string name){
   size_t pos=name.find(".txt");
   std::string save_name=name.substr(0,pos);
   return save_name; 

}
int file_number(std::string name){
    char name_temp[1000];
    int number = 0;
    while (true){
	number+=1;
        sprintf(name_temp,"%s.dat.%d",name.c_str(),number);
=======
int file_number(char* name){
    char name_temp[200];
    int number = 0;
    while (true){
	number+=1;
        sprintf(name_temp,"%s.dat.%d",name,number);
>>>>>>> c++ package to deal with the stream readout result
        if ((access(name_temp,F_OK))!= -1){
          //  std::cout<<((access(name_temp,F_OK))!= -1)<<std::endl;
        }
        else{break;}
    }
    return number-1;
}
