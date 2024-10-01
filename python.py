import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la page que tu veux scraper
url = 'https://basketlfb.com/laboulangerewonderligue/match/789988-lyon-roche-vendee'

# Envoyer la requête GET
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Scraper les statistiques
def get_player_stats(team):
    stats = []
    players = team.find_all('tr')[1:-1]  # Exclure les en-têtes et les totaux
    for player in players:
        data = player.find_all('td')
        if len(data) > 2:  # S'assurer que la ligne a des données
            player_stats = {
                'Numéro': data[0].text.strip(),
                'Nom': data[1].text.strip(),
                'Minutes': data[2].text.strip() if len(data) > 3 else 'N/A',
                'Points': data[3].text.strip() if len(data) > 4 else 'N/A',
                '2pts': data[4].text.strip() if len(data) > 5 else 'N/A',
                '3pts': data[5].text.strip() if len(data) > 6 else 'N/A',
                'Pourcentage de tirs': data[6].text.strip() if len(data) > 7 else 'N/A',
                'Lancers francs': data[7].text.strip() if len(data) > 8 else 'N/A',
                'Pourcentage LF': data[8].text.strip() if len(data) > 9 else 'N/A',
                'Rebonds offensifs': data[9].text.strip() if len(data) > 10 else 'N/A',
                'Rebonds défensifs': data[10].text.strip() if len(data) > 11 else 'N/A',
                'Total rebonds': data[11].text.strip() if len(data) > 12 else 'N/A',
                'Passes décisives': data[12].text.strip() if len(data) > 13 else 'N/A',
                'Interceptions': data[13].text.strip() if len(data) > 14 else 'N/A',
                'Ballons perdus': data[14].text.strip() if len(data) > 15 else 'N/A',
                'Contres': data[15].text.strip() if len(data) > 16 else 'N/A',
                'Fautes': data[16].text.strip() if len(data) > 17 else 'N/A',
                'Évaluation': data[19].text.strip() if len(data) > 20 else 'N/A'  # Ajout de la condition pour éviter l'erreur
            }
            stats.append(player_stats)
    return stats


# Récupérer les statistiques des deux équipes
teams = soup.find_all('table', class_='table')
lyon_stats = get_player_stats(teams[0])
roche_vendee_stats = get_player_stats(teams[1])

# Créer des DataFrames pandas pour chaque équipe
df_lyon = pd.DataFrame(lyon_stats)
df_roche_vendee = pd.DataFrame(roche_vendee_stats)

# Afficher les DataFrames
print("Statistiques de Lyon :\n", df_lyon)
print("\nStatistiques de Roche Vendée :\n", df_roche_vendee)

# Exporter les DataFrames en fichiers CSV si nécessaire
df_lyon.to_csv('lyon_stats.csv', index=False)
df_roche_vendee.to_csv('roche_vendee_stats.csv', index=False)
