from WEATHERAPP import *

def test_status_code_of_request_equals_200():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + "Krems" + "&appid=06c921750b9a82d8f5d1294e1586276f")
    assert response.status_code == 200

def test_status_code_of_request_equals_205():
    response = requests.get("https://api.openweathermap.org/data/2.5/weather?q=" + "Krems" + "&appid=06c921750b9a82d8f5d1294e1586276f")
    assert response.status_code != 205

def test_for_Typos():
    F = FirstPage(root)
    assert F.add("&%IDNUE0!") == "Location does not exist"


def test_for_Upper_and_lower_Cases():
    F = FirstPage(root)
    assert F.add("krems") == F.add("KREMS")
    assert F.add("SaLZburg") == F.add("salzburg")


def test_result_in_different_languages():
    F = FirstPage(root)
    assert F.add("Hokkaidō") == F.add("北海道")
    assert F.add("Austria") == F.add("Österreich")
    assert F.add("Dalat") == F.add("Đà Lạt")


def test_If_Empty_After_Clear_History():
    S = SecondPage(root)
    assert S.Clear_History() == []

def test_Max_and_Min_Temp():
    F = FirstPage(root)
    F.add("Salzburg")
    assert F.max_temp > F.min_temp
    F.add("krems")
    assert F.max_temp > F.min_temp


def test_if_a_search_is_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)
    F.add("vienna")



def test_if_multiple_searches_are_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)

    # make multiple cummulative searches
    cities = ["dalias", "Austin", "Linz"]

    n = len(cities)
    for c in cities:
        F.add(c)

    assert cities[:n] == S.History_Table()[-n:]


def test_if_unsuccessful_searches_are_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)
    F.add("&%IDNUE0!")
    assert S.History_Table()[-1] != "&%IDNUE0!"



def test_if_multiple_unsuccesful_searches_are_saved_in_History():
    F = FirstPage(root)
    S = SecondPage(root)

    # make multiple cummulative wrong searches
    typos = ["2343", "BWAHAHAAHAHAHA", "   ", " . _____ . ", "0.342"]

    n = len(typos)
    for t in typos:
        F.add(t)

    assert typos[:n] != S.History_Table()[-n:]



if __name__ == "__main__":

    root.mainloop()
