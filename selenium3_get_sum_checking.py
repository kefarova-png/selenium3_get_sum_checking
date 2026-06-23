#  Импортируем необходимые библиотеки и модули
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException


def press_allow_all():  #  Находим и жмём всплывшее [Allow all], чтобы не мешало(сь)
    wait = WebDriverWait(driver, 3)
    try:
        allow_all_button = wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[@id='CybotCookiebotDialogBodyLevelButtonLevelOptinAllowAll']")
            )
        )
        allow_all_button.click()
        print('Кнопка [Allow all] нажата')
    except TimeoutException:
        print('Кнопка [Allow all] не отобразилась')


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

#  Находим и жмём всплывшее [Allow all], чтобы не мешало(сь)
press_allow_all()

#  Найдем поле ввода текста и введем текст
text_field = driver.find_element(By.XPATH, "//*[@id='user-message']")
text_value = 'A text for a test'
text_field.send_keys(text_value)
print('Текстовое поле заполнено')
time.sleep(1)

#  Найдем поля ввода слагаемых и введём в каждое по одному числу
first_field = driver.find_element(By.XPATH, "//input[@id='sum1']")
second_field = driver.find_element(By.XPATH, "//input[@id='sum2']")
first_value = 0.1
second_value = 0.9
first_field.send_keys(first_value)
second_field.send_keys(second_value)
print('Числовые поля заполнены')
time.sleep(1)

#  Находим и жмём всплывшее [Allow all], чтобы не мешало(сь)
press_allow_all()

#  Находим и жмём [Get Checked Value]
driver.find_element(By.XPATH,"//button[@id='showInput']").click()
print('Кнопка [Get Checked Value] нажата')
time.sleep(1)

#  Находим и жмём [Get Sum]
driver.find_element(By.XPATH,"//*[@id='gettotal']/button").click()
print('Кнопка [Get Sum] нажата')
time.sleep(1)

#  Проверяем соответствие отображаемого текста ожидаемому
fact_text = None  #  если отображаемый в превью текст не найдется
try:
    text_element = driver.find_element(By.XPATH, "//p[@id='message']")
    fact_text = text_element.text
except NoSuchElementException:
    print('Элемент не найден')
except StaleElementReferenceException:
    print('Сохраненная ссылка на элемент стала недействительной')
print(f"\nФактический текст:\t'{fact_text}' \nОжидаемый текст:\t'{text_value}'", sep='')
time.sleep(1)
assert fact_text == text_value, 'Отображаемый в превью текст должен совпадать с введенным'
print("Превью текста отображается корректно")

#  Проверяем соответствие отображаемой суммы ожидаемой
expected_sum = float(first_value + second_value)
fact_sum = None  #  Если отображаемая в превью сумма не найдется
try:
    sun_element = driver.find_element(By.XPATH,"//p[@id='addmessage']")
    fact_sum = float(sun_element.text)
except NoSuchElementException:
    print('Элемент не найден')
except ValueError:
    fact_sum = "Not_a_Number"
    print('Отображается НЕчисло')
except StaleElementReferenceException:
    print('Сохраненная ссылка на элемент стала недействительной')
print(f"\nФактическая сумма:\t'{fact_sum}', \nОжидаемая сумма:\t'{expected_sum}'", sep='')
time.sleep(1)
assert fact_sum == expected_sum, 'Отображаемая сумма должна совпадать с вычисленной'
print("Результат суммирования отображается корректно")
time.sleep(3)

driver.close()  #  Закрываем браузер