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
        stopMachine();
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

// IN arrays add size after (a short), etc.
// think records and so on for different types

inline void assign(DynType *d1, DynType *d2) {
    int sz;
    char *p1, *p2;
    p1 = (char *)d1;
    p2 = (char *)d2;
    checktype(d1, d2);
    sz = typeSZ(d1);
    memmove(d1, d2, sz+1);
}

// Hay que hacer otro para literales que reciba un void * y el tipo
// Entonces todas las variables y parámetros son de tipo DynType.

// Por ejemplo:
int a;

// Ahora sería:
DynType a:
a.tvar = INT;

// Para las funciones de la librería habría que hacer trampolines.
// Los trampolines reciben una lista de tipos (INT, STR,....), un puntero
//a functions (la funcion de halduino a llamar) y los argumentos,
//una lista de DynTypes. Se comprueban los tipos, se desempaquetan y luego se
//llama a la función. La función puede ser la función como ya era antes.


//El caso de las strings, es especial porque las strings serán punteros y
//habrá que
//reservar su espacio (y hacer free al final del ámbito, a menos que se
//retorne, Escape Analysis).

//Si tengo una string de tamaño 32, por ejemplo:

DynType *s;

s = (DynType *)malloc(sizeof(DynType)-MinTypeSz+32);

// Se puede empezar con cosas intermedias, como por ejemplo un MinTypeSz gordo.
// Y luego ir arreglando


// This function is call to stop the robot
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