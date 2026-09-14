"""Contrôle qualité : recalcul indépendant des KPIs du rapport Power BI à partir des CSV bruts.

Les définitions reprennent exactement celles des mesures DAX (voir docs/dictionnaire-de-donnees.md).
Les résultats servent à vérifier que les chiffres affichés dans le rapport sont justes.

Usage :
    pip install pandas
    python scripts/verifier_kpis.py            # lit data/raw/
    python scripts/verifier_kpis.py chemin/vers/les/csv
"""
import sys
from pathlib import Path

import pandas as pd

DOSSIER = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parents[1] / "data" / "raw"
BOUTIQUE_EN_LIGNE = 999999

pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 20)


def charger():
    ventes = pd.read_csv(DOSSIER / "sales.csv", parse_dates=["OrderDate", "DeliveryDate"])
    produits = pd.read_csv(DOSSIER / "product.csv", dtype={"ProductCode": str})
    magasins = pd.read_csv(DOSSIER / "store.csv")
    clients = pd.read_csv(DOSSIER / "customer.csv", dtype=str, keep_default_na=False)
    clients["CustomerKey"] = clients["CustomerKey"].astype(int)
    return ventes, produits, magasins, clients


def controles_qualite(ventes, produits, magasins, clients):
    """Vérifie l'intégrité des données avant tout calcul."""
    controles = {
        "Doublons (OrderKey, LineNumber)": ventes.duplicated(["OrderKey", "LineNumber"]).sum(),
        "Ventes sans produit connu": (~ventes.ProductKey.isin(produits.ProductKey)).sum(),
        "Ventes sans magasin connu": (~ventes.StoreKey.isin(magasins.StoreKey)).sum(),
        "Ventes sans client connu": (~ventes.CustomerKey.isin(clients.CustomerKey)).sum(),
        "Prix net supérieur au prix unitaire": (ventes.NetPrice > ventes.UnitPrice).sum(),
        "Livraison avant la commande": (ventes.DeliveryDate < ventes.OrderDate).sum(),
    }
    print("=== Contrôles qualité (0 attendu partout)")
    for libelle, valeur in controles.items():
        print(f"  {'OK ' if valeur == 0 else 'KO '} {libelle} : {valeur}")
    return all(v == 0 for v in controles.values())


def kpis_par_annee(ventes):
    v = ventes.assign(
        CA_brut=ventes.Quantity * ventes.UnitPrice,
        CA_net=ventes.Quantity * ventes.NetPrice,
        Cout=ventes.Quantity * ventes.UnitCost,
        Annee=ventes.OrderDate.dt.year,
        EnLigne=ventes.StoreKey.eq(BOUTIQUE_EN_LIGNE),
        Delai=(ventes.DeliveryDate - ventes.OrderDate).dt.days,
    )
    premiere_annee = v.groupby("CustomerKey").OrderDate.min().dt.year
    v["Nouveau"] = v.CustomerKey.map(premiere_annee) == v.Annee

    def calcul(g):
        commandes = g.OrderKey.nunique()
        en_ligne = g[g.EnLigne]
        return pd.Series({
            "CA net (M$)": g.CA_net.sum() / 1e6,
            "Taux remise %": (1 - g.CA_net.sum() / g.CA_brut.sum()) * 100,
            "Taux marge %": (1 - g.Cout.sum() / g.CA_net.sum()) * 100,
            "Commandes": commandes,
            "Panier moyen $": g.CA_net.sum() / commandes,
            "Clients actifs": g.CustomerKey.nunique(),
            "Nouveaux clients": g.loc[g.Nouveau, "CustomerKey"].nunique(),
            "Part en ligne %": en_ligne.CA_net.sum() / g.CA_net.sum() * 100,
            "Délai en ligne (j)": en_ligne.groupby("OrderKey").Delai.max().mean(),
        })

    resultat = v.groupby("Annee")[v.columns].apply(calcul)
    resultat.insert(1, "Évolution CA %", resultat["CA net (M$)"].pct_change() * 100)
    return resultat


def main():
    ventes, produits, magasins, clients = charger()
    ok = controles_qualite(ventes, produits, magasins, clients)
    print("\n=== KPIs par année (à comparer au rapport Power BI)")
    print(kpis_par_annee(ventes).round(1).to_string())
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
