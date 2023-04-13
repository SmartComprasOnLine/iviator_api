from flask import Flask, jsonify
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
import time
from webdriver_manager.chrome import ChromeDriverManager

# Inicializa o aplicativo Flask
app = Flask(__name__)

# Inicializa o driver do Selenium
driver = uc.Chrome()

# Rota para obter os resultados do jogo
@app.route('/results')
def get_results():
    # Navega até a página do jogo
    driver.get('https://estrelabet.com/ptb/games/detail/casino/normal/7787')

    # Espera até que o iframe seja carregado
    while len(driver.find_elements(By.ID, 'gm-frm')) == 0:
        time.sleep(2)

    # Muda para o iframe
    iframe = driver.find_element(By.XPATH,'/html/body/app-root/app-out-component/div[1]/main/app-games/app-casino-detail/div[2]/div/div/div[2]/iframe')
    driver.switch_to.frame(iframe)

    # Inicializa a lista de resultados
    results = []

    # Espera até que os resultados sejam carregados
    while len(driver.find_elements(By.XPATH, '/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div'))== 0:
        time.sleep(6)

    # Obtém os resultados em tempo real e adiciona à lista
    while True:
        resultado = driver.find_element(By.XPATH, "/html/body/app-root/app-game/div/div[1]/div[2]/div/div[2]/div[1]/app-stats-widget/div/div[1]/div").text.split()

        if ' '.join(resultado) not in results:
            results.append(' '.join(resultado))

        # Espera alguns segundos antes de atualizar novamente
        time.sleep(6)

        # Retorna a lista de resultados
        return jsonify(results)

# Função para fechar o driver do Selenium corretamente
#@app.teardown_appcontext
#def shutdown_driver(exception=None):
#    global driver
#    driver.quit()

# Executa a aplicação
if __name__ == '__main__':
    app.run(debug=True)
