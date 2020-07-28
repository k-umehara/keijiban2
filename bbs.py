#!/usr/bin/env python3
# cording: utf-8


import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
import MySQLdb
con = None
cur = None

#-------------------------設定情報を外部設定ファイル（.env）から読み取るライブラリ
import os
from pathlib import Path
env_path = Path('cgi-bin') / '.env'
from dotenv import load_dotenv
load_dotenv( dotenv_path = env_path, verbose = True)

#-------------------------HTML 開始
import cgi
form_data = cgi.FieldStorage(keep_blank_values = True)

def print_html():
	print('<!DOCTYPE html>')
	print('<html>')

#------------------------head 出力
	print('<head>')
	print('<meta charset="UTF-8">')
	print('</head>')

#------------------------body 開始
	print('<body>')
	print('<p>ひとこと掲示板</p>')

#------------------------書き込みフォームの出力
	print('<form action="" method="POST">')
	print('<input type="hidden" name="method_type" value="tweet">')
	print('<input type="text" name="poster_name" value="" placeholder="なまえ">')
	print('<br>')
	print('<textarea name="body_text" value="" placeholder="本文"></textarea>')
	print('<input type="submit" value="投稿">')
	print('</form>')

#------------------------罫線を出力
	print('<hr>')

#------------------------書き込みの一覧を取得するSQL分を作成
	sql = "select * from posts"

#------------------------SQLを実行
	cur.execute(sql)

#------------------------取得した書き込みの一覧の全レコードを取り出し
	rows = cur.fetchall()

#------------------------全レコードから1レコードずつ取り出すループ処理
	for row in rows:
		print('<div class="meta">')
		print('<span class="id">' + str(row['id']) + '</span>')
		print('<span class="name">' + str(row['name']) + '</span>')
		print('<span class="data">' + str(row['created_at']) + '</span>')
		print('</div>')
		print('<div class="message"><span>' + str(row['body']) + '</span></div>')

#------------------------body 終了
	print('</body>')

#------------------------HTML 終了
	print('</html>')

#------------------------MySQLDB接続用ライブラリの用意
def proceed_methods():
	method = form_data[ 'method_type' ].value

	if(method == 'tweet'):
		poster_name = form_data[ 'poster_name' ].value
		body_text = form_data[ 'body_text' ].value

		sql = 'insert into posts ( name, body )values ( %s, %s)'

		cur.execute( sql, ( poster_name, body_text))
		con.commit()

#------------------------処理に成功したらトップ画面に自動遷移するページを出力
	print( '<!DOCTYPE html>')
	print('<html>')
	print('		<head>')
	print('				<meta http-equiv="refresh" content="5; url=./bbs.py">')
	print('		</head>')
	print('		<body>')
	print('				処理が成功しました。5秒後に元のページに戻ります。')
	print('		</body>')
	print('</html>')


#------------------------メイン処理を実行する関数
def main():

	print('Content-Type: text/html; charset=utf-8')
	print('')

#ここでDBに接続
	global con, cur
	try:
		con = MySQLdb.connect(
			host = str(os.environ.get( 'bbs_db_host' )),
			user = str(os.environ.get( 'bbs_db_user' )),
			passwd = str(os.environ.get( 'bbs_db_pass' )),
			db = str(os.environ.get( 'bbs_db_name' )),
			use_unicode = True,
			charset = 'utf8'
		)

	except MySQLdb.Error as e:
		print('データベース接続に失敗しました。')
		print( e )

		exit()
	
	cur = con.cursor( MySQLdb.cursors.DictCursor )

#------------------------フォーム経由のアクセスか判定
	if( 'method_type' in form_data ):
		#--------------------フォーム経由のアクセスである場合は、フォームの種類に従って処理を実行
		proceed_methods()

	else:
		#--------------------フォーム経由のアクセスでない場合は通常のトップ画面を表示
		print_html()

#------------------------Pythonスクリプトとして実行された場合の処理
if __name__== "__main__":
	main()

#------------------------一通りの処理が完了したら最後にデータベースを切断しておく
cur.close()
con.close()

