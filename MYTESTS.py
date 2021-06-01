from WEATHERAPP import *
import pytest

''' I commented out the root.mainloop() in WEATHERAPP.py file to perform these tests '''

@pytest.fixture(scope="module")
def cur():
    # Database set up
    conn = sqlite3.connect('HistoryDB.db')
    cursor = conn.cursor()
    yield cursor
    cursor.close()
    conn.close()


def test_status_code_of_request_equals_200():
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + "Krems" + "&appid=06c921750b9a82d8f5d1294e1586276f")
    assert response.status_code == 200


def test_status_code_of_request_equals_404():
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather?q=" + "Krems" + "&appid=06c921750b9a82d8f5d1294e1586276f")
    assert response.status_code != 404


def test_if_history_table_in_database(cur):
    cur.execute("SELECT count(*) FROM sqlite_master WHERE type='table' AND name='search_history'")
    assert cur.fetchall()[0][0] == 1


def test_to_confirm_History_table_is_accurate(cur):
    S = SecondPage(root)
    cur.execute("SELECT * FROM search_history")
    assert [a[0] for a in cur.fetchall()] == S.History_Table()


def test_for_Typos():
    F = FirstPage(root)
    assert F.Get_Weather_Info("&%IDNUE0!") == "Location does not exist"


def test_for_Upper_and_lower_Cases():
    F = FirstPage(root)
    assert F.Get_Weather_Info("krems") == F.Get_Weather_Info("KREMS")
    assert F.Get_Weather_Info("SaLZburg") == F.Get_Weather_Info("salzburg")


def test_for_search_in_different_languages():
    F = FirstPage(root)
    assert F.Get_Weather_Info("Austria") == F.Get_Weather_Info("Österreich")
    #assert F.Get_Weather_Info("Hokkaidō") == F.Get_Weather_Info("北海道")
    assert F.Get_Weather_Info("Dalat") == F.Get_Weather_Info("Đà Lạt")


def test_If_Empty_After_Clear_History():
    S = SecondPage(root)
    assert S.Clear_History() == []


def test_Max_and_Min_Temp():
    F = FirstPage(root)

    F.Get_Weather_Info("Salzburg")
    assert F.max_temp > F.min_temp

    F.Get_Weather_Info("krems")
    assert F.max_temp > F.min_temp


def test_if_a_search_is_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)

    F.Get_Weather_Info("vienna")
    assert S.History_Table()[-1] == "vienna"


def test_if_multiple_searches_are_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)

    # make multiple cummulative searches
    cities = ["dalias", "Austin", "Linz"]

    n = len(cities)
    for c in cities:
        F.Get_Weather_Info(c)

    assert cities[:n] == S.History_Table()[-n:]


def test_if_unsuccessful_searches_are_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)
    F.Get_Weather_Info("&%IDNUE0!")

    assert S.History_Table()[-1] != "&%IDNUE0!"


def test_if_multiple_wrong_searches_are_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)

    # make multiple cummulative wrong searches
    typos = ["2343", "BWAHAHAAHAHAHA", "   ", " . _____ . ", "0.342"]

    n = len(typos)
    for t in typos:
        F.Get_Weather_Info(t)

    assert typos[:n] != S.History_Table()[-n:]

def test_if_a_search_changes_in_History():
    F = FirstPage(root)
    S = SecondPage(root)

    F.Get_Weather_Info("vienna")
    assert S.History_Table()[-1] != "VIENNA"
    assert S.History_Table()[-1] != "VIennA"
    assert S.History_Table()[-1] != "wien"

def test_to_ensure_weather_info_is_not_empty():
    api = "https://api.openweathermap.org/data/2.5/weather?q=" + "Krems" + "&appid=06c921750b9a82d8f5d1294e1586276f"

    json_data = requests.get(api).json()

    assert json_data["main"] != {}
    assert json_data["wind"] != {}
    assert json_data["weather"][0] != {}



if __name__ == "__main__":
    root.mainloop()
