import requests

URL = "https://localhost:8443/dataset/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/resource/XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX/download/data.csv"

def test1():
    username = "admin"
    password = "secret123"
    response = requests.get(URL, auth=(username, password), verify=False)

    if response.status_code == 200:
        with open("data.csv", "wb") as f:
            f.write(response.content)
        print("✅ CSVファイルを保存しました: data.csv")
    else:
        print(f"❌ エラー: {response.status_code}")

def test2():
    response = requests.get(URL,  verify=False)

    if response.status_code == 200:
        with open("data.csv", "wb") as f:
            f.write(response.content)
        print("✅ CSVファイルを保存しました: data.csv")
    else:
        print(f"❌ エラー: {response.status_code}")

if __name__ == '__main__':
    test1()
    test2()