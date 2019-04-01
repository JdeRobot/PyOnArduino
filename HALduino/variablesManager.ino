#include <assert.h>
#include <string.h>
using namespace std;

enum {
    MinTypeSz = 32,
};

enum VarTypes {
    CHAR,
    INT,
    FLOAT,
    BOOL,
    STR,
    TUP,
    ARRAY
};

int VarTypesSz[7] = {
    [CHAR] = 8,
    [INT] = 32,
    [FLOAT] = 64,
    [BOOL] = 1,
    [STR] = 32,
    [TUP]= -1,
    [ARRAY]= -1
};

class DynType {
private:
    unsigned char tvar;
    char   data[MinTypeSz];
public:
    DynType() {
    }

    unsigned char getTVar() {
        return tvar;
    }

    char* getData() {
        return data;
    }

    inline void checktype (DynType *d1, DynType *d2) {
        if(d1->tvar != d2->tvar) {
            //Serial.print("Error");
            exit(0);
        }
    }

    DynType* newDynTypeInt(int x) {
        String s = String(x);
        char const *pchar = s.c_str();
        DynType *var = static_cast<DynType*>(malloc(sizeof(DynType) + VarTypesSz[INT]));
        var->tvar=INT;
        memcpy(var->data, pchar, VarTypesSz[INT]);

        return var;
    }

    int typeSZ(DynType *d) {
        int sz;
        char *start;
        sz = VarTypesSz[d->tvar];
        // cout << sz << "\n";
        if(sz > 0) {
            return sz;
        }
        // If it's not a basic type
        start = (char *)d + 1;
        if(d->tvar == STR){
            return strlen(start+1);
        }
        return 0;
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
};