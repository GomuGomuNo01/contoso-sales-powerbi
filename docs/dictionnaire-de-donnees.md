# Dictionnaire de données

Description du modèle Power BI `Contoso-Ventes` : tables, colonnes, règles de transformation et mesures.

## Vue d'ensemble du modèle

Le modèle suit un **schéma en étoile** : une table de faits (`Ventes`) entourée de tables de dimensions reliées par des relations de type plusieurs-à-un (`*` vers `1`), avec un filtrage dans un seul sens (de la dimension vers les faits).

```
                 Calendrier (Date)
                        │ 1
                        │
 Produits ──1───*── Ventes ──*───1── Magasins
 (ProductKey)           │           (StoreKey)
                        │ *
                        │
                        1
                     Clients (CustomerKey)
```

| Table | Type | Source | Lignes | Grain (une ligne =) |
|---|---|---|---|---|
| `Ventes` | Faits | `sales.csv` | 223 974 | une ligne de commande |
| `Produits` | Dimension | `product.csv` | 2 517 | un produit |
| `Magasins` | Dimension | `store.csv` | 74 | un magasin (dont la boutique en ligne) |
| `Clients` | Dimension | `customer.csv` | 104 990 | un client |
| `Calendrier` | Dimension (table de dates) | Table calculée DAX | 3 653 | un jour, du 01/01/2016 au 31/12/2025 |
| `Mesures` | Table technique | Table vide | 0 | regroupe les mesures DAX |

Toutes les requêtes Power Query lisent leur fichier via le paramètre **`CheminDonnees`** (dossier `data/raw/`).

---

## Ventes (table de faits)

Toutes les colonnes sont masquées dans le rapport : l'utilisateur passe par les mesures et les dimensions.

| Colonne | Type | Source | Description |
|---|---|---|---|
| `OrderKey` | Entier | `OrderKey` | Identifiant de la commande (une commande peut contenir plusieurs lignes) |
| `Date de commande` | Date | `OrderDate` | Date de la commande, reliée à `Calendrier[Date]` |
| `Date de livraison` | Date | `DeliveryDate` | Date de livraison au client |
| `CustomerKey` | Entier | `CustomerKey` | Clé vers `Clients` |
| `StoreKey` | Entier | `StoreKey` | Clé vers `Magasins` |
| `ProductKey` | Entier | `ProductKey` | Clé vers `Produits` |
| `Quantité` | Entier | `Quantity` | Nombre d'unités vendues sur la ligne |
| `Prix unitaire` | Décimal (USD) | `UnitPrice` | Prix de vente unitaire avant remise |
| `Prix net` | Décimal (USD) | `NetPrice` | Prix de vente unitaire après remise |
| `Coût unitaire` | Décimal (USD) | `UnitCost` | Coût d'achat unitaire |
| `Délai de livraison (jours)` | Entier | Calculée | `Date de livraison − Date de commande`. Toujours 0 en magasin |

**Colonnes écartées :** `LineNumber` (numéro de ligne sans intérêt analytique), `CurrencyCode` et `ExchangeRate` (l'analyse est menée en USD).

## Produits

| Colonne | Type | Source | Description |
|---|---|---|---|
| `ProductKey` | Entier (masquée) | `ProductKey` | Clé du produit |
| `Produit` | Texte | `ProductName` | Nom commercial du produit |
| `Marque` | Texte | `Brand` | Marque (8 marques) |
| `Catégorie` | Texte | `CategoryName` | Catégorie (8 catégories) |
| `Sous-catégorie` | Texte | `SubCategoryName` | Sous-catégorie |

**Colonnes écartées :** `Manufacturer` (une marque correspond toujours à un seul fabricant, doublon), `Cost` et `Price` (prix catalogue actuels, les prix réellement pratiqués sont dans `Ventes`), `ProductCode`, `CategoryKey`, `SubCategoryKey`, `Color`, `Weight`, `WeightUnit` (non utilisés).

## Magasins

| Colonne | Type | Source | Description |
|---|---|---|---|
| `StoreKey` | Entier (masquée) | `StoreKey` | Clé du magasin. `999999` = boutique en ligne |
| `Magasin` | Texte | Calculée | `Région (année d'ouverture)`, ou `Boutique en ligne`. L'année rend le libellé unique : plusieurs magasins restructurés partagent la même région |
| `Canal` | Texte | Calculée | `En ligne` si `StoreKey = 999999`, sinon `Magasin physique` |
| `Pays du magasin` | Texte | `CountryName` | Pays d'implantation (`Online` traduit en `En ligne`) |
| `Région du magasin` | Texte | `State` | Région ou État d'implantation |
| `Date d'ouverture` | Date | `OpenDate` | Date d'ouverture |
| `Date de fermeture` | Date | `CloseDate` | Date de fermeture (vide si le magasin est ouvert) |
| `Surface (m²)` | Entier | `SquareMeters` | Surface de vente (vide pour la boutique en ligne) |
| `Statut` | Texte | `Status` | `Ouvert` (valeur vide dans la source), `Fermé` (`Closed`), `Restructuré` (`Restructured`) |

**Colonnes écartées :** `StoreCode`, `GeoAreaKey`, `CountryCode`, `Description` (remplacée par `Magasin`).

## Clients

| Colonne | Type | Source | Description |
|---|---|---|---|
| `CustomerKey` | Entier (masquée) | `CustomerKey` | Clé du client |
| `Genre` | Texte | `Gender` | `Homme` / `Femme` |
| `Date de naissance` | Date | `Birthday` | Date de naissance |
| `Ville du client` | Texte | `City` | Ville |
| `Région du client` | Texte | `StateFull` | Région ou État (nom complet) |
| `Pays du client` | Texte | `CountryFull` | Pays (8 pays) |

**Colonnes écartées :** nom, prénom, titre, adresse, code postal, entreprise, profession, véhicule, coordonnées GPS (données personnelles inutiles à l'analyse, principe de minimisation), `Age` (figé à la date de génération des données), `StartDT`, `EndDT`, `GeoAreaKey`, `Continent`, `State`, `Country` (doublons ou non utilisés).

## Calendrier

Table calculée en DAX, marquée comme **table de dates**. Elle couvre les années complètes de la première à la dernière vente.

| Colonne | Type | Exemple | Tri par |
|---|---|---|---|
| `Date` | Date (clé) | 18/05/2016 | |
| `Année` | Entier | 2016 | |
| `Trimestre` | Texte | T2 | `N° trimestre` |
| `Mois` | Texte | Mai | `N° mois` |
| `Mois court` | Texte | Mai | `N° mois` |
| `Année-mois` | Texte | mai 2016 | `N° année-mois` |
| `Jour de la semaine` | Texte | Mercredi | `N° jour de la semaine` |

Les colonnes `N° …` servent uniquement au tri chronologique et sont masquées.

---

## Mesures

| Dossier | Mesure | Définition | Format |
|---|---|---|---|
| 1. Chiffre d'affaires | `CA brut` | Somme de Quantité × Prix unitaire | $ |
| | **`CA net`** | Somme de Quantité × Prix net. **Indicateur principal** | $ |
| | `Remises` | CA brut − CA net | $ |
| | `Taux de remise` | Remises ÷ CA brut | % |
| | `Quantité vendue` | Somme des quantités | Nombre |
| | `Prix moyen par unité` | CA net ÷ Quantité vendue | $ |
| 2. Rentabilité | `Coût des ventes` | Somme de Quantité × Coût unitaire | $ |
| | `Marge brute` | CA net − Coût des ventes | $ |
| | `Taux de marge` | Marge brute ÷ CA net | % |
| 3. Commandes et clients | `Commandes` | Nombre distinct de `OrderKey` | Nombre |
| | `Panier moyen` | CA net ÷ Commandes | $ |
| | `Clients actifs` | Nombre distinct de clients ayant commandé | Nombre |
| | `Nouveaux clients` | Clients actifs dont la première commande (tous canaux et pays) a lieu dans la période | Nombre |
| | `Clients fidèles` | Clients actifs − Nouveaux clients | Nombre |
| | `Part de nouveaux clients` | Nouveaux clients ÷ Clients actifs | % |
| 4. Canaux | `CA net en ligne` | CA net filtré sur `Canal = En ligne` | $ |
| | `Part du CA en ligne` | CA net en ligne ÷ CA net | % |
| | `Délai moyen de livraison (jours)` | Moyenne, par commande en ligne, du délai de livraison | Jours |
| 5. Évolution N-1 | `CA net N-1`, `Marge brute N-1`, `Commandes N-1`, `Panier moyen N-1`, `Clients actifs N-1`, `Nouveaux clients N-1` | Valeur sur la même période de l'année précédente (`SAMEPERIODLASTYEAR`) | Selon la mesure |
| | `Évolution CA net`, `Évolution marge brute`, `Évolution commandes`, `Évolution panier moyen`, `Évolution clients actifs`, `Évolution nouveaux clients` | (Valeur − Valeur N-1) ÷ Valeur N-1, affichée seulement quand une année unique est sélectionnée | % |

Le code DAX complet et commenté se trouve dans [`report/Contoso-Ventes.SemanticModel/definition/tables/Mesures.tmdl`](../report/Contoso-Ventes.SemanticModel/definition/tables/Mesures.tmdl).
