#include <stdlib.h>


void showresults_ana()
{

//TPad *pad_1=new TPad();
//TImage *img=TImage::Open("/u1/home/hanyubo/atlas-chess2/software/scripts/fast_s/chess2_f.png");
//if (!img){printf("no background img \n");return;}
//img->SetConstRatio(kFALSE);
//img->Draw();
//cv0->SetFixedAspectRatio();
TCanvas *c1=new TCanvas("cv0","cv0",407,51,1373,1018);
c1->cd();
gStyle->SetOptStat(0);
gStyle->SetOptTitle(0);
c1->Range(-3340.151,-2544.738,30061.36,22902.64);
c1->SetFillColor(0);
c1->SetBorderMode(0);
c1->SetBorderSize(2);
c1->SetFrameBorderMode(0);
c1->SetFrameLineColor(0);
c1->SetFrameBorderMode(0);
double chass2_point_x[27]={87.9,20228,24300,24300,24300,20227,87.9,87.9,87.9,87.9,87.9,20227,20227,20227,20227,20227,20227,87.9,87.9,20227,20227,87.9,87.9,20227,20227,87.9,87.9};
double chass2_point_y[27]={108,108,108,18517,18517,18517,18517,13413,13138,8034,5212,5212,8034,13138,13413,18517,13413,13413,13138,13138,8034,8034,5212,5212,108,108,5212};
TGraph *chass2=new TGraph(27,chass2_point_x,chass2_point_y);
chass2->GetXaxis()->SetAxisColor(0);
chass2->GetXaxis()->SetLabelColor(0);
chass2->GetXaxis()->SetLabelFont(42);
chass2->GetXaxis()->SetLabelSize(0.035);
chass2->GetXaxis()->SetTitleSize(0.035);
chass2->GetXaxis()->SetTitleFont(42);
chass2->GetYaxis()->SetAxisColor(0);
chass2->GetYaxis()->SetLabelColor(0);
chass2->GetYaxis()->SetLabelFont(42);
chass2->GetYaxis()->SetLabelSize(0.035);
chass2->GetYaxis()->SetTitleSize(0.035);
chass2->GetYaxis()->SetTitleFont(42);
chass2->SetLineWidth(2);
chass2->Draw("APL");

char *f1_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-01/chess2_scan_SCurveTest_05212018_board_192.168.3.28_run_test_BL_744_chargeInjectionEnbled_1_thN_0x6_Bias_-7_hitmap_AllPixelsEnabled_cor.root";
char *f2_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04232018_board_192.168.3.28_run_N7_BL_744_chargeInjectionEnbled_0_thN_0x6nobias_m2_th0.802v_oneth_hitmap_AllPixelsEnabled.root";
//char *f3_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04122018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_02_AllPixelsEnabled.root";
//char *f4_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04122018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_04_AllPixelsEnabled.root";
//char *f5_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04132018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_05_AllPixelsEnabled.root";
//char *f6_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04132018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_06_AllPixelsEnabled.root";
//char *f7_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04132018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_07_AllPixelsEnabled.root";
//char *f8_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04132018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_08_AllPixelsEnabled.root";
//char *f9_name="/u1/atlas-chess2-Asic-tests/data/data_h/pre-ampdata-02/chess2_scan_SCurveTest_04132018_board_192.168.3.28_run_N6_BL_744_chargeInjectionEnbled_1_thN_0x6_500ns_nobias_event_1_th0.75v_3_09_AllPixelsEnabled.root";
//TCanvas *cv0=new TCanvas();
//cv0->cd();
int p1=16,p2=40,p3=1675,p4=872;
int lw=2;
double sc=0.00125;// count=100
char hit_num[10]="";
int co1=2,co2=3,co3=9,co4=2;
int co_m0=2,co_m1=4,co_m2=3;
char leg1[50],leg2[50],leg3[50],leg4[50],leg5[50],leg6[50],leg7[50],leg8[50],leg9[50],leg10[50],leg11[50],;
//sprintf(leg3,"%s%s_matrix_%s_bias12_Qinj",p_2,hit_num,asic_num);
const char *data_type_name[3]={"-1.0","-2.0","Time data"};
TFile *f1= TFile::Open(f1_name);
TFile *f2= TFile::Open(f2_name);
//TFile *f3= TFile::Open(f3_name);
//TFile *f4= TFile::Open(f4_name);
//TFile *f5= TFile::Open(f5_name);
//TFile *f6= TFile::Open(f6_name);
//TFile *f7= TFile::Open(f7_name);
//TFile *f8= TFile::Open(f8_name);
//TFile *f9= TFile::Open(f9_name);
gBenchmark->Start("canvas");
TPad *pad1=new TPad("pad1","pad11",0.05743825,0.590081,0.7174038,0.8593117);
pad1->Draw();
pad1->Range(-2.379409,-2.775361,32.67112,17.31547);
pad1->SetFillColor(0);pad1->SetFillStyle(4000);pad1->SetBorderMode(0);pad1->SetBorderSize(2);pad1->SetLeftMargin(0.06788512);pad1->SetRightMargin(0.0191471);pad1->SetTopMargin(0.1152501);pad1->SetBottomMargin(0.1381407);pad1->SetFrameBorderMode(0);pad1->SetFrameFillStyle(0);pad1->SetFrameBorderMode(0); 
TPad *pad2=new TPad("pad2","pad22",0.07466973,0.04352227,0.7133831,0.3390688);
pad2->Draw();
pad2->Range(-1.464252,-38.53697,32.45758,149.6623);
pad2->SetFillColor(0);pad2->SetFillStyle(4000);pad2->SetBorderMode(0);pad2->SetBorderSize(2);pad2->SetLeftMargin(0.04316547);pad2->SetRightMargin(0.01348919);pad2->SetTopMargin(0.115103);pad2->SetBottomMargin(0.2047669);pad2->SetFrameBorderMode(0);pad2->SetFrameBorderMode(0);pad2->SetFrameFillStyle(0);
TPad *pad3=new TPad("pad3","pad33",0.07696726,0.388664,0.716255,0.6224696);
pad3->Draw();
pad3->Range(-1.340952,-17.51004,32.57905,131.3736);
pad3->SetFillColor(0);pad3->SetFillStyle(4000);pad3->SetBorderMode(0);pad3->SetBorderSize(2);pad3->SetLeftMargin(0.0395328);pad3->SetRightMargin(0.01707094);pad3->SetTopMargin(0.02265935);pad3->SetBottomMargin(0.1176089);pad3->SetFrameFillStyle(0);pad3->SetFrameBorderMode(0);

char h0_0[50],h0_1[50],h0_2[50],h0_3[50],h0_4[50],h0_5[50],h0_6[50],h0_7[50],h01[50];
TCanvas *cv1=new TCanvas("cv1","cv1",223,122,990,387);
TH2D *hist_m0=new TH2D("Matrix0","2d hitmap0",32,0,32,128,0,128);
TH2D *hist_m1=new TH2D("Matrix1","2d hitmap1",32,0,32,128,0,128);
TH2D *hist_m2=new TH2D("Matrix2","2d hitmap2",32,0,32,128,0,128);
for (int asic_num=0;asic_num<3;asic_num++){
   // cv0->cd(asic_num*3+1);
    //cv0->cd(asic_num+2);
    if (asic_num==0){pad1->cd();}
    if (asic_num==1){pad3->cd();}
    if (asic_num==2){pad2->cd();}
    sprintf(h0_0,"chess2_matrix%i_allhit",asic_num);
    TH2D *hist01_1=(TH2D*)f1->Get(h0_0);
    TH2D *hist01_2=(TH2D*)f2->Get(h0_0);
    //TH2D *hist01_3=(TH2D*)f3->Get(h0_0);
    //TH2D *hist01_4=(TH2D*)f4->Get(h0_0);
    //TH2D *hist01_5=(TH2D*)f5->Get(h0_0);
    //TH2D *hist01_6=(TH2D*)f6->Get(h0_0);
    //TH2D *hist01_7=(TH2D*)f7->Get(h0_0);
    //TH2D *hist01_8=(TH2D*)f8->Get(h0_0);
    //TH2D *hist01_9=(TH2D*)f9->Get(h0_0);

    //TH2D *hist01=new TH2D(*hist01_2);
    sprintf(h01,"chess2_matrix%i",asic_num);
    TH2D *hist01=new TH2D(h01,"2d hitmap0",32,0,32,128,0,128);
    hist01->Add(hist01_1,hist01_2,1,0);
    //hist01->Add(hist01,hist01_3,1,1);
    //hist01->Add(hist01,hist01_4,1,1);
    //hist01->Add(hist01,hist01_5,1,1);
    //hist01->Add(hist01,hist01_6,1,1);
    //hist01->Add(hist01,hist01_7,1,1);
    //hist01->Add(hist01,hist01_8,1,1);
    //hist01->Add(hist01,hist01_9,1,1);
    gStyle->SetOptTitle(0);gStyle->SetOptStat(0);

    if (asic_num==0){
    hist01->GetXaxis()->SetTitle("col");
    hist01->GetXaxis()->SetLabelFont(42);
    hist01->GetXaxis()->SetTitleSize(0.06);
    hist01->GetXaxis()->SetTitleOffset(0.5);
    hist01->GetXaxis()->SetTitleFont(42);
    hist01->GetYaxis()->SetTitle("row");
    hist01->GetYaxis()->SetLabelFont(42);
    hist01->GetYaxis()->SetTitleSize(0.06);
    hist01->GetYaxis()->SetTickLength(0.02);
    hist01->GetYaxis()->SetTitleOffset(0.3);
    hist01->GetYaxis()->SetTitleFont(42);
    //pad1->Modified();
    hist01->SetFillColor(2);
    hist01->Draw("box");
    cout<<"Drawing ..."<<endl;
    hist_m0=hist01;
     }//sprintf(p_col0,"chess2_matrix%i_p_col",asic_num);pro_col=TH1D(p_col0,"proj_col",32,0,32);cv2->cd(asic_num*2+1);pro_col=hist01.ProjectionX("_col",0,-1,"col");pro_col->Draw();sprintf(p_row0,"chess2_matrix%i_p_row",asic_num);pro_row=TH1D(p_row0,"proj_row",128,0,128);pro_row=hist01.ProjectionY("_row",0,-1,"row");cv2->cd(asic_num*2+2);pro_row->Draw();}
    else {
    if (asic_num==1){hist_m1=hist01;}   
    if (asic_num==2){hist_m2=hist01;}   
     TH2D *hist01_inve=new TH2D(h01,"2d hitmap",32,0,32,128,0,128);
     for (int i_col=1;i_col<33;i_col++){
         for (int i_row=1;i_row<129;i_row++){
             int nu=hist01->GetBinContent(i_col,i_row);for (int yy=0;yy<nu;yy++){int j_row=128-i_row;hist01_inve->Fill(i_col-1,j_row-1);}

}}   
    
    hist01_inve->GetXaxis()->SetTitle("col");
    hist01_inve->GetXaxis()->SetLabelFont(42);
    hist01_inve->GetXaxis()->SetTitleSize(0.06);
    hist01_inve->GetXaxis()->SetTitleOffset(0.5);
    hist01_inve->GetXaxis()->SetTitleFont(42);
    hist01_inve->GetYaxis()->SetTitle("row");
    hist01_inve->GetYaxis()->SetLabelFont(42);
    hist01_inve->GetYaxis()->SetTitleSize(0.06);
    hist01_inve->GetYaxis()->SetTickLength(0.02);
    hist01_inve->GetYaxis()->SetTitleOffset(0.3);
    hist01_inve->GetYaxis()->SetTitleFont(42);
    hist01_inve->Draw("box");
    ReverseYAxis(hist01_inve);
    cout<<"Drawing ..."<<endl;
    hist01_inve->SetFillColor(2);


     }
    //hist01_inve->Write();
    //sprintf(p_col0,"chess2_matrix%i_p_col",asic_num);pro_col=TH1D(p_col0,"proj_col",32,0,32);pro_col=hist01_inve->ProjectionX("_col",0,-1,"col");sprintf(p_row0,"chess2_matrix%i_p_row",asic_num);pro_row=TH1D(p_row0,"proj_row",128,0,128);pro_row=hist01_inve->ProjectionY("_row",0,-1,"row");pro_col->Write();pro_row->Write();

    
    cv1->cd();
    sprintf(h0_3,"chess2_matrix%i_allhit_t",asic_num);
    TH1D *hist01y_1=(TH1D*)f1->Get(h0_3);
    TH1D *hist01y_2=(TH1D*)f2->Get(h0_3);
    //TH1D *hist01y_3=(TH1D*)f3->Get(h0_3);
    //TH1D *hist01y_4=(TH1D*)f4->Get(h0_3);
    //TH1D *hist01y_5=(TH1D*)f5->Get(h0_3);
    //TH1D *hist01y_6=(TH1D*)f6->Get(h0_3);
    //TH1D *hist01y_7=(TH1D*)f7->Get(h0_3);
    //TH1D *hist01y_8=(TH1D*)f8->Get(h0_3);
    //TH1D *hist01y_9=(TH1D*)f9->Get(h0_3);
    TH1D *hist01y=new TH1D(*hist01y_1);
    hist01y->Add(hist01y_1,hist01y_2,1,0);
   // hist01y->Add(hist01y,hist01y_3,1,1);
   // hist01y->Add(hist01y,hist01y_4,1,1);
   // hist01y->Add(hist01y,hist01y_5,1,1);
   // hist01y->Add(hist01y,hist01y_6,1,1);
   // hist01y->Add(hist01y,hist01y_7,1,1);
   // hist01y->Add(hist01y,hist01y_8,1,1);
   // hist01y->Add(hist01y,hist01y_9,1,1);

    hist01y->GetYaxis()->SetTitle("counts_number");
    if (asic_num==0){
        hist01y->Draw("");
        hist01y->SetLineColor(co_m0);hist01y->SetLineWidth(0.3);hist01y->GetXaxis()->SetLabelSize(0.04);}
    if (asic_num==1){
        hist01y->Draw("same");
        hist01y->SetLineColor(co_m1);hist01y->SetLineWidth(0.3);hist01y->GetXaxis()->SetLabelSize(0.04);}
    if (asic_num==2){
        hist01y->Draw("same");
        hist01y->SetLineColor(co_m2);hist01y->SetLineWidth(0.3);hist01y->GetXaxis()->SetLabelSize(0.04);}
  //  cv1->cd(asic_num*2+2);
  //  sprintf(h0_4,"chess2_matrix%i_allhit_th",asic_num);
  //  TH1D *hist01x_1=(TH1D*)f1->Get(h0_4); 
  //  TH1D *hist01x_2=(TH1D*)f2->Get(h0_4); 
  //  TH1D *hist01x=new TH1D(*hist01x_1);
  //  hist01x->Add(hist01x_1,hist01x_2,1,-1);
  //  hist01x->GetYaxis()->SetTitle("counts_number");
  //  hist01x->Draw("");hist01x->SetLineColor(co1);hist01x->SetLineWidth(0.3);hist01x->GetXaxis()->SetLabelSize(0.04);
    }
TCanvas *cv2=new TCanvas("cv2","cv2",246,251,844,476);
cv2->cd();
cv2->Divide(1,2);
cv2->cd(1);
//TH1D *p_col0=new TH1D("col_m0","proj_col",32,0,32);
TH1D *p_col0=hist_m0->ProjectionX();p_col0->SetFillColor(co_m0);p_col0->SetFillStyle(3005);p_col0->SetLineColor(co_m0);p_col0->SetLineWidth(2);
TH1D *p_col1=hist_m1->ProjectionX();p_col1->SetFillColor(co_m1);p_col1->SetFillStyle(3005);p_col1->SetLineColor(co_m1);p_col1->SetLineWidth(2);
TH1D *p_col2=hist_m2->ProjectionX();p_col2->SetFillColor(co_m2);p_col2->SetFillStyle(3005);p_col2->SetLineColor(co_m2);p_col2->SetLineWidth(2);
p_col0->GetYaxis()->SetTitle("HitNumber");
p_col0->GetXaxis()->SetTitle("COL");
p_col0->GetXaxis()->SetLabelSize(0.05);p_col0->GetXaxis()->SetTitleSize(0.06); |p_col0->GetXaxis()->SetTitleOffset(0.49);p_col0->GetYaxis()->SetLabelSize(0.05);p_col0->GetYaxis()->SetTitleSize(0.06);p_col0->GetYaxis()->SetTitleOffset(0.53);
p_col0->Draw();p_col2->Draw("same");p_col1->Draw("same");
TLegend *le1 = new TLegend(0.249757,0.2953869,0.526725,0.672061,NULL,"brNDC");
le1->AddEntry(p_col0,"matrix 0","l");
le1->AddEntry(p_col1,"matrix 1","l");
le1->AddEntry(p_col2,"matrix 2","l");
le1->SetFillStyle(0);le1->SetLineColor(0);
le1->Draw("L");

cv2->cd(2);
TH1D *p_row0=hist_m0->ProjectionY();p_row0->SetFillColor(co_m0);p_row0->SetFillStyle(3005);p_row0->SetLineColor(co_m0);p_row0->SetLineWidth(2);
TH1D *p_row1=hist_m1->ProjectionY();p_row1->SetFillColor(co_m1);p_row1->SetFillStyle(3005);p_row1->SetLineColor(co_m1);p_row1->SetLineWidth(2);
TH1D *p_row2=hist_m2->ProjectionY();p_row2->SetFillColor(co_m2);p_row2->SetFillStyle(3005);p_row2->SetLineColor(co_m2);p_row2->SetLineWidth(2);
p_row0->GetYaxis()->SetTitle("HitNumber");
p_row0->GetXaxis()->SetTitle("ROW");
p_row0->GetXaxis()->SetLabelSize(0.05);p_row0->GetXaxis()->SetTitleSize(0.06);p_row0->GetXaxis()->SetTitleOffset(0.49);p_row0->GetYaxis()->SetLabelSize(0.05);p_row0->GetYaxis()->SetTitleSize(0.06);p_row0->GetYaxis()->SetTitleOffset(0.53);
p_row0->Draw();p_row2->Draw("same");p_row1->Draw("same");

TLegend *le1 = new TLegend(0.249757,0.2953869,0.526725,0.672061,NULL,"brNDC");
le1->AddEntry(p_row0,"matrix 0","l");
le1->AddEntry(p_row1,"matrix 1","l");
le1->AddEntry(p_row2,"matrix 2","l");
le1->SetFillStyle(0);le1->SetLineColor(0);
le1->Draw("L");


}


void ReverseYAxis(TH2D *h)
{
 
   h->GetYaxis()->SetLabelOffset(999);
   h->GetYaxis()->SetTickLength(0);
   gPad->Update();
   TGaxis *newaxis = new TGaxis(gPad->GetUxmin(),gPad->GetUymax(),gPad->GetUxmin()-0.001, gPad->GetUymin(),0,128,510,"+");
   newaxis->SetLabelOffset(-0.02);
   newaxis->Draw();
                                                                                                                                                                                                                      }

