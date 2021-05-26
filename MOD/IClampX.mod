TITLE IClampX.mod 

COMMENT
Since this is an electrode current, positive values of i depolarize the cell
and in the presence of the extracellular mechanism there will be a change
in vext since i is not a transmembrane current but a current injected
directly to the inside of the cell.

---------------- Signal types ---------------
Type #  Description;                Inputs
1       IClamp (NEURON original);   del, dur, amp
2       Triangular;                 del, risedur, falldur, amp, after_fall_amp
3       Sine;                       del, dur, amp, frq, phase, offset, sinedelay
4       Random;                     del, dur, amp, mu, sigma

ENDCOMMENT

VERBATIM
#include <time.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include <unistd.h>
ENDVERBATIM


NEURON {
        POINT_PROCESS IClampX
        RANGE   signal_type, del, dur, amp,
                risedur, falldur, amp, after_fall_amp,
                frq, phase, offset, sinedelay,
                mu, sigma, std, media
        ELECTRODE_CURRENT i
}

UNITS {
        (nA) = (nanoamp)
             }

PARAMETER {
        signal_type = 1
    
        del = 10 (ms)
        dur = 50 (ms)
        amp = 1 (nA)   
        
        risedur = 200 (ms)
        falldur = 200 (ms)
        after_fall_amp = 0 (nA)
        
        frq = 2 (Hz)
        phase = 0 (degree)
        offset = 0 (nA)
        sinedelay = 0 (ms)

        mu = 0 (nA)
        sigma = 1 (nA)

        std = 1 :(nA)
        media = 0 :(nA)

        high = 1
}

INITIAL{
        VERBATIM
        #include <time.h>
        srand(getpid()*time(NULL));
        ENDVERBATIM
}
ASSIGNED {
        i (nA)
        ibb (nA)
}

:BEFORE BREAKPOINT {
:        VERBATIM
:        double u1, u2, z0;
:        double randmax = RAND_MAX * 1.0;
:        double two_pi = 2.0*3.14159265358979323846;
:        if (signal_type==4){
:            u1 = rand()/randmax;
:            u2 = rand()/randmax;
:            z0 = sqrt(-2.0 * log(u1)) * cos(two_pi * u2);
:            ibb = (z0*sigma + mu);
:        }
:        ENDVERBATIM
:}
            
BREAKPOINT {
        VERBATIM
                
        int typeint = signal_type;
        int phase_rad = 0;
        switch(typeint){

            case 1: // step, NEURON's IClamp
                at_time(nrn_threads, del);
                at_time(nrn_threads, del+dur);
                if (t < del + dur && t >= del)
                    i = amp;
                else
                    i = 0;
                break;                 
                 
            case 2: // triangular
                at_time(nrn_threads, del);
                at_time(nrn_threads, del + risedur);
                at_time(nrn_threads, del + risedur + falldur);
                if (t < del)
                    i = 0;
                else{
                    if (t < del+risedur)
                        i = amp * (t-del)/risedur;
                    else{
                        if (t < del+risedur+falldur)
                            i = amp - ((amp-after_fall_amp) * (t-(del+risedur))/falldur);
                        else
                            i = 0;
                    }
                }
                break;
                
            case 3: // sine
                at_time(nrn_threads, del);
                at_time(nrn_threads, del + sinedelay);
                at_time(nrn_threads, del + dur);
                //phase_rad = M_PI*phase/180;
                if(t < del)
                    i = 0;
                else{
                    if(t < del + sinedelay)
                        i = offset;
                    else{
                        if(t < del + dur)
                            i = offset + amp*sin(2*M_PI*(frq/1000)*(t-del-sinedelay)
                                                     + (M_PI*phase/180));
                        else
                            i = 0;
                    }
                }
                break;
            
            case 4: // random
                at_time(nrn_threads, del);
                at_time(nrn_threads, del + dur);
                double a1,a2,a3,a4,a5,a6,a7,a8,a9,a10,a11,a12;
                double sum;
                if(t < del){
                     i = 0;
                }
                else{
                    if(t < del + dur){
                        //a1 =  rand()/randmax;
                        //a2 =  rand()/randmax;
                        //a3 =  rand()/randmax;
                        //a4 =  rand()/randmax;
                        //a5 =  rand()/randmax;
                        //a6 =  rand()/randmax;
                        //a7 =  rand()/randmax;
                        //a8 =  rand()/randmax;
                        //a9 =  rand()/randmax;
                        //a10 = rand()/randmax;
                        //a11 = rand()/randmax;
                        //a12 = rand()/randmax;
                        //sum = a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12;
                        //i = std*(sum-6) + media;

                        i = ibb;
                        
                    }
                    else
                        i = 0;
                }
                break;
        }
        ENDVERBATIM
}

