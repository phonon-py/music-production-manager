# 音楽制作・配信管理アプリケーション テーブル定義書

## 1. tracks テーブル
楽曲の基本情報を管理するテーブル

| カラム名 | データ型 | NULL | キー | 初期値 | 説明 |
|---------|--------|------|-----|-------|------|
| id | INT | NO | PK | AUTO_INCREMENT | 楽曲ID |
| title | VARCHAR(100) | NO | | | 楽曲タイトル |
| spotify_url | VARCHAR(255) | YES | | NULL | SpotifyのURL |
| flp_file_path | VARCHAR(255) | YES | | NULL | FLStudioプロジェクトファイルのパス |
| created_at | DATETIME | NO | | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | | CURRENT_TIMESTAMP | 更新日時 |

インデックス：
- PRIMARY KEY (id)
- INDEX idx_track_title (title)

## 2. projects テーブル
楽曲の制作プロセスを管理するテーブル

| カラム名 | データ型 | NULL | キー | 初期値 | 説明 |
|---------|--------|------|-----|-------|------|
| id | INT | NO | PK | AUTO_INCREMENT | プロジェクトID |
| track_id | INT | NO | FK | | 関連する楽曲ID |
| status | ENUM | NO | | | プロジェクトの状態 |
| created_at | DATETIME | NO | | CURRENT_TIMESTAMP | 作成日時 |
| updated_at | DATETIME | NO | | CURRENT_TIMESTAMP | 更新日時 |

インデックス：
- PRIMARY KEY (id)
- FOREIGN KEY (track_id) REFERENCES tracks(id)
- INDEX idx_project_status (status)

ENUMの値：
- 'Idea'
- 'In Progress'
- 'Mixing'
- 'Mastering'
- 'Completed'

## 3. platforms テーブル
配信プラットフォームを管理するテーブル

| カラム名 | データ型 | NULL | キー | 初期値 | 説明 |
|---------|--------|------|-----|-------|------|
| id | INT | NO | PK | AUTO_INCREMENT | プラットフォームID |
| name | VARCHAR(50) | NO | | | プラットフォーム名 |
| created_at | DATETIME | NO | | CURRENT_TIMESTAMP | 作成日時 |

インデックス：
- PRIMARY KEY (id)

## 4. sales テーブル
楽曲の販売情報を管理するテーブル

| カラム名 | データ型 | NULL | キー | 初期値 | 説明 |
|---------|--------|------|-----|-------|------|
| id | INT | NO | PK | AUTO_INCREMENT | 販売ID |
| track_id | INT | NO | FK | | 関連する楽曲ID |
| platform_id | INT | NO | FK | | 関連するプラットフォームID |
| sale_date | DATE | NO | | | 販売日 |
| amount | DECIMAL(10, 2) | NO | | | 販売金額 |
| created_at | DATETIME | NO | | CURRENT_TIMESTAMP | 作成日時 |

インデックス：
- PRIMARY KEY (id)
- FOREIGN KEY (track_id) REFERENCES tracks(id)
- FOREIGN KEY (platform_id) REFERENCES platforms(id)
- INDEX idx_sales_date (sale_date)

## 注意事項
1. すべてのテーブルにおいて、`id`カラムは自動増分の主キーとして設定されています。
2. 日時を扱うカラムには、`CURRENT_TIMESTAMP`を使用して自動的に現在の日時が設定されます。
3. `tracks`テーブルと`projects`テーブルの`updated_at`カラムは、レコードが更新されるたびに自動的に更新されます。
4. 外部キー制約により、データの整合性が保たれます（例：存在しない`track_id`を`sales`テーブルに挿入することはできません）。
5. パフォーマンス向上のため、適切なカラムにインデックスが設定されています。

この定義書は、アプリケーションの要件に基づいて作成されていますが、開発の進行に伴い、必要に応じて更新や拡張を行うことができます。