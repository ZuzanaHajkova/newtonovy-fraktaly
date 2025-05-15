**Newtonovy fraktály** - vizualizace konvergence komplexních funkcí

Funkce programu:

- uživatel zadává vlastní komplexní funkci ve formě 'z**3 - 1', 'sin(z)', atd.
- proběhne převedení vstupu na matematickou funkci pomocí sympy
- uživatel vybere oblast výpočtu (xmin, xmax, ymin, ymax) a rozlišení(velikost) matice v GUI
- proběhne výpočet a vizualizace konvergence ke konkrétním kořenům
- barevně jsou rozlišeny oblasti s konvergencí ke konkrétním kořenům, sytost pak udává rychlost konvergence


Pro snížení náročnosti a vyšší rychlost výpočtu je použit
- clustering(DBSCAN) pro určení jednotlivých kořenů
- dvoufázový výpočet: kořeny jsou nejprve nalezeny na malé mřížce (100×100), následně probíhá výpočet pro uživatelem zadané rozlišení
