import math
import statistics
from typing import Optional

from poognagen import odavaim_hind, query_paberid, query_trykimasinad, Leht, KorduvPoogen, \
    LiitPoogen, VYVPoogen, VLiitPoogen, VKorduvPoogen, YVPoogen, Fitter, MctsRandomMonteerija


class MctsNode:
    def __init__(self, layout, parent=None, price=None, price_components=None, is_terminal=False):
        self.layout = layout
        self.parent = parent
        self.price = price # Antud poogna(te) koguhind
        self.price_components = price_components # Antud poogna(te) hinnakomponendid
        self.children = []
        self.visits = 0
        self.is_terminal = is_terminal
        self.reward = None #  Poogna ja tema alampoognate hindade keskmine miinusmärgiga


    # kui poogenast enam uusi poognaid genereerida ei saa, on poogna staatus is_terminal=True
    # puus allapoole liikudes välistame sellised harud, et mitte otsinguga ühte harusse kinni jääda
    # kui ette tuleb haru, mida ei ole veel külastatud, siis seda kindlasti külastada
    # muul juhul valib parima olemasoleva haru hinna alusel
    def best_child(self):
        if self.is_terminal:
            return float('-inf')
        if self.visits == 0:
            return float('inf')
        return self.reward / self.visits + math.sqrt(math.log(self.parent.visits) / self.visits)


    def simulate_and_expand(self, colour, new_layouts, print_run, returns_from_simulation, terminal=False):
        layout_prices = {}
        for layouts in new_layouts:
            price = get_price(layouts, print_run, colour)
            if price is not None:
                layout_prices[tuple(layouts)] = price

        # Sorteerib poognad hinna alusel ja lisab puusse maksimaalselt 10 madalaima hinnaga poognat
        # Listi pikkust muutes, saab muuta mudeli poolt genereeritud uute alampoognate hulka ja laiendada-kitsendada otsingut
        sorted_layouts = sorted(layout_prices.items(), key=lambda item: item[1][0])[:10]

        for layouts, price in sorted_layouts:
            returns_from_simulation.append(price[0])
            child_node = MctsNode(list(layouts), parent=self, price=price[0], price_components=price[1],
                                  is_terminal=terminal)
            self.children.append(child_node)


    def back_propagate(self, reward):
        current = self
        while current is not None:
            if all(child.is_terminal for child in current.children): #uuendab is_terminal=True, kui alampoognaid enam laiendada ei saa
                current.is_terminal = True
            current.visits += 1
            current.reward = ((current.visits - 1) * (current.reward if current.visits > 1 else 0) + reward) / current.visits
            current = current.parent


def search(node, generator, print_run, colour, max_layouts):

    # Valib välja kõige kõrgema skooriga haru puus antud punktist edasi
    while node.children:
        node = max(node.children, key=lambda n: n.best_child())

    # Genereerib uued poognad antud poognast ja lisab need puusse antud poogna alamharudeks ainult juhul kui need on trükitavad
    # Genereerib ka igast alampoognast uued poognad, kuid lisab need ALGSE poogna alampoognateks puu struktuuris (ehk 1 kiht kõrgemale),
    # nii on võimalik ajada puu struktuur pigem laiemaks kui sügavamaks, mis aitab kaasa parima lahendi leidmisele
    returns_from_simulation = [node.price]
    if not node.children and node.is_terminal == False:
        new_layouts = get_new_layouts(generator, max_layouts, node, go_backwards=False)
        if len(new_layouts) == 0:
            node.is_terminal = True
        else:
            node.simulate_and_expand(colour, new_layouts, print_run, returns_from_simulation, terminal=True)
        for child in (child for child in node.children if child.is_terminal):
            new_child_layouts = get_new_layouts(generator, max_layouts, child, go_backwards=True)
            if len(new_child_layouts) == 0:
                child.is_terminal = True
            else:
                node.simulate_and_expand(colour, new_child_layouts, print_run, returns_from_simulation)

    # Reward-muutuja on poogna ja temast genereeritud 2 täiendava kihi alampoognate hindade keskmine miinusmärgiga
    # Muutujat kasutatakse MCTS puu struktuuris navigeerimiseks ja parima haru leidmiseks
    if node.reward is None:
        node.reward = -(statistics.mean(returns_from_simulation))

    # Signaliseerib reward-väärtuse puu algusesse
    node.back_propagate(node.reward)


def get_new_layouts(generator, max_layouts, node, go_backwards=False):
    generated_layouts = generator.additional_layouts(node.layout, max_layouts, go_backwards=go_backwards)
    return list(generated_layouts)


def get_price(layouts, print_run, colour):
    simulated_layouts = [odavaim_hind(sheet, print_run / sheet.N, colour) for sheet in layouts]
    if None not in simulated_layouts:
        total_sum = sum([cheapest[0][0] for cheapest in simulated_layouts])
        simulated_layouts = [(layout,) + triple for triple, layout in zip(simulated_layouts, layouts)] #tagastab poogna koos hinnakomponentidega
        return total_sum, simulated_layouts
    return None


def get_valid_root(fitter, root_candidate, print_run, colour = 1) -> Optional[MctsNode]:
    if fitter.fits_all(root_candidate):
        price = get_price(root_candidate, print_run, colour)
        return MctsNode(root_candidate, price=price[0], price_components=price[1]) if price is not None else None
    return None


def find_cheapest_node(root):
    def dfs(node):
        best_node = node if node.price is not None else None
        for child in node.children:
            candidate = dfs(child)
            if candidate is not None and (best_node is None or candidate.price < best_node.price):
                best_node = candidate
        return best_node

    return dfs(root)


def mcts(sheets_to_print, print_run, colour, iterations):

    # Iteratsioonide arvu suurendades otsib MCTS algoritm kauem ja võib leida parema lahenduse
    # go_backwards_ratio on väärtus vahemikus 0...1 (enamus katseid on tehtud väärtusega 0.3), määrab %, mis lubab otsida juhuslikult väljaspool senist rada

    fitter = Fitter(query_paberid())
    generator = MctsRandomMonteerija([LiitPoogen.mod_poognad,
                                      VLiitPoogen.mod_poognad,
                                      KorduvPoogen.mod_poognad,
                                      VKorduvPoogen.mod_poognad,
                                      YVPoogen.mod_poognad,
                                      VYVPoogen.mod_poognad], fitter, 0.00)

    # Esimese sammuna kontrollib, kas sisendlehed on trükitavad ja kui on siis sisendlehtede poognast saab MCTS puu alguspunkt
    root = get_valid_root(fitter, sheets_to_print, print_run, colour)

    # Kui sisendlehed ei ole trükitavad lõpetab algoritm veateatega
    (lambda: (_ for _ in ()).throw(Exception("Antud sisendlehed ei ole trükitavad: ", sheets_to_print)))() if root is None else None

    max_layouts = generator.max_poognaid(query_trykimasinad(), sheets_to_print)
    for i in range(iterations):
        search(root, generator, print_run, colour, max_layouts)

    # Kui iteratsioonid on läbi käidud, tagastab algoritm puu struktuuris parimad poognad ja nende koguhinna
    best_offer = find_cheapest_node(root)
    return best_offer.price, best_offer.price_components


def demo_main_mcts_v9():
    sisendlehed = [[Leht(210, 297), Leht(148, 210), Leht(297, 420), Leht(594, 420), Leht(105, 148), Leht(74, 105)]]
    #sisendlehed = [[Leht(210, 297), Leht(148, 210), Leht(105, 148), Leht(74, 105), Leht(52, 74), Leht(37, 52)]]
    #sisendlehed = [[Leht(302, 216), Leht(150, 216), Leht(302, 432), Leht(150, 432), Leht(150, 108), Leht(216, 108)]]
    #sisendlehed = [[Leht(302, 216), Leht(150, 216),Leht(148, 210), Leht(302, 216), Leht(150, 216), Leht(148, 210)]]
    #sisendlehed = [[Leht(52, 74), Leht(74, 105), Leht(37, 52), Leht(52, 74), Leht(74, 105), Leht(37, 52)]]
    #sisendlehed = [[Leht(302, 216),Leht(302, 548), Leht(74, 105), Leht(148, 210), Leht(105, 148), Leht(150, 108)]]
    #sisendlehed = [[Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216)]]
    #sisendlehed = [[Leht(74, 105), Leht(74, 105), Leht(74, 105), Leht(74, 105)]]
    #sisendlehed = [[Leht(148, 210), Leht(148, 210), Leht(148, 210), Leht(148, 210)]]
    #sisendlehed = [[Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216)]]
    #sisendlehed = [[Leht(105, 148)]]
    #sisendlehed = [[Leht(105, 148),Leht(74, 105)]]
    #sisendlehed = [[Leht(52, 74), Leht(52, 74), Leht(302, 216)]]
    #sisendlehed = [[Leht(210, 297), Leht(148, 210), Leht(105, 148), Leht(74, 105)]]
    #sisendlehed = [[Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216), Leht(302, 216)]]
    #sisendlehed = [[Leht(302, 216), Leht(150, 216), Leht(302, 432), Leht(150, 432), Leht(150, 108)]]
    #sisendlehed = [[Leht(210, 297), Leht(148, 210), Leht(297, 420), Leht(594, 420), Leht(105, 148)]]
    #sisendlehed = [[Leht(148, 210), Leht(148, 210), Leht(148, 210), Leht(148, 210), Leht(148, 210), Leht(148, 210)]]
    #sisendlehed = [[Leht(105, 148), Leht(105, 148), Leht(105, 148), Leht(297, 420), Leht(297, 420), Leht(297, 420)]]
    #sisendlehed = [[Leht(74, 105), Leht(210, 297), Leht(210, 297), Leht(210, 297), Leht(210, 297), Leht(210, 297)]]
    #sisendlehed = [[Leht(105, 148), Leht(105, 148), Leht(105, 148), Leht(297, 420), Leht(297, 420), Leht(297, 420)]]
    #sisendlehed = [[Leht(302,216), Leht(302,216), Leht(302,216), Leht(302,216)]]
    #sisendlehed = [[Leht(302, 216), Leht(150, 216), Leht(302, 432), Leht(150, 432)]]
    print("\nODAVAIMA LAHENDUSE OTSIMINE")
    for sl in sisendlehed:
        print("\nSisendlehed: ", sl)
        for tk in [10000]:
            hind, lahend = mcts(sl, tk, 1, iterations=6000)
            print("\nTiraaž: ", tk)
            print("Leitud odavaim koguhind: ", hind)
            for ps, h, tm, p in lahend:
                print("\nPoognen: ", ps, ps.N)
                print("Hind: ", h)
                print("Trükimasin: ", tm)
                print("Paber: ", p)


if __name__ == "__main__":
    demo_main_mcts_v9()
