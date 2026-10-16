
import os
import requests
import folium
from dotenv import load_dotenv

load_dotenv(".env")

codigo_linha = 1206-10 #PQ. VL. MARIA / CORREIO

# Autenticação
s = requests.Session()
res = s.post(
    "http://api.olhovivo.sptrans.com.br/v2.1/Login/Autenticar",
    params={"token": os.getenv("SPTRANS_TOKEN")},
    timeout=15
)
res.raise_for_status()

if res.json() is not True:
    raise Exception("Falha na autenticação")

# Busca as paradas da linha
res = s.get(
    "http://api.olhovivo.sptrans.com.br/v2.1/Parada/BuscarParadasPorLinha",
    params={"codigoLinha": codigo_linha},
    timeout=15
)
res.raise_for_status()
paradas = res.json()

#verificar se tem paradas
print(paradas)
print("Quantidade de paradas:", len(paradas))
if paradas == []:
    print("Não tem paradas cadastradas. Tente outra linha")
else:
    # Cria o mapa
    m = folium.Map(
        location=[paradas[0]["py"], paradas[0]["px"]],
        zoom_start=14
    )

    # Busca a posição dos ônibus
    pos = s.get(
        "http://api.olhovivo.sptrans.com.br/v2.1/Posicao/Linha",
        params={"codigoLinha": codigo_linha}
    )
    pos.raise_for_status()
    posicoes = pos.json()

    #adiciona paradas
    for parada in paradas:
        # folium.CircleMarker(
        #     location=[parada["py"], parada["px"]],
        #     radius=6,
        #     color="blue",
        #     fill=True,
        #     fill_collor="blue",
        #     fill_opacity=1,
        #     popup=parada["np"]
        folium.Marker(
            location=[parada["py"], parada["px"]],
            popup=parada["np"],
            icon=folium.Icon(
                color="darkpurple",
                icon="circle",
                prefix="fa"
            )
        ).add_to(m)

    # Adiciona os ônibus
    for veiculo in posicoes.get("vs", []):
        folium.Marker(
            location=[veiculo["py"], veiculo["px"]],
            popup=f"Ônibus: {veiculo.get('p', 'Não identificado')}",
            tooltip="Ônibus em tempo real",
            icon=folium.Icon(color="purple", icon="bus", prefix="fa")
        ).add_to(m)

    m.save("paradas.html")
