from collections import deque
from itertools import product

from model.etat import Etat
from model.transition import Transition


class Automate:
    def _init_(self, nom, alphabet=None):
        self.nom = nom
        self.etats = {}  # dict : {nom: Etat}
        self.transitions = []  # liste d'objets Transition
        self.alphabet = alphabet if alphabet else set()
        self.etat_initial = None  # nom de l'état initial

    def ajouter_etat(self, nom, est_initial=False, est_final=False):
        if nom not in self.etats:
            self.etats[nom] = Etat(nom, est_initial, est_final)
        if est_initial:
            self.etat_initial = nom

    def ajouter_transition(self, source, symbole, destination):
        if source not in self.etats or destination not in self.etats:
            raise ValueError("Source ou destination non existant dans les états")
        self.transitions.append(Transition(source, symbole, destination))

    def est_deterministe(self):
        transitions_par_etat = {}
        for t in self.transitions:
            key = (t.source, t.symbole)
            if key in transitions_par_etat:
                return False
            transitions_par_etat[key] = t.destination
        nb_initiaux = sum(1 for e in self.etats.values() if e.est_initial)
        return nb_initiaux == 1

    def est_complet(self):
        """Vérifie si l'automate est complet (tous les états ont des transitions pour tous les symboles)"""
        for etat in self.etats:
            symboles_vus = set()
            for t in self.transitions:
                if t.source == etat:
                    symboles_vus.add(t.symbole)
            if symboles_vus != self.alphabet:
                return False
        return True

    def completer(self):
        if not self.est_deterministe():
            raise ValueError("L'automate doit être déterministe pour être complété.")

        nouvel_automate = Automate(nom=f"{self.nom}_complet", alphabet=self.alphabet.copy())

        # Copier les états existants
        for etat in self.etats.values():
            nouvel_automate.ajouter_etat(etat.nom, est_initial=etat.est_initial, est_final=etat.est_final)

        # Ajouter un état puits si nécessaire
        etat_puits = "PUITS"
        if etat_puits not in self.etats:
            nouvel_automate.ajouter_etat(etat_puits, est_initial=False, est_final=False)

        # Ajouter transitions manquantes vers l'état puits
        for etat in nouvel_automate.etats.values():
            symboles_vus = {t.symbole for t in nouvel_automate.transitions if t.source == etat.nom}
            symboles_manquants = nouvel_automate.alphabet - symboles_vus
            for symb in symboles_manquants:
                nouvel_automate.ajouter_transition(etat.nom, symb, etat_puits)

        # Pour l'état puits, ajouter toutes les transitions vers lui-même
        for symb in nouvel_automate.alphabet:
            nouvel_automate.ajouter_transition(etat_puits, symb, etat_puits)

        return nouvel_automate

    def complement(self):
        if not self.est_deterministe():
            raise Exception("L'automate doit être déterministe pour calculer le complément.")
        if not self.est_complet():
            raise Exception("L'automate doit être complet pour calculer le complément.")

        complement = Automate(nom=self.nom + "_complement")
        complement.alphabet = self.alphabet.copy()

        # Copier les états en inversant la finalité
        for nom_etat, etat in self.etats.items():
            complement.ajouter_etat(nom_etat, est_initial=etat.est_initial, est_final=not etat.est_final)

        # Copier les transitions
        for t in self.transitions:
            complement.ajouter_transition(t.source, t.symbole, t.destination)

        return complement

    def determiniser(self):
        new_automate = Automate(self.nom + "_deterministe")
        etats_afn = self.etats
        transitions_afn = self.transitions

        initiaux = [e.nom for e in etats_afn.values() if e.est_initial]
        file = deque()
        initial_set = frozenset(initiaux)
        file.append(initial_set)
        visited = {initial_set}

        new_automate.ajouter_etat(str(initial_set), est_initial=True,
                                  est_final=any(etats_afn[s].est_final for s in initial_set))

        while file:
            current_set = file.popleft()
            for symbole in self.alphabet:
                next_set = set()
                for etat in current_set:
                    for t in transitions_afn:
                        if t.source == etat and t.symbole == symbole:
                            next_set.add(t.destination)
                if next_set:
                    next_frozen = frozenset(next_set)
                    if next_frozen not in visited:
                        visited.add(next_frozen)
                        new_automate.ajouter_etat(str(next_frozen),
                                                  est_initial=False,
                                                  est_final=any(etats_afn[s].est_final for s in next_frozen))
                        file.append(next_frozen)
                    new_automate.ajouter_transition(str(current_set), symbole, str(next_frozen))

        return new_automate

    def ajouter_transition(self, source, symbole, destination):
        self.transitions.append(Transition(source, symbole, destination))
        self.alphabet.add(symbole)

    def get_etat_initial(self):
        for etat in self.etats.values():
            if etat.est_initial:
                return etat.nom
        return None

    def est_final(self, etat_nom):
        return self.etats[etat_nom].est_final if etat_nom in self.etats else False

    def transition(self, etat_nom, symbole):
        for t in self.transitions:
            if t.source == etat_nom and t.symbole == symbole:
                return t.destination
        return None

    def est_deterministe(self):
        # Pas de transitions epsilon autorisées
        for t in self.transitions:
            if t.symbole == 'ε' or t.symbole == '':
                return False

        # Vérifier qu'il n'y a pas plusieurs transitions pour un même état + symbole
        transitions_par_etat_symbole = {}

        for t in self.transitions:
            cle = (t.source, t.symbole)
            if cle in transitions_par_etat_symbole:
                return False
            transitions_par_etat_symbole[cle] = t.destination

        return True

    def to_graphviz(self, filename="automate"):
        from graphviz import Digraph
        dot = Digraph(format='png')
        dot.attr(rankdir='LR')

        for etat in self.etats.values():
            shape = "doublecircle" if etat.est_final else "circle"
            dot.node(etat.nom, shape=shape)

        for etat in self.etats.values():
            if etat.est_initial:
                dot.node("init", label="", shape="none")
                dot.edge("init", etat.nom)

        for t in self.transitions:
            dot.edge(t.source, t.destination, label=t.symbole)

        dot.render(filename=filename, cleanup=True)

    def union(self, autre):
        from collections import deque

        alphabet_union = self.alphabet.union(autre.alphabet)
        etat_initial = (self.get_etat_initial(), autre.get_etat_initial())
        etats = {}
        transitions = []
        file = deque()
        file.append(etat_initial)

        etats[etat_initial] = {
            'est_initial': True,
            'est_final': self.est_final(etat_initial[0]) or autre.est_final(etat_initial[1])
        }

        while file:
            etat_courant = file.popleft()
            for symbole in alphabet_union:
                etat_suivant_1 = self.transition(etat_courant[0], symbole)
                etat_suivant_2 = autre.transition(etat_courant[1], symbole)

                if etat_suivant_1 is None or etat_suivant_2 is None:
                    continue

                etat_suivant = (etat_suivant_1, etat_suivant_2)

                if etat_suivant not in etats:
                    est_final = self.est_final(etat_suivant_1) or autre.est_final(etat_suivant_2)
                    etats[etat_suivant] = {'est_initial': False, 'est_final': est_final}
                    file.append(etat_suivant)

                transitions.append((etat_courant, symbole, etat_suivant))

        etats_noms = {etat: f"{etat[0]}_{etat[1]}" for etat in etats}
        transitions_nouvelles = [(etats_noms[src], symb, etats_noms[dest]) for (src, symb, dest) in transitions]
        etats_finals_dict = {etats_noms[etat]: props for etat, props in etats.items()}

        nouvel_automate = Automate(f"Union_{self.nom}_{autre.nom}")
        nouvel_automate.alphabet = alphabet_union
        for nom, props in etats_finals_dict.items():
            nouvel_automate.ajouter_etat(nom, props['est_initial'], props['est_final'])
        for src, symb, dest in transitions_nouvelles:
            nouvel_automate.ajouter_transition(src, symb, dest)

        return nouvel_automate

    def intersection(self, autre):
        if self.alphabet != autre.alphabet:
            raise ValueError("Les alphabets des deux automates doivent être identiques pour l'intersection.")

        nom_intersection = f"Intersection_{self.nom}_{autre.nom}"
        automate_inter = Automate(nom_intersection)
        automate_inter.alphabet = self.alphabet

        # Création des états du produit cartésien
        for (nom1, etat1) in self.etats.items():
            for (nom2, etat2) in autre.etats.items():
                nouveau_nom = f"{nom1}_{nom2}"
                est_initial = etat1.est_initial and etat2.est_initial
                est_final = etat1.est_final and etat2.est_final
                automate_inter.ajouter_etat(nouveau_nom, est_initial, est_final)

        # Ajout des transitions
        for t1 in self.transitions:
            for t2 in autre.transitions:
                if t1.symbole == t2.symbole:
                    source = f"{t1.source}_{t2.source}"
                    symbole = t1.symbole
                    destination = f"{t1.destination}_{t2.destination}"
                    automate_inter.ajouter_transition(source, symbole, destination)

        # Définir l'état initial (le premier état marqué initial)
        for etat in automate_inter.etats.values():
            if etat.est_initial:
                automate_inter.etat_initial = etat.nom
                break

        return automate_inter

    def complement(self):
        # Vérifier que l'automate est déterministe et complet
        if not self.est_deterministe():
            raise Exception("L'automate doit être déterministe pour calculer le complément.")
        if not self.est_complet():
            raise Exception("L'automate doit être complet pour calculer le complément.")

        # Création d'un nouvel automate complémentaire avec le nom
        complement = Automate(self.nom + "_complement")

        # Copier l'alphabet
        complement.alphabet = self.alphabet.copy()

        # Copier les états en inversant leur propriété 'est_final'
        complement.etats = {}
        for nom_etat, etat in self.etats.items():
            nouvel_etat = Etat(nom=etat.nom, est_initial=etat.est_initial, est_final=not etat.est_final)
            complement.etats[nom_etat] = nouvel_etat

        # Copier les transitions telles quelles (même structure)
        complement.transitions = [t for t in self.transitions]

        return complement

    def etats_finaux(self):
        return [etat.nom for etat in self.etats.values() if etat.est_final]

    def reconnait(self, mot):
        etat_courant = self.get_etat_initial()
        if etat_courant is None:
            return False

        for symbole in mot:
            if symbole not in self.alphabet:
                return False  # symbole inconnu
            trouve = False
            for t in self.transitions:
                if t.source == etat_courant and t.symbole == symbole:
                    etat_courant = t.destination
                    trouve = True
                    break
            if not trouve:
                return False
        return etat_courant in self.etats_finaux()

    def est_equivalent(self, autre_automate, longueur_max):
        """
        Vérifie si deux automates sont équivalents en testant tous les mots possibles
        jusqu'à une longueur donnée.
        """
        from itertools import product

        if self.alphabet != autre_automate.alphabet:
            return False

        alphabet = list(self.alphabet)
        for n in range(longueur_max + 1):
            for p in product(alphabet, repeat=n):
                mot = "".join(p)
                if self.reconnait(mot) != autre_automate.reconnait(mot):
                    return False
        return True

    def ajouter_transition(self, source, symbole, destination):
        self.ajouter_etat(source)
        self.ajouter_etat(destination)
        self.transitions.append(Transition(source, symbole, destination))
        self.alphabet.add(symbole)

    def generer_mots_acceptes(self, longueur_max):
        """
        Génère tous les mots acceptés par l'automate jusqu'à une longueur maximale donnée.
        """
        mots_acceptes = set()
        initiaux = [e.nom for e in self.etats.values() if e.est_initial]
        if not initiaux:
            return list(mots_acceptes)

        file = deque()
        for etat in initiaux:
            file.append((etat, ""))

        while file:
            etat_courant, mot = file.popleft()

            if len(mot) > longueur_max:
                continue

            if self.etats[etat_courant].est_final:
                mots_acceptes.add(mot)

            for t in self.transitions:
                if t.source == etat_courant:
                    file.append((t.destination, mot + t.symbole))

        return sorted(mots_acceptes)

    def mots_rejetes(self, longueur_max):
        """
        Retourne tous les mots sur l'alphabet de l'automate de longueur <= longueur_max
        qui ne sont pas acceptés.
        """
        if not self.alphabet:
            return []

        tous_les_mots = set()
        for l in range(longueur_max + 1):
            for mot in product(self.alphabet, repeat=l):
                tous_les_mots.add("".join(mot))

        mots_acceptes = set(self.generer_mots_acceptes(longueur_max))
        return sorted(
            [mot for mot in tous_les_mots - mots_acceptes if mot != ""],
            key=lambda x: (len(x), x)
        )

    def generer_mots_acceptes(self, longueur_max):
        """
        Génère tous les mots acceptés par l'automate jusqu'à une longueur maximale donnée.
        """
        mots_acceptes = set()

        # Vérifie qu’il existe au moins un état initial
        initiaux = [e.nom for e in self.etats.values() if e.est_initial]
        if not initiaux:
            return list(mots_acceptes)

        file = deque()
        # Chaque élément de la file contient : (état courant, mot formé jusqu’ici)
        for etat in initiaux:
            file.append((etat, ""))

        while file:
            etat_courant, mot = file.popleft()

            if len(mot) > longueur_max:
                continue

            if self.etats[etat_courant].est_final:
                mots_acceptes.add(mot)

            for t in self.transitions:
                if t.source == etat_courant:
                    file.append((t.destination, mot + t.symbole))

        return sorted(mots_acceptes)

    def supprimer_etat(self, nom):
        if nom in self.etats:
            del self.etats[nom]
            self.transitions = [
                t for t in self.transitions
                if t.source != nom and t.destination != nom
            ]

    def supprimer_transition(self, source, symbole, destination):
        self.transitions = [
            t for t in self.transitions
            if not (t.source == source and t.symbole == symbole and t.destination == destination)
        ]

    def to_dict(self):
        return {
            "nom": self.nom,
            "etats": [
                {"nom": e.nom, "est_initial": e.est_initial, "est_final": e.est_final}
                for e in self.etats.values()
            ],
            "alphabet": list(self.alphabet),
            "transitions": [
                {"source": t.source, "symbole": t.symbole, "destination": t.destination}
                for t in self.transitions
            ]
        }

    @staticmethod
    def from_dict(data):
        a = Automate(data["nom"])
        for e in data["etats"]:
            a.ajouter_etat(e["nom"], e["est_initial"], e["est_final"])
        for t in data["transitions"]:
            a.ajouter_transition(t["source"], t["symbole"], t["destination"])
        return a

    def est_minimal(self):
        """Vérifie si l'automate est minimal en comparant avec sa version minimisée."""
        automate_min = self.minimiser()
        return len(self.etats) == len(automate_min.etats)

    def minimiser(self):
        """Minimise l'automate en utilisant l'algorithme de Hopcroft"""
        if not self.est_deterministe():
            raise ValueError("L'automate doit être déterministe pour être minimisé.")

        # Initialisation des partitions
        partitions = []
        finaux = {e.nom for e in self.etats.values() if e.est_final}
        non_finaux = set(self.etats.keys()) - finaux

        if finaux:
            partitions.append(finaux)
        if non_finaux:
            partitions.append(non_finaux)

        # Raffinement des partitions
        while True:
            nouvelles_partitions = []
            for partition in partitions:
                if len(partition) == 1:
                    nouvelles_partitions.append(partition)
                    continue

                groupes = {}
                for etat in partition:
                    signature = tuple(
                        frozenset({t.destination for t in self.transitions
                                   if t.source == etat and t.symbole == symbole})
                        for symbole in self.alphabet
                    )
                    if signature not in groupes:
                        groupes[signature] = set()
                    groupes[signature].add(etat)

                nouvelles_partitions.extend(groupes.values())

            if nouvelles_partitions == partitions:
                break
            partitions = nouvelles_partitions

        # Création du nouvel automate minimal
        automate_min = Automate(self.nom + "_minimal")
        correspondance = {min(part): part for part in partitions}

        # Ajout des états
        for representant in correspondance:
            est_final = any(e in finaux for e in correspondance[representant])
            est_initial = any(e in [e.nom for e in self.etats.values() if e.est_initial]
                              for e in correspondance[representant])
            automate_min.ajouter_etat(representant, est_initial, est_final)

        # Ajout des transitions
        for part in partitions:
            representant = f"G{partitions.index(part)}"
            representant = min(part)
            transitions_vues = set()
            for t in self.transitions:
                if t.source in part and (t.symbole, t.destination) not in transitions_vues:
                    dest_repr = min([p for p in partitions if t.destination in p][0])
                    automate_min.ajouter_transition(representant, t.symbole, dest_repr)
                    transitions_vues.add((t.symbole, dest_repr))

        return automate_min

    def _repr_(self):
        res = f"Automate : {self.nom}\n"
        res += f"États initiaux : {[e.nom for e in self.etats.values() if e.est_initial]}\n"
        res += f"États finaux : {[e.nom for e in self.etats.values() if e.est_final]}\n"
        res += f"Tous les états : {sorted(self.etats.keys())}\n"
        res += f"Alphabet : {sorted(self.alphabet)}\n"
        res += "Transitions :\n"
        for t in self.transitions:
            res += f"  {t.source} -{t.symbole}-> {t.destination}\n"
        return res