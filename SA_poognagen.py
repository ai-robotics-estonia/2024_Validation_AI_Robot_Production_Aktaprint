# -*- coding: utf-8 -*-
"""
Created on Mon Oct 21 16:41:24 2024

@author: ator-
"""
from poognagen import  LiitPoogen, VLiitPoogen, KorduvPoogen, VKorduvPoogen, YVPoogen, VYVPoogen
from poognagen import Fitter, Monteerija, Leht, odavaim_hind, query_paberid
import random
import copy
import math

def get_price(layouts, print_run, colour):
    simulated_layouts = [odavaim_hind(sheet, print_run / sheet.N, colour) for sheet in layouts]
    if None not in simulated_layouts:
        total_sum = sum([cheapest[0][0] for cheapest in simulated_layouts])
        simulated_layouts = [(layout,) + triple for triple, layout in zip(simulated_layouts, layouts)] #tagastab poogna koos hinnakomponentidega
        return total_sum, simulated_layouts
    return None


class SAMonteerija(Monteerija):
    """
    Simulated Annealing tüüpi monteerija. Monteerija on siin realisatsiooni pärimiseks, liides ei säili.
    """
    
    def __init__(self, mods, fitter, decay=0.95):
        """
        tpoognad: võimalike trükipoognate hulk, suurus piirab lahendusi
        mods: modifitseerimismeetodid, tavaliselt poogna klasside mod_poognad meetodid
        decay: temperatuuri kahanemise kordaja
        """
        self.fitter = fitter
        self.mods = mods
        self.cache = {}
        self.decay = decay
        
        
    def teisenda_poognad(self, poognad, max_poognaid=100, backprob=0.3):
        """
        Rekursiivne liitpoognate generaator.

        Parameters
        ----------
        poognad : Sisendpoognad
        backprob: tagasilihtsustamise tõenäosus

        Yields
        ------
        Juhuslikult modifitseeritud variant poognate hulgast

        """
        if len(poognad) > max_poognaid:
            mods = [LiitPoogen, VLiitPoogen]
        else:
            mods = self.mods
        while True:
            t_poognad = copy.copy(poognad)
            if random.random() < backprob:
                p = random.choice(poognad)
                k = p.komponendid()
                if k != None:
                    t_poognad.remove(p)
                    t_poognad += k
                    if self.fitter.fits_all(t_poognad): return t_poognad
            g = random.choice(mods)
            t_poognad = g(poognad)
            if t_poognad != None and self.fitter.fits_all(t_poognad): 
                return t_poognad
            
            
    def taiendatud_poognad(self, poognad, tk, varv=1,  max_poognaid=100, iter_len=10, backprob=0.3, k=1000):
        """
        
        Parameters
        ----------
        poognad : sisendlehed.
        max_poognaid : Kui palju poognaid võib maksimaalselt vaja minna The default is 100.
        iter_len: Kui mitu lahendit ühes iteratsioonis (enne temperatuuri vähendamist) genereerida?
        backprob: tagasilihtsustamise tõenäosus
        tm: trükimasin
        tk: tiraaž
        k: Ebasoodsa ülemineku tõenäosust suurendav konstant. Oluliselt suurem kui tüüpiline hinnavahe, 
            et protsessi alguses oleks ebasoodne üleminek väga tõenäoline.

        Yields
        ------
        Simulated Annealing (SA) algoritmiga genereeritud poognate jada. 
        SA üritab läheneda optimaalsele hinnale.

        """
        t = 1 
        eelmine_hind = None
        hind, lahend = get_price(poognad, tk, varv) 
        while True:
            #if hind == eelmine_hind: return # Kui hind iteratsioonide tagajärjel ei muutunud, siis lõpeta
            if t < 0.001: return # Madala temperatuuri korral lõpeta
            eelmine_hind = hind
            for _ in range(iter_len):
                uued_poognad = self.teisenda_poognad(poognad, max_poognaid, backprob)
                uus_hind, uus_lahend = get_price(uued_poognad, tk, varv) 
                if uus_hind == None: 
                    # See pole sobiv kandidaat
                    pass
                elif uus_hind < hind:
                    # Soodsama kandidaadi valime alati
                    poognad = uued_poognad
                    hind = uus_hind
                    lahend = uus_lahend
                    yield hind, lahend
                else:
                    # Temperatuurist sõltub tõenäosus liikuda ebasoodsa kandidaadini
                    astendaja = (hind - uus_hind) / (t * k)
                    if random.random() < math.e**astendaja:
                        # Valime ebasoodsa kandidaadi
                        #print("hüpe")
                        poognad = uued_poognad
                        hind = uus_hind
                        lahend = uus_lahend
                        yield hind, lahend
                    else:
                        #print("pidur")
                        pass
            t = self.new_temp(t) 
            #print(t)                                     
                                   
    def parim_lahend(self, poognad, tk, varv=1,  max_poognaid=100, iter_len=10, backprob=0.2, k=1000):
        """
        Tagastab parima lahendi SA genereeritute hulgast
        """
        parim_sig = None
        parim_hind = 10**10
        for hind, sig in self.taiendatud_poognad(poognad, tk, varv=varv,  max_poognaid=max_poognaid, iter_len=iter_len, backprob=backprob, k=k):
            if hind < parim_hind:
                parim_sig = sig
                parim_hind = hind
        return parim_hind, parim_sig
        
        
    def new_temp(self, old_temp): return self.decay * old_temp
                 
            
if __name__ == "__main__":
    sam = SAMonteerija([LiitPoogen.rnd_poognad, 
                    VLiitPoogen.rnd_poognad, 
                    KorduvPoogen.rnd_poognad, 
                    VKorduvPoogen.rnd_poognad,
                    YVPoogen.rnd_poognad,
                    VYVPoogen.rnd_poognad], Fitter(query_paberid()), decay=0.995)
    #tp = [Leht(302, 216), Leht(302, 432)]
    #tp = [Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216)]
    tp = [Leht(302, 216), Leht(150, 216), Leht(302, 432), Leht(150, 432), Leht(150, 108), Leht(216, 108)]
    h, l = sam.parim_lahend(tp, 10000, iter_len=10)
    print(h)
    for ps, h, tm, p in l: 
        print("\nPoognen: ", ps, ps.N)
        print("Hind: ", h )
        print("Trükimasin: ", tm)
        print("Paber: ", p)
    #for p, h in sam.taiendatud_poognad(tp, 10000, iter_len=100):
    #    print(p, h)
    #for i in range(20):
    #    tp = sam.teisenda_poognad(tp)
    #    print(tp)

        
        