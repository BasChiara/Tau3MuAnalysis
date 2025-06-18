#ifndef trigger_SFs_2022_h
#define trigger_SFs_2022_h

namespace SF_HLT_DoubleMu_src
{

inline float L1_SF_2022(float pT, float eta, float DR){
    float SF=1;
    if(fabs(eta)<0.9){  
        if (DR<0.35){
            if (pT<6.5) SF=0.940464;
            else if (pT<10) SF=0.995195;
            else if (pT<15) SF=0.936098;
            else if (pT<20) SF=0.869899;
            else SF=0.844248;
        }
        else{
            if (pT<6.5) SF=0.974512;
            else SF=0.954343;     
        }    
    }
    else if (fabs(eta)<1.2){
        if (DR<0.35){
            if (pT<6.5) SF=0.974163;
            else if (pT<10) SF=0.983871;
            else if (pT<15) SF=0.946724;
            else if (pT<20) SF=0.854219;
            else SF=0.725096;
        }
        else{
            if (pT<6.5) SF=0.94757;
            else SF=0.982829;     
        }     
    }
    else{
        if (DR<0.35){
            if (pT<6.5) SF=0.890303;
            else if (pT<10) SF=0.968846;
            else if (pT<15) SF=0.829491;
            else if (pT<20) SF=0.785405;
            else SF=0.760657;
        }
        else{
            if (pT<6.5) SF=0.942586;
            else SF=0.893215;     
        }    
    }
    return SF;
    }



inline float L1_SF_unc_2022(float pT, float eta, float DR){
    double SF=1;
    if(fabs(eta)<0.9){
        if (DR<0.35){
            if (pT<6.5) SF=0.00513163;
            else if (pT<10) SF=0.0175254;
            else if (pT<15) SF=0.0147551;
            else if (pT<20) SF=0.00579038;
            else SF=0.00607634;
        }
        else{
            if (pT<6.5) SF=0.00327296;
            else SF=0.00766454;     
        }    
    }
    else if (fabs(eta)<1.2){
        if (DR<0.35){
            if (pT<6.5) SF=0.112774;
            else if (pT<10) SF=0.0106754;
            else if (pT<15) SF=0.0814474;
            else if (pT<20) SF=0.0135183;
            else SF=0.0606656;
        }
        else{
            if (pT<6.5) SF=0.00518568;
            else SF=0.0129203;     
        }     
    }  
    else{
        if (DR<0.35){
            if (pT<6.5) SF=0.0562114;
            else if (pT<10) SF=0.0553319;
            else if (pT<15) SF=0.058834;
            else if (pT<20) SF=0.0220265;
            else SF=0.0133128;
        }
        else{
            if (pT<6.5) SF=0.0435326;
            else SF=0.0792481;     
        }  
    }
    return SF;
    }  
    
    
    
    
    
    
    
    
    
inline float HLT_SF_2022(float pT, float eta, float DR){
    float SF=1;
    if(fabs(eta)<0.9){  
        if (DR<0.35){
            if (pT<6.5) SF=0.636192;
            else if (pT<10) SF=0.595192;
            else if (pT<15) SF=0.934145;
            else if (pT<20) SF=0.963782;          
            else SF=0.953331;
        }
        else{
            if (pT<6.5) SF=0.76362;
            else if (pT<10) SF=0.954411;
            else if (pT<15) SF=0.95733;
            else SF=0.798721;     
        }    
    }
    else if (fabs(eta)<1.2){
        if (DR<0.35){
            if (pT<6.5) SF=0.932408;
            else if (pT<10) SF=0.732941;
            else if (pT<15) SF=0.92941;
            else if (pT<20) SF=0.936802;
            else SF=0.957847;
        }
        else{
            if (pT<6.5) SF=0.807071;
            else if (pT<10) SF=0.997961;
            else SF=0.937493;    
        }     
    }
    else{
        if (DR<0.35){
            if (pT<6.5) SF=0.730769;
            else if (pT<10) SF=0.70067;
            else if (pT<15) SF=0.905507;
            else if (pT<20) SF=0.934546;
            else SF=0.974615;
        }
        else{
            if (pT<6.5) SF=0.826671;
            else if (pT<10) SF=0.926821;
            else SF=0.926857;    
        }   
    }
    return SF;
    }



inline float HLT_SF_unc_2022(float pT, float eta, float DR){
    double SF=1;
    if(fabs(eta)<0.9){  
        if (DR<0.35){
            if (pT<6.5) SF=0.0824157;
            else if (pT<10) SF=0.0420128;
            else if (pT<15) SF=0.042563;
            else if (pT<20) SF=0.00625994;          
            else SF=0.00583198;
        }
        else{
            if (pT<6.5) SF=0.0152802;
            else if (pT<10) SF=0.0323239;
            else if (pT<15) SF=0.0031901;
            else SF=0.036421;     
        }    
    }
    else if (fabs(eta)<1.2){
        if (DR<0.35){
            if (pT<6.5) SF=0.28918;
            else if (pT<10) SF=0.0907367;
            else if (pT<15) SF=0.0475792;
            else if (pT<20) SF=0.0109483;
            else SF=0.0500664;
        }
        else{
            if (pT<6.5) SF=0.04195;
            else if (pT<10) SF=0.0102457;
            else SF=0.0137191;    
        }     
    } 
    else{
        if (DR<0.35){
            if (pT<6.5) SF=0.205952;
            else if (pT<10) SF=0.0825737;
            else if (pT<15) SF=0.0222346;
            else if (pT<20) SF=0.031868;
            else SF=0.051794;
        }
        else{
            if (pT<6.5) SF=0.0144921;
            else if (pT<10) SF=0.038853;
            else SF=0.0424426;    
        }   
    }
    return SF;
    }
}
#endif
  
  
  

  
  
