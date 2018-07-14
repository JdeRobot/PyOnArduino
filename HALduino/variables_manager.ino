#include <assert.h>

enum {
    MinTypeSz = 8,
};

struct DynType {
    unsigned char tvar;
    char   data[MinTypeSz];
};

inline void checktype (DynType *d1, DynType *d2) {
    if(d1->tvar != d2->tvar) {
        // stopMachine();
        Serial.print("Stops giving the line");
    }
}

enum VarTypes{
    CHAR,
    INT,
    STR,
    TUP,
    ARRAY
};

int VarTypesSz[] = {
    [CHAR] = 8,
    [INT] = 64,
    [STR] = -1,
    [TUP]= -1,
    [ARRAY]= -1
};

int typeSZ(DynType *d) {
    int sz;
    char *start;
    sz = VarTypesSz[d->tvar];
    if(sz > 0) {
        return sz;
    }
    // If it's not a basic type
    start = (char *)d + 1;
    if(d->tvar == STR){
        return strlen(start+1);
    }
}

// In arrays add size after (a short), etc.
// think records and so on for different types
inline void assign(DynType *d1, DynType *d2) {
    int sz;
    char *p1, *p2;
    p1 = (char *)d1;
    p2 = (char *)d2;
    checktype(d1, d2);
    sz = typeSZ(d1);
    memmove(p1, p2, sz+1);
}

// This function is called to stop the robot
void stopMachine() {
    char *p, q;

    p=(char *)0;
    cli();//no interrupts
    // sleep_enable();
    // sleep_cpu();//should stop
    exit(0);//should finish
    *p=1; //crash, may require more
    q=*p;
    Serial.print(q, HEX); //use it, bc the optimizer deletes q if not
    for(;;){}//will stop here for sure
}

