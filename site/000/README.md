# nurse-riko 静的サイト（/000/ 配信用）

`nurse-rikox.web-rider.biz/000` で配信するために、ブラウザ保存版（Wayback Machine
のキャプチャ）を静的サイトへ成形したものです。

## 構成

```
site/000/
├── index.html     ← 成形済みトップページ
├── assets/        ← 画像・CSS・JS（※要投入。下記参照）
├── ASSETS.txt     ← index.html が参照する全アセット一覧（38件）
└── README.md
```

公開時は `site/000/` の中身を、そのまま公開ディレクトリの `000/` へ配置してください。

```
https://nurse-rikox.web-rider.biz/000/            → index.html
https://nurse-rikox.web-rider.biz/000/assets/...  → 画像・CSS・JS
```

## assets/ が空になっている理由

アップロードされたのは HTML 単体で、対になる `ナースが教える仕事術_files`
フォルダが含まれていませんでした。またこの環境からは web.archive.org への
通信が遮断されているため、こちらでの取得もできていません。

`index.html` 側のパス書き換えは完了しているので、**元のフォルダの中身を
`assets/` へ入れれば、そのまま表示されます。**

### 投入手順

保存フォルダ `ナースが教える仕事術_files` が手元にある場合は、リポジトリ
ルートで次を実行すると、ファイル名の正規化（`.ダウンロード` の除去、
`(1)` の重複サフィックス除去）と不要ファイルの除外を自動で行います。

```bash
python3 scripts/build_site.py \
  "ナースが教える仕事術.html" \
  --assets "ナースが教える仕事術_files" \
  --out site/000
```

実行後、不足ファイルがあれば標準出力に一覧が出ます。

### 必要なファイル（38件）

| 種別 | ファイル |
|------|----------|
| CSS | `design.css` `mobile.css` `advanced.css` `print.css` `wpp.css` `style.css` |
| JS | `jquery.js` `jquery-migrate.min.js` `utility.js` |
| ロゴ・共通 | `logo.png` `loading.gif` `favicon.ico` `home-icon.png` `ogp.png` |
| サイドアイコン | `icon-side-riko.gif` `icon-side-yoshimi.gif` `icon-side-nakamura.gif` `icon-side-yuko.gif` |
| バナー | `bnr_naoko.gif` `bnr_nurseful.gif` |
| 記事サムネイル | `*-640x520.png`（10件） / `*-100x100.png`（7件） / `20170825_ill21.png` |

完全な一覧は `ASSETS.txt` を参照してください。

## HTML に加えた変更

成形時に以下を処理しています。

**削除したもの（保存時に紛れ込んだ不要物）**

- Wayback Machine のツールバー一式（`BEGIN/END WAYBACK TOOLBAR INSERT`）
- リプレイ用スクリプト（`wombat.js` `bundle-playback.js` `ruffle.js` `athena.js`）
  と、それに紐づく `banner-styles.css` `iconochive.css`
- archive.org のアクセス解析、および `<html>` の `--wm-toolbar-height`
- 保存時に凍結された各 SDK の生成済み iframe（Twitter / Facebook / はてな）。
  SDK が実行時に作り直すため、残すと旧ドメイン向けの状態が残存します
- ブラウザ拡張が `</body>` 以降に注入した DOM

**書き換えたもの**

- `./ナースが教える仕事術_files/...` → `/000/assets/...`
- Wayback のラッパー（`https://web.archive.org/web/20170928093538/...`、
  プロトコル相対の `//web.archive.org/...` を含む）を除去
- `http://nurse-riko.net/...` → `/000/...`（内部リンク 67件）
- WordPress の `wp-content/themes|uploads/...` 配下の画像も `/000/assets/` に集約
- ソーシャルウィジェットは配信元 CDN を参照するよう復元
  （Twitter / Facebook / Pocket / はてな）

## 補足

- `index.html` はトップページのみです。内部リンク（記事・カテゴリ・月別
  アーカイブ）は `/000/...` を指しますが、それらのページ自体は今回の
  アップロードに含まれていないため 404 になります。全体を復元する場合は、
  各ページの保存版を同じ手順にかけてください。
- アクセス解析ビーコン `le.nakanohito.jp`（サービス終了済み）が 1 件
  残っています。表示には影響しませんが、削除しても問題ありません。
