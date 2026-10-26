#!/bin/sh
# Wikiの「値段一覧表」を取得し、UTF-8に変換して price.utf8.html に保存する
curl -sS -L "https://shiren6.game-info.wiki/d/%c3%cd%c3%ca%b0%ec%cd%f7%c9%bd" | iconv -f EUC-JP -t UTF-8//IGNORE > price.utf8.html
