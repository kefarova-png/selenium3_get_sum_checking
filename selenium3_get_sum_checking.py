#  Импортируем необходимые библиотеки и модули
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager


#  Chrome. Создаём переменную для опций браузера
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver. Chrome (
    options=options,
    service=ChromeService(ChromeDriverManager().install())
)

#  Открываем вебдрайвером ссылку
base_url = 'https://lambdatest.com/selenium-playground/simple-form-demo'
driver.get(base_url)
driver.set_window_size(920, 1080)
time.sleep(5)

#  Найдем поле ввода текста и введем текст
text_field = driver.find_element(By.XPATH, "//*[@id='user-message']")
text_value = 'A text for a test'
text_field.send_keys(text_value)
time.sleep(5)

#  Найдем поля ввода слагаемых и введём в каждое по одному числу
first_field = driver.find_element(By.XPATH, "//input[@id='sum1']")
second_field = driver.find_element(By.XPATH, "//input[@id='sum2']")
first_value = 100
second_value = 200
first_field.send_keys(first_value)
second_field.send_keys(second_value)
time.sleep(5)

#  Находим и жмём всплывшее [Allow all], чтобы не мешало(сь)
try:
    driver.find_element(
        By.XPATH,
        "//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']"
    ).click()
except:
    pass
time.sleep(2)

#  Находим и жмём [Get Checked Value]
driver.find_element(By.XPATH,"//button[@id='showInput']").click()
time.sleep(0.1)

#  Находим и жмём [Get Sum]
driver.find_element(By.XPATH,"//*[@id='gettotal']/button").click()

#  Проверяем соответствие отображаемого текста ожидаемому
fact_text = None  #  если отображаемый в превью текст не найдется
try:
    fact_text = driver.find_element(By.XPATH,"//p[@id='message']").text
except:
    pass
print(f"\nФактический текст:\t'{fact_text}' \nОжидаемый текст:\t'{text_value}'", sep='')
time.sleep(1)
assert fact_text == text_value, 'Отображаемый в превью текст должен совпадать с введенным'
print("Превью текста отображается корректно")

#  Проверяем соответствие отображаемой суммы ожидаемой
expected_sum = float(first_value + second_value)
fact_sum = None  #  Если отображаемая в превью сумма не найдется
try:
    fact_sum = float(driver.find_element(By.XPATH,"//p[@id='addmessage']").text)
except:
    fact_sum = "Not_a_Number"  #  если отображается НЕчисло
print(f"\nФактическая сумма:\t'{fact_sum}', \nОжидаемая сумма:\t'{expected_sum}'", sep='')
time.sleep(1)
assert fact_sum == expected_sum, 'Отображаемая сумма должна совпадать с вычисленной'
print("Результат суммирования отображается корректно")
time.sleep(3)

driver.close()  #  Закрываем браузер