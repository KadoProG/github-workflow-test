import json
import os
from datetime import datetime

# データを保存するファイル名
DATA_FILE = "kakeibo_data.json"


def load_data():
    """保存されたデータを読み込む"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []


def save_data(data):
    """データをファイルに保存する"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def add_entry(data, type_, amount, category, memo=""):
    """新しい記録を追加する"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M")
    entry = {
        "date": date,
        "type": type_,  # "収入" または "支出"
        "amount": amount,  # 金額
        "category": category,  # カテゴリ（食費、給料など）
        "memo": memo,  # メモ
    }
    data.append(entry)
    save_data(data)
    print("\n✅ 記録しました！")


def show_entries(data):
    """履歴と残高を表示する"""
    if not data:
        print("\n⚠️ 記録がありません。")
        return

    total_income = 0
    total_expense = 0

    print("\n" + "=" * 50)
    print("【 家計簿の履歴 】")
    print("-" * 50)
    for entry in data:
        # 履歴を1行ずつ表示
        line = (
            f"[{entry['date']}] {entry['type']} | {entry['category']} | "
            f"{entry['amount']:,}円 | メモ: {entry['memo']}"
        )
        print(line)

        # 合計の計算
        if entry["type"] == "収入":
            total_income += entry["amount"]
        else:
            total_expense += entry["amount"]

    print("-" * 50)
    print(f"総収入:     {total_income:,}円")
    print(f"総支出:     {total_expense:,}円")
    print(f"現在の残高: {(total_income - total_expense):,}円")
    print("=" * 50)


def main():
    """メインプログラム"""
    data = load_data()

    while True:
        print("\n=== 💰 シンプル家計簿 💰 ===")
        print("1: 収入を記録する")
        print("2: 支出を記録する")
        print("3: 履歴と残高を表示する")
        print("4: 終了する")

        choice = input("メニューを選択してください (1-4): ")

        if choice in ["1", "2"]:
            type_ = "収入" if choice == "1" else "支出"
            try:
                amount = int(input(f"{type_}の金額を入力してください (半角数字): "))
                if amount < 0:
                    print("⚠️ エラー: マイナスの金額は入力できません。")
                    continue

                category = input("カテゴリを入力してください (例: 給料、食費、日用品など): ")
                memo = input("メモを入力してください (省略する場合はそのままEnter): ")

                add_entry(data, type_, amount, category, memo)

            except ValueError:
                print("\n⚠️ エラー: 金額は半角数字のみで入力してください。")

        elif choice == "3":
            show_entries(data)

        elif choice == "4":
            print("\nプログラムを終了します。お疲れ様でした！")
            break

        else:
            print("\n⚠️ エラー: 1から4の番号を入力してください。")


if __name__ == "__main__":
    main()
