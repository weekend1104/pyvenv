from app import app


if __name__ == '__main__':

	# 测试时的启动方式
	# app.run(debug=True, port=8777) 

	#uwsgi的启动方式
	app.run(debug=False)