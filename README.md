# Comparaison des indemnités de VIE par pays

## Introduction:

Le script que vous consultez permet de croiser et comparer des données relatives au Volontariat International en Entreprise (VIE). Le but est de permettre aux volontaires ou aux entreprises d'avoir un aperçu des pays qui offrent la meilleure indemnité. Toutefois, l'aspect financier n'est pas le seul critère à considérer. La sécurité est un facteur crucial lorsqu'on décide de travailler à l'étranger. C'est pourquoi ce script ne se contente pas de comparer les indemnités; il intègre également des indicateurs de criminalité pour chaque pays, fournissant ainsi une évaluation du rapport entre l'indemnité et le risque encouru.

## Fonctionnalités:

- Nettoyage des données: Les fonctions intégrées assurent le nettoyage et la standardisation des noms des pays pour garantir la cohérence lors de la comparaison des différentes sources de données.

- Calcul de ratios: Le script fournit plusieurs métriques de comparaison, notamment:
    > Indemnité par rapport au PIB par habitant.
    > Indemnité par rapport à l'indice de criminalité.
    > Indemnité en fonction de la dangerosité et du PIB par habitant.
    > Indemnité par rapport au revenu médian.

- Affichage des résultats: Pour chaque métrique, le script affiche le top n des pays, où n est un nombre configurable par l'utilisateur.

## Comment utiliser le script:

- Prérequis: Assurez-vous d'avoir les fichiers de données suivants dans le même répertoire que le script:
    > `data_vie.json` : Contient les données relatives aux indemnités VIE par pays.
    > `data_pib.csv` : Fournit les données du PIB pour chaque pays.
    > `data_criminality.csv` : Contient les indices de criminalité par pays.
    > `median-income_data.csv` : Fournit des informations sur le revenu médian par pays.

- Exécution: Exécutez le script. Par défaut, il affichera le top 5 des pays pour chaque métrique. Si vous souhaitez modifier cela, ajustez simplement la variable n au début de la section if __name__ == "__main__":.

-Analyse des résultats: Examinez les résultats affichés pour prendre une décision éclairée sur le choix du pays pour un VIE.

## Conclusion:

Que vous soyez un volontaire cherchant la meilleure destination pour votre prochaine mission ou une entreprise cherchant à affecter un employé à l'étranger, ce script vous offre un aperçu précieux pour combiner indemnité et sécurité. La décision finale doit cependant tenir compte de nombreux autres facteurs, mais ce script est un excellent point de départ.