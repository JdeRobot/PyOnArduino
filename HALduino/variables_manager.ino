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
    FLOAT,
    BOOL,
    STR,
    TUP,
    ARRAY
};

int VarTypesSz[] = {
    [CHAR] = 8,
    [INT] = 64,
    [FLOAT] = 64,
    [BOOL] = 1,
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



