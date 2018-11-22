# 二酸化炭素濃度を CCS811/BME280 で計ってSlackに通知するマン with Python

## 購入物品 @ スイッチサイエンス

- Raspberry Pi 3 Model B+（RSコンポーネンツ製）
    - https://www.switch-science.com/catalog/3920/
- ラズパイ3Bおよび3B+に最適なACアダプター 5V/3.0A USB Micro-Bコネクタ出力
    - https://www.switch-science.com/catalog/2801/
- Qwiicケーブル（50mm）
    - https://www.switch-science.com/catalog/3542/
- SparkFun Raspberry Pi用Qwiic拡張基板
    - https://www.switch-science.com/catalog/3593/
- Qwiic - CCS811/BME280搭載 空気品質/環境センサモジュール
    - https://www.switch-science.com/catalog/3539/

## 参考URL

- 空気品質センサでオフィスの二酸化炭素濃度をモニターする @ ユニファ開発者ブログ
    - https://tech.unifa-e.com/entry/2018/06/29/115534
    - CCS811からデータを取得して継続的に監視、Slackに通知
        - このリポジトリのコードのもと

- CCS811/BME280 (Qwiic) Environmental Combo Breakout Hookup Guide
    - https://learn.sparkfun.com/tutorials/ccs811bme280-qwiic-environmental-combo-breakout-hookup-guide
    - CCS811のBME280計測結果による補正コードのってる
