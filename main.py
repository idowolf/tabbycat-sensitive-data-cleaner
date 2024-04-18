from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os

admin_url = os.getenv('TABBYCAT_URL')
username = os.getenv('TABBYCAT_ADMIN_USERNAME')
password = os.getenv('TABBYCAT_ADMIN_PASSWORD')

def construct_url(base_url, path):
    return f'{base_url.rstrip("/")}/{path.lstrip("/")}'

login_url = f'{admin_url}database/login/'
login_url = construct_url(admin_url, 'database/login/')
adjudicators_url = construct_url(admin_url, 'database/participants/adjudicator/')
adjudicator_adjudicator_conflict_url = construct_url(admin_url, 'database/adjallocation/adjudicatoradjudicatorconflict/')
adjudicator_team_conflict_url = construct_url(admin_url, 'database/adjallocation/adjudicatorteamconflict/')
preformed_panel_url = construct_url(admin_url, 'database/adjallocation/preformedpanel/')
adjudicator_base_score_history_url = construct_url(admin_url, 'database/adjfeedback/adjudicatorbasescorehistory/')
adjudicator_feedbacks_url = construct_url(admin_url, 'database/adjfeedback/adjudicatorfeedback/')
users_url = construct_url(admin_url, 'database/auth/user/')

driver = webdriver.Chrome()

def login():
    driver.get(login_url)
    username_field = driver.find_element(By.NAME, 'username')
    password_field = driver.find_element(By.NAME, 'password')
    login_button = driver.find_element(By.XPATH, '//input[@type="submit"]')

    username_field.send_keys(username)
    password_field.send_keys(password)
    login_button.click()

def update_base_scores():
    driver.get(adjudicators_url)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result_list"))
    )
    base_scores = driver.find_elements(By.CSS_SELECTOR, 'input[name^="form-"][name$="-base_score"]')
    for score in base_scores:
        if score.get_attribute('value') != '10.0':
            score.clear()
            score.send_keys('10.0')

    save_button = driver.find_element(By.NAME, '_save')
    save_button.click()

def delete_table(urlPath, deletionName):
    driver.get(urlPath)
    checkboxPath = '//*[@id="result_list"]/thead/tr/th[1]'
    try:
        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, checkboxPath))
        )
    except Exception as e:
        print(f'Checkbox not found {e}')
        return
    select_all_checkbox = driver.find_element(By.XPATH, checkboxPath)
    ActionChains(driver).move_to_element(select_all_checkbox).click().perform()
    action_dropdown = driver.find_element(By.NAME, 'action')
    for option in action_dropdown.find_elements(By.TAG_NAME, 'option'):
        if option.text == deletionName:
            option.click()
            break

    go_button = driver.find_element(By.NAME, 'index')
    go_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//input[@type="submit"]'))
    )
    confirm_button = driver.find_element(By.XPATH, '//input[@type="submit"]')
    confirm_button.click()

def deactivate_users_except_current():
    driver.get(users_url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "result_list"))
    )

    users = driver.find_elements(By.XPATH, '//table[@id="result_list"]/tbody/tr')

    for user_row in users:
        username_cell = user_row.find_element(By.CLASS_NAME, 'field-username')
        user_status = user_row.find_element(By.XPATH, 'td[3]/img').get_attribute('alt')
        if username_cell.text != username and user_status == 'True':
            username_cell.click()

            WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="user_form"]/div/ul/li[3]'))
            )
            status_dropdown = driver.find_element(By.XPATH, '//*[@id="user_form"]/div/ul/li[3]')
            status_dropdown.click()
            checkbox_names = ['is_active', 'is_staff', 'is_superuser']
            for name in checkbox_names:
                checkbox = driver.find_element(By.NAME, name)
                if checkbox.get_attribute('checked') is not None:
                    driver.execute_script("arguments[0].click();", checkbox)
            save_button = driver.find_element(By.NAME, '_save')
            save_button.click()
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "result_list"))
            )

def main():
    login()
    update_base_scores()
    delete_table(adjudicator_adjudicator_conflict_url, 'Delete selected adjudicator-adjudicator conflicts')
    delete_table(adjudicator_team_conflict_url, 'Delete selected adjudicator-team conflicts')
    delete_table(preformed_panel_url, 'Delete selected preformed panels')
    delete_table(adjudicator_base_score_history_url, 'Delete selected adjudicator base score histories')
    delete_table(adjudicator_feedbacks_url, 'Delete selected adjudicator feedbacks')
    deactivate_users_except_current()
    driver.quit()

if __name__ == "__main__":
    main()
