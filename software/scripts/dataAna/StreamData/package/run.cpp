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


int file_number(std::string name);
std::string file_name(std::string name);
int main(int argc, char* argv[]){

    std::string configure_f;
    std::string data_f;
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
    ReadConfigure::ReadConfigure *conf=new ReadConfigure::ReadConfigure(configure_f);

    int Steps;
    std::vector<int> frames, parameters;
    std::string paramter_name;
   
    Steps=conf->getSteps();
    frames=conf->getFramesatStep();
    parameters=conf->getParameterValues();
    paramter_name=conf->getParameterChanged();
   
    struct Frame frame;
    char file_name_s[1000];
    
   
 //   TH2D* M_0_step[Steps];  
 //   TH2D* M_1_step[Steps];  
 //   TH2D* M_2_step[Steps];  
   
 //   char m0_n[200],m1_n[200],m2_n[200];
 //   for(int m=0;m<Steps;m++){ 
 //   sprintf(m0_n,"Matrix0_2D_HitMap_with_TH_at_%d",parameters[m]);
 //   M_0_step[m]= new TH2D(m0_n,";Col;Row",32,0,32,128,0,128);
 //   sprintf(m1_n,"Matrix1_2D_HitMap_with_TH_at_%d",parameters[m]);
 //   M_1_step[m]= new TH2D(m1_n,";Col;Row",32,0,32,128,0,128);
 //   sprintf(m2_n,"Matrix2_2D_HitMap_with_TH_at_%d",parameters[m]);
 //   M_2_step[m]= new TH2D(m2_n,";Col;Row",32,0,32,128,0,128);
 //   }
 //   Hitmap::Hitmap *h0 =  new Hitmap::Hitmap();
 //   Hitmap::Hitmap *h1 =  new Hitmap::Hitmap();
 //   Hitmap::Hitmap *h2 =  new Hitmap::Hitmap();
 //   
 //   TH2D *M_0_all= new TH2D("Matrix0_2D_HitMap",";Col;Row",32,0,32,128,0,128);
 //   TH2D *M_1_all= new TH2D("Matrix1_2D_HitMap",";Col;Row",32,0,32,128,0,128);
 //   TH2D *M_2_all= new TH2D("Matrix2_2D_HitMap",";Col;Row",32,0,32,128,0,128);
 // 
 //   char h_3d[100];
 //   sprintf(h_3d,";Col;Row;TH");
 //   int p_end=parameters[Steps-1];
 //   TH3D *M_0_3d= new TH3D("Matrix0_3D_HitMap",h_3d,32,0,32,128,0,128,Steps,parameters[0],p_end);
 //   TH3D *M_1_3d= new TH3D("Matrix1_3D_HitMap",h_3d,32,0,32,128,0,128,Steps,parameters[0],p_end);
 //   TH3D *M_2_3d= new TH3D("Matrix2_3D_HitMap",h_3d,32,0,32,128,0,128,Steps,parameters[0],p_end);

 //   TH1D *m0_eff = new TH1D("Matrix0_3D_efficiency",";TH;Counts",Steps,parameters[0],p_end);
 //   TH1D *m1_eff = new TH1D("Matrix1_3D_efficiency",";TH;Counts",Steps,parameters[0],p_end);
 //   TH1D *m2_eff = new TH1D("Matrix2_3D_efficiency",";TH;Counts",Steps,parameters[0],p_end);

    std::cout<<"steps : "<<Steps<<" from "<<parameters[0]<<" to "<<parameters[Steps-1]<<std::endl;
    std::vector<int> threshold_t;
    std::vector<int> col_t_0;
    std::vector<int> row_t_0;
    std::vector<int> Dv_flag_0;
    std::vector<int> Mv_flag_0;
    std::vector<int> col_t_1;
    std::vector<int> row_t_1;
    std::vector<int> Dv_flag_1;
    std::vector<int> Mv_flag_1;
    std::vector<int> col_t_2;
    std::vector<int> row_t_2;
    std::vector<int> Dv_flag_2;
    std::vector<int> Mv_flag_2;
    char save_name_root[100];
    sprintf(save_name_root,"%s_tree.root",save_name.c_str());
    TFile *file_r=TFile::Open(save_name_root,"RECREATE");  
    TTree Chess2_tree("Chess2_Tree","A tree with data from chess2 test");

    Chess2_tree.Branch("threshold_tr",&threshold_t);
    Chess2_tree.Branch("col_tr_0",&col_t_0); 
    Chess2_tree.Branch("row_tr_0",&row_t_0); 
    Chess2_tree.Branch("Dv_flag_tr_0",&Dv_flag_0); 
    Chess2_tree.Branch("Mv_flag_tr_0",&Mv_flag_0); 

    Chess2_tree.Branch("col_tr_1",&col_t_1); 
    Chess2_tree.Branch("row_tr_1",&row_t_1); 
    Chess2_tree.Branch("Dv_flag_tr_1",&Dv_flag_1); 
    Chess2_tree.Branch("Mv_flag_tr_1",&Mv_flag_1); 

    Chess2_tree.Branch("col_tr_2",&col_t_2); 
    Chess2_tree.Branch("row_tr_2",&row_t_2); 
    Chess2_tree.Branch("Dv_flag_tr_2",&Dv_flag_2); 
    Chess2_tree.Branch("Mv_flag_tr_2",&Mv_flag_2); 

    int frame_number=0;
    int hist=0;
    //DataClass::DataClass *data_t = new DataClass::DataClass(&frame);
    DataClass::DataClass *data_t = new DataClass::DataClass();
    for (int file_n=1; file_n<num+1 ;file_n++){
        
        sprintf(file_name_s,"%s.dat.%d",save_name.c_str(),file_n);
        std::cout<<"reading :"<<file_name_s<< std::endl;
        file = fopen(file_name_s,"rb");
        
        while(get_next_frame(file,&frame)==0){
            if (1){
            //if (frame.payload_size!=0){
                //std::cout<< "frame -> payload_size: "<< frame.payload_size <<std::endl;
                frame_number++;//std::cout<<"frame number : "<<frame_number<<std::endl;
                data_t->Init();
                //std::cout<<"Init "<<(data_t->get_Hitmap(0)).size()<<std::endl; 
                data_t->setFrame(&frame);
                threshold_t.push_back(parameters[hist]);
                if (frame_number<=frames[hist]){
                    if (frame_number == frames[hist]){
                        std::cout<<"filling "<< frames[hist] << std::endl;
                        hist+=1;
              
                    }
                }
                if (0){ //ignore M0
                //if ((data_t->get_Hitmap(0)).size()>0){
                    for (int h_0=0;h_0<(data_t->get_Hitmap(0)).size();h_0++){
                         col_t_0.push_back((data_t->get_Hitmap(0))[h_0][1]);
                         row_t_0.push_back((data_t->get_Hitmap(0))[h_0][0]);
                         Dv_flag_0.push_back(data_t->get_dv(0)[h_0]);
                         Mv_flag_0.push_back(data_t->get_mv(0)[h_0]);
                    }     
                }
                if ((data_t->get_Hitmap(1)).size()>0){ 
                    for (int h_1=0;h_1<(data_t->get_Hitmap(1)).size();h_1++){
                         col_t_1.push_back((data_t->get_Hitmap(1))[h_1][1]);
                         row_t_1.push_back((data_t->get_Hitmap(1))[h_1][0]);
                         Dv_flag_1.push_back(data_t->get_dv(1)[h_1]);
                         Mv_flag_1.push_back(data_t->get_mv(1)[h_1]);
                    }    
                }
                if (0){ // ingnore M2
                //if ((data_t->get_Hitmap(2)).size()>0){ 
                    for (int h_2=0;h_2<(data_t->get_Hitmap(2)).size();h_2++){
                         col_t_2.push_back((data_t->get_Hitmap(2))[h_2][1]);
                         row_t_2.push_back((data_t->get_Hitmap(2))[h_2][0]);
                         Dv_flag_2.push_back(data_t->get_dv(2)[h_2]);
                         Mv_flag_2.push_back(data_t->get_mv(2)[h_2]);
                    }   
                }
                Chess2_tree.Fill();
                threshold_t.clear();
                col_t_0.clear();
                row_t_0.clear();
                Dv_flag_0.clear();
                Mv_flag_0.clear();
                col_t_1.clear();
                row_t_1.clear();
                Dv_flag_1.clear();
                Mv_flag_1.clear();
                col_t_2.clear();
                row_t_2.clear();
                Dv_flag_2.clear();
                Mv_flag_2.clear();
            }
            delete_frame(&frame);
          //  std::cout<< "frame size is 0"<<std::endl;

        }
        std::cout<< "hists number in total :"<< hist <<std::endl;
        std::cout<< "frame number in total :"<<frame_number << std::endl;
        //delete_frame(&frame);
    }
    file_r->Write(); 
    return 1;
    
}
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
        if ((access(name_temp,F_OK))!= -1){
          //  std::cout<<((access(name_temp,F_OK))!= -1)<<std::endl;
        }
        else{break;}
    }
    return number-1;
}
