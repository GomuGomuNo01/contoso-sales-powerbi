# Cahier des charges

> Document de cadrage rédigé **avant** la construction du rapport.
> Scénario fictif, basé sur le jeu de données Contoso V2 (SQLBI).

## 1. Contexte

**Entreprise.** Contoso est un distributeur de produits électroniques et d'électroménager. L'entreprise vend dans des magasins physiques répartis dans 8 pays (États-Unis, Royaume-Uni, Allemagne, Canada, Australie, Pays-Bas, Italie, France) et via une boutique en ligne.

**Mon rôle.** Data Analyst junior au sein de l'équipe Business Intelligence.

**La demande.** En janvier 2026, à la clôture de l'exercice 2025, la Direction commerciale constate que le chiffre d'affaires a reculé deux années de suite après un niveau record en 2023. Elle demande un rapport Power BI pour :

- comprendre **d'où vient ce recul** (canaux, pays, produits, clients) ;
- vérifier que la **rentabilité** reste maîtrisée ;
- disposer d'un **outil de pilotage** réutilisable pour suivre l'année 2026.

## 2. Parties prenantes

| Partie prenante | Ce qu'elle veut savoir | Décision qu'elle prendra grâce au rapport |
|---|---|---|
| Direction commerciale (commanditaire) | L'évolution globale du chiffre d'affaires et de la marge | Fixer les priorités et les objectifs 2026 |
| Responsable e-commerce | Le poids et la dynamique de la boutique en ligne, la qualité de livraison | Arbitrer les investissements dans le canal en ligne et la logistique |
| Responsables pays et magasins | Les pays et magasins qui progressent ou reculent | Cibler les plans d'action locaux |
| Chefs de produit (category managers) | Les catégories qui portent le chiffre d'affaires et la marge | Ajuster l'assortiment et la politique de prix |
| Marketing | L'évolution de la base clients et du panier moyen | Orienter les actions d'acquisition et de fidélisation |

## 3. Questions métier

1. **Tendance.** Comment le chiffre d'affaires net et la marge ont-ils évolué entre 2016 et 2025, et quelle est leur variation d'une année sur l'autre ?
2. **Canaux.** Quelle part du chiffre d'affaires est réalisée en ligne par rapport aux magasins physiques, comment cette part évolue-t-elle, et le délai de livraison des commandes en ligne s'améliore-t-il ?
3. **Géographie.** Quels pays et quels magasins contribuent le plus au chiffre d'affaires, et lesquels reculent le plus depuis 2023 ?
4. **Produits.** Quelles catégories génèrent le plus de chiffre d'affaires et de marge, et lesquelles expliquent le recul observé ?
5. **Clients.** Le recul s'explique-t-il par moins de commandes, moins de clients (nouveaux ou fidèles) ou un panier moyen plus faible ?
6. **Remises.** Quel est le poids des remises accordées, et pèsent-elles sur la rentabilité ?

## 4. Indicateurs clés (KPIs)

| Indicateur | Définition en une phrase | Calcul | Question |
|---|---|---|---|
| CA brut | Chiffre d'affaires au prix de vente, avant remise | Somme de Quantité × Prix unitaire | 1, 6 |
| **CA net** | Chiffre d'affaires réellement facturé, après remise | Somme de Quantité × Prix net | 1 à 5 |
| Montant des remises | Manque à gagner lié aux remises | CA brut − CA net | 6 |
| Taux de remise | Part du CA brut abandonnée en remises | Montant des remises ÷ CA brut | 6 |
| Coût des ventes | Coût d'achat des produits vendus | Somme de Quantité × Coût unitaire | 1, 4 |
| Marge brute | Ce qu'il reste une fois les produits payés | CA net − Coût des ventes | 1, 4, 6 |
| Taux de marge | Rentabilité relative des ventes | Marge brute ÷ CA net | 1, 4, 6 |
| Variation N / N-1 | Évolution par rapport à l'année précédente | (Valeur N − Valeur N-1) ÷ Valeur N-1 | 1, 3, 4 |
| Part du CA en ligne | Poids de la boutique en ligne | CA net en ligne ÷ CA net total | 2 |
| Délai moyen de livraison | Nombre moyen de jours entre commande et livraison | Moyenne de (Date de livraison − Date de commande), commandes en ligne | 2 |
| Nombre de commandes | Volume d'activité | Nombre distinct de commandes | 5 |
| Panier moyen | Montant moyen d'une commande | CA net ÷ Nombre de commandes | 5 |
| Clients actifs | Clients ayant commandé sur la période | Nombre distinct de clients | 5 |
| Nouveaux clients | Clients dont la première commande a lieu sur la période | Clients actifs dont la date de 1re commande est dans la période | 5 |

**Indicateur principal (North Star) : le CA net.** C'est l'indicateur au cœur de l'inquiétude de la Direction. Il est suivi avec le **taux de marge** comme garde-fou : une hausse du chiffre d'affaires obtenue en bradant les prix ne serait pas une bonne nouvelle.

## 5. Périmètre

- **Période analysée :** du 18 mai 2016 (première vente enregistrée) au 31 décembre 2025.
- **Inclus :** toutes les ventes des magasins physiques et de la boutique en ligne, dans les 8 pays.
- **Devise :** tous les montants sont exprimés en **dollars US (USD)**, devise de référence du jeu de données.
- **Tables utilisées :** `sales` (ventes), `product` (produits), `store` (magasins), `customer` (clients).
- **Exclu :**
  - `orders` et `orderrows` : elles contiennent les mêmes informations que `sales`, découpées en deux tables ;
  - `currencyexchange` : inutile puisque l'analyse est menée en USD ;
  - `date` : remplacée par une table calendrier créée dans Power BI, avec des libellés en français ;
  - les données personnelles des clients sans intérêt pour l'analyse (nom, adresse, entreprise, véhicule), écartées par principe de minimisation des données.

## 6. Livrables

- Un rapport Power BI au format `.pbip`, organisé en 4 pages :
  1. **Synthèse** : KPIs principaux et tendance ;
  2. **Canaux et pays** : répartition en ligne / magasins, pays, magasins, délais de livraison ;
  3. **Produits et rentabilité** : catégories, marges, remises ;
  4. **Clients** : clients actifs, nouveaux clients, panier moyen.
- Un dictionnaire de données (`docs/dictionnaire-de-donnees.md`).
- Un README présentant la démarche, les constats et les recommandations.

## 7. Hypothèses et limites

- **Données fictives.** Le jeu de données est généré par un outil (SQLBI). Les constats servent à démontrer une démarche d'analyse, pas à décrire une entreprise réelle.
- **Année 2016 incomplète.** Les ventes commencent le 18 mai 2016 : les comparaisons d'une année sur l'autre ne sont pertinentes qu'à partir de 2017.
- **Boutique en ligne.** Elle apparaît dans la table des magasins comme un magasin à part, avec « Online » en guise de pays. Pour l'analyse géographique des ventes en ligne, il faut utiliser le **pays du client**.
- **Délais de livraison.** En magasin, la livraison est immédiate (0 jour). Le délai n'est donc analysé que pour les commandes en ligne.
- **Informations absentes.** Pas de retours produits, de trafic en magasin ou sur le site, de coûts marketing ni d'objectifs budgétaires : impossible de calculer un taux de retour, un taux de conversion ou un écart au budget.
- **Âge des clients.** La colonne `Age` est figée à la date de génération des données : elle sera recalculée à partir de la date de naissance si nécessaire.
- **Qualité des données.** Le contrôle initial ne montre ni doublon ni clé orpheline (vente rattachée à un produit, magasin ou client inexistant). Quelques valeurs manquent sans impact sur les KPIs : région pour 66 clients, poids pour 284 produits.
